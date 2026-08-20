"""S0 — render `results/s0_baseline/report.md` from the committed tables.

Decision **D13**, inherited from the parent project: nothing in this report
is written by hand. Every number is read back out of the TSVs that
`s0_catalogue_verify.py` wrote, so the report cannot drift from the data, and
re-running the verification after a catalogue edit produces a report that
disagrees with the last one exactly where the catalogue changed.

    python3 scripts/s0_report.py [--dir results/s0_baseline]
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


def pct(n: int, d: int) -> str:
    return f"{100 * n / d:.0f} %" if d else "—"


def table(header: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def build(d: Path) -> str:
    summary = json.loads((d / "verification_summary.json").read_text())
    pfam = read_tsv(d / "pfam_verification.tsv")
    exres = read_tsv(d / "exemplars_resolved.tsv")
    arch = read_tsv(d / "exemplar_architecture.tsv")
    tax = read_tsv(d / "taxonomy_check.tsv")
    share = read_tsv(d / "signature_sharing.tsv")
    problems = read_tsv(d / "catalogue_validation.tsv")
    anchors = read_tsv(d / "anchor_verification.tsv")
    cat = summary["catalogue"]

    L: list[str] = []
    A = L.append
    A("# S0 — catalogue verification baseline")
    A("")
    A(f"*Generated {summary['generated']} by `scripts/s0_report.py` from the "
      f"tables in `{d.relative_to(ROOT)}`. Nothing here is hand-written "
      f"(D13). {summary['requests']} live requests, "
      f"{len(summary.get('request_failures', []))} failure(s), "
      f"{summary['elapsed_s']} s.*")
    A("")
    A("## What the catalogue claims")
    A("")
    A(table(["quantity", "n"],
            [[k.replace("_", " "), v] for k, v in cat.items()]))
    A("")
    A(f"The census denominator is **{cat['human_genes_census']} human "
      f"genes encoding a Ca2+-conducting pore** across "
      f"**{cat['families_census']} families** in "
      f"**{cat['superfamilies']} superfamilies**, with "
      f"**{cat['families_control']} further families catalogued specifically "
      f"so they can be excluded** — auxiliary subunits, Ca2+ pumps and "
      f"exchangers, EF-hand sensors and channels that are gated by calcium "
      f"without conducting it.")
    A("")
    A("**That denominator is never quoted flat (D31).** Calcium membership "
      "is a permeability, not a clade, so the census is reported in tiers "
      "and a reader can see exactly how much of the count rests on "
      "non-selective channels and on families whose permeability the genome "
      "does not encode:")
    A("")
    tiers = summary.get("tiers", {})
    if tiers:
        A(table(["tier", "families", "human genes"],
                [[k, v["families"], v["human_genes"]] for k, v in tiers.items()]))
        A("")

    A("## 1. Internal consistency")
    A("")
    if problems:
        A(f"**{len(problems)} problem(s)** found by `src.catalogue.validate()`:")
        A("")
        for r in problems:
            A(f"- {r['problem']}")
    else:
        A("`src.catalogue.validate()` is clean: every family points at a "
          "superfamily that exists, no human gene is claimed by two census "
          "families, every exemplar is resolvable, every `confusable_with` "
          "and every hazard family reference matches a catalogue key.")
    A("")

    A("## 2. Pfam accessions")
    A("")
    ok = [r for r in pfam if r["status"] == "ok"]
    missing = [r for r in pfam if r["status"] == "MISSING"]
    renamed = [r for r in pfam if r["status"] == "NAME_MISMATCH"]
    A(f"{len(pfam)} distinct accessions declared across the catalogue; "
      f"**{len(ok)} verified ({pct(len(ok), len(pfam))})**, "
      f"{len(missing)} missing from InterPro, "
      f"{len(renamed)} carrying a different short name.")
    A("")
    if missing:
        A("**Missing accessions** — these are claims the catalogue makes that "
          "InterPro does not support:")
        A("")
        A(table(["accession", "declared name", "families using it"],
                [[r["accession"], r["declared_name"], r["n_families_using"]]
                 for r in missing]))
        A("")
    if renamed:
        A("**Short-name mismatches** — the accession exists; the catalogue "
          "calls it something else:")
        A("")
        A(table(["accession", "catalogue", "InterPro"],
                [[r["accession"], r["declared_name"], r["interpro_short"]]
                 for r in renamed]))
        A("")
    counted = [r for r in pfam if r.get("n_uniprot_proteins", "").isdigit()]
    if counted:
        counted.sort(key=lambda r: -int(r["n_uniprot_proteins"]))
        A("**The ten largest search spaces** — how many UniProt proteins carry "
          "each signature. This is the census's raw denominator, and the "
          "reason S2 is a task of its own:")
        A("")
        A(table(["accession", "name", "UniProt proteins", "families"],
                [[r["accession"], r["interpro_short"],
                  f"{int(r['n_uniprot_proteins']):,}", r["n_families_using"]]
                 for r in counted[:10]]))
        A("")

    A("## 3. Exemplars")
    A("")
    st = Counter(r["status"] for r in exres)
    A(f"{len(exres)} exemplars declared; "
      f"{st.get('ok', 0)} resolved cleanly, "
      f"{st.get('UNRESOLVED', 0)} unresolvable, "
      f"{st.get('DECLARED_GENE_MISMATCH', 0)} with a declared accession that "
      f"names a different gene, "
      f"{st.get('GENE_NAME_DIFFERS', 0)} where UniProt's primary symbol "
      f"differs from the catalogue's.")
    A("")
    A(table(["status", "n"], [[k, v] for k, v in st.most_common()]))
    A("")
    bad = [r for r in exres if r["status"] not in ("ok", "")]
    if bad:
        A("Every exemplar that did not resolve cleanly:")
        A("")
        A(table(["family", "label", "gene", "species", "declared", "resolved",
                 "resolved gene", "status"],
                [[r["family"], r["label"], r["gene"], r["species"],
                  r["declared_accession"] or "—",
                  r["resolved_accession"] or "—",
                  r["resolved_gene"] or "—", r["status"]] for r in bad]))
        A("")
    A(f"`reference_panel.fasta` holds "
      f"{summary['exemplars'].get('sequences', 0)} sequences — the panel the "
      f"classifier's reference tier scores against.")
    A("")

    A("## 4. Declared architecture vs observed")
    A("")
    if arch and "family_level_absent" not in arch[0]:
        # The tables predate the level-aware architecture check. Rendering
        # anyway would silently produce a report about columns that are not
        # there, which is the drift D13 exists to prevent.
        raise SystemExit(
            "[s0_report] exemplar_architecture.tsv has no "
            "'family_level_absent' column - it was written by an older "
            "s0_catalogue_verify.py. Re-run the verification before "
            "rendering the report (D13).")
    exact = [r for r in arch if r["status"] == "ok"]
    expected = [r for r in arch if r["status"] == "subfamily_absence_expected"]
    real = [r for r in arch if r["status"] == "FAMILY_SIGNATURE_ABSENT"]
    A(f"{len(arch)} exemplars had their Pfam architecture re-derived. "
      f"**{len(exact)} match the catalogue's declaration exactly, "
      f"{len(expected)} differ only at signatures the catalogue does not "
      f"promise every member carries, and {len(real)} are missing a "
      f"signature declared at `FAMILY` level.**")
    A("")
    A("The split matters and is the reason this table is not one column "
      "(**D25**). A `FAMILY`-level signature is a claim that *every* member "
      "carries it, so its absence from an exemplar is a catalogue error. A "
      "`SUBFAMILY` signature says only that some members carry it, and "
      "`ACCESSORY` and `SUPERFAMILY` signatures make no per-member promise "
      "at all — reporting those absences as mismatches would bury the real "
      "errors in noise. Hazard **HC7** is the canonical case: most TRP "
      "families carry no `PF00520`, which is a fact about Pfam's coverage "
      "and not a fault in the catalogue.")
    A("")
    if real:
        A("**Missing at `FAMILY` level — each of these is either a catalogue "
          "correction or a signature that should be demoted to `SUBFAMILY`:**")
        A("")
        A(table(["family", "exemplar", "family-level signature absent",
                 "observed but not declared"],
                [[r["family"], r["label"],
                  r["family_level_absent"] or "—",
                  (r["observed_not_declared"] or "—")[:60]]
                 for r in real[:40]]))
        A("")
    if expected:
        A("**Expected absences** (subfamily-, accessory- or "
          "superfamily-level only):")
        A("")
        A(table(["family", "exemplar", "declared but not observed"],
                [[r["family"], r["label"], r["declared_not_observed"] or "—"]
                 for r in expected[:40]]))
        if len(expected) > 40:
            A("")
            A(f"*({len(expected) - 40} further rows in "
              f"`exemplar_architecture.tsv`.)*")
        A("")

    A("## 5. Projection anchors")
    A("")
    if not anchors:
        A("**Not run.** `anchor_verification.tsv` is absent — run "
          "`python3 scripts/s0_anchors.py`. Until it does, every projected "
          "filter call rests on an anchor that nothing has checked against "
          "the live reference.")
        A("")
    else:
        abad = [r for r in anchors if r["verified"] != "yes"]
        A(f"{len(anchors)} anchors re-verified against live UniProt; "
          f"{len(anchors) - len(abad)} read what the catalogue claims, "
          f"{len(abad)} do not. Every filter call this project makes is a "
          f"projection from one of these references, so an anchor that has "
          f"drifted makes each of those calls silently wrong — and "
          f"`verify_anchor()` refuses to project rather than guess "
          f"(**D26**, **D28**). The TRPV6 row is why the check exists: the "
          f"aspartate is at **D582**, not the literature's D542, because the "
          f"canonical entry is the long isoform.")
        A("")
        A(table(["anchor", "reference", "accession", "positions", "expected",
                 "observed", "length aa", "context", "verified"],
                [[r["anchor"], r["reference_label"], r["uniprot"],
                  r["positions"], r["expected"], r["observed"] or "—",
                  r["ref_length"], r["context"].replace(";", "; ") or "—",
                  "yes" if r["verified"] == "yes" else f'**{r["verified"]}**']
                 for r in anchors]))
        A("")

    A("## 6. Shared signatures — the hazard registry's evidence")
    A("")
    crossing = [r for r in share if r["crosses_census_boundary"] == "yes"]
    A(f"{len(share)} signatures are carried by more than one family. "
      f"**{len(crossing)} of them cross the census boundary** — a domain "
      f"that is evidence for a calcium-channel family and is also carried by "
      f"something the census does not count: a sodium channel, a "
      f"Ca2+-activated channel, a pump, an auxiliary subunit or a sensor. "
      f"This table is the hazard registry's empirical basis, and every row "
      f"in it is a place where architecture alone cannot decide membership "
      f"(**D25**).")
    A("")
    A(table(["accession", "families", "statuses"],
            [[r["accession"], r["families"][:80], r["statuses"]]
             for r in share[:15]]))
    A("")

    A("## 7. Taxonomy")
    A("")
    tbad = [r for r in tax if r["status"] != "ok"]
    A(f"{len(tax)} taxon ids checked against the UniProt taxonomy service; "
      f"{len(tax) - len(tbad)} confirmed, {len(tbad)} mismatched.")
    A("")
    if tbad:
        A(table(["taxon_id", "catalogue", "UniProt", "status"],
                [[r["taxon_id"], r["declared"], r["uniprot_scientific"] or "—",
                  r["status"]] for r in tbad]))
        A("")

    A("## 8. What this does not verify")
    A("")
    A("- **Family membership.** That `CACNA1C` belongs to `cav_hva` is a "
      "literature assignment. S1 tests whether the classifier reproduces it; "
      "nothing here tests whether it is right.")
    A("- **Calcium permeability.** Every P_Ca/P_Na in the catalogue is a "
      "literature value with a method attached, and none of it is "
      "recoverable from sequence (hazards **HC8**, **HC16**). No database "
      "check can confirm a permeability, and this project never predicts "
      "one. Auditing those numbers against their sources is S1b's job, not "
      "S0's.")
    A("- **The tier boundaries.** Whether a P_Ca/P_Na of 3 counts as "
      "`ca_permeable` is a decision recorded in "
      "`docs/scope_and_boundaries.md`, not a fact. S0 checks that every "
      "census family carries evidence for the tier it claims; it cannot "
      "check that the tier is the right one.")
    A("- **Completeness.** A verified catalogue is not a complete one. "
      "Whether these are the right human genes is the question S2 answers, "
      "and it is answered against a declared search space, never against "
      "\"all calcium channels\".")
    A("")
    fails = summary.get("request_failures", [])
    if fails:
        A("## Request failures")
        A("")
        for fdict in fails[:20]:
            A(f"- `{fdict['url']}` — {fdict['why']}")
        A("")
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dir", type=Path, default=ROOT / "results" / "s0_baseline")
    args = ap.parse_args()
    if not (args.dir / "verification_summary.json").exists():
        print(f"[s0_report] no verification_summary.json in {args.dir} — "
              f"run scripts/s0_catalogue_verify.py first")
        return 1
    out = args.dir / "report.md"
    out.write_text(build(args.dir))
    print(f"[s0_report] wrote {out} ({out.stat().st_size / 1000:.1f} kB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
