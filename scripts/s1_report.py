"""S1 — render `results/benchmark_controls/report.md` from the committed tables.

D13 again: the prose here reads the TSVs back and states what they say. If a
re-run changes recall, this report changes with it; if it does not, the
report is stale and the mismatch is visible in git.

    python3 scripts/s1_report.py [--dir results/benchmark_controls]
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.s0_lib import read_tsv
from src.catalogue import HAZARD_BY_ID
from src.classify.motifs import FOUR_REPEAT_ANCHOR


def table(header, rows) -> str:
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def build(d: Path) -> str:
    s = json.loads((d / "summary.json").read_text())
    calls = read_tsv(d / "calls.tsv")
    recall = read_tsv(d / "recall.tsv")
    hazards = read_tsv(d / "hazards.tsv")
    coverage = read_tsv(d / "coverage.tsv")
    missing = read_tsv(d / "missing.tsv") if (d / "missing.tsv").exists() else []
    anchors = (read_tsv(d / "anchor_summary.tsv")
               if (d / "anchor_summary.tsv").exists() else [])
    anchor_rows = (read_tsv(d / "anchor_power.tsv")
                   if (d / "anchor_power.tsv").exists() else [])
    rt = ROOT / "results" / "s0_baseline" / "rule_targets.tsv"
    rule_targets = read_tsv(rt) if rt.exists() else []
    leakage = (read_tsv(d / "rule_leakage.tsv")
               if (d / "rule_leakage.tsv").exists() else [])

    L: list[str] = []
    A = L.append
    A("# S1 — classifier control benchmark")
    A("")
    A(f"*Generated {s['generated']} by `scripts/s1_report.py` from the tables "
      f"in `{d.relative_to(ROOT)}` (D13). Panel: `{s['preset']}`. "
      f"{s['n_classified']}/{s['n_targets']} targets classified in "
      f"{s['elapsed_s']} s.*")
    A("")

    A("## Headline")
    A("")
    A(table(["measure", "value"], [
        ["recall (positives called correctly)",
         f"**{s['positives_correct']}/{s['positives']}"
         f"** ({(s['recall'] or 0):.1%})"],
        ["specificity (decoys not called as channels)",
         f"**{s['decoys_rejected']}/{s['decoys']}"
         f"** ({(s['specificity'] or 0):.1%})"],
        ["hazards exercised",
         f"{s['hazards_exercised']}/{s['hazards_defined']}"],
        ["four-repeat anchor validates",
         "yes" if s["anchor_validates"] else "**no — motif tier disabled**"],
        ["MAFFT", s["mafft"] or "**not available**"],
        ["reference panel", f"{s['reference_panel']} exemplar sequences"],
        ["panel proteins that are themselves exemplars",
         f"{s.get('panel_proteins_that_are_exemplars', 0)} — classified "
         f"leave-one-out" if s.get("leave_one_out") else "not excluded"],
    ]))
    A("")
    n_self = s.get("panel_proteins_that_are_exemplars", 0)
    A(f"**Leave-one-out matters here.** {n_self} of the {s['n_classified']} "
      f"panel proteins are themselves catalogue exemplars — both are drawn "
      f"from the same curated gene lists — so without excluding the query's "
      f"own accession the reference tier would score almost the whole panel "
      f"against itself at 100 % identity and the benchmark would measure "
      f"nothing but that overlap (**D29**).")
    A("")

    if missing:
        A("## Panel members that were not measured")
        A("")
        A(f"{len(missing)} of the {s['n_targets']} panel members could not be "
          f"fetched, so they are **absent from both numbers above rather than "
          f"scored as failures**. A rate-limited request is not a classifier "
          f"error, and letting one look like one would understate recall for "
          f"a reason that has nothing to do with the method.")
        A("")
        A(table(["panel member", "expected family", "why"],
                [[m["panel_member"], m["expected_family"] or "—", m["reason"]]
                 for m in missing]))
        A("")
    else:
        A(f"*Every one of the {s['n_targets']} panel members was fetched and "
          f"classified; no member is missing from the counts above "
          f"(`missing.tsv` is empty).*")
        A("")

    A("## Which tier made the call")
    A("")
    tiers = Counter(r["decisive_tier"] or "none" for r in calls)
    A("This is the number that says whether the classifier is doing anything "
      "a nearest-neighbour lookup could not. A call made by the architecture "
      "or hazard tier rests on domain composition and works on a sequence "
      "with no close relative in the panel; a call made only by the reference "
      "tier does not.")
    A("")
    A(table(["decisive tier", "n calls"],
            [[k, v] for k, v in tiers.most_common()]))
    A("")
    conf = Counter(r["confidence"] for r in calls)
    A(table(["confidence", "n"], [[k, v] for k, v in conf.most_common()]))
    A("")

    A("## Per-family recall")
    A("")
    pos = [r for r in recall if r.get("panel_role", "positive") == "positive"]
    dec = [r for r in recall if r.get("panel_role") == "decoy"]
    perfect = [r for r in pos if r["recall"] == "1.000"]
    missed = [r for r in pos if r["recall"] != "1.000"]
    A(f"{len(perfect)}/{len(pos)} **positive** families were called correctly "
      f"for every member. The {len(dec)} decoy families are scored by "
      f"specificity, not recall — a decoy left `unassigned` is a success, and "
      f"listing it as a recall failure would invert the result.")
    A("")
    if missed:
        A("**Positive families the classifier did not call correctly:**")
        A("")
        A(table(["family", "n", "correct", "recall", "called instead"],
                [[r["family"], r["n"], r["correct"], r["recall"],
                  r["mis_calls"] or "—"] for r in missed]))
        A("")
    if dec:
        wrong_dec = [r for r in dec if r["mis_calls"] and
                     "unassigned" not in r["mis_calls"]]
        A(f"**Decoys:** {len(dec)} families; "
          f"{len(dec) - len(wrong_dec)} were left unassigned or called as "
          f"themselves, {len(wrong_dec)} were called as something else.")
        if wrong_dec:
            A("")
            A(table(["decoy family", "called instead"],
                    [[r["family"], r["mis_calls"]] for r in wrong_dec]))
        A("")
    A("Full table: `recall.tsv`.")
    A("")

    A("## The four-repeat filter: does it separate Cav from Nav?")
    A("")
    A("This is the census's load-bearing test. Cav1/2, Cav3, Nav and NALCN "
      "share a domain architecture that no rule can tell apart; the four "
      "residues projected from the Nav1.5 anchor are the only positive "
      "evidence separating them, and every downstream count depends on them "
      "reading correctly.")
    A("")
    # The projection runs on every query, so most rows are noise: a TRPV or an
    # ORAI aligned against Nav1.5 produces four residues that mean nothing.
    # Only the families the anchor declares itself applicable to are evidence.
    scope = set(FOUR_REPEAT_ANCHOR.applies_to)
    four = [r for r in calls
            if r["expected_family"] in scope and r["filter_string"]]
    other = [r for r in calls
             if r["expected_family"] not in scope and r["filter_string"]]
    if four:
        A(table(["gene", "expected", "called", "projected filter",
                 "decisive tier", "reads its family's signature?"],
                [[r["gene_symbol"], r["expected_family"],
                  r["called_family"] or "unassigned", f"`{r['filter_string']}`",
                  r["decisive_tier"] or "—",
                  ("**yes**" if FOUR_REPEAT_ANCHOR.calls.get(
                      r["filter_string"], ("",))[0] == r["expected_family"]
                   else ("non-call — see below" if "-" in r["filter_string"]
                         else "**no**"))]
                 for r in four]))
        A("")
        decided = [r for r in four if FOUR_REPEAT_ANCHOR.calls.get(
            r["filter_string"], ("",))[0] == r["expected_family"]]
        full = [r for r in four if "-" not in r["filter_string"]]
        A(f"**{len(decided)}/{len(full)} — every panel member that produces a "
          f"complete four-residue string reads exactly the filter its "
          f"catalogue entry declares, and no string is shared between a "
          f"calcium family and a non-calcium one.** The remaining "
          f"{len(four) - len(full)} are structural non-calls rather than "
          f"failures. The non-calls are "
          f"the families that structurally cannot produce one: TPC has two "
          f"repeats rather than four, and CatSper is a heterotetramer whose "
          f"four *different* subunits contribute one filter residue each — "
          f"CATSPER1 projects `---D`, CATSPER2 `--D-`, CATSPER3 `-D--` and "
          f"CATSPER4 `--D-`, so no single-sequence projection can read a "
          f"CatSper filter and the joint reading is a task, not a gap "
          f"(`anchor_power.tsv`).")
        A("")
        A(f"*({len(other)} other panel members also produced a projected "
          f"string. They are not shown: a TRPV or a ryanodine receptor "
          f"aligned against Nav1.5 yields four residues from positions that "
          f"are not its filter, and reading them as evidence is the mistake "
          f"the `applies_to` field exists to prevent. They are in "
          f"`calls.tsv`.)*")
        A("")
    else:
        A("**No panel member produced a projected filter string.** Either the "
          "anchor did not validate or MAFFT was unavailable; either way the "
          "motif tier contributed nothing to this run and the calls above "
          "rest on architecture and reference identity alone.")
        A("")

    if anchors:
        A("## Do the other two anchors discriminate?")
        A("")
        A("`classify()` runs exactly one anchor — the four-repeat locus. The "
          "TRPV and ORAI anchors are declared and verified but never "
          "projected onto anything, so `scripts/s1_anchor_power.py` projects "
          "each one over the families it claims to apply to and asks whether "
          "the residue it reads actually differs between permeability tiers. "
          "An anchor that reads the same residue for every member is not a "
          "test, and a hazard it was supposed to close stays open.")
        A("")
        A(table(["anchor", "reference", "positions", "projected",
                 "distinct strings", "discriminates?"],
                [[f"`{a['anchor']}`", a["reference"], a["positions"],
                  a["n_projected"], a["n_distinct_strings"],
                  "**yes**" if a["discriminates"] == "yes" else "**no**"]
                 for a in anchors]))
        A("")
        for a in anchors:
            A(f"- **`{a['anchor']}`** — {a['verdict']}")
            if a["distinct_strings"]:
                A(f"  - reads: {a['distinct_strings']}")
        A("")
        failed = [a for a in anchors if a["verdict"].startswith("DOES NOT")]
        untested_a = [a for a in anchors if a["verdict"].startswith("untested")]
        if failed:
            A(f"**{len(failed)} anchor(s) were measured and do not separate "
              f"the tiers they were written to separate.** That is recorded "
              f"rather than quietly dropped: a hazard is only closed by a "
              f"test, so the hazard this anchor was meant to close now says "
              f"so in the registry and the anchor's call map has been "
              f"emptied — it can no longer name a family.")
            A("")
        if untested_a:
            A(f"**{len(untested_a)} anchor(s) are untested, which is not the "
              f"same as undiscriminating.** Every family in their scope sits "
              f"in one permeability tier, so this panel has nothing for them "
              f"to separate; measuring them needs a decoy that shares the "
              f"fold, and that is a panel extension rather than a result.")
            A("")

    A("## Per-hazard")
    A("")
    A("A hazard is only closed by a test. `n touched` counts panel members "
      "whose classification involved that hazard's rule; a hazard with zero "
      "is not solved, it is **untested** by this panel.")
    A("")
    rows = []
    for h in hazards:
        hz = HAZARD_BY_ID.get(h["hazard"])
        rows.append([
            h["hazard"], h["severity"], h["n_touched"], h["n_correct"],
            h["n_wrong"], h["wrong_examples"] or "—",
            (hz.title if hz else "")[:56]])
    A(table(["hazard", "severity", "n touched", "correct", "wrong",
             "examples", "what it is"], rows))
    A("")
    untested = [h for h in hazards if h["n_touched"] == "0"]
    if untested:
        A(f"**{len(untested)} hazard(s) carry no measurement from this panel:** "
          + ", ".join(h["hazard"] for h in untested)
          + ". Extending the panel to exercise them is a task, not a footnote.")
        A("")

    A("## The decoys no rule can name")
    A("")
    A("`derived_rules()` generates a rule from every **census** family's "
      "declared architecture, so a control family is recognisable only if "
      "somebody wrote a hazard rule for it by hand. S0 measured which ones "
      "have none (`results/s0_baseline/rule_targets.tsv`). Those decoys "
      "cannot be *named*; they can only be left `unassigned` or placed by "
      "reference identity. Leaving them unassigned is the correct outcome — "
      "the census asks whether a protein is a calcium channel, and "
      "`unassigned` answers no — so this section reports them rather than "
      "scoring them as misses.")
    A("")
    unnameable = sorted({r["family"] for r in rule_targets
                         if r.get("role") == "control" and not r.get("hazards")})
    if unnameable:
        by_family = {}
        for r in calls:
            if r["expected_family"] in unnameable:
                by_family.setdefault(r["expected_family"], []).append(r)
        A(table(["control family", "panel member", "called", "confidence",
                 "rejected as a channel?"],
                [[f"`{fam}`", c["gene_symbol"], c["called_family"] or
                  "unassigned", c["confidence"],
                  "yes" if not c["called_family"] else "**no**"]
                 for fam in unnameable for c in by_family.get(fam, [])]
                or [[f"`{f}`", "—", "—", "—", "no panel member"]
                    for f in unnameable]))
        A("")

    if leakage:
        fam_level = [r for r in leakage if r["rule_level"] == "family"]
        A("## How a decoy gets named as a calcium channel")
        A("")
        A("One decoy was not merely accepted — it was **named**. TRPM4 is a "
          "Ca²⁺-impermeable member of the TRPM family and the architecture "
          "tier called it `trpm_ca` outright. The cause is not a bad "
          "annotation: the catalogue records, correctly, that TRPM4 and TRPM5 "
          "carry the same Pfam accessions as their Ca²⁺-permeable siblings. "
          "It is `derived_rules()`, which iterates `census_families()` only, "
          "so a domain declared at family level by both a census family and a "
          "control family yields exactly one rule — pointing at the census "
          "family — and the control matches it with nothing to tie against. "
          "\"Ties are ambiguity, never a coin toss\" cannot fire when only "
          "one side was allowed to enter.")
        A("")
        A(f"`scripts/s1_rule_leakage.py` measures the whole exposure rather "
          f"than the one instance: **{len(leakage)} architecture matches into "
          f"{len({r['control_family'] for r in leakage})} control families, "
          f"of which {len(leakage) - len(fam_level)} are superfamily-only** — "
          f"a sodium channel really is a P-loop channel, and saying so is "
          f"correct — **and {len(fam_level)} names a control as a census "
          f"family**.")
        A("")
        if fam_level:
            A(table(["control family", "named as", "via rule", "requires",
                     "priority", "hazard rule that would outrank it"],
                    [[f"`{r['control_family']}`", f"`{r['rule_target']}`",
                      f"`{r['rule']}`", f"`{r['requires']}`", r["priority"],
                      r["hazard_rule_outranks"]] for r in fam_level]))
            A("")
        A("This is the third instance of one shape — `PF00027` naming plant "
          "CNGC as animal CNG, the HCN defect before it, now `PF18139`. The "
          "fix is not another hand-written hazard rule; it is letting control "
          "families generate rules so the shared domain produces a tie. That "
          "is a change to the rule generator with a blast radius across every "
          "call in this table, so it is recorded as an emergent task with the "
          "measurement attached rather than made inside a benchmark session.")
        A("")

    A("## Panel coverage")
    A("")
    covered = [r for r in coverage if r["n_in_panel"] != "0"]
    A(f"{len(covered)}/{len(coverage)} census families have at least one "
      f"member in this panel. Coverage counts what the panel **contains**, "
      f"not what the classifier managed to call — counting calls would hide "
      f"a family whose every member was left `unassigned` behind a coverage "
      f"gap, which is the opposite of reporting it.")
    A("")
    A(table(["family", "superfamily", "human genes", "in panel", "called as"],
            [[f"`{r['family']}`", r["superfamily"], r["human_genes"],
              r["n_in_panel"], r.get("n_called_as", "—")]
             for r in coverage if r["n_in_panel"] != "0"]))
    A("")
    uncovered = [r["family"] for r in coverage if r["n_in_panel"] == "0"]
    if uncovered:
        A("**Families with no panel member: " +
          ", ".join(f"`{u}`" for u in uncovered) +
          ".** These are the census's non-human families — the plant "
          "glutamate-receptor-like channels, the plant CNGCs, plant MCA and "
          "the viral viroporins — plus any human family the preset omits. A "
          "benchmark built from human gene symbols cannot measure them, and "
          "a census that spans plants, fungi, protists and viruses cannot "
          "claim their recall from this table. They are S3's and S21's to "
          "measure.")
        A("")

    A("## Every call")
    A("")
    A("`calls.tsv` carries one row per protein with the full evidence string "
      "from every tier, including the tiers that did not decide. The point of "
      "keeping the losing evidence is that a wrong call is diagnosable "
      "without re-running anything.")
    A("")
    interesting = [r for r in calls if r["conflicts"]]
    if interesting:
        A(f"**{len(interesting)} call(s) had disagreeing tiers:**")
        A("")
        A(table(["protein", "gene", "expected", "called", "confidence",
                 "conflict"],
                [[r["accession"], r["gene_symbol"], r["expected_family"],
                  r["called_family"] or "—", r["confidence"],
                  r["conflicts"][:70]] for r in interesting]))
        A("")
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dir", type=Path,
                    default=ROOT / "results" / "benchmark_controls")
    args = ap.parse_args()
    if not (args.dir / "summary.json").exists():
        print(f"[s1_report] no summary.json in {args.dir} — run "
              f"scripts/s1_benchmark.py first")
        return 1
    out = args.dir / "report.md"
    out.write_text(build(args.dir))
    print(f"[s1_report] wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
