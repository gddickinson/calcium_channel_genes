"""Assemble the dashboard's views from committed files (no number is computed or typed here).

overview()  headline counts from the S0 / S1 summary JSONs plus ledger progress
census()    the four tiers (S0 summary) and every family: role/superfamily from rule_coverage.tsv, per-family human
            gene counts from coverage.tsv, and the labels (name, tier, status, gene symbols) from src/catalogue,
            which is the repo's committed definition of its subject
phylogeny() committed tree files (if any), the phylogeny tasks' ledger state, and the superfamilies with the
            alignable flag that decides which get a tier-2 tree (D27)
ledger()    both ledger tables (parsed by scripts/dashboard.py:parse_ledger, the repo's own parser), the emergent
            tasks and their status words, and the questions Q1-Q7
pending()   every "(pending: task)" marker in FINDINGS.md and the review, with the sentence it qualifies
"""
from __future__ import annotations

import importlib.util
import re
from functools import lru_cache

from . import provenance as pv
from .sources import FINDINGS, REVIEW, ROADMAP, SUMMARY_S0, SUMMARY_S1, TABLES


def _src(*paths: str) -> list[dict]:
    return [pv.source(p) for p in paths]


@lru_cache(maxsize=None)
def _dashboard():
    """The repo's own dashboard module (stdlib only), so the ledger is parsed exactly as the project parses it."""
    spec = importlib.util.spec_from_file_location("ccg_dashboard", pv.ROOT / "scripts" / "dashboard.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ledger_tasks() -> list[dict]:
    pv.read_text(ROADMAP)  # registers the file as served (and refuses it if uncommitted)
    return _dashboard().parse_ledger()


def _md_table(text: str, heading: str) -> list[list[str]]:
    """Rows of the first markdown table under `## heading`."""
    sect = text.split(f"## {heading}", 1)
    if len(sect) < 2:
        return []
    rows = []
    for line in sect[1].split("\n## ", 1)[0].splitlines():
        if line.startswith("|") and not re.match(r"^\|[\s\-|]+\|$", line):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows[1:]  # drop the header


def _status_word(status: str) -> str:
    s = re.sub(r"\*\*|`", "", status).lower()
    if s.startswith("closed"):
        return "closed"
    if s.startswith("half closed"):
        return "half closed"
    return "open"


def ledger() -> dict:
    text = pv.read_text(ROADMAP)
    emergent = [{"added": r[0], "origin": r[1], "task": r[2], "status": r[3], "state": _status_word(r[3])}
                for r in _md_table(text, "Emergent tasks & new aims") if len(r) >= 4]
    questions = re.findall(r"^- \*\*(Q\d)\*\* — (.+?)(?=^- \*\*Q|\n\n|\Z)", text.split("## The questions", 1)[-1],
                           flags=re.M | re.S)
    return {"tasks": ledger_tasks(), "emergent": emergent,
            "questions": [{"id": q, "text": " ".join(t.split())} for q, t in questions],
            "source": _src(ROADMAP)}


def progress(tasks: list[dict]) -> dict:
    states = [t["state"] for t in tasks]
    return {"total": len(tasks), "completed": states.count("completed"),
            "in_progress": states.count("in_progress"), "pending": states.count("pending")}


def overview() -> dict:
    s0, s1 = pv.read_json(SUMMARY_S0), pv.read_json(SUMMARY_S1)
    tasks = ledger_tasks()
    return {"catalogue": s0["catalogue"], "tiers": s0["tiers"], "s0": {k: s0[k] for k in
            ("generated", "requests", "elapsed_s", "pfam", "exemplars", "taxonomy", "superfamilies_not_alignable")},
            "s0_request_failures": len(s0.get("request_failures", [])),
            "s1": s1, "progress": progress(tasks), "trees": len(committed_trees()),
            "done": [t for t in tasks if t["state"] == "completed"],
            "next": next((t for t in tasks if t["state"] == "in_progress"), None)
            or next((t for t in tasks if t["state"] == "pending"), None),
            "head": pv.head(), "source": _src(SUMMARY_S0, SUMMARY_S1, ROADMAP)}


def census() -> dict:
    from src.catalogue import registry as reg  # stdlib-only; the authoritative definition of the subject

    s0 = pv.read_json(SUMMARY_S0)
    roles = {r["family"]: r for r in pv.tsv_records(TABLES["rule_coverage"][0])}
    counts = {r["family"]: r for r in pv.tsv_records(TABLES["coverage"][0])}
    pv.SERVED.update(f"src/catalogue/{p.name}" for p in (pv.ROOT / "src" / "catalogue").glob("*.py"))
    families = []
    for key, row in roles.items():
        fam = reg.family(key)
        sf = reg.SUPERFAMILIES.get(fam.superfamily)
        cov = counts.get(key)
        families.append({
            "key": key, "name": fam.name, "role": row["role"], "superfamily": row["superfamily"],
            "superfamily_name": sf.name if sf else "", "alignable": sf.alignable if sf else None, "status": fam.status.value,
            "tier": fam.permeability.ca_class.value, "permeability_provenance": fam.permeability.provenance.value,
            "human_genes_n": cov["human_genes"] if cov else None,
            "human_genes": list(fam.human_genes), "other_genes": list(fam.other_genes),
            "rule_verdict": row["verdict"], "hazards": row["hazards"]})
    return {"tiers": s0["tiers"], "catalogue": s0["catalogue"],
            "superfamilies_not_alignable": s0["superfamilies_not_alignable"], "families": families,
            "source": _src(SUMMARY_S0, TABLES["rule_coverage"][0], TABLES["coverage"][0], "src/catalogue/registry.py")}


_PENDING = re.compile(r"\(\*?pending:\s*([^)]*?)\*?\)")


def pending() -> dict:
    """Every pending marker, with the ledger state of each task it names (a marker naming a completed task is due
    for the sweep the evidence-audit rule asks for: promote it or re-word it)."""
    states = {t["id"]: t["state"] for t in ledger_tasks()}
    out = []
    for rel in (FINDINGS, REVIEW):
        heading = ""
        paras = re.split(r"\n\s*\n", pv.read_text(rel))
        for para in paras:
            if para.startswith("#"):
                heading = para.splitlines()[0].lstrip("# ").strip()
            for m in _PENDING.finditer(para):
                on = " ".join(m.group(1).split()).rstrip("*. ")
                if on == "task":  # the file's own definition of the marker
                    continue
                flat = " ".join(para.split())
                tasks = re.findall(r"\bS\d+[a-z]?\b", on)
                out.append({"file": rel, "section": heading, "on": on,
                            "tasks": [{"id": t, "state": states.get(t, "unknown")} for t in tasks],
                            "context": flat[:420] + ("..." if len(flat) > 420 else "")})
    return {"markers": out, "source": _src(FINDINGS, REVIEW, ROADMAP)}


TREE_SUFFIXES = (".treefile", ".contree", ".nwk", ".newick", ".tre", ".tree")
PHYLO_TASKS = ("S6", "S7", "S8", "S9", "S12", "S18")


def committed_trees() -> list[dict]:
    """Every tree file git tracks (none until S7/S8 commit theirs)."""
    return [pv.source(p) for p in sorted(pv.tracked_files()) if p.endswith(TREE_SUFFIXES)]


def phylogeny() -> dict:
    from src.catalogue import registry as reg

    s0 = pv.read_json(SUMMARY_S0)
    tasks = [t for t in ledger_tasks() if t["id"] in PHYLO_TASKS]
    sfs = [{"key": k, "name": sf.name, "alignable": sf.alignable, "fold": sf.fold.value,
            "root_with": list(sf.root_with), "anchor_module": sf.anchor_module}
           for k, sf in reg.SUPERFAMILIES.items()]
    return {"trees": committed_trees(), "tasks": tasks, "not_alignable": s0["superfamilies_not_alignable"],
            "superfamilies": sfs,
            "source": _src(SUMMARY_S0, ROADMAP, "src/catalogue/registry.py", "docs/phylogeny_protocol.md")}
