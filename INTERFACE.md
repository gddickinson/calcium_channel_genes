# INTERFACE.md — Module Navigation Map

> Read this **before** opening any source files. Each `.py` is < 500 lines
> and has one focused responsibility.

## Top-level

| File | Purpose |
|------|---------|
| `run.py` | CLI/GUI entry. `--catalogue`, `--classify`, `--phylo` need only stdlib + `requests`; `--headless` and the GUI need Biopython (D18). |
| `PUBLICATION_ROADMAP.md` | **The multi-session publication plan**: session protocol, task ledger (S0–S24), the seven questions, emergent tasks, and the Decisions log — D1–D30 inherited from the PIEZO / IP3R / ion-channel projects, **D31** new here. Read at the start of every session. |
| `docs/session_briefs.md` | Per-task instructions: goal, steps, completion criteria, outputs. |
| `docs/scope_and_boundaries.md` | **What counts as a calcium channel** — the seven boundary questions and this project's answers (D23). The reason the census has a denominator, and the document to read first. |
| `docs/calcium_background.md` | **The biology baseline.** Every statement tagged `[db]` / `[lit]` / `[open]`, including the measured annotation and anchor facts that decide how the census must run. |
| `docs/classification_rules.md` | How a protein gets classified: the three tiers, the rules they apply, the confidence scheme, and what the classifier deliberately does not do. |
| `docs/phylogeny_protocol.md` | **Why the phylogeny is a forest** (D27), the three tiers, the rooting table, and the trap specific to this project — a tier-2 P-loop tree contains the sodium channels and must keep them. |
| `docs/analysis_catalogue.md` | What the harvested data can answer — the analysis menu behind S15–S22, plus the analyses deliberately not attempted. |
| `docs/review/` | The literature review's **source** (task S23): numbered section files, citation rules, and the planned section list. `docs/channel_review_2026.md` will be *generated* from them and must never be hand-edited. |
| `CLAUDE.md` | Session-start instructions, conventions, the four things that will bite you. |
| `INTERFACE.md` | (this file) navigation map. |
| `README.md` | User-facing docs + the project status board. |
| `SESSION_LOG.md` | Running notes per session: what ran, what resulted, what's next. |
| `FINDINGS.md` | **The biological story, task by task** — plain-language, appended after every completed task. |
| `roadmap.md` | Feature-development history of the app itself (inherited v1.0–v2.x plus this project's v3.x). |
| `data_root.txt` | Path to the bulk-data root, read by `src/utils/data_root.py`. |
| `requirements.txt` | `requests` (required), `biopython` + `matplotlib` (search / analysis / figures only). |
| `presets/` | `calcium_human` (all 98 census genes), `controls_benchmark` (the S1 panel: a positive per census family, a decoy per control family), `ca_domain_scan`, `calcium_all` (exhaustive mode), and the scoped surveys `cav_survey`, `release_survey`, `soce_survey`, `mito_survey`, `ca_discovery`. |
| `cache/` | On-disk JSON cache (auto-created, gitignored). |
| `results/` | Committed analysis output, one directory per task. |
| `manuscript/` | The submission package, built by `scripts/s14_assemble.py`. |

---

## `src/catalogue/` — the project's definition of its own subject

**The single place any family, signature, size band, permeability or
exemplar is declared.** Nothing else in `src/` hard-codes a gene name.
49 families in 17 superfamilies; 29 are census families covering 98 human
genes, and the other 20 exist so they can be excluded — 147 human genes'
worth.

| File | Contents |
|------|----------|
| `schema.py` | `ChannelFamily`, `Superfamily`, `Signature`, `Exemplar`, `Hazard`, **`Permeability`**, and the enums: `CaClass` (the census tier — the idea D31 rests on), `Level` (the level at which a signature is diagnostic — D25), `Provenance`, `Gating`, `Selectivity`, `Fold`, `Status`. |
| `ploop.py` | The voltage-gated-like superfamily's calcium branches: Cav1/2 (`cav_hva`), Cav3 (`cav_lva`), CatSper, CNG, TPC. `PLOOP_SUPERFAMILY` and the shared `ION_TRANS` signatures live here. Declared **by descent, not by ion** — its non-calcium members are in `controls_excluded.py`. |
| `trp.py` | TRPV split by measured permeability (`trpv_ca` / `trpv_ns`), TRPC, TRPM (`trpm_ca`; TRPM4/5 are a control), TRPA, TRPML, TRPP. |
| `release.py` | ITPR and RYR — the `ca_release` superfamily, and the two largest proteins in the catalogue. |
| `store_operated.py` | ORAI. One family, its own fold, and a gate in another organelle. |
| `organelle.py` | MCU (+MCUB) and VDAC — the mitochondrial pathway. |
| `lgic.py` | The Ca²⁺-permeable ligand-gated channels: nicotinic α7/α9/α10, AMPA, kainate, NMDA, P2X. The `ca_conditional` tier lives here. |
| `mechano.py` | Piezo. |
| `largepore.py` | CALHM. The superfamily is `alignable=False`. |
| `nonanimal.py` | Plant GLR, plant CNGC, plant MCA, OSCA/TMEM63, and the viral viroporins. |
| `controls_associated.py` | `CHANNEL_ASSOCIATED`: the sixteen `CACN`-prefixed auxiliary subunits, the CatSper accessories, STIM, the MCU regulators, the release-channel regulators, polycystin-1. |
| `controls_excluded.py` | `OUT_OF_SCOPE` / `TRANSPORTER` / `NON_CHANNEL_HOMOLOG`: Nav, NALCN, HCN, the Ca²⁺-activated potassium and chloride channels, TRPM4/5, TRIC, connexins, the P-type pumps, the Na⁺/Ca²⁺ exchangers, the EF-hand sensors, CASR, POMT. |
| `hazards.py` | **The hazard registry** — 19 recorded ways to classify wrongly, each with the families involved, the shared evidence, the discriminating positive test, and the module that owns it. |
| `registry.py` | Assembly and lookup: `CATALOGUE`, `SUPERFAMILIES`, `census_families()`, `control_families()`, **`census_by_tier()`**, **`families_by_ca_class()`**, `human_genes()`, `signature_index()`, `shared_signatures()`, `pore_signatures()`, `exemplars()`, `reference_panel()`, `hazards_for()`, `validate()`, `stats()`. |
| `__main__.py` | `python3 -m src.catalogue [--tiers] [--families] [--shared] [--excluded]` — validate and print. Exits non-zero on any validation problem, so it works as a pre-commit gate. |

## `src/classify/` — three tiers, one call, an audit trail

| File | Key types / functions |
|------|-----------------------|
| `rules.py` | `ArchitectureRule`, `derived_rules()` (generated from the catalogue), `HAZARD_RULES` (hand-written, priority 100, one or more per closable hazard), `_CENSUS_SIGNATURES` (the "carries nothing a calcium channel carries" set, derived from the catalogue), `match_architecture()` → `RuleMatch` (ties are *ambiguity*, never a coin toss), `topology_check()`. |
| `motifs.py` | Three reference-free regexes — `K_FILTER_RE` (TxGYG ⇒ potassium ⇒ not calcium), `MCU_DXXE_RE` (the DIME motif), `EF_HAND_RE` (the HC12 decoy detector) — and three projected anchors: `FOUR_REPEAT_ANCHOR` (Nav1.5 `Q14524` 372/898/1419/1711 ⇒ DEKA), `TRPV_CA_ANCHOR` (TRPV6 `Q9H1D0` D582), `ORAI_ANCHOR` (ORAI1 `Q96D31` E106). `verify_anchor()`, `filter_signature()`, `scan()`. |
| `reference.py` | `ReferenceSet` (loads `reference_panel.fasta`, 3-mer prefilter, MAFFT identity over mutually covered columns), `best_match(...)` → `ReferenceResult` with the D7 margin, the D29 leave-one-out and the D30 coverage floor. |
| `classifier.py` | `ChannelQuery`, `ChannelCall`, `Evidence`, `classify()`, `classify_all()`. Tier precedence, confidence tiers, conflict recording. The gene symbol is carried and never consulted. **No permeability is ever predicted.** |
| `report.py` | `calls_table`, `confusion_table`, `recall_table`, `hazard_table`, `coverage_table`, `summary_counts`, `write_tsv` — the tables S1's report is rendered from (D13). |

## `src/phylo/` — a forest and a network

| File | Key types / functions |
|------|-----------------------|
| `modules.py` | `PoreModule`, `ModuleSet`, `module_from_envelope()`, `modules_from_envelopes()`, `module_by_projection()`, `whole_sequence_module()`. |
| `forest.py` | `build_tree()` (MAFFT → trimAl → IQ-TREE 2, every command recorded in `TreeRun`), `build_tier1()`, `build_tier2()` which **raises `NotAlignable`** for a superfamily the catalogue marks non-alignable, `refused_superfamilies()`. There is no `build_tier3()` (D27). |
| `network.py` | `FoldNetwork`, `FoldEdge`, `seed_network()`, `LITERATURE_EDGES`, **`UNCONNECTED`** — tier 3. Edges are structural similarity with no branch lengths and no support values; an unmeasured pair is recorded as unmeasured, never as unrelated. Q6 is answered here. |

## `src/utils/`

| File | Functions |
|------|-----------|
| `scope.py` | **`Scope` and `scope_for(key)`** — narrows the catalogue to "all", a superfamily or a family, and derives the signatures, size band, reference panel, *sister panel* (from the hazard registry) and known genes for a run. The `cav_hva` sister panel contains the sodium channels, the auxiliary subunits and the pumps, which is the point. |
| `mafft.py` | Stdlib-only MAFFT wrapper: `align()`, `parse_fasta()`, `project_positions()`, `alignment_stats()` (identity **plus coverage of both sequences** — the D30 guard), `percent_identity()`, `MafftUnavailable`. Raises rather than degrading (D28). |
| `species.py` | 51 species across 15 groups; `PANELS`, `resolve_species()`, `ensembl_species_slug()`, `panel()`. |
| `data_root.py` | `get_data_root()`, **`require_data_root()`**, `free_bytes()`. `python3 -m src.utils.data_root --require` is the session-protocol check. |
| `exporters.py` | `write_fasta()`, `write_csv()`, `write_json()`. |
| `results_writer.py` | `make_bundle_dir()`, `write_bundle()`. |
| `report.py` | `write_report()` — publication-style markdown + standalone HTML. |

## `src/core/`, `src/databases/`, `src/analysis/`, `src/discovery/`, `src/investigation/`, `src/gui/`

Ported from the parent projects and retargeted at this catalogue.

| File | Key types / functions |
|------|-----------------------|
| `core/models.py` | `ProteinVariant`, `GeneRecord`, `SearchQuery`, `SearchResult`, `SearchStatus`. |
| `core/cache.py` | `DiskCache(root, ttl_s)`. |
| `core/search.py` | `SearchOrchestrator` — fans queries across enabled DBs on worker threads, marshals results back via `queue.Queue`. |
| `databases/*.py` | One client per source: NCBI, Ensembl, UniProt, AlphaFold, Foldseek, Compara, BLAST; `interpro.py` carries `list_proteins_with_pfam()` (census mode, `strict` failure, raw-page `dump_dir`). |
| `analysis/pipeline.py` | `analyse(variants, …)` → `AnalysisResult`; `write_analysis()`. |
| `analysis/distance.py` | `identity_matrix(covered_only=True)` — fragment-aware identity. |
| `discovery/candidates.py` | `DiscoveryConfig` / `discover_novel_paralogs()` — the composite scorer with the D3 evidence gate and the **sister-family test** (D14). |
| `investigation/pipeline.py` | `Investigator(accession, options).run()` — seven evidence lines on one candidate. |
| `gui/app.py`, `gui/tools*.py` | `MainWindow`; the Analysis menu, the task runner, and `classify_selection()`, which shows the whole audit trail rather than just the answer. |

## `src/cli.py` and `src/cli_channel.py`

`cli.py` — `run_headless()` and `run_investigate()`, both scope-aware. Needs
Biopython.

`cli_channel.py` — `run_classify()`, `run_catalogue()` (which prints the
census tiers, never a flat total), `run_phylo()`, plus the stdlib fetchers.
**Deliberately Biopython-free.**

---

## `scripts/` — roadmap-session tooling (not part of the app)

| File | Purpose |
|------|---------|
| `dashboard.py` | **Project dashboard** (stdlib-only) → `dashboard.html`. Session protocol step 0. |
| `figstyle.py` | **The one figure style.** `SUPERFAMILY` (four safe categorical hues for seventeen superfamilies — the constraint is stated, not hidden), **`CA_CLASS`** (the census tiers, as an *ordered* scale so `ca_activated` never reads as membership), `SELECTIVITY`, `CONFIDENCE`, `STATUS`/`QUALITY`, `CLINICAL`. `save()` raises rather than writing a figure whose bbox runs off-canvas. |
| `selftest.py` | **The offline invariants**, under a second and no network: catalogue validation, the census-tier rules (D31), every hazard rule fired against the synthetic architecture it was written for, the classifier's blindness to gene symbols, the three motif regexes, the alignment helpers, the D27 refusal, and the scope's derivation of its sister panel. Session-protocol step 4. |
| `s0_lib.py` | S0 fetchers: `Fetcher` (polite, retrying, keeps a failure ledger), `pfam_entry`, `protein_pfams`, `resolve_gene`, `sequence`, `taxon`, `write_tsv`, `read_tsv`, `live_progress`. |
| `s0_catalogue_verify.py` | **S0** — re-derives every claim the catalogue makes against live databases and writes six TSVs plus `reference_panel.fasta`. Reports mismatches; never edits the catalogue. |
| `s0_rule_coverage.py` | **S0, offline** — feeds every family its own declared architecture back through the rule table and records what the architecture tier makes of it. Turns "domain architecture is not a family call" into a number, and **exits non-zero on a family the rules cannot name that no hazard row explains** — which is how hazard **HC17** was found. |
| `s0_report.py` | **S0** — renders `results/s0_baseline/report.md` purely from those tables (D13), including the census-tier table. |
| `s0_figures.py` | **S0's figure** — families and human genes per superfamily, and every domain signature carried by more than one family with the ones crossing the calcium / non-calcium boundary marked. |
| `s0_domain_map.py` | InterPro match **coordinates** for the proteins the review's architecture figures compare. |
| `s0_filter_atlas.py` | The two filter alignments → `filter_k.tsv` (TxGYG, located directly) and `filter_four_repeat.tsv` (projected from Nav1.5). Records near misses explicitly. |
| `review_sources.py`, `s0_review_refs.py`, `s0_review_build.py`, `review_figlib.py`, `s0_review_fig_*.py` | The review pipeline (task S23). Titles → Europe PMC resolution → generated markdown + PDF. A cited key with no verified reference is a build error. |
| `s1_toolchain.py` | **S1 step 1** — probes every external binary and Python package, writes `results/toolchain_manifest.txt`. |
| `s1_benchmark.py` | **S1 driver** — verifies the anchors, loads the reference panel, classifies the control panel, writes recall / confusion / hazard / coverage tables. |
| `s1_report.py` | **S1** — renders `results/benchmark_controls/report.md`, including per-tier attribution and the untested-hazard list. |
| `s14_*.py` | Manuscript assembly: page geometry and figure maps; figure copying under publication numbers; **the claim checker** (D12); the deposit manifest with SHA-256s; the typeset PDF; the driver. |
| `build_findings_page.py` + `findings_page.css` | Renders `docs/findings_summary.md` to one self-contained HTML page. |

Each ledger task adds its own `s<n>_*.py`. The parent projects'
equivalents (`../ion_channel_genes/scripts/`, `../ip3r_genes/scripts/`) are
reference implementations worth reading first.

---

## Data flow

### Classification (the core operation)

```
accession / gene symbol
        │  cli_channel.build_query()  → UniProt meta + InterPro pfam counts + sequence
        ▼
   ChannelQuery
        │
        ├─► rules.match_architecture()      hazard rules (100) > family rules (40-50)
        │                                   > superfamily-only (10); ties = ambiguous
        ├─► motifs.scan()                   TxGYG / DIME / EF-hand regexes;
        │                                   four-repeat, TRPV and ORAI projections
        └─► reference.best_match()          3-mer prefilter → MAFFT → covered-only
                                            identity → D7 margin, D30 coverage floor
        ▼
   combine by tier precedence (hazard > motif > reference > architecture)
        ▼
   ChannelCall  ── family · superfamily · status · confidence · margin
                   evidence[] from every tier · hazards[] · conflicts[]
                   ** and no permeability claim ** (HC8, HC16)
```

### The census

```
catalogue ──► census_families()   status ∈ {CHANNEL, CHANNEL_CONTESTED}
                                  AND CaClass ∈ {SELECTIVE, PERMEABLE,
                                                 CONDITIONAL, RELEASE}
          └─► census_by_tier()    the four tiers, reported separately (D31)
```

### Phylogeny

```
catalogue exemplars / census sequences
        │
        ├─ tier 1 ─► build_tier1()  full length, rooted on the catalogue's outgroup
        ├─ tier 2 ─► modules.*  ─►  build_tier2()  pore module only; the WHOLE
        │                                          superfamily, non-calcium members
        │                                          included; REFUSES if
        │                                          Superfamily.alignable is False
        └─ tier 3 ─► network.seed_network() + Foldseek  ── a network, never a tree
```
