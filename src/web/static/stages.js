// The completed stages: S0 (catalogue verification) and S1 (classifier benchmark). Headline tiles come from each
// stage's summary JSON; the panels are the stage's committed TSVs; each page ends with the stage's own report.md,
// which the repo renders purely from those tables (D13).
import { route, app, api, esc } from './core.js';
import { prov, state, tile, tablePanel, docPanel } from './ui.js';

const statusClass = v => (/^ok$|^yes$|^named$|^harmless/.test(v) ? 'r-ok' : /mismatch|bad|absent$|^no$|missing|leak|fail|false positive/i.test(v) ? 'r-bad' : '');

route('verification', async () => {
  const [o, figs] = await Promise.all([api('/overview'), api('/figures')]);
  const s = o.s0, done = o.done.find(t => t.id === 'S0');
  const fig = figs.figures.find(f => f.group === 'S0');
  app().innerHTML = `<p class="kicker">S0 ${state('completed', done ? done.date : '')}</p>
  <h1>Catalogue verification</h1>
  <p class="lead">Every Pfam accession, exemplar, architecture, anchor and taxon id the catalogue declares, re-derived
    against live databases rather than inherited. The permeability values are not verified here: no database holds
    them <mark class="pending">(pending: S1b)</mark>.</p>
  <div class="tiles">
    ${tile(`${s.pfam.n}`, `Pfam accessions checked · ${s.pfam.missing.length} missing · ${s.pfam.renamed.length} renamed`)}
    ${tile(`${s.exemplars.resolved}/${s.exemplars.n}`, `exemplars resolved · ${s.exemplars.unresolved} unresolved`)}
    ${tile(`${s.exemplars.arch_mismatch}`, 'architecture differences (see table: subfamily-level vs family-level)')}
    ${tile(`${s.taxonomy.n}`, `taxa checked · ${s.taxonomy.bad} problems`)}
    ${tile(`${s.requests}`, `live requests · ${o.s0_request_failures} failures · ${s.elapsed_s} s`)}
  </div>
  ${prov(o.source[0])}
  ${fig ? `<figure class="panel"><img src="files/${esc(fig.path)}" alt="${esc(fig.caption)}" loading="lazy"><figcaption>${esc(fig.label)}: ${esc(fig.caption)}</figcaption>${prov(fig.source)}</figure>` : ''}
  <div id="tabs"></div>`;
  const host = document.getElementById('tabs');
  const rc = o => statusClass(o.status || o.verified || o.crosses_census_boundary || '');
  await tablePanel(host, 'anchors', { rowClass: rc, cols: ['anchor', 'reference_label', 'uniprot', 'positions', 'expected', 'observed', 'verified', 'note'] });
  await tablePanel(host, 'pfam', { rowClass: rc });
  await tablePanel(host, 'architecture', { rowClass: o => (o.status === 'ok' ? 'r-ok' : o.status === 'subfamily_absence_expected' ? '' : 'r-bad') });
  await tablePanel(host, 'exemplars', { rowClass: rc, cols: ['family', 'label', 'gene', 'species', 'declared_accession', 'resolved_accession', 'length_aa', 'status'] });
  await tablePanel(host, 'taxonomy', { rowClass: rc });
  await tablePanel(host, 'sharing', { rowClass: o => (o.crosses_census_boundary === 'yes' ? 'r-warn' : '') ,
    note: '<p class="small">Rows marked are signatures carried by both a census family and a family that does not conduct calcium.</p>' });
  await tablePanel(host, 'rule_coverage');
  await tablePanel(host, 'rule_targets');
  await tablePanel(host, 'filter_four');
  await tablePanel(host, 'filter_k');
  await docPanel(host, 's0_report');
  await docPanel(host, 's0_provenance');
});

route('benchmark', async () => {
  const o = await api('/overview');
  const s = o.s1, done = o.done.find(t => t.id === 'S1');
  app().innerHTML = `<p class="kicker">S1 ${state('completed', done ? done.date : '')}</p>
  <h1>Classifier benchmark</h1>
  <p class="lead">The classifier run leave-one-out on a control panel: a positive from every census family and a decoy
    from every control family. A decoy is the hard case: the nearest relative that is not a calcium channel.</p>
  <div class="tiles">
    ${tile(`${s.positives_correct}/${s.positives}`, `positives called correctly (recall ${s.recall})`)}
    ${tile(`${s.decoys_rejected}/${s.decoys}`, `decoys rejected (specificity ${s.specificity})`)}
    ${tile(`${s.hazards_exercised}/${s.hazards_defined}`, 'hazards exercised')}
    ${tile(`${s.n_classified}/${s.n_targets}`, `panel members classified · ${s.n_missing} not fetched`)}
    ${tile(`${s.counts_conf_gold} · ${s.counts_conf_silver} · ${s.counts_conf_bronze} · ${s.counts_conf_unassigned}`, 'gold · silver · bronze · unassigned confidence')}
  </div>
  ${prov(o.source[1])}
  <p class="small mute">Generated ${esc(s.generated)} · MAFFT ${esc(s.mafft)} · reference panel ${esc(s.reference_panel)} sequences ·
    leave-one-out ${esc(s.leave_one_out)} · anchor validates: ${esc(s.anchor_validates)}</p>
  <div id="tabs"></div>`;
  const host = document.getElementById('tabs');
  const ok = o => (+o.correct === +o.n ? 'r-ok' : 'r-bad');
  await tablePanel(host, 'recall', { rowClass: ok });
  await tablePanel(host, 'hazards', { rowClass: o => (+o.n_wrong > 0 ? 'r-bad' : +o.n_touched === 0 ? 'r-warn' : 'r-ok'),
    note: '<p class="small">Marked rows: a hazard with a wrong call, or one no panel member touched (untested, not solved).</p>' });
  await tablePanel(host, 'anchor_summary', { rowClass: o => (o.discriminates === 'yes' ? 'r-ok' : 'r-warn') });
  await tablePanel(host, 'anchor_power');
  await tablePanel(host, 'calls', { cols: ['accession', 'gene_symbol', 'expected_family', 'called_family', 'status', 'confidence', 'margin', 'filter_string', 'decisive_tier', 'hazards', 'conflicts'],
    note: '<p class="small">For a decoy, <code>unassigned</code> is a success: the census asks whether a protein is a calcium channel. See the recall table for what counted as correct.</p>' });
  await tablePanel(host, 'confusion');
  await tablePanel(host, 'coverage');
  await tablePanel(host, 'leakage', { rowClass: o => statusClass(o.severity || '') });
  await tablePanel(host, 'missing');
  await tablePanel(host, 'toolchain', { cols: ['tool', 'version', 'status', 'needed_by'], rowClass: o => statusClass(o.status) });
  await docPanel(host, 's1_report');
});
