# S0 baseline — provenance

**Status: complete.** Every table in this directory was written by a single
uninterrupted run of `scripts/s0_catalogue_verify.py` against the catalogue
as it stands, on **2026-08-20**: 533 requests, **0 request failures**, 721.8 s.
`report.md` is rendered from those tables by `scripts/s0_report.py` and
contains no hand-written numbers (**D13**).

This replaces an earlier state in which the directory held tables from three
different passes. That state was real and is worth recording: five passes
were run, each finding errors that were then fixed, which invalidated the
pass that found them. The tables here are the first coherent set.

## What is in this directory

| file | written by | result |
|------|-----------|--------|
| `catalogue_validation.tsv` | offline | clean |
| `pfam_verification.tsv` | pass of 2026-08-20 | 87 accessions, 0 missing, 0 name mismatches |
| `exemplars_resolved.tsv` | pass of 2026-08-20 | 102/102 resolved, 0 unresolved, 0 wrong-gene |
| `exemplar_architecture.tsv` | pass of 2026-08-20 | 72 ok, 30 subfamily-level absences, **0 family-level** |
| `signature_sharing.tsv` | offline | 18 shared signatures |
| `taxonomy_check.tsv` | pass of 2026-08-20 | 53/53, 0 problems |
| `anchor_verification.tsv` | `scripts/s0_anchors.py` | 3/3 anchors validate against live UniProt |
| `rule_coverage.tsv`, `rule_targets.tsv` | offline | 17/29 census families nameable by architecture; exits 0 |
| `filter_k.tsv`, `filter_four_repeat.tsv` | `scripts/s0_filter_atlas.py` | 3/4 K-filters located; 7/9 four-repeat signatures complete |
| `reference_panel.fasta` | pass of 2026-08-20 | **102 sequences — every exemplar** |
| `references.tsv` | `scripts/s0_review_refs.py` | 122/122 sources resolved against Europe PMC |
| `verification_summary.json` | pass of 2026-08-20 | headline counts for the report |
| `figures/` | `scripts/s0_figures.py` | families and human genes per superfamily |

## Reproducing it

```bash
python3 -m src.catalogue                 # must be clean
python3 scripts/selftest.py              # must be clean
python3 scripts/s0_rule_coverage.py      # must exit 0
python3 scripts/s0_anchors.py            # must exit 0 — an anchor drift is a stop
python3 scripts/s0_catalogue_verify.py   # ~12 min, ~530 requests
python3 scripts/s0_filter_atlas.py       # needs MAFFT
python3 scripts/s0_report.py
python3 scripts/s0_figures.py            # needs matplotlib (piezo1 env)
```

Every exemplar now declares a UniProt accession, so the pass no longer
resolves ~90 gene symbols live and is both faster and reproducible offline.

## What S0 still does not verify

The **permeability values**. Every P_Ca/P_Na in the catalogue is a literature
value recorded by hand, no database holds one, and nothing here checks them —
so the four census tiers rest on claims that remain unaudited. That is task
**S1b**.
