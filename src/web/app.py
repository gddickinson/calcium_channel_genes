"""FastAPI web app for the calcium-channel census dashboard: read-only views of the committed outputs.

Run with `python run_web.py` (http://127.0.0.1:8177, local only). `scripts/build_static.py` exports every path in
STATIC_ENDPOINTS to JSON (and every file in FILES) for the GitHub Pages site, so keep those lists in step with the
routes below. Every response carries `source`: the committed file(s) it was read from and the commit that last
changed each one.
"""
from __future__ import annotations

import re
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import data
from . import provenance as pv
from .sources import DOCS, FIGURES, REVIEW, REVIEW_FIGURES, STAGE_FIGURES, TABLES

STATIC = Path(__file__).resolve().parent / "static"

app = FastAPI(title="Calcium channels: census dashboard")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/files/{path:path}", include_in_schema=False)
def files(path: str):
    """The committed figures listed in sources.FIGURES (and nothing else)."""
    if path not in FIGURES or path not in pv.tracked_files():
        raise HTTPException(404, "not a published figure")
    return FileResponse(pv.ROOT / path)


@app.get("/api/info")
def info():
    return {"title": "Calcium channels: census, classification and phylogeny", "repo": pv.REPO_URL,
            "head": pv.head()}


@app.get("/api/overview")
def overview():
    return data.overview()


@app.get("/api/census")
def census():
    return data.census()


@app.get("/api/ledger")
def ledger():
    return data.ledger()


@app.get("/api/phylogeny")
def phylogeny():
    return data.phylogeny()


@app.get("/api/pending")
def pending():
    return data.pending()


@app.get("/api/tables")
def tables():
    """Index of every committed table the dashboard shows, with its row count and provenance."""
    out = []
    for key, (rel, task, title, blurb) in TABLES.items():
        t = pv.read_tsv(rel)
        out.append({"key": key, "task": task, "title": title, "blurb": blurb, "rows": len(t["rows"]),
                    "columns": len(t["columns"]), "source": t["source"]})
    return {"tables": out}


@app.get("/api/table/{key}")
def table(key: str):
    if key not in TABLES:
        raise HTTPException(404, f"no table {key}")
    rel, task, title, blurb = TABLES[key]
    return {"key": key, "task": task, "title": title, "blurb": blurb, **pv.read_tsv(rel)}


@app.get("/api/doc/{key}")
def doc(key: str):
    if key not in DOCS:
        raise HTTPException(404, f"no document {key}")
    rel, title = DOCS[key]
    return {"key": key, "title": title, "markdown": pv.read_text(rel), "base": str(Path(rel).parent),
            "source": pv.source(rel)}


def _review_captions() -> dict[str, str]:
    """Figure number -> caption, from the review's own `## Figures` table (`| **N** | caption |`)."""
    text = pv.read_text(REVIEW).split("## Figures", 1)[-1].split("\n## ", 1)[0]
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"^\| \*\*(\d+)\*\* \| (.+?) \|$", text, re.M)}


@app.get("/api/figures")
def figures():
    caps = _review_captions()
    out = []
    for rel in REVIEW_FIGURES:
        num = re.match(r"fig(\d+)_", Path(rel).name).group(1)
        out.append({"path": rel, "group": "review", "label": f"Review figure {num}", "caption": caps.get(num, ""),
                    "source": pv.source(rel)})
    reserved = [{"label": f"Review figure {n}", "caption": c} for n, c in caps.items()
                if not any(Path(f).name.startswith(f"fig{n}_") for f in REVIEW_FIGURES)]
    for rel, (task, cap) in STAGE_FIGURES.items():
        out.append({"path": rel, "group": task, "label": f"{task} figure", "caption": cap, "source": pv.source(rel)})
    return {"figures": out, "reserved": reserved, "captions_from": pv.source(REVIEW)}


# GET paths (without the /api prefix) written to the static site as api/<path>.json.
STATIC_ENDPOINTS = (["/info", "/overview", "/census", "/ledger", "/phylogeny", "/pending", "/tables", "/figures"]
                    + [f"/table/{k}" for k in TABLES] + [f"/doc/{k}" for k in DOCS])
# Committed files copied to the static site at files/<path>.
FILES = list(FIGURES)
