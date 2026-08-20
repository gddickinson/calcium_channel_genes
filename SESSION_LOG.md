# SESSION_LOG.md — operational record

One entry per session: what ran, what resulted, what is next. Findings in
plain language go in `FINDINGS.md`; this file is the mechanics.

---

## 2026-08-20 — Setup: the project, ported and pointed at calcium

**Task.** Project setup. Not a ledger task — the ledger starts at S0.

**What was done.**

Ported the machinery from `../ion_channel_genes` (itself ported from
`../ip3r_genes` and `../piezo_genes`): `src/core`, `src/databases`,
`src/analysis`, `src/discovery`, `src/investigation`, `src/gui`,
`src/phylo`, `src/utils`, the classifier framework, the figure style, the
dashboard, the manuscript-assembly and claim-checking tooling, and the
session protocol. **No result was ported.** `results/` was created empty.

Wrote a new subject definition in `src/catalogue/` — eleven division files,
a hazard registry and a registry module — and extended the schema with the
one idea this project needs and the parent did not:

- **`CaClass`** — the four census tiers (`ca_selective`, `ca_permeable`,
  `ca_conditional`, `ca_release`) plus `ca_activated` and `not_calcium` for
  the things catalogued so they can be excluded.
- **`Permeability`** — P_Ca/P_Na recorded **as a string, as reported**, with
  the method that produced it and its provenance. Decision **D31**.
- `Gating.STORE_DEPLETION` and `Gating.MEMBRANE_APPOSITION`, because ORAI's
  gate is in another organelle and RyR1's is a mechanical link to Cav1.1.
- `Selectivity.MONOVALENT_CATION`, because TRPM4/5 need a value that is
  neither "cation non-selective" nor "not a channel".

`validate()` gained three calcium-specific invariants: a census family whose
permeability claim records no method is an error; a `CHANNEL` record in the
`NOT_CALCIUM` tier is an error (it should be `OUT_OF_SCOPE`); and a calcium
claim on a non-census record is an error.

Rewrote `src/classify/rules.py`'s hazard rules (24 rules across 19 hazards),
`src/classify/motifs.py` (three reference-free regexes and three projected
anchors), `src/utils/scope.py`, `src/phylo/forest.py` and
`src/phylo/network.py` for the new subject; retargeted `figstyle.py` with a
`CA_CLASS` ordered palette; rewrote `scripts/selftest.py` (56 invariants);
generated `presets/calcium_human.json` and `presets/controls_benchmark.json`
from the catalogue so they cannot drift from it; wrote the seven docs.

**Live verification done during setup** (three anchors, one regex):

