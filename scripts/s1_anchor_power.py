"""S1 — how much does each projection anchor actually discriminate?

`classify()` runs exactly one anchor: the four-repeat locus. The TRPV and
ORAI anchors are declared in `src/classify/motifs.py`, verified live by
`scripts/s0_anchors.py`, and then **never projected onto anything**. So the
project has three anchors and a measurement of one, and hazard **HC7b**
("TRPV6 beside TRPV1 — identical architecture, hundredfold difference in
P_Ca/P_Na") is currently closed by a test nobody has run.

This script runs each anchor over the panel members it claims to apply to and
records what it reads. A discriminating anchor gives one residue to the
calcium members and a different one to the decoys. An anchor that gives every
member the same residue is not a test — and the honest thing is to say so and
leave the hazard open, not to keep the anchor and quietly stop asking.

The brief names this as one of S1's three headline results:

    "Does the TRPV anchor discriminate at all? TRPV1-4 carry acidic residues
     in the outer pore too. If projecting TRPV6's D582 returns D for all of
     them, HC7b has no positive test - record that, do not quietly drop it."

Every projection is gated on `verify_anchor()` first (D28): a reference that
no longer reads what the anchor claims makes every projection from it
silently wrong.

    python3 scripts/s1_anchor_power.py [--out results/benchmark_controls]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.s0_lib import write_tsv
from src.catalogue import CATALOGUE
from src.classify.motifs import ANCHORS, filter_signature, verify_anchor
from src.classify.reference import fetch_uniprot_sequence
from src.cli_channel import resolve_symbol
from src.utils.http import FetchFailed
from src.utils.http import ledger as http_ledger
from src.utils.mafft import MafftUnavailable, mafft_available, mafft_version

HEADER = ("anchor", "gene", "accession", "family", "expected_group",
          "projected", "reference_reads", "same_as_reference", "note")

SUMMARY_HEADER = ("anchor", "reference", "positions", "expected",
                  "n_projected", "n_distinct_strings", "distinct_strings",
                  "discriminates", "verdict")


def log(m: str) -> None:
    print(f"[s1-anchor] {m}", flush=True)


def panel_for(anchor) -> list[tuple[str, str]]:
    """`(gene symbol, family key)` for every human gene in the anchor's scope.

    Read from the catalogue, never hard-coded — the anchor declares which
    families it applies to and the catalogue says which genes those are.
    """
    out: list[tuple[str, str]] = []
    for key in anchor.applies_to:
        fam = CATALOGUE.get(key)
        if not fam:
            continue
        for gene in fam.human_genes:
            out.append((gene, key))
    return out


def run_anchor(anchor, cap: int, seq_cache: dict[str, str]) -> tuple[list, dict]:
    """Project one anchor over its declared families. Returns (rows, summary)."""
    log(f"anchor {anchor.key}: reference {anchor.reference_label} "
        f"({anchor.reference_uniprot}) positions {anchor.positions} "
        f"expected {anchor.expected!r}")
    try:
        ref = fetch_uniprot_sequence(anchor.reference_uniprot)
    except FetchFailed as exc:
        log(f"  reference NOT FETCHED — {exc.reason}; this anchor is "
            f"unmeasured, which is not the same as undiscriminating")
        return [], {"anchor": anchor.key, "verdict": "unmeasured: "
                    f"reference fetch failed ({exc.reason})"}
    if not verify_anchor(ref, anchor):
        log(f"  ANCHOR DRIFT — {anchor.reference_uniprot} ({len(ref)} aa) no "
            f"longer reads {anchor.expected!r} at {anchor.positions}; "
            f"refusing to project (D28)")
        return [], {"anchor": anchor.key,
                    "verdict": "REFUSED: anchor does not validate"}
    log(f"  reference validates ({len(ref)} aa)")

    rows: list[tuple] = []
    projected: dict[str, list[str]] = {}
    members = panel_for(anchor)[:cap] if cap else panel_for(anchor)
    for i, (gene, family_key) in enumerate(members, 1):
        try:
            acc = resolve_symbol(gene)
        except FetchFailed as exc:
            log(f"  [{i}/{len(members)}] {gene}: lookup failed ({exc.reason})")
            continue
        if not acc:
            log(f"  [{i}/{len(members)}] {gene}: no reviewed human entry")
            continue
        seq = seq_cache.get(acc, "")
        if not seq:
            try:
                seq = fetch_uniprot_sequence(acc)
            except FetchFailed as exc:
                log(f"  [{i}/{len(members)}] {gene}: fetch failed "
                    f"({exc.reason})")
                continue
            seq_cache[acc] = seq
        if not seq:
            continue
        try:
            sig = filter_signature(seq, ref, anchor)
        except (MafftUnavailable, RuntimeError) as exc:
            log(f"  [{i}/{len(members)}] {gene}: projection failed "
                f"({str(exc)[:60]})")
            continue
        same = "yes" if sig == anchor.expected else "no"
        call = anchor.calls.get(sig)
        rows.append((anchor.key, gene, acc, family_key,
                     CATALOGUE[family_key].ca_class().value, sig,
                     anchor.expected, same,
                     call[1] if call else "no call for this string"))
        projected.setdefault(sig, []).append(gene)
        log(f"  [{i}/{len(members)}] {gene:10s} {acc:10s} {family_key:16s} "
            f"→ {sig!r}")
        time.sleep(0.05)

    distinct = sorted(projected)
    # Discrimination is not "more than one string exists" — it is "the census
    # members read something the non-census members do not". Measured per
    # ca_class so a split inside one tier does not count as separating tiers.
    by_class: dict[str, set[str]] = {}
    for r in rows:
        by_class.setdefault(r[4], set()).add(r[5])
    classes = sorted(by_class)
    separates = (len(classes) > 1 and
                 all(not (by_class[a] & by_class[b])
                     for i_, a in enumerate(classes) for b in classes[i_ + 1:]))
    if len(classes) < 2:
        verdict = (f"untested: every projected member is in one tier "
                   f"({classes[0] if classes else 'none'}) — this panel "
                   f"cannot separate anything")
    elif separates:
        verdict = ("discriminates: no projected string is shared between "
                   "permeability tiers")
    else:
        shared = sorted(set.intersection(*(by_class[c] for c in classes)))
        verdict = (f"DOES NOT discriminate: {', '.join(repr(s) for s in shared)} "
                   f"is read by members of more than one permeability tier")
    log(f"  {len(rows)} projected, {len(distinct)} distinct string(s): "
        f"{', '.join(repr(d) for d in distinct)}")
    log(f"  verdict — {verdict}")
    return rows, {
        "anchor": anchor.key,
        "reference": f"{anchor.reference_label} {anchor.reference_uniprot}",
        "positions": "/".join(str(p) for p in anchor.positions),
        "expected": anchor.expected,
        "n_projected": len(rows),
        "n_distinct_strings": len(distinct),
        "distinct_strings": "; ".join(
            f"{d}={','.join(projected[d])}" for d in distinct),
        "discriminates": "yes" if separates else "no",
        "verdict": verdict,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path,
                    default=ROOT / "results" / "benchmark_controls")
    ap.add_argument("--cap", type=int, default=0,
                    help="limit members per anchor (debugging only)")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    if not mafft_available():
        log("MAFFT is not on PATH. Every anchor here is a projection and "
            "there is no weaker fallback, so this measurement does not run "
            "(D28).")
        return 1
    log(f"mafft: {mafft_version()}")

    all_rows: list[tuple] = []
    summaries: list[dict] = []
    seq_cache: dict[str, str] = {}
    for key in ("four_repeat", "trpv_ca_ring", "orai_e106"):
        rows, summary = run_anchor(ANCHORS[key], args.cap, seq_cache)
        all_rows.extend(rows)
        summaries.append(summary)
        log("")

    write_tsv(args.out / "anchor_power.tsv", HEADER, all_rows)
    write_tsv(args.out / "anchor_summary.tsv", SUMMARY_HEADER,
              [tuple(s.get(k, "") for k in SUMMARY_HEADER) for s in summaries])
    (args.out / "anchor_summary.json").write_text(json.dumps(
        {"generated": time.strftime("%Y-%m-%d %H:%M:%S"),
         "mafft": mafft_version(),
         "anchors": summaries,
         "http": http_ledger()}, indent=2))
    log(f"→ {args.out / 'anchor_power.tsv'} ({len(all_rows)} projection(s))")
    log(f"→ {args.out / 'anchor_summary.tsv'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
