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

Rewrote `src/classify/rules.py`'s hazard rules (24 rules across 18 hazards),
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
                                18 hazards
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
