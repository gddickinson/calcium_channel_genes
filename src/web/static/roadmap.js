// Roadmap (the ledger, emergent tasks and the seven questions, parsed from PUBLICATION_ROADMAP.md by the repo's own
// dashboard parser) and Pending claims (every "(pending: task)" marker, checked against the ledger).
import { route, app, api, esc, list } from './core.js';
import { prov, state, panel } from './ui.js';
import { inline } from './markdown.js';

route('roadmap', async (args, query) => {
  const L = await api('/ledger');
  const show = query.show || 'all';
  const tasks = L.tasks.filter(t => show === 'all' || t.state === show);
  app().innerHTML = `<p class="kicker">roadmap</p><h1>The task ledger</h1>
  <p class="lead">Each row is one session's task, with the status word the roadmap itself records. Results are the
    ledger's own headline text for completed tasks.</p>
  <div class="seg" role="group" aria-label="Filter by status">${list(['all', 'completed', 'in_progress', 'pending'], s =>
    `<a class="btn alt ${s === show ? 'on' : ''}" href="#/roadmap?show=${s}">${esc(s)}</a>`)}</div>
  <div class="panel"><div class="scroll"><table class="ledger"><thead><tr><th>task</th><th>status</th><th>depends on</th><th>task and results</th></tr></thead><tbody>
  ${list(tasks, t => `<tr class="st-${t.state}"><td><b>${esc(t.id)}</b></td><td>${state(t.state, t.date)}</td><td class="small">${esc(t.depends)}</td>
    <td>${esc(t.title)}${t.results ? `<details><summary class="small">results</summary><p class="small">${esc(t.results)}</p></details>` : ''}</td></tr>`)}
  </tbody></table></div>${prov(L.source)}</div>
  ${panel('Emergent tasks', `<div class="scroll"><table><thead><tr><th>added</th><th>from</th><th>status</th><th>task</th></tr></thead><tbody>
    ${list(L.emergent, e => `<tr><td class="small">${esc(e.added)}</td><td class="small">${esc(e.origin)}</td><td>${state(e.state)}</td>
      <td class="small">${esc(e.task.replace(/\*\*|`/g, ''))}<details><summary class="small">status note</summary><p class="small">${esc(e.status.replace(/\*\*|`/g, ''))}</p></details></td></tr>`)}
    </tbody></table></div>`, L.source)}
  ${panel('The questions this project answers', `<ol class="qs">${list(L.questions, q => `<li><b>${esc(q.id)}</b> ${esc(q.text)}</li>`)}</ol>`, L.source)}`;
});

route('pending', async () => {
  const P = await api('/pending');
  const due = P.markers.filter(m => m.tasks.some(t => t.state === 'completed'));
  app().innerHTML = `<p class="kicker">evidence audit</p><h1>Pending claims</h1>
  <p class="lead">A claim that depends on an unfinished task is written <mark class="pending">(pending: task)</mark>.
    These are all of them, in FINDINGS.md and the review, with the ledger status of each task they wait on.</p>
  <div class="tiles"><div class="tile"><b>${esc(P.markers.length)}</b><span>pending markers</span></div>
    <div class="tile"><b>${esc(due.length)}</b><span>name a task the ledger marks completed: due for a re-read</span></div></div>
  <div class="panel"><div class="scroll"><table><thead><tr><th>waits on</th><th>where</th><th>the claim</th></tr></thead><tbody>
  ${list(P.markers, m => `<tr class="${m.tasks.some(t => t.state === 'completed') ? 'r-warn' : ''}">
    <td>${m.tasks.length ? list(m.tasks, t => `<div><b>${esc(t.id)}</b> ${state(t.state)}</div>`) : esc(m.on)}</td>
    <td class="small"><code>${esc(m.file)}</code><br>${esc(m.section)}</td><td class="small">${inline(m.context)}</td></tr>`)}
  </tbody></table></div>
  <p class="small mute">Marked rows wait on a task the ledger already records as completed. Per the project's own rule,
    when a task finishes the markers pending on it are swept: promoted to a plain statement or re-worded. The ledger
    records that the review was written against S0 only.</p>
  ${prov(P.source)}</div>`;
});
