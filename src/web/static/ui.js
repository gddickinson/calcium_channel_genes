// Shared dashboard widgets: provenance footers, ledger-state badges, tiles and a sortable / filterable table for any
// committed TSV. Values are shown exactly as the committed file holds them; nothing here computes a number.
import { esc, list, api } from './core.js';

// Provenance line(s) under a panel: file path (linked to GitHub at that commit), commit, date.
export function prov(sources) {
  const arr = Array.isArray(sources) ? sources : [sources];
  return `<p class="prov">source: ${list(arr.filter(Boolean), s =>
    `<a href="${esc(s.url)}" target="_blank" rel="noopener"><code>${esc(s.path)}</code></a> @ <code>${esc(s.commit)}</code>${s.date ? ` (${esc(s.date)})` : ''}${s.modified ? ' <span class="state pending">uncommitted edits</span>' : ''}`, ' · ')}</p>`;
}

// The repo's own status words: completed / in_progress / pending (ledger), open / half closed / closed (emergent).
export function state(word, date = '') {
  const cls = String(word).replace(/\s+/g, '_');
  return `<span class="state ${esc(cls)}">${esc(word)}${date ? ' ' + esc(date) : ''}</span>`;
}

export const tile = (value, label, href = '') => href
  ? `<a class="tile" href="${esc(href)}"><b>${esc(value)}</b><span>${esc(label)}</span></a>`
  : `<div class="tile"><b>${esc(value)}</b><span>${esc(label)}</span></div>`;

export function panel(title, body, sources, extra = '') {
  return `<section class="panel"><h3>${esc(title)}</h3>${extra}${body}${sources ? prov(sources) : ''}</section>`;
}

// Render table t ({columns, rows, source}) into host with a text filter, click-to-sort headers and an optional
// per-row class. opts: { cols: [names to show], limit, rowClass(rowObj), cell(name, value, rowObj) -> html }.
export function dataTable(host, t, opts = {}) {
  const idx = (opts.cols || t.columns).map(c => t.columns.indexOf(c)).filter(i => i >= 0);
  const names = idx.map(i => t.columns[i]);
  let sortCol = -1, asc = true, q = '';
  const id = 'f' + Math.random().toString(36).slice(2, 8);
  host.innerHTML = `<div class="tbar"><label for="${id}">Filter rows</label><input id="${id}" type="search" placeholder="type to filter (${t.rows.length} rows)"></div>
    <div class="scroll"><table class="data"><thead><tr>${names.map((n, k) => `<th><button class="sort" data-k="${k}">${esc(n)}</button></th>`).join('')}</tr></thead><tbody></tbody></table></div>
    <p class="small mute count"></p>${t.source ? prov(t.source) : ''}`;
  const body = host.querySelector('tbody'), count = host.querySelector('.count');
  const num = v => (v !== '' && !isNaN(+v) ? +v : null);
  const draw = () => {
    let rows = t.rows.filter(r => !q || r.some(c => c.toLowerCase().includes(q)));
    if (sortCol >= 0) {
      const i = idx[sortCol];
      rows = [...rows].sort((a, b) => {
        const x = num(a[i]), y = num(b[i]);
        const c = x !== null && y !== null ? x - y : String(a[i]).localeCompare(String(b[i]));
        return asc ? c : -c;
      });
    }
    const shown = opts.limit ? rows.slice(0, opts.limit) : rows;
    body.innerHTML = shown.map(r => {
      const obj = Object.fromEntries(t.columns.map((c, i) => [c, r[i]]));
      const cls = opts.rowClass ? opts.rowClass(obj) : '';
      return `<tr class="${esc(cls)}">${idx.map(i => `<td>${opts.cell ? opts.cell(t.columns[i], r[i], obj) : esc(r[i])}</td>`).join('')}</tr>`;
    }).join('');
    count.textContent = `${shown.length} of ${t.rows.length} rows shown` + (q ? ` (filter: "${q}")` : '');
  };
  host.querySelector('input').addEventListener('input', e => { q = e.target.value.trim().toLowerCase(); draw(); });
  host.querySelectorAll('button.sort').forEach(b => b.addEventListener('click', () => {
    const k = +b.dataset.k; asc = sortCol === k ? !asc : true; sortCol = k; draw();
  }));
  draw();
}

// Fetch /table/<key> and render it into a new panel appended to parent.
export async function tablePanel(parent, key, opts = {}) {
  const t = await api('/table/' + key);
  const sec = document.createElement('section');
  sec.className = 'panel';
  sec.id = 'tbl-' + key;
  sec.innerHTML = `<h3>${esc(t.title)} <span class="mute small">${esc(t.task)}</span></h3>${t.blurb ? `<p class="small mute">${esc(t.blurb)}</p>` : ''}${opts.note || ''}<div></div>`;
  parent.appendChild(sec);
  dataTable(sec.lastElementChild, t, opts);
  return t;
}

// A collapsible rendered markdown document (a stage's own report) inside parent.
export async function docPanel(parent, key, open = false) {
  const [{ render }, d, figs] = await Promise.all([import('./markdown.js'), api('/doc/' + key), api('/figures')]);
  const det = document.createElement('details');
  det.className = 'panel doc';
  if (open) det.open = true;
  const { html } = render(d.markdown, { base: d.base, figures: new Set(figs.figures.map(f => f.path)) });
  det.innerHTML = `<summary>${esc(d.title)}</summary><div class="md">${html}</div>${prov(d.source)}`;
  parent.appendChild(det);
}
