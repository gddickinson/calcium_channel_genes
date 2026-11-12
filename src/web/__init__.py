"""Read-only web dashboard of the census's committed outputs (local FastAPI app + static GitHub Pages export).

Contents:
    app.py         FastAPI routes under /api, the files/ route for figures, STATIC_ENDPOINTS and FILES for the export
    data.py        overview / census / ledger / pending views assembled from committed files
    provenance.py  committed-file readers that refuse untracked files, and per-file commit provenance
    sources.py     the one list of committed tables, documents and figures the site shows
    static/        the ES-module front end (hash router, one module per page)
"""
