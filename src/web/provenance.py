"""Read committed files for the dashboard, and say where each one came from.

Every panel on the dashboard is backed by one or more files that are tracked by git. `source(rel)` returns the
provenance record shown under a panel (path, the commit that last changed the file, its date, and whether the working
copy differs from that commit); `read_tsv` / `read_json` / `read_text` read the file and refuse anything git does not
track, so nothing unpublished can reach the public site. The static build is stricter still: `scripts/build_static.py`
fails when a served file is modified or untracked (see `served_problems()`).
"""
from __future__ import annotations

import csv
import json
import subprocess
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO_URL = "https://github.com/gddickinson/calcium_channel_genes"

#: every repo path a response was built from, so the build can audit them
SERVED: set[str] = set()


def _git(*args: str) -> str:
    try:
        r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return r.stdout.strip() if r.returncode == 0 else ""


@lru_cache(maxsize=None)
def tracked_files() -> frozenset[str]:
    """Paths git tracks (empty when git is unavailable, which makes every read fail loudly)."""
    return frozenset(_git("ls-files").splitlines())


@lru_cache(maxsize=None)
def head() -> dict:
    out = _git("log", "-1", "--format=%H%x09%h%x09%cs%x09%s")
    full, short, date, subject = (out.split("\t") + ["", "", "", ""])[:4]
    return {"commit": short or "unknown", "full": full, "date": date, "subject": subject}


@lru_cache(maxsize=None)
def _modified() -> frozenset[str]:
    return frozenset(_git("diff", "--name-only", "HEAD").splitlines())


@lru_cache(maxsize=None)
def source(rel: str) -> dict:
    """Provenance of one committed file: path, last commit touching it, its date, a GitHub link."""
    out = _git("log", "-1", "--format=%H%x09%h%x09%cs", "--", rel)
    full, short, date = (out.split("\t") + ["", "", ""])[:3]
    ref = full or "main"
    return {"path": rel, "commit": short or "unknown", "date": date,
            "url": f"{REPO_URL}/blob/{ref}/{rel}", "modified": rel in _modified()}


def _path(rel: str) -> Path:
    if rel not in tracked_files():
        raise FileNotFoundError(f"{rel} is not a committed file; the dashboard only shows committed outputs")
    SERVED.add(rel)
    return ROOT / rel


def read_text(rel: str) -> str:
    return _path(rel).read_text(encoding="utf-8")


def read_json(rel: str):
    return json.loads(read_text(rel))


def read_tsv(rel: str) -> dict:
    """A TSV as {columns, rows (lists of strings, exactly as committed), source}."""
    with _path(rel).open(encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh, delimiter="\t"))
    columns = rows[0] if rows else []
    body = [r + [""] * (len(columns) - len(r)) for r in rows[1:] if any(c.strip() for c in r)]
    return {"columns": columns, "rows": body, "source": source(rel)}


def tsv_records(rel: str) -> list[dict]:
    t = read_tsv(rel)
    return [dict(zip(t["columns"], r)) for r in t["rows"]]


def served_problems() -> list[str]:
    """Served files that are untracked or differ from HEAD (the static build refuses to publish these)."""
    return sorted(f"{rel}: modified since {head()['commit']}" for rel in SERVED if rel in _modified())
