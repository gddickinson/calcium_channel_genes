"""Web interface tests: every exported endpoint answers, the static build is complete, the JS tests pass, and the
dashboard's evidence rules hold (committed files only, census tiers consistent across the committed tables).

Run: python -m pytest -q tests/test_web.py
"""
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.web import provenance as pv  # noqa: E402
from src.web.app import FILES, STATIC, STATIC_ENDPOINTS, app  # noqa: E402
from src.web.sources import SUMMARY_S0, TABLES  # noqa: E402

client = TestClient(app)


def test_index_served():
    r = client.get("/")
    assert r.status_code == 200 and "static/main.js" in r.text


@pytest.mark.parametrize("path", STATIC_ENDPOINTS)
def test_endpoint(path):
    r = client.get("/api" + path)
    assert r.status_code == 200, r.text
    assert r.json() is not None


def test_static_build(tmp_path):
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_static
    build_static.build(tmp_path / "site")
    assert (tmp_path / "site" / "index.html").read_text().count("APP_STATIC") == 1
    for path in STATIC_ENDPOINTS:
        assert (tmp_path / "site" / "api" / (path.strip("/") + ".json")).exists()
    for rel in FILES:
        assert (tmp_path / "site" / "files" / rel).exists()
    size = sum(f.stat().st_size for f in (tmp_path / "site").rglob("*") if f.is_file())
    assert size < 50e6, size


def test_static_assets_referenced_exist():
    html = (STATIC / "index.html").read_text()
    for name in ("style.css", "main.js"):
        assert f"static/{name}" in html and (STATIC / name).exists()


@pytest.mark.skipif(not shutil.which("node"), reason="node not installed")
def test_js_engine():
    tests = sorted(STATIC.glob("*.test.mjs"))
    for t in tests:
        r = subprocess.run(["node", str(t)], capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr


# --- evidence rules -------------------------------------------------------------------------------------------------

def test_only_committed_files_are_read(tmp_path):
    with pytest.raises(FileNotFoundError):
        pv.read_text("dashboard.html")  # generated and gitignored
    with pytest.raises(FileNotFoundError):
        pv.read_text("results/does_not_exist.tsv")


def test_every_source_is_tracked():
    for path in STATIC_ENDPOINTS:
        client.get("/api" + path)
    tracked = pv.tracked_files()
    assert pv.SERVED and all(rel in tracked for rel in pv.SERVED), sorted(pv.SERVED - tracked)


def test_files_route_serves_only_listed_figures():
    assert client.get("/files/" + FILES[0]).status_code == 200
    assert client.get("/files/README.md").status_code == 404
    assert client.get("/files/data_root.txt").status_code == 404


def test_tables_are_served_as_committed():
    for key, (rel, *_rest) in TABLES.items():
        t = client.get(f"/api/table/{key}").json()
        lines = [ln for ln in (ROOT / rel).read_text(encoding="utf-8").splitlines()[1:] if ln.strip()]
        assert len(t["rows"]) == len(lines), key
        assert t["source"]["path"] == rel and t["source"]["commit"]


def test_census_tiers_agree_across_committed_tables():
    """S0 summary tiers == per-family coverage counts summed by catalogue tier (no flat total is ever served)."""
    c = client.get("/api/census").json()
    summary = pv.read_json(SUMMARY_S0)["tiers"]
    assert c["tiers"] == summary
    by_tier = {}
    for f in c["families"]:
        if f["role"] == "census":
            t = by_tier.setdefault(f["tier"], {"families": 0, "human_genes": 0})
            t["families"] += 1
            t["human_genes"] += int(f["human_genes_n"])
    assert by_tier == summary


def test_overview_numbers_are_the_committed_ones():
    o = client.get("/api/overview").json()
    assert o["catalogue"] == pv.read_json(SUMMARY_S0)["catalogue"]
    assert o["s1"] == pv.read_json(TABLES["recall"][0].rsplit("/", 1)[0] + "/summary.json")
    assert o["progress"]["total"] == len(client.get("/api/ledger").json()["tasks"])


def test_ledger_uses_the_repos_status_words():
    L = client.get("/api/ledger").json()
    ids = [t["id"] for t in L["tasks"]]
    assert len(ids) == len(set(ids)) and "S0" in ids
    assert {t["state"] for t in L["tasks"]} <= {"completed", "in_progress", "pending"}
    assert {e["state"] for e in L["emergent"]} <= {"open", "half closed", "closed"}
    assert [q["id"] for q in L["questions"]] == [f"Q{i}" for i in range(1, 8)]


def test_pending_markers_carry_ledger_state():
    P = client.get("/api/pending").json()["markers"]
    assert P and all(m["file"] in ("FINDINGS.md", "docs/channel_review_2026.md") for m in P)
    states = {t["id"]: t["state"] for t in client.get("/api/ledger").json()["tasks"]}
    for m in P:
        for t in m["tasks"]:
            assert t["state"] == states.get(t["id"], "unknown")


def test_phylogeny_lists_only_committed_trees():
    p = client.get("/api/phylogeny").json()
    assert all(t["path"] in pv.tracked_files() for t in p["trees"])
    assert set(p["not_alignable"]) == {s["key"] for s in p["superfamilies"] if not s["alignable"]}


def test_strict_build_refuses_uncommitted_edits(tmp_path, monkeypatch):
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_static
    monkeypatch.setattr(pv, "_modified", lambda: frozenset({FILES[0]}))
    with pytest.raises(SystemExit, match="uncommitted"):
        build_static.build(tmp_path / "site", allow_dirty=False)
