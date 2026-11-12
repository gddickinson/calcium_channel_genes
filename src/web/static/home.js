// Home (headline numbers from the S0 / S1 summary JSONs and the ledger) and About.
import { route, app, api, esc, list } from './core.js';
import { prov, state, tile } from './ui.js';

// What each census tier means (from the CaClass docstring in src/catalogue/schema.py), in ledger order.
export const TIERS = {
  ca_selective: 'the pore discriminates strongly for Ca2+ (Cav, ORAI, TRPV5/6, MCU)',
  ca_permeable: 'a non-selective cation channel that carries a physiologically important Ca2+ current',
  ca_conditional: 'Ca2+ permeability depends on something the genome does not show: subunits, splicing or RNA editing',
  ca_release: 'releases Ca2+ from an intracellular store rather than admitting it across the plasma membrane',
};

export function tierTiles(tiers) {
  return `<div class="tiles tiers">${list(Object.keys(TIERS).filter(k => tiers[k]), k =>
    `<a class="tile tier-${k}" href="#/census?tier=${k}"><b>${esc(tiers[k].human_genes)}</b><span>human genes in <code>${esc(k)}</code> · ${esc(tiers[k].families)} families</span></a>`)}</div>`;
}

const CARDS = [
  ['census', 'Census', 'The four tiers and all 49 catalogue families, census and excluded'],
  ['verification', 'S0 verification', 'Every catalogue claim re-derived against live databases'],
  ['benchmark', 'S1 benchmark', 'The classifier against positives and decoys: recall, specificity, hazards'],
  ['phylogeny', 'Phylogeny', 'The forest, the refused superfamilies, and which trees are still pending'],
  ['roadmap', 'Roadmap', 'The task ledger, emergent tasks and the seven questions'],
  ['pending', 'Pending claims', 'Every (pending: task) marker, checked against the ledger'],
  ['findings', 'Findings', 'The biological story, task by task (FINDINGS.md)'],
  ['tables', 'All tables', 'Every committed table the dashboard reads, with provenance'],
];