| claim | result |
|---|---|
| Nav1.5 `Q14524` 372/898/1419/1711 | **DEKA** ✓ |
| ORAI1 `Q96D31` position 106 | **E** ✓ |
| MCU `Q8NE86` `WDxxE` regex | **WDIME at 260** ✓ |
| TRPV6 `Q9H1D0` position 542 (literature's D542) | **L — the anchor does not validate** ✗ |
| TRPV6 `Q9H1D0` `TIIDGP` search | **579–584, so the aspartate is D582** ✓ |
| EF-hand regex on CALM1 / CALB1 / PVALB / MICU1 / STIM1 | 4 / 4 / 2 / 2 / 1 loops ✓ |
| EF-hand regex on CACNA1C / MCU | 0 / 0 ✓ |

The TRPV6 result is the setup session's one real finding and is written up
in `FINDINGS.md`.

**Checks.**

```
python3 -m src.catalogue      → validation: clean
                                49 families / 17 superfamilies / 29 census
                                98 human census genes / 245 catalogued
                                19 hazards
python3 scripts/selftest.py   → all invariants hold
```

**State.** Catalogue written, validated offline, committed. Nothing in it
checked against a live database except the four items above.

**Next.** **S0** — catalogue verification baseline. Re-derive every Pfam
accession, exemplar, architecture and taxon id; build
`reference_panel.fasta`; report mismatches without fixing them. Brief in
`docs/session_briefs.md`.

**Not done, on purpose.** The external drive was not attached; setup needs
no bulk storage, and S4/S5 cannot start until it is. The literature review
(`docs/review/`) is section stubs plus its build pipeline; writing it is
task S23 and it is deliberately blocked on S0 and S9 so its measured
sections report this project's results rather than restating the
literature.

---

## 2026-08-20 — S0 (partial): five passes, eight catalogue corrections, three classifier defects

**Task.** S0 — catalogue verification baseline. **Left `in_progress`.**

**What ran.** Five passes of `scripts/s0_catalogue_verify.py`. Each pass
found errors; fixing them invalidated the pass that found them, so the
sequence was pass → correct → re-run, which is what the parent project's
ledger describes as "clean on the third pass". Here it did not reach clean.

| pass | outcome |
|------|---------|
| 1 | 4 wrong Pfam short names, incl. `PF02714`/`PF13967` **swapped**; 33 exemplar-architecture differences; 101/102 exemplars resolved; 52/52 taxa; 514 requests, 0 failures |
| 2 | stopped early, deliberately, to fold in the architecture findings first |
| 3 | 2 further wrong names (`CaMBD`, `MCAfunc`) — both on signatures added in response to pass 1; 524 requests, 0 failures |
| 4 | stale before it finished (catalogue edited mid-run); stopped |
| 5 | **Pfam clean: 84 accessions, 0 missing, 0 name mismatches.** Exemplar stage throttled by InterPro after ~2,000 requests across the five passes; stopped rather than left hammering a rate-limited endpoint |

**Catalogue corrections (8).** Six Pfam short names; `PF00027` demoted from
`FAMILY` to `ACCESSORY` on plant CNGC after CNGC4 was measured to carry none;
three undeclared domains added (`PF02816` on TRPM7, `PF14703` on
OSCA/TMEM63, `PF19584` on MCA1); BK's and SK's signatures split to
`SUBFAMILY` after KCNN2 was measured to share nothing with BK.

**Classifier defects (3), all found by a new offline check.** Wrote
`scripts/s0_rule_coverage.py`, which feeds every family its own declared
architecture back through the rule table and exits non-zero on a family the
rules cannot name that no hazard explains. On its first run it found a
missing hazard (**HC17**, plant GLR vs animal iGluR). It then found that my
own `PF00027` demotion had made HCN classify as a plant channel, and that
polycystin-1 tied with TRPP at equal priority — a tie that would have put a
non-pore into the census. Fixed with a positive HCN test (`PF08412`) and by
raising the PKD1 rule above the other HC9 rules.

**Checks improved.** The signature-sharing boundary test compared `Status`
values, so a signature spanning `CHANNEL` and `CHANNEL_CONTESTED` counted as
"crossing" when both are census members — it now tests census membership.
The architecture check reported every declared-but-absent signature as a
mismatch, burying real errors among ~30 expected ones — it is now
level-aware and separates `FAMILY_SIGNATURE_ABSENT` (a catalogue error) from
`subfamily_absence_expected` (**D25**). `scripts/s0_report.py` now refuses
to render against tables written by an older verification script rather than
silently reporting on columns that are not there (**D13**).

**State.** `python3 -m src.catalogue` clean; `scripts/selftest.py` 61
invariants, all holding; `scripts/s0_rule_coverage.py` exits 0.
`results/s0_baseline/` is **mixed-provenance** and carries a `PROVENANCE.md`
saying which table came from which pass. The stale rendered `report.md` was
deleted rather than committed.

**NEXT — the exact resume point.** Leave the InterPro endpoint alone for a
while, then one uninterrupted `python3 scripts/s0_catalogue_verify.py`
(~7–14 min, ~520 requests), then `s0_report.py` and `s0_figures.py`. The
catalogue has not changed since pass 5's clean Pfam stage, so Pfam and
taxonomy are expected clean; **the exemplar-architecture table is the one
thing still genuinely unreviewed** — review only its
`FAMILY_SIGNATURE_ABSENT` rows, which is what the level-aware check now
isolates.

**Not done, on purpose.** No figures (they render from tables that are not
final). No S1 work. The permeability audit (S1b) remains the catalogue's
biggest unchecked surface: no database holds a P_Ca/P_Na, so nothing in S0
can verify the numbers the census tiers rest on.
