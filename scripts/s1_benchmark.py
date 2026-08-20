"""S1 — measure the classifier against positives and the decoys that look like them.

The parent project's equivalent benchmark is the reason this project has a
hazard registry at all: on its first run, every one of six ryanodine-receptor
decoys was promoted as a candidate IP3 receptor, because RyRs carry all four
IP3R-diagnostic Pfam domains. Specificity was 25/31 and every failure was the
same mistake.

Here there are nineteen such mistakes on the register, so the benchmark is
built around them. `presets/controls_benchmark.json` names positives from
every census family with a resolvable human gene, and a decoy for the
confusions that matter — SCN5A for Cav's architecture, TRPM4 for a
Ca2+-impermeable member of a census family, KCNMA1 and ANO1 for the
Ca2+-*activated* channels, CACNB1 for a calcium-channel symbol on a protein
with no pore, ATP2A1 and SLC8A1 for calcium transport without a pore, CALM1
and CASR for calcium binding and sensing, POMT1 for MIR. The tables answer
four questions:

    recall      does the classifier find each family's own member?
    precision   does it reject each decoy?
    per hazard  did the rule that closes each hazard actually fire?
    per tier    which tier made each correct call — is the architecture tier
                doing the work, or is the reference tier carrying it?

The last one matters most. A classifier whose calls all come from
reference identity is a nearest-neighbour lookup with extra steps, and it
will fail on exactly the sequences a census cares about: the ones with no
close relative in the panel.

    python3 scripts/s1_benchmark.py [--preset controls_benchmark]
                                    [--limit N] [--no-reference]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.s0_lib import live_progress
from src.catalogue import HAZARDS
from src.classify import ReferenceSet, classify_all
from src.classify.motifs import FOUR_REPEAT_ANCHOR, verify_anchor
from src.classify.reference import fetch_uniprot_sequence
from src.classify.report import (CALLS_HEADER, calls_table, confusion_table,
                                 coverage_table, hazard_table, recall_table,
                                 summary_counts, write_tsv)
from src.cli_channel import build_query, resolve_symbol
from src.utils.http import FetchFailed
from src.utils.http import ledger as http_ledger
from src.utils.mafft import mafft_available, mafft_version


def log(m: str) -> None:
    print(f"[s1] {m}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--preset", default="controls_benchmark")
    ap.add_argument("--out", type=Path,
                    default=ROOT / "results" / "benchmark_controls")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--no-reference", action="store_true")
    args = ap.parse_args()

    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    live = ROOT / "results" / "session_live.json"
    t0 = time.time()

    preset = json.loads((ROOT / "presets" / f"{args.preset}.json").read_text())
    targets = list(preset["classify"])
    expected_by_symbol = dict(preset["expected"])
    positives = set(preset.get("positives", []))
    if args.limit:
        targets = targets[:args.limit]

    # -- gate 1: does the four-repeat anchor still validate? --------------
    log("verifying the four-repeat filter anchor "
        f"({FOUR_REPEAT_ANCHOR.reference_label} "
        f"{FOUR_REPEAT_ANCHOR.reference_uniprot} "
        f"{FOUR_REPEAT_ANCHOR.positions} == {FOUR_REPEAT_ANCHOR.expected})")
    # A completion criterion of this task is that `verify_anchor()` passed
    # *before* any filter result was reported, so this gate stops the run
    # rather than quietly turning the motif tier off. It stops for two very
    # different reasons and says which: a fetch that could not be completed is
    # a network problem, while a fetch that succeeded and returned the wrong
    # residues is an anchor drift — and this project has already been bitten
    # once by a real drift (TRPV6 D542 → D582), so the two must never be
    # allowed to look alike.
    try:
        nav_ref = fetch_uniprot_sequence(FOUR_REPEAT_ANCHOR.reference_uniprot)
    except FetchFailed as exc:
        log(f"  ANCHOR NOT FETCHED — {exc.reason}. This is a network failure, "
            f"not a drift: the anchor has not been checked either way.")
        log("  → refusing to report filter calls against an unverified anchor "
            "(D28). Re-run when UniProt answers.")
        return 2
    anchor_ok = bool(nav_ref) and verify_anchor(nav_ref)
    log(f"  anchor {'validates' if anchor_ok else 'DOES NOT VALIDATE'} "
        f"(reference {len(nav_ref)} aa)")
    if not anchor_ok:
        log(f"  ANCHOR DRIFT — {FOUR_REPEAT_ANCHOR.reference_uniprot} was "
            f"fetched ({len(nav_ref)} aa) but positions "
            f"{FOUR_REPEAT_ANCHOR.positions} no longer read "
            f"{FOUR_REPEAT_ANCHOR.expected}. Every projected filter call in "
            f"this project is now suspect; fix the anchor before re-running.")
        return 3

    # -- gate 2: is MAFFT there? -----------------------------------------
    log(f"mafft: {mafft_version() or 'NOT AVAILABLE'}")
    if not mafft_available():
        log("  → both the motif and reference tiers are unavailable; this "
            "run measures the architecture tier alone (D28)")

    # -- reference panel --------------------------------------------------
    refs = None
    if not args.no_reference:
        cache = ROOT / "results" / "s0_baseline" / "reference_panel.fasta"
        if cache.exists():
            refs = ReferenceSet.from_fasta(cache)
            log(f"reference panel: {len(refs.sequences)} exemplars from "
                f"{cache.relative_to(ROOT)}")
        else:
            log(f"no reference panel at {cache.relative_to(ROOT)} — run "
                f"scripts/s0_catalogue_verify.py first")

    # -- fetch evidence ---------------------------------------------------
    steps = [(t, False) for t in targets]
    live_progress(live, "S1", steps)
    queries, expected, alias = [], {}, {}
    # A panel member that could not be fetched is MISSING, not wrong. Scoring
    # it as a miss would understate recall for a reason that has nothing to do
    # with the classifier, so it is held here and reported separately.
    missing: list[tuple[str, str]] = []
    for i, sym in enumerate(targets):
        try:
            acc = sym if (len(sym) in (6, 10) and sym[1:2].isdigit()) \
                else resolve_symbol(sym)
        except FetchFailed as exc:
            log(f"  [{i+1}/{len(targets)}] {sym}: LOOKUP FAILED ({exc.reason})")
            missing.append((sym, f"symbol lookup: {exc.reason}"))
            continue
        if not acc:
            log(f"  [{i+1}/{len(targets)}] {sym}: no reviewed human entry")
            missing.append((sym, "no reviewed UniProt entry for this symbol"))
            continue
        try:
            q = build_query(acc)
        except FetchFailed as exc:
            log(f"  [{i+1}/{len(targets)}] {sym} {acc}: EVIDENCE FETCH FAILED "
                f"({exc.reason})")
            missing.append((sym, f"evidence fetch: {exc.reason}"))
            continue
        alias[acc] = sym
        if sym in expected_by_symbol:
            expected[acc] = expected_by_symbol[sym]
        queries.append(q)
        steps[i] = (sym, True)
        if (i + 1) % 5 == 0:
            live_progress(live, "S1", steps)
        log(f"  [{i+1}/{len(targets)}] {sym:10s} {acc:10s} "
            f"{q.length_aa or '?':>5} aa  {len(q.pfam_counts)} pfam  "
            f"tm={q.tm_count}")
    live_progress(live, "S1", steps)

    # -- classify ---------------------------------------------------------
    n_self = 0
    if refs:
        panel_accs = {q.accession for q in queries}
        n_self = len(panel_accs & set(refs.accession_of.values()))
        log(f"{n_self}/{len(queries)} panel proteins are themselves catalogue "
            f"exemplars — classifying leave-one-out so the reference tier "
            f"cannot score a protein against itself")
    log(f"classifying {len(queries)} protein(s)… "
        f"(each is up to {12} MAFFT alignments against the panel)")
    calls = classify_all(queries, refs, nav_ref, leave_one_out=True,
                         on_progress=lambda m: log(f"  {m}"))
    for c in calls:
        c.gene_symbol = alias.get(c.query, c.gene_symbol)

    # -- tables -----------------------------------------------------------
    write_tsv(out / "calls.tsv", CALLS_HEADER, calls_table(calls, expected))
    write_tsv(out / "confusion.tsv", ("expected", "called", "n"),
              confusion_table(calls, expected))
    positive_accs = {c.query for c in calls if alias.get(c.query) in positives}
    write_tsv(out / "recall.tsv",
              ("family", "panel_role", "name", "n", "correct", "recall",
               "decisive_tiers", "confidence", "mis_calls"),
              recall_table(calls, expected, positive_accs))
    write_tsv(out / "hazards.tsv",
              ("hazard", "severity", "families", "n_touched", "n_correct",
               "n_wrong", "wrong_examples", "test_owner", "discriminator"),
              hazard_table(calls, expected))
    write_tsv(out / "coverage.tsv",
              ("family", "superfamily", "human_genes", "n_in_panel",
               "n_called_as"),
              coverage_table(calls, expected))
    write_tsv(out / "missing.tsv", ("panel_member", "expected_family", "reason"),
              [(sym, expected_by_symbol.get(sym, ""), why)
               for sym, why in missing])

    pos_calls = [c for c in calls if alias.get(c.query) in positives]
    dec_calls = [c for c in calls if alias.get(c.query) not in positives]
    correct_pos = sum(1 for c in pos_calls if c.family == expected.get(c.query))
    rejected = sum(1 for c in dec_calls if not c.census_member())

    summary = {
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "preset": args.preset,
        "anchor_validates": anchor_ok,
        "mafft": mafft_version(),
        "reference_panel": len(refs.sequences) if refs else 0,
        "panel_proteins_that_are_exemplars": n_self,
        "leave_one_out": True,
        "n_targets": len(targets),
        "n_classified": len(calls),
        "n_missing": len(missing),
        "missing": [{"symbol": sym, "reason": why} for sym, why in missing],
        "http": http_ledger(),
        "positives": len(pos_calls),
        "positives_correct": correct_pos,
        "recall": round(correct_pos / len(pos_calls), 4) if pos_calls else None,
        "decoys": len(dec_calls),
        "decoys_rejected": rejected,
        "specificity": round(rejected / len(dec_calls), 4) if dec_calls else None,
        "hazards_defined": len(HAZARDS),
        "hazards_exercised": sum(
            1 for h in HAZARDS if any(h.hid in c.hazards for c in calls)),
        "elapsed_s": round(time.time() - t0, 1),
    }
    summary.update({f"counts_{k}": v
                    for k, v in summary_counts(calls, expected).items()})
    (out / "summary.json").write_text(json.dumps(summary, indent=2))

    log("")
    log(f"recall      {correct_pos}/{len(pos_calls)} "
        f"({summary['recall'] or 0:.1%}) on positives")
    log(f"specificity {rejected}/{len(dec_calls)} "
        f"({summary['specificity'] or 0:.1%}) — decoys not called as channels")
    log(f"hazards     {summary['hazards_exercised']}/{len(HAZARDS)} exercised "
        f"by this panel")
    if missing:
        log(f"missing     {len(missing)}/{len(targets)} panel member(s) could "
            f"not be fetched — absent from both numbers above, not scored "
            f"as failures (results/benchmark_controls/missing.tsv)")
    led = http_ledger()
    log(f"network     {led['requests']} request(s), {led['failures']} "
        f"unrecoverable failure(s)")
    log(f"done in {summary['elapsed_s']}s → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
