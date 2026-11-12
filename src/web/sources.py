"""The committed files the dashboard shows, declared in one place.

TABLES maps a short key to a committed TSV and the ledger task that wrote it; the API serves each as
/api/table/<key>. FIGURES lists the committed PNGs the site may show (served at files/<path>). DOCS are committed
markdown files rendered on the site. Captions and blurbs are descriptions of what a file is, never numbers: every
number the dashboard shows is read from the files themselves at build time.
"""
from __future__ import annotations

S0 = "results/s0_baseline"
S1 = "results/benchmark_controls"

#: key -> (path, task, title, what the table is)
TABLES: dict[str, tuple[str, str, str, str]] = {
    # S0 - catalogue verification
    "pfam": (f"{S0}/pfam_verification.tsv", "S0", "Pfam accessions",
             "every Pfam accession the catalogue declares, re-derived against InterPro"),
    "exemplars": (f"{S0}/exemplars_resolved.tsv", "S0", "Exemplars resolved",
                  "every exemplar resolved to a UniProt accession"),
    "architecture": (f"{S0}/exemplar_architecture.tsv", "S0", "Declared vs observed architecture",
                     "each exemplar's observed Pfam architecture against the catalogue's declaration"),
    "taxonomy": (f"{S0}/taxonomy_check.tsv", "S0", "Taxonomy check",
                 "every declared taxon id checked against UniProt taxonomy"),
    "anchors": (f"{S0}/anchor_verification.tsv", "S0", "Projection anchors",
                "the three projection anchors verified against live UniProt"),
    "sharing": (f"{S0}/signature_sharing.tsv", "S0", "Shared signatures",
                "domain signatures carried by more than one family, and whether they cross the census boundary"),
    "rule_coverage": (f"{S0}/rule_coverage.tsv", "S0", "Rule coverage",
                      "what the architecture tier makes of each family's own declared architecture"),
    "rule_targets": (f"{S0}/rule_targets.tsv", "S0", "Families no rule can name", "one row per family that no architecture rule can name at all"),
    "filter_four": (f"{S0}/filter_four_repeat.tsv", "S0", "Four-repeat filter atlas",
                    "the four filter residues, projected from Nav1.5"),
    "filter_k": (f"{S0}/filter_k.tsv", "S0", "Potassium filter (TxGYG)", "located directly, no alignment"),
    "references": (f"{S0}/references.tsv", "S23", "Review references",
                   "every source cited by the review, resolved against Europe PMC"),
    # S1 - classifier benchmark
    "recall": (f"{S1}/recall.tsv", "S1", "Per-family recall",
               "positives and decoys per family, with the tier that decided"),
    "hazards": (f"{S1}/hazards.tsv", "S1", "Per-hazard specificity",
                "how each recorded hazard fared on the control panel"),
    "calls": (f"{S1}/calls.tsv", "S1", "Every call, with its audit trail", "leave-one-out calls on the control panel"),
    "confusion": (f"{S1}/confusion.tsv", "S1", "Confusion (expected vs called)", ""),
    "coverage": (f"{S1}/coverage.tsv", "S1", "Panel coverage per census family",
                 "what the panel holds per census family, not what was called"),
    "anchor_power": (f"{S1}/anchor_power.tsv", "S1", "Anchor projections",
                     "each anchor projected over the families it applies to"),
    "anchor_summary": (f"{S1}/anchor_summary.tsv", "S1", "Does each anchor discriminate?", ""),
    "leakage": (f"{S1}/rule_leakage.tsv", "S1", "Rule leakage into control families",
                "control families whose declared domains satisfy a census family's generated rule"),
    "missing": (f"{S1}/missing.tsv", "S1", "Panel members not fetched",
                "absent from the denominators rather than scored as misses"),
    "toolchain": (f"{S1}/toolchain.tsv", "S1", "Toolchain", "every external binary and package probed"),
}

SUMMARY_S0 = f"{S0}/verification_summary.json"
SUMMARY_S1 = f"{S1}/summary.json"
ROADMAP = "PUBLICATION_ROADMAP.md"
FINDINGS = "FINDINGS.md"
REVIEW = "docs/channel_review_2026.md"

#: committed markdown shown on the site: key -> (path, title)
DOCS: dict[str, tuple[str, str]] = {
    "s0_report": (f"{S0}/report.md", "S0 report (rendered from its tables, D13)"),
    "s0_provenance": (f"{S0}/PROVENANCE.md", "S0 provenance"),
    "s1_report": (f"{S1}/report.md", "S1 report (rendered from its tables, D13)"),
    "findings": (FINDINGS, "FINDINGS.md: the biological story, task by task"),
    "review": (REVIEW, "The calcium channels: one permeability, many origins (S23 review)"),
    "scope": ("docs/scope_and_boundaries.md", "What counts as a calcium channel"),
    "phylogeny_protocol": ("docs/phylogeny_protocol.md", "Phylogeny protocol: why a forest"),
}

#: committed figures the site may show. Review figures are captioned from the review's own figure list.
REVIEW_FIGURES = [
    "docs/figures/fig1_folds.png",
    "docs/figures/fig2_potassium_filter.png",
    "docs/figures/fig3_four_repeat_filter.png",
    "docs/figures/fig4_length_range.png",
    "docs/figures/fig5_domain_matrix.png",
    "docs/figures/fig7_forest.png",
    "docs/figures/fig8_architecture_traps.png",
]
STAGE_FIGURES = {
    "results/s0_baseline/figures/catalogue_scope.png":
        ("S0", "the census by calcium tier, and which domain signatures are shared with something that does not "
               "conduct calcium (caption from scripts/dashboard.py)"),
}
FIGURES = REVIEW_FIGURES + list(STAGE_FIGURES)
