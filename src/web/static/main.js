// Entry point: registers the page modules (loaded on first visit), sets the mode line and starts the router.
import { start, lazy, route, app, $, isStatic } from './core.js';

const PAGES = {
  'home.js': ['home', 'about'], 'census.js': ['census'], 'stages.js': ['verification', 'benchmark'],
  'phylogeny.js': ['phylogeny'], 'roadmap.js': ['roadmap', 'pending'],
  'docs.js': ['findings', 'review', 'scope', 'doc', 'figures', 'tables', 'table'],
};
lazy(Object.fromEntries(Object.entries(PAGES).flatMap(([file, names]) => names.map(n => [n, () => import('./' + file)]))));

route('notfound', () => { app().innerHTML = '<h1>Not found</h1><p><a href="#/">Back to the start</a></p>'; });

$('#mode').textContent = isStatic() ? 'static site: read-only snapshot of the committed outputs' : 'local app';
start();
