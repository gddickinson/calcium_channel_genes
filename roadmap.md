# roadmap.md — development history of the app itself

Feature history of the toolkit, as distinct from the science plan
(`PUBLICATION_ROADMAP.md`). Versions v1.0–v2.x are inherited; v3.x is this
project.

## Inherited (v1.0 – v1.7, `../piezo_genes` → `../ip3r_genes`)

- v1.0 — tkinter GUI, NCBI/Ensembl/UniProt clients, `SearchOrchestrator` on
  worker threads with a `queue.Queue` back to the main loop.
- v1.1 — disk cache; results bundles; publication-style report writer.
- v1.2 — analysis pipeline: MSA, identity matrix, clustering, trees.
- v1.3 — AlphaFold and Foldseek clients; structure evidence.
- v1.4 — discovery scorer with the D3 evidence gate.
- v1.5 — investigation pipeline: seven evidence lines on one candidate.
- v1.6 — the sister-family test (D14), after the ITPR/RYR benchmark failure.
- v1.7 — figure style, dashboard, manuscript assembly, claim checker.

## Inherited (v2.0 – v2.4, `../ion_channel_genes`)

- v2.0 — `src/catalogue/`: the subject as data, with `Signature.level` (D25).
- v2.1 — the three-tier classifier and the hazard registry.
- v2.2 — `src/phylo/`: tiered forest, the D27 refusal, the fold network.
- v2.3 — `src/utils/scope.py`: run-time scoping over a multi-family subject.
- v2.4 — the D30 coverage floor, after the connexin/ryanodine identity bug.

## This project (v3.x)

- **v3.0** (2026-08-20) — the catalogue retargeted at calcium, and the schema
  extended with the one idea a permeability-defined subject needs:
  `CaClass`, `Permeability` (ratio as a string, with its method and
  provenance), and three `validate()` invariants that enforce **D31**.
  `census_by_tier()` throughout, so no flat total is reportable.
  `Gating.STORE_DEPLETION` and `Gating.MEMBRANE_APPOSITION`;
  `Selectivity.MONOVALENT_CATION`.
- **v3.1** (2026-08-20) — the motif tier rebuilt for calcium: three
  reference-free regexes (`K_FILTER_RE` as a *negative* test used positively,
  `MCU_DXXE_RE`, `EF_HAND_RE`) and three verified projection anchors
  (four-repeat, TRPV6 D582, ORAI1 E106). `FilterAnchor.calls` moved onto the
  anchor so each projection carries its own call map.
- **v3.2** (2026-08-20) — `figstyle.CA_CLASS`: the census tiers as an
  *ordered* palette, so `ca_activated` can never be drawn in a hue that
  reads as membership.

### Planned

- v3.3 — fold the S0-resolved exemplar accessions back into the catalogue so
  the reference panel is reproducible offline.
- v3.4 — a scaling path for the reference tier (the parent measured ~9 s per
  protein against a 162-sequence panel; a census cannot pay that).
- v3.5 — a four-sequence joint projection so CatSper's heterotetrameric
  filter can be read at all.
