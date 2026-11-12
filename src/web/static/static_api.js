// Static-site data layer: answers api(path) from the JSON files scripts/build_static.py exported (api/<path>.json).
// The dashboard is read-only and every view is precomputed from committed files, so nothing needs the server.
const files = new Map();

export async function staticApi(path, body) {
  if (body) throw new Error('The static site is read-only.');
  const clean = path.split('?')[0].replace(/^\/+|\/+$/g, '');
  if (!files.has(clean)) {
    files.set(clean, fetch('api/' + clean + '.json').then(r => {
      if (!r.ok) throw new Error(`${r.status}: no exported data for ${clean}`);
      return r.json();
    }));
  }
  return files.get(clean);
}
