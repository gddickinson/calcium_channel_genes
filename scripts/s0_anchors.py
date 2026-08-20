#!/usr/bin/env python3
"""S0 — re-verify the three projection anchors against live UniProt.

Every filter call this project makes is a projection from one of three
reference sequences, and a projection is only as good as the claim that the
reference itself still reads what the anchor says it reads. A UniProt
sequence-version bump, an isoform boundary moving, or a position copied out
of a paper's numbering all produce the same failure: the alignment still
runs, the projection still returns residues, and every call downstream is
silently wrong.

That failure is not hypothetical here. The TRPV6 anchor sits at **D582**,
not the literature's D542, because the canonical human entry `Q9H1D0` is the
765 aa long isoform — a 40-residue offset that would have projected the
wrong column without complaint. `verify_anchor()` exists for exactly that,
and this script is the S0 stage that runs it against the live database
rather than against a sequence cached at the time the anchor was written.

Three anchors, three UniProt requests, no InterPro traffic:

    four_repeat   Nav1.5   Q14524   372/898/1419/1711  ->  DEKA
    trpv_ca_ring  TRPV6    Q9H1D0   582                ->  D
    orai_e106     ORAI1    Q96D31   106                ->  E

Writes `anchor_verification.tsv` and **exits non-zero on any mismatch**: the
brief calls an anchor failure a stop, not a warning, so it must be able to
fail a session rather than add a row to a report nobody reads.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.s0_lib import Fetcher, sequence, write_tsv          # noqa: E402
from src.classify.motifs import ANCHORS, verify_anchor           # noqa: E402

HEADER = ["anchor", "reference_label", "uniprot", "positions", "expected",
          "observed", "verified", "ref_length", "context", "note"]

#: Residues either side of each anchor position recorded in `context`, so a
#: drift can be diagnosed from the table instead of re-fetching by hand.
FLANK = 4


def context_for(seq: str, positions: tuple[int, ...]) -> str:
    """`567-TIIDGP-572`-style windows, one per anchor position."""
    out = []
    for p in positions:
        lo, hi = max(1, p - FLANK), min(len(seq), p + FLANK)
        window = seq[lo - 1:hi]
        out.append(f"{lo}-{window}-{hi}")
    return ";".join(out)


def check(f: Fetcher, out: Path) -> tuple[int, int]:
    rows, failed = [], 0
    for key, anchor in ANCHORS.items():
        seq = sequence(f, anchor.reference_uniprot)
        if not seq:
            rows.append([key, anchor.reference_label, anchor.reference_uniprot,
                         "/".join(str(p) for p in anchor.positions),
                         anchor.expected, "", "FETCH_FAILED", 0, "",
                         "sequence could not be retrieved"])
            failed += 1
            print(f"  [FAIL] {key}: could not fetch "
                  f"{anchor.reference_uniprot}")
            continue

        short = len(seq) < max(anchor.positions)
        observed = ("" if short else
                    "".join(seq[p - 1] for p in anchor.positions))
        ok = verify_anchor(seq, anchor)
        if not ok:
            failed += 1
        rows.append([key, anchor.reference_label, anchor.reference_uniprot,
                     "/".join(str(p) for p in anchor.positions),
                     anchor.expected, observed, "yes" if ok else "no",
                     len(seq), "" if short else context_for(seq, anchor.positions),
                     anchor.note])
        mark = "ok  " if ok else "FAIL"
        detail = (f"reference is {len(seq)} aa, shorter than position "
                  f"{max(anchor.positions)}" if short
                  else f"reads {observed}, expected {anchor.expected}")
        print(f"  [{mark}] {key:14s} {anchor.reference_label:10s} "
              f"{anchor.reference_uniprot}  {detail}")

    write_tsv(out / "anchor_verification.tsv", HEADER, rows)
    return len(rows), failed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="results/s0_baseline")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    print(f"[anchors] verifying {len(ANCHORS)} projection anchors "
          f"against live UniProt")
    f = Fetcher()
    n, failed = check(f, out)
    print(f"[anchors] wrote {out / 'anchor_verification.tsv'} "
          f"({n} anchors, {f.n_requests} requests)")

    if f.failures:
        for url, why in f.failures:
            print(f"[anchors] request failed: {why}  {url}")
    if failed:
        print(f"[anchors] {failed}/{n} anchors DO NOT VALIDATE — this is a "
              f"stop. Every projected filter call depends on them, and "
              f"`verify_anchor()` will now refuse to project rather than "
              f"return a guess (D26, D28).")
        return 1
    print("[anchors] all anchors validate against the live reference")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
