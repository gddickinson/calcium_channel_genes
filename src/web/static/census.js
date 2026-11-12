// Census: the four tiers (S0 summary) and every catalogue family, census and excluded. Per-family human gene counts
// are from results/benchmark_controls/coverage.tsv; names, tiers, statuses and gene symbols from src/catalogue.
import { route, app, api, esc, list } from './core.js';
import { prov, state, panel } from './ui.js';
import { TIERS, tierTiles } from './home.js';

const ORDER = [...Object.keys(TIERS), 'ca_activated', 'not_calcium'];

function famRow(f) {
  const genes = f.human_genes.length ? f.human_genes.join(', ') : (f.other_genes.length ? `(non-human) ${f.other_genes.join(', ')}` : '');
  return `<tr class="${f.role}"><td><code>${esc(f.key)}</code><br><span class="small">${esc(f.name)}</span></td>
    <td><span class="tierchip tier-${esc(f.tier)}">${esc(f.tier)}</span></td>
    <td>${f.human_genes_n === null ? '<span class="mute">not in census</span>' : esc(f.human_genes_n)}</td>
    <td class="small">${esc(f.superfamily || '(none)')}${f.alignable === false ? ' <span class="state open">no tree (D27)</span>' : ''}</td>
    <td class="small">${esc(f.status)}</td><td class="small genes">${esc(genes)}</td></tr>`;
}

route('census', async (args, query) => {
  const c = await api('/census');
  const census = c.families.filter(f => f.role === 'census');
  const control = c.families.filter(f => f.role !== 'census');
  const sel = query.tier || 'all';
  app().innerHTML = `<p class="kicker">census</p><h1>The census, in tiers</h1>
  <p class="lead">${esc(c.catalogue.human_genes_census)} human genes in ${esc(c.catalogue.families_census)} census families,
    out of ${esc(c.catalogue.human_genes_catalogued)} human genes catalogued in ${esc(c.catalogue.families_total)} families.
    The others are catalogued so that they can be excluded: auxiliary subunits, pumps, exchangers, sensors, and channels
    gated by calcium that do not conduct it.</p>
  ${tierTiles(c.tiers)}
  ${prov(c.source[0])}
  <div class="callout">Tier assignments rest on literature permeability values (<code>Provenance.LIT</code>) that no
    database holds and nothing has audited yet: <mark class="pending">(pending: S1b)</mark>, the permeability audit,
    is ${state('pending')} in the ledger.</div>
  <div class="panel"><h3>Census families</h3>
    <div class="seg" role="group" aria-label="Filter by tier">${list(['all', ...Object.keys(TIERS)], t =>
      `<button data-t="${t}" class="${t === sel ? 'on' : ''}">${esc(t)}</button>`)}</div>
    <div class="scroll"><table class="fam"><thead><tr><th>family</th><th>tier</th><th>human genes</th><th>superfamily</th><th>status</th><th>members</th></tr></thead>
    <tbody id="cfam"></tbody></table></div>
    <p class="small mute">"human genes" is the <code>human_genes</code> column of the S1 coverage table; families with 0 are
      plant or viral families with no human member.</p>
    ${prov(c.source.slice(1))}</div>
  ${panel('Excluded families: catalogued so they can be excluded', `<p class="small mute">${esc(control.length)} control
    families. Each is in the catalogue because a search for "calcium channel" returns it; its status says what it is instead.</p>
    <div class="scroll"><table class="fam"><thead><tr><th>family</th><th>calcium relation</th><th>counted</th><th>superfamily</th><th>status</th><th>human genes</th></tr></thead>
    <tbody>${list([...control].sort((a, b) => ORDER.indexOf(a.tier) - ORDER.indexOf(b.tier) || a.status.localeCompare(b.status)), famRow)}</tbody></table></div>`,
    [c.source[1], c.source[3]])}`;
  const draw = t => {
    const rows = census.filter(f => t === 'all' || f.tier === t).sort((a, b) => ORDER.indexOf(a.tier) - ORDER.indexOf(b.tier));
    document.getElementById('cfam').innerHTML = list(rows, famRow);
  };
  app().querySelectorAll('.seg button').forEach(b => b.addEventListener('click', () => {
    app().querySelectorAll('.seg button').forEach(x => x.classList.toggle('on', x === b));
    draw(b.dataset.t);
  }));
  draw(sel);
});