route('home', async () => {
  const o = await api('/overview');
  const c = o.catalogue, s1 = o.s1, p = o.progress;
  app().innerHTML = `
  <section class="hero">
    <p class="kicker">gene census · classification · phylogeny</p>
    <h1 class="glow">Calcium channels</h1>
    <p class="lead">A census of the pathways that carry Ca2+ down its gradient through an open pore, classified by
      positive tests with an audit trail. This is a read-only dashboard of the project's committed outputs: every
      number below is read from a committed table at build time, with its file and commit shown.</p>
    <a class="btn" href="#/census">Open the census</a><a class="btn alt" href="#/roadmap">See what is pending</a>
  </section>
  <div class="callout"><b>No flat total (D31).</b> "Calcium channel" is a permeability, not a clade, so the census is
    always reported in four tiers. ${o.next ? `The tier boundaries rest on literature permeability values that have
    not been audited yet ${state('pending')} <a href="#/roadmap">S1b</a>.` : ''}</div>
  ${tierTiles(o.tiers)}
  <div class="tiles">
    ${tile(`${c.families_census} / ${c.families_total}`, 'census families / catalogue families', '#/census')}
    ${tile(`${c.human_genes_census} / ${c.human_genes_catalogued}`, 'human genes counted / catalogued', '#/census')}
    ${tile(c.superfamilies, 'superfamilies')}
    ${tile(c.hazards, 'recorded hazards', '#/table/hazards')}
  </div>
  ${prov(o.source[0])}
  <h2>Where the project is</h2>
  <div class="progress" role="img" aria-label="${p.completed} of ${p.total} ledger tasks completed">
    <span style="width:${(100 * p.completed / p.total).toFixed(2)}%"></span></div>
  <p>${esc(p.completed)} of ${esc(p.total)} ledger tasks ${state('completed')} · ${esc(p.in_progress)} ${state('in_progress')} ·
    ${esc(p.pending)} ${state('pending')}. ${o.next ? `Next by the ledger's own rule: <b>${esc(o.next.id)}</b>, ${esc(o.next.title)}.` : ''}</p>
  <div class="grid wide">
    <a class="card" href="#/verification"><small>S0 ${state('completed', o.done.find(t => t.id === 'S0')?.date || '')}</small>
      <b>Catalogue verification</b>
      <span>${esc(o.s0.pfam.n)} Pfam accessions, ${esc(o.s0.pfam.missing.length)} missing ·
      ${esc(o.s0.exemplars.resolved)}/${esc(o.s0.exemplars.n)} exemplars resolved ·
      ${esc(o.s0.taxonomy.n)} taxa, ${esc(o.s0.taxonomy.bad)} problems ·
      ${esc(o.s0.requests)} requests, ${esc(o.s0_request_failures)} failures</span></a>
    <a class="card" href="#/benchmark"><small>S1 ${state('completed', o.done.find(t => t.id === 'S1')?.date || '')}</small>
      <b>Classifier benchmark</b>
      <span>recall ${esc(s1.positives_correct)}/${esc(s1.positives)} · specificity ${esc(s1.decoys_rejected)}/${esc(s1.decoys)} ·
      hazards exercised ${esc(s1.hazards_exercised)}/${esc(s1.hazards_defined)} · ${esc(s1.n_missing)} panel member(s) not fetched</span></a>
    <a class="card" href="#/phylogeny"><small>S7 / S8 ${state('pending')}</small><b>Phylogeny</b>
      <span>${o.trees ? `${esc(o.trees)} tree file(s) committed.` : 'No tree files are committed yet.'} ${esc(o.s0.superfamilies_not_alignable.length)} superfamilies are refused a tree by rule (D27).</span></a>
  </div>
  ${prov(o.source)}
  <h2>Explore</h2>
  <div class="grid">${list(CARDS, ([r, t, d]) => `<a class="card" href="#/${r}"><b>${esc(t)}</b><span>${esc(d)}</span></a>`)}</div>
  <p class="small mute">Built from commit <code>${esc(o.head.commit)}</code> (${esc(o.head.date)}): ${esc(o.head.subject)}</p>`;
});

route('about', async () => {
  const info = await api('/info');
  app().innerHTML = `<p class="kicker">about</p><h1>About this dashboard</h1>
  <p class="lead">A read-only view of the committed outputs of <a href="${esc(info.repo)}">calcium_channel_genes</a>,
    a multi-session publication project: a census, a classification and a phylogeny of the calcium channels.</p>
  <div class="panel"><h3>The rules this page follows</h3><ul>
    <li>Every number is read from a committed file (TSV, JSON or a stage's rendered report) when the site is built.
      Nothing is typed by hand or recomputed. Each panel names its file and the commit that last changed it.</li>
    <li>The census is never shown as a flat total (decision D31): always the four tiers.</li>
    <li>Status words are the repo's own: ledger <code>completed</code> / <code>in_progress</code> / <code>pending</code>,
      emergent tasks <code>open</code> / <code>half closed</code> / <code>closed</code>, and the <code>(pending: task)</code>
      marker in FINDINGS.md and the review.</li>
    <li>Only files tracked by git are read, and the static build refuses to publish a file with uncommitted edits.</li>
  </ul></div>
  <div class="panel"><h3>Run it yourself</h3>
  <pre>pip install -r requirements-web.txt
python run_web.py                     # http://127.0.0.1:8177
python scripts/build_static.py        # the static site, as published on GitHub Pages</pre>
  <p>The project's own tools: <code>python3 -m src.catalogue --tiers</code> (the census in tiers),
    <code>python3 run.py --classify CACNA1C,SCN5A</code> (classify with an audit trail),
    <code>python3 scripts/dashboard.py --open</code> (the session dashboard). See the README.</p></div>
  <div class="panel"><h3>Credits</h3><p>Project and data: George Dickinson. Licence: MIT (see LICENSE). The app,
    classifier and phylogeny frameworks are ported from the sibling ion-channel, IP3R and PIEZO census projects.</p></div>
  <p class="small mute">Built from commit <code>${esc(info.head.commit)}</code> (${esc(info.head.date)}).</p>`;
});
