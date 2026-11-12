// Phylogeny: what the forest will be, which superfamilies are refused a tree by rule (D27), the ledger state of
// every phylogeny task, and any committed tree files (none until S7 / S8 commit theirs).
import { route, app, api, esc, list } from './core.js';
import { prov, state, panel } from './ui.js';

route('phylogeny', async () => {
  const [p, figs] = await Promise.all([api('/phylogeny'), api('/figures')]);
  const forest = figs.figures.find(f => f.path.endsWith('fig7_forest.png'));
  const folds = figs.figures.find(f => f.path.endsWith('fig1_folds.png'));
  const fig = f => f ? `<figure class="panel"><img src="files/${esc(f.path)}" alt="${esc(f.label)}: ${esc(f.caption)}" loading="lazy">
    <figcaption><b>${esc(f.label)}.</b> ${esc(f.caption.replace(/\*/g, ''))}</figcaption>${prov(f.source)}</figure>` : '';
  app().innerHTML = `<p class="kicker">phylogeny</p><h1>A forest, not a tree</h1>
  <p class="lead">There is no tree of calcium channels: unrelated folds share no alignable position. The phylogeny is
    a forest of within-family (tier 1) and within-superfamily (tier 2) trees, plus a structural network between folds
    (tier 3). A tier-2 P-loop tree keeps its sodium and potassium channels, because superfamilies are defined by descent.</p>
  ${panel('Committed trees', p.trees.length
    ? `<ul>${list(p.trees, t => `<li><a href="${esc(t.url)}" target="_blank" rel="noopener"><code>${esc(t.path)}</code></a> @ <code>${esc(t.commit)}</code></li>`)}</ul>`
    : `<p>No tree files are committed yet ${state('pending')}. The tree-building tasks below have not run; this panel
       lists every <code>.treefile</code> / <code>.contree</code> / <code>.nwk</code> git tracks, so it fills in when they do.</p>`)}
  ${panel('Phylogeny tasks in the ledger', `<div class="scroll"><table><thead><tr><th>task</th><th>status</th><th>depends on</th><th>what it does</th></tr></thead><tbody>
    ${list(p.tasks, t => `<tr><td><b>${esc(t.id)}</b></td><td>${state(t.state, t.date)}</td><td class="small">${esc(t.depends)}</td><td class="small">${esc(t.title)}</td></tr>`)}
    </tbody></table></div>`, p.source[1])}
  ${panel('Superfamilies and the D27 rule', `<p class="small">A superfamily marked not alignable gets no tier-2 tree:
    <code>build_tier2()</code> raises <code>NotAlignable</code>, and it joins the tier-3 fold network instead.
    Refused by S0's run: ${list(p.not_alignable, k => `<code>${esc(k)}</code>`, ', ')}.</p>
    <div class="scroll"><table><thead><tr><th>superfamily</th><th>fold</th><th>tier-2 tree</th><th>rooted with</th></tr></thead><tbody>
    ${list(p.superfamilies, s => `<tr><td><code>${esc(s.key)}</code><br><span class="small">${esc(s.name)}</span></td><td class="small">${esc(s.fold)}</td>
      <td>${s.alignable ? '<span class="state completed">alignable</span>' : '<span class="state open">refused (D27)</span>'}</td>
      <td class="small">${esc(s.root_with.join(', '))}</td></tr>`)}</tbody></table></div>`, [p.source[0], p.source[2]])}
  ${fig(forest)}${fig(folds)}
  ${list(figs.reserved, r => `<div class="callout"><b>${esc(r.label)}</b>: ${esc(r.caption.replace(/\*/g, ''))} ${state('pending')}</div>${prov(figs.captions_from)}`)}
  <div id="proto"></div>`;
  const { docPanel } = await import('./ui.js');
  await docPanel(document.getElementById('proto'), 'phylogeny_protocol');
});
