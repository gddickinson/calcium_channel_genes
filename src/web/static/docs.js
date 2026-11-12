// Documents (FINDINGS.md, the review, scope), the figure gallery, and the index / viewer for every committed table.
import { route, app, api, esc, list } from './core.js';
import { prov, dataTable } from './ui.js';
import { render } from './markdown.js';

async function showDoc(key, kicker, intro = '') {
  const [d, figs] = await Promise.all([api('/doc/' + key), api('/figures')]);
  const { html, toc } = render(d.markdown, { base: d.base, figures: new Set(figs.figures.map(f => f.path)) });
  const nav = toc.filter(t => t.level === 2);
  app().innerHTML = `<p class="kicker">${esc(kicker)}</p>
  <div class="callout a small">${intro}Shown verbatim from the committed file; <mark class="pending">(pending: task)</mark>
    markers are highlighted. ${prov(d.source)}</div>
  <div class="side doc">
    <aside class="panel toc"><h3>Contents</h3><nav aria-label="Document sections">${list(nav, t => `<a href="#" data-id="${esc(t.id)}">${esc(t.text.replace(/\*\*|`|\*/g, ''))}</a>`)}</nav></aside>
    <article class="md">${html}</article></div>`;
  app().querySelectorAll('.toc a').forEach(a => a.addEventListener('click', e => {
    e.preventDefault();
    document.getElementById(a.dataset.id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }));
}

route('findings', () => showDoc('findings', 'findings', 'The project\'s plain-language biological story, appended after every completed task. '));
route('review', () => showDoc('review', 'literature review (S23)', 'The review is generated from <code>docs/review/</code>; every citation was resolved against Europe PMC (see the <a href="#/table/references">references table</a>). '));
route('scope', () => showDoc('scope', 'scope', 'What counts as a calcium channel: the boundary decisions the census denominator rests on. '));
route('doc', args => showDoc(args[0], 'document'));

route('figures', async () => {
  const f = await api('/figures');
  app().innerHTML = `<p class="kicker">figures</p><h1>Figures</h1>
  <p class="lead">Committed figures: the review's (captions from the review's own figure list) and the stages'.</p>
  <div class="figs">${list(f.figures, x => `<figure class="panel"><a href="files/${esc(x.path)}" target="_blank" rel="noopener">
    <img src="files/${esc(x.path)}" alt="${esc(x.label)}: ${esc(x.caption.replace(/\*/g, ''))}" loading="lazy"></a>
    <figcaption><b>${esc(x.label)}.</b> ${esc(x.caption.replace(/\*/g, ''))}</figcaption>${prov(x.source)}</figure>`)}</div>
  ${list(f.reserved, r => `<div class="callout"><b>${esc(r.label)}</b> is reserved: ${esc(r.caption.replace(/\*/g, ''))}</div>`)}
  ${prov(f.captions_from)}`;
});

route('tables', async () => {
  const t = await api('/tables');
  app().innerHTML = `<p class="kicker">data</p><h1>Every committed table</h1>
  <p class="lead">The tables this dashboard reads, by the ledger task that wrote them. Open one to filter, sort and
    read it exactly as committed.</p>
  <div class="panel"><div class="scroll"><table><thead><tr><th>table</th><th>task</th><th>rows</th><th>file @ commit</th></tr></thead><tbody>
  ${list(t.tables, x => `<tr><td><a href="#/table/${esc(x.key)}">${esc(x.title)}</a><br><span class="small mute">${esc(x.blurb)}</span></td>
    <td>${esc(x.task)}</td><td>${esc(x.rows)}</td><td class="small"><a href="${esc(x.source.url)}" target="_blank" rel="noopener"><code>${esc(x.source.path)}</code></a> @ <code>${esc(x.source.commit)}</code></td></tr>`)}
  </tbody></table></div></div>`;
});

route('table', async args => {
  const t = await api('/table/' + args[0]);
  app().innerHTML = `<p class="kicker">${esc(t.task)} · <a href="#/tables">all tables</a></p><h1>${esc(t.title)}</h1>
    ${t.blurb ? `<p class="lead">${esc(t.blurb)}</p>` : ''}<div class="panel" id="tb"></div>`;
  dataTable(document.getElementById('tb'), t);
});
