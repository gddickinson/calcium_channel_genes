# S0 is INCOMPLETE — read this before using anything in this directory

**Status: `in_progress`.** These tables are *not* one coherent run. They were
produced by different passes of `scripts/s0_catalogue_verify.py` against a
catalogue that changed between passes, because each pass found errors that
were then fixed. Nothing here should be cited, and `report.md` has been
deleted rather than left stale — a rendered report that disagrees with its
own tables is exactly the drift **D13** exists to prevent.
(`scripts/s0_report.py` now refuses to render against tables written by an
older verification script, so this state cannot be papered over.)

## What came from where

| file | pass | matches the current catalogue? |
|------|------|-------------------------------|
| `pfam_verification.tsv` | 5 (final) | **yes** — 84 accessions, 0 missing, **0 name mismatches** |
| `catalogue_validation.tsv` | current | **yes** — clean |
| `rule_coverage.tsv` | current (offline) | **yes** |
| `rule_targets.tsv` | current (offline) | **yes** |
| `exemplars_resolved.tsv` | 3 | no — predates six catalogue corrections |
| `exemplar_architecture.tsv` | 3 | no — and lacks the `family_level_absent` column |
| `signature_sharing.tsv` | 3 | no — and uses the old `crosses_channel_boundary` column |
| `taxonomy_check.tsv` | 3 | taxa did not change, so effectively yes (52 checked, 0 problems) |
| `reference_panel.fasta` | 3 | sequences did not change; 101 of 102 exemplars |
| `verification_summary.json` | 3 | no |

## Why it stopped

Five passes were run. Passes 1 and 3 found six wrong Pfam short names
(including `PF02714`/`PF13967` **swapped**); the exemplar stage found four
families whose declared architecture disagreed with InterPro. Each finding
was fixed, which invalidated the pass that found it. Pass 5's Pfam stage came
back **clean** — 84 accessions, zero mismatches — and its exemplar stage was
then throttled by InterPro after roughly 2,000 requests across the five
passes, and was stopped rather than left hammering a rate-limited endpoint.

## To finish S0

```bash
python3 -m src.catalogue          # must be clean
python3 scripts/selftest.py       # must be clean
python3 scripts/s0_rule_coverage.py   # must exit 0
python3 scripts/s0_catalogue_verify.py
python3 scripts/s0_report.py
python3 scripts/s0_figures.py
```

One full uninterrupted pass is ~7-14 minutes and ~520 requests. The catalogue
has not changed since pass 5's clean Pfam stage, so the run is expected to be
clean on the Pfam and taxonomy stages; the exemplar architecture stage is the
one that still has unreviewed output. **Do not start it immediately after
another pass** — leave the endpoint alone for a while first.
