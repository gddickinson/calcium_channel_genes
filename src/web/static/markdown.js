// Small, safe Markdown renderer for the repo's committed reports, FINDINGS.md and the review: headings, paragraphs,
// bullet / numbered lists, pipe tables, blockquotes, fenced code, horizontal rules, images, **bold**, *italic*,
// `code`, links, and the (pending: task) marker, which is wrapped in <mark class="pending"> so it stands out.
// All text is HTML-escaped first, so no raw HTML from a source file reaches the page. Images and relative links are
// resolved against the document's folder; only images listed as published figures are shown (others become a note).
const ESC = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
const escape = s => String(s).replace(/[&<>"']/g, c => ESC[c]);
const REPO = 'https://github.com/gddickinson/calcium_channel_genes/blob/main/';

export function slug(text) {
  return text.toLowerCase().replace(/<[^>]+>/g, '').replace(/&[a-z#0-9]+;/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

// Join a relative path onto a folder ('docs' + 'figures/x.png' -> 'docs/figures/x.png'; '../a' handled).
export function joinPath(base, rel) {
  const parts = (base ? base.split('/') : []).filter(Boolean);
  for (const p of rel.split('/')) {
    if (p === '..') parts.pop(); else if (p && p !== '.') parts.push(p);
  }
  return parts.join('/');
}

export function inline(text, opt = {}) {
  const base = opt.base || '';
  return escape(text)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\(\*?pending:\s*([^)]*?)\*?\)/g, '<mark class="pending">(pending: $1)</mark>')
    .replace(/(^|[^*\w])\*([^*\s][^*]*?)\*(?!\w)/g, '$1<em>$2</em>')
    .replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
    .replace(/\[([^\]]+)\]\(([^\s)#:]+)(#[^\s)]*)?\)/g,
      (_, label, rel) => `<a href="${REPO}${joinPath(base, rel)}" target="_blank" rel="noopener">${label}</a>`);
}

function image(alt, src, opt) {
  const path = joinPath(opt.base || '', src);
  if (opt.figures && opt.figures.has(path)) {
    return `<figure class="mdfig"><img src="files/${escape(path)}" alt="${escape(alt || path)}" loading="lazy"></figure>`;
  }
  return `<p class="small mute">[figure not published on this site: ${escape(path)}]</p>`;
}

const cells = line => line.trim().replace(/^\||\|$/g, '').split('|').map(c => c.trim());
const isRule = line => /^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$/.test(line);

// Returns { html, toc: [{level, text, id}] }. opt: { base, figures: Set of published paths }.
export function render(md, opt = {}) {
  const out = [], toc = [], used = new Map();
  const lines = String(md).replace(/\r\n?/g, '\n').split('\n');
  let para = [], list = null, quote = [];
  const il = t => inline(t, opt);
  const flushPara = () => { if (para.length) { out.push(`<p>${il(para.join(' '))}</p>`); para = []; } };
  const flushList = () => { if (list) { out.push(`<${list.tag}>${list.items.map(i => `<li>${il(i)}</li>`).join('')}</${list.tag}>`); list = null; } };
  const flushQuote = () => { if (quote.length) { out.push(`<blockquote>${render(quote.join('\n'), opt).html}</blockquote>`); quote = []; } };
  const flush = () => { flushPara(); flushList(); flushQuote(); };
  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i], line = raw.trimEnd();
    let m;
    if (/^\s*>/.test(line)) { flushPara(); flushList(); quote.push(line.replace(/^\s*>\s?/, '')); continue; }
    if (quote.length) flushQuote();
    if (!line.trim()) { flushPara(); flushList(); continue; }
    if (/^```/.test(line)) {
      flush();
      const code = [];
      while (++i < lines.length && !/^```/.test(lines[i])) code.push(lines[i]);
      out.push(`<pre>${escape(code.join('\n'))}</pre>`);
    } else if ((m = line.match(/^(#{1,5})\s+(.*)$/))) {
      flush();
      const level = m[1].length, text = m[2].trim();
      let id = slug(text) || 'section';
      const n = used.get(id) || 0; used.set(id, n + 1);
      if (n) id += '-' + n;
      toc.push({ level, text, id });
      out.push(`<h${Math.min(level + 1, 6)} id="${id}">${il(text)}</h${Math.min(level + 1, 6)}>`);
    } else if (line.trim().startsWith('|') && i + 1 < lines.length && isRule(lines[i + 1])) {
      flush();
      const head = cells(line), rows = [];
      i += 1;
      while (i + 1 < lines.length && lines[i + 1].trim().startsWith('|')) rows.push(cells(lines[++i]));
      const th = head.some(h => h) ? `<thead><tr>${head.map(h => `<th>${il(h)}</th>`).join('')}</tr></thead>` : '';
      out.push(`<div class="scroll"><table>${th}<tbody>${rows.map(r => `<tr>${r.map(c => `<td>${il(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`);
    } else if ((m = line.match(/^\s*!\[([^\]]*)\]\(([^)\s]+)\)\s*$/))) {
      flush(); out.push(image(m[1], m[2], opt));
    } else if (/^(-{3,}|\*{3,}|_{3,})$/.test(line.trim())) {
      flush(); out.push('<hr>');
    } else if ((m = line.match(/^\s*[-*+]\s+(.*)$/)) || (m = line.match(/^\s*\d+[.)]\s+(.*)$/))) {
      flushPara();
      const tag = /^\s*\d/.test(line) ? 'ol' : 'ul';
      if (!list || list.tag !== tag) { flushList(); list = { tag, items: [] }; }
      list.items.push(m[1]);
    } else if (list && /^\s{2,}\S/.test(raw)) {
      list.items[list.items.length - 1] += ' ' + line.trim();
    } else {
      flushList(); para.push(line.trim());
    }
  }
  flush();
  return { html: out.join('\n'), toc };
}
