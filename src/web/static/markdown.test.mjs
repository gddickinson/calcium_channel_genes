// node markdown.test.mjs: the renderer handles the constructs used in the repo's reports, FINDINGS.md and the review,
// marks (pending: task) in both of the repo's spellings, and never passes raw HTML through.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { render, inline, joinPath } from './markdown.js';

const { html, toc } = render('# Title\n\n## Part\n\nText *soft* and `code`.\n\n- one\n- two\n  continued\n\n1. first\n\n---\n\n## Part\n');
assert.match(html, /<h2 id="title">Title<\/h2>/);
assert.match(html, /<h3 id="part-1">/, 'duplicate headings get unique ids');
assert.match(html, /<em>soft<\/em>/);
assert.match(html, /<ul><li>one<\/li><li>two continued<\/li><\/ul>/);
assert.match(html, /<ol><li>first<\/li><\/ol>/);
assert.deepEqual(toc.map(t => t.level), [1, 2, 2]);

// pipe tables (with an empty header row, as in the review's figure list) and blockquotes
const t = render('| tier | n |\n|---|---|\n| ca_selective | 28 |\n\n| | |\n|---|---|\n| **1** | folds |\n\n> quoted **bold**\n> more');
assert.match(t.html, /<thead><tr><th>tier<\/th><th>n<\/th><\/tr><\/thead><tbody><tr><td>ca_selective<\/td><td>28<\/td><\/tr><\/tbody>/);
assert.match(t.html, /<table><tbody><tr><td><strong>1<\/strong><\/td><td>folds<\/td>/, 'empty header row is dropped');
assert.match(t.html, /<blockquote><p>quoted <strong>bold<\/strong> more<\/p><\/blockquote>/);

// fenced code is escaped verbatim
assert.match(render('```\na <b> *x*\n```').html, /<pre>a &lt;b&gt; \*x\*<\/pre>/);

// pending markers, FINDINGS spelling *(pending: S1b)* and review spelling (*pending: S9*)
assert.match(inline('rests on it *(pending: S1b)*.'), /<mark class="pending">\(pending: S1b\)<\/mark>/);
assert.match(inline('subunits (*pending: S9*).'), /<mark class="pending">\(pending: S9\)<\/mark>/);

// images: published figures resolve against the document folder; anything else is not shown
const figs = new Set(['docs/figures/fig1_folds.png']);
assert.match(render('![](figures/fig1_folds.png)', { base: 'docs', figures: figs }).html, /<img src="files\/docs\/figures\/fig1_folds.png"/);
assert.match(render('![](figures/other.png)', { base: 'docs', figures: figs }).html, /not published on this site/);
assert.equal(joinPath('results/s0_baseline', '../benchmark_controls/report.md'), 'results/benchmark_controls/report.md');
assert.match(inline('[`report.md`](results/s0_baseline/report.md)'), /href="https:\/\/github.com\/gddickinson\/calcium_channel_genes\/blob\/main\/results\/s0_baseline\/report.md"/);

// safety
assert.equal(inline('<script>alert(1)</script>'), '&lt;script&gt;alert(1)&lt;/script&gt;');
assert.doesNotMatch(inline('[x](javascript:alert(1))'), /href="javascript/);

// the repo's real documents render without throwing and keep their pending markers
const root = fileURLToPath(new URL('../../../', import.meta.url));
for (const [rel, minMarks] of [['FINDINGS.md', 5], ['docs/channel_review_2026.md', 5]]) {
  const out = render(readFileSync(root + rel, 'utf8'), { base: rel.split('/').slice(0, -1).join('/'), figures: figs });
  assert.ok((out.html.match(/class="pending"/g) || []).length >= minMarks, rel);
  assert.doesNotMatch(out.html, /<script/i, rel);
}
console.log('markdown tests passed');
