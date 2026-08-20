# PUBLICATION_ROADMAP.md — a census, classification and phylogeny of the calcium channels

**Goal.** Identify every calcium-conducting channel in a declared search
space, classify each one by positive tests with a recorded audit trail, and
reconstruct the phylogeny that the data actually supports — a forest of
within-family and within-superfamily trees plus a structural network between
them. To the evidence standard of an MBE / GBE / *Genome Research* paper: an
enumerated search space with a completeness argument, a benchmarked
classifier with per-family recall and per-hazard specificity, ML phylogenies
with support values, and one-command reproducibility.

**How the claim is scoped.** "A systematic census across N reference
proteomes spanning M lineages" (N and M fixed in S4), never an unbounded "all
calcium channels". Every absence claim is a claim about a *declared* search
space, and every count is a count under the boundary decisions recorded in
`docs/scope_and_boundaries.md`.

**The biology this rests on** is `docs/calcium_background.md`, which tags
every statement `[db]` / `[lit]` / `[open]`. Read it before S1.

**The four things that will bite you.**

1. **Calcium membership is a permeability, not a clade.** There is no motif
   and no fold that defines the subject. The census is reported in four
   tiers with the evidence for each attached, and a flat headline number is
   never quoted. Decision **D31**.
2. **The nearest relative of a calcium channel is usually not one.** Cav
   beside Nav (four residues), CNG beside HCN, TRPV6 beside TRPV1, TRPM7
   beside TRPM4. Domain architecture cannot make these calls. Decisions
   **D25**, **D26**; hazards **HC1**, **HC7b**, **HC15**, **HC16**.
3. **The word "calcium" is the census's biggest source of error.** The
   Ca²⁺-activated channels, the pumps, the exchangers, the EF-hand sensors
   and the sixteen `CACN`-prefixed auxiliary subunits all arrive with calcium
   annotations. The catalogue holds **245 human genes and counts 98**.
4. **Some permeabilities are not in the genome.** ADAR2 editing of the GRIA2
   Q/R codon decides whether an AMPA receptor conducts calcium. Hazard
   **HC8**; there is no test and the project says so.

---

## Session protocol

Claude: follow this protocol in every session that touches this project.

### Start of session
0. Open the project dashboard: `python3 scripts/dashboard.py --open` and
   start its watcher in the background (`python3 scripts/dashboard.py
   --watch`) so the page stays live through the session. Stdlib-only.
1. Read this file top to bottom. Read `docs/session_briefs.md` for the brief
   of the task you are about to work.
2. `git pull`.
3. Run `python3 -m src.utils.data_root --require`. It exits non-zero if the
   bulk-storage drive is not attached. **If it fails, stop and tell the
   user** — do not download anything, and do not "temporarily" use the
   internal disk. Note free space (`df -h`) before any bulk task.
4. Run `python3 -m src.catalogue` and `python3 scripts/selftest.py`. Both
   must be clean before anything else runs: the catalogue is the project's
   definition of its own subject, and the self-test is what proves the
   hazard rules, the census-tier invariants, the D27 refusal and the
   symbol-blindness still hold after whatever the last session changed.
5. Pick the task: the single ledger row whose Status is `in_progress`, else
   the topmost `pending` row whose dependencies are all `completed`.
   Announce it. Set its Status to `in_progress` (commit at session end).
6. Work **only that task** until its completion criteria pass. Do not start
   the next task even if time remains — spend surplus on tests, docs, or
   hardening of the current task.

### During the session
- Big/raw files → `get_data_root()` subdirs, never the repo. Committed
  artefacts: summaries, TSV/CSV ≤ ~20 MB, figures, manifests, code.
- Record every load-bearing number and file path in the task's Results
  column (link out to a file under `results/` if long).
- Write `results/session_live.json` from any long-running driver
  (`{"task": "S5", "workers": 2, "steps": [{"label": …, "done": …}]}`) so the
  dashboard shows real progress. `scripts/s0_lib.py:live_progress()` does it.
- A new confusable pair discovered mid-task is a **hazard row**
  (`src/catalogue/hazards.py`) with a discriminating test, not a note.
- A new permeability measurement is a **`Permeability` edit** with its method
  and provenance, not a sentence in a report.
- New leads, surprises, or scope changes → add a row to **Emergent tasks**.
  Never silently expand the current task.
- A task too large for one session: split it in the ledger (S5 → S5a/S5b),
  complete the first part properly, leave the rest `pending` with a note.
- Anything needing an interactive login or sudo: ask the user to run it via
  the `!` prefix.

### End of session (checklist — do all of it)
1. Completion criteria all pass → Status `completed` + date. Not all passing
   → stays `in_progress` with a NEXT note giving the exact resume point.
2. Update this file (ledger, Results, Emergent, Decisions).
3. Append a dated entry to `SESSION_LOG.md`.
3a. **Append a biological-findings entry to `FINDINGS.md`** — what the task
   changed in the biological story, plain language, findings before methods,
   unconfirmed claims marked *(pending: which task confirms it)*.
3b. **Refresh `README.md`** — the state-of-the-project summary for someone
   arriving cold.
4. `git add -A && git commit` (message: `S<n>: <one-line outcome>`) and
   `git push` if a remote is configured.
5. Tell the user: task status, headline results, what the next session does.

---

## Storage

- Active bulk-data root: see `data_root.txt`, read via
  `src/utils/data_root.py:get_data_root()`. Currently
  `/Volumes/FANTOM/CALCIUM_CHANNEL_DATA` — **an external drive that must be
  attached before any bulk session**.
- `require_data_root()` raises rather than falling back, so an unplugged
  drive stops the session at the top instead of after 200 GB has landed on
  the laptop.
- Expected bulk footprint: reference proteomes across ~60 lineages ~25 GB;
  HMMER raw output ~20 GB; AlphaFold structures for the reference panel
  ~5 GB; Foldseek databases ~15 GB; per-genome sweep evidence ~30 GB.
- Budget rule: any single download > 20 GB needs a note in Decisions with the
  running disk total.

---

## Task ledger

Statuses: `pending` / `in_progress` / `completed YYYY-MM-DD`.
Full step-by-step briefs: `docs/session_briefs.md`.

> **Next session: finish S0.** It is `in_progress`, not `pending`. Most of
> it has run and it has already paid for itself — eight catalogue
> corrections and three classifier defects — but the exemplar-
> architecture stage was throttled and stopped, so
> `results/s0_baseline/` holds tables from three different passes.
> **Read `results/s0_baseline/PROVENANCE.md` first**: it says which
> table came from which pass and gives the exact resume command. Leave
> the InterPro endpoint alone for a while before re-running.
>
> The one thing still genuinely unreviewed is the exemplar
> architecture table: the last full one (pass 3) listed 33 families
> whose declared signatures were not all observed, and the check has
> since been made level-aware so that a `SUBFAMILY` absence is no
> longer reported as a mismatch. Re-run it and review only the
> `FAMILY_SIGNATURE_ABSENT` rows.
>
> **Three things S0 must not skip.** (1) The three projection anchors —
> Nav1.5 `Q14524` DEKA, TRPV6 `Q9H1D0` D582, ORAI1 `Q96D31` E106 — must be
> re-verified, because an anchor that has drifted makes every filter call
> silently wrong and the TRPV6 case already proves the risk is real. (2) The
> `Provenance.CURATED` accessions need particular attention: `PF04749`
> (PLAC8, plant MCA), `PF02714`/`PF13967` (OSCA/TMEM63), `PF01452`
> (rotavirus NSP4) and `PF07766` (LETM1) were written from memory and are
> the most likely errors in the file. (3) The **permeability values are not
> verified by S0** — no database holds them. Auditing every P_Ca/P_Na against
> its source is task **S1b**, and until it runs the tier boundaries rest on
> `Provenance.LIT` claims that nothing has checked.
>
> **The external drive was not attached during setup** (setup needs no bulk
> storage). S4/S5 cannot start until it is.
>
> **This project is the ion-channel project's machinery pointed at a
> different subject.** The app (`src/core`, `src/databases`, `src/analysis`,
> `src/gui`, `src/investigation`, `src/discovery`), the classifier and
> phylogeny frameworks, the figure style, the dashboard, the
> manuscript-assembly and claim-checking tooling and this protocol are
> ported from `../ion_channel_genes`, itself ported from `../ip3r_genes` and
> `../piezo_genes`. The **Decisions** section carries their methodological
> scar tissue forward as pre-agreed rules. What is *not* ported is any
> result. Cav, ITPR, RYR, TRP, ORAI and MCU appear in the parent's catalogue
> as a handful of its ninety families; its census of them is an external
> check on this one, never an input.

| ID | Task (one session each) | Depends | Status | Results (headline) |
|----|-------------------------|---------|--------|--------------------|
| S0 | Catalogue verification + scope confirmation: re-derive every Pfam accession, exemplar, architecture, anchor and taxon id against live databases; build the reference panel | — | **completed 2026-08-20** | **Clean single pass: 533 requests, 0 failures.** 87 Pfam accessions (0 missing, 0 name mismatches), 102/102 exemplars resolved to a declared accession, 53/53 taxa, 3/3 projection anchors verified live, **0 family-level architecture mismatches** (30 subfamily-level, all expected). `reference_panel.fasta` covers all 102 exemplars. **Eleven families corrected** — one wrong accession (`PF00702`→`PF08282`, two Pfam families share a description), four domains demoted to the level they are actually diagnostic at, and six heterogeneous groups whose members share no domain. **Four tooling defects**: the missing anchor stage, the `GRIK2`/`GRIK5` synonym collision, `PF00027` contradicting its own hazard row, and the review build swallowing its README. See `results/s0_baseline/report.md` and `PROVENANCE.md`. |
| S1 | Classifier control benchmark: positives from every census family, one decoy per control family; per-family recall, per-hazard specificity, per-tier attribution | S0 | **completed 2026-08-20** | **Recall 38/48 (79.2 %), specificity 18/20 (90 %), 18/19 hazards exercised**, 68/69 panel members fetched (CHRNA7's fetch failed after four attempts and is reported in `missing.tsv`, excluded from the denominators rather than scored as a miss). Tier attribution: hazard 28, reference 20, architecture 5, motif 3, undecided 12 — the classifier is not a nearest-neighbour lookup, but the reference tier carries the architecturally identical families and that is where it fails. **The four-repeat filter is 27/27**: every Cav1/2 `EEEE`, every Cav3 `EEDD`, NALCN `EEKE`, eight Nav `DEKA`, SCN7A (Na_x) `DENA`; no string crosses the calcium boundary. **The TRPV anchor was measured not to discriminate** — TRPV1/3/4/5/6 all read `D` — so HC7b's discriminator is now "none from sequence" and `TRPV_CA_ANCHOR.calls` is empty. Nine of ten recall misses are the D7 margin refusing to guess, not wrong calls. **Two specificity failures**: TRPM4 named `trpm_ca` by a rule-generator leak (1 of 37 matches, measured), and CHRNA1 (a *muscle* subunit, out of census) named `nachr_ca` at margin +0.165 while CHRNA9 (in census) was left unassigned at +0.004 — the classifier gets the nicotinic boundary exactly backwards, because it is a permeability boundary and not a sequence one. Five defects fixed, including a whole class of silent fetch degradation (`src/utils/http.py`). See `results/benchmark_controls/report.md`. |
| S1b | **Permeability audit** — every `P_Ca/P_Na` in the catalogue traced to a resolved reference with its method; the tier boundaries re-examined against what the audit finds | S0 | pending | |
| S2 | Uncapped InterPro enumeration of every pore signature → census v2, with a positive family call on every record | S1 | pending | |
| S3 | Profile-HMM sweep (one HMM per family, best-profile assignment) over reference proteomes + jackhmmer-to-convergence completeness argument → census v3 | S1, S2 | pending | |
| S4 | Proteome scope: declared reference-proteome manifest across the lineage panel (the denominator) + download tooling | S1 | pending | |
| S5 | Genomic tblastn + miniprot sweep for families the proteomes miss → per-lineage ledger (found / lost / assembly-gap) → census v4 | S4 | pending | |
| S6 | Alignment upgrade: MAFFT L-INS-i + trimAl per family, and pore-module extraction for every tier-2 unit | S2, S3, S5 | pending | |
| S7 | **Tier-1 phylogenies**: IQ-TREE 2 + ModelFinder + 1000 UFBoot for every census family, rooted on its declared outgroup | S6 | pending | |
| S8 | **Tier-2 pore-module phylogenies** for every alignable superfamily — each showing the whole superfamily including its non-calcium members — plus the **tier-3 fold network** for the refused ones | S6, S7 | pending | |
| S9 | **Selectivity-filter atlas**: the filter locus for every family that has one, and whether it is congruent with the tier-2 tree (Q5) | S7, S8 | pending | |
| S10 | Repertoire evolution: presence/absence of every family across the lineage panel; ancestral reconstruction; the MCU-loss-in-yeast and Cav-absence-in-plants questions (Q4) | S5, S8 | pending | |
| S11 | Duplication history: which families expanded in which lineage, 2R/3R ohnologue status, and the order of the two repeat duplications that built Cav from a 6TM ancestor | S7, S10 | pending | |
| S12 | Structures: AFDB coverage per family, TM-align against the experimental reference set, Foldseek all-vs-all for the fold network → **how many times a Ca²⁺-selective pore has evolved** (Q6) | S2, S6 | pending | |
| S13 | ML selection tests on the families with clinical variant sets (RYR1, RYR2, CACNA1C, CACNA1A, ORAI1) | S6, S7 | pending | |
| S14a | **Manuscript assembly** — draft, figures, methods, deposit manifest, reviewer self-audit | S3, S5, S7, S8, S9, S10, S12, S15–S19 | pending | |
| S23 | **Literature review** — `docs/review/*.md` written, every citation resolved against Europe PMC before it can be used, figures rendered from committed tables | S0, S9 | **completed 2026-08-20** | `docs/channel_review_2026.md` — 17 sections, ~13,000 words, **122/122 sources resolved against Europe PMC**, 122 cited, 0 unused, 7 figures rendered from committed tables. Written against S0 only: every claim resting on S9/S12 or on the census sweeps is marked *(pending: task)* in the text, and §15 lists the nine open measurements. **Re-read §2.4, §7 and §13 after S9 lands** — the filter-congruence and convergence claims are the ones S9/S12 will either confirm or change. |
| S24 | Supplementary alignment + structure figures, and a figure-by-figure audit | S14a | pending | |
| S14b | **Deposit + release** — Zenodo DOI, repo public (D2 flip), reference verification, preprint upload | S14a | pending | **Human-gated; cannot be completed autonomously.** |

### Analysis & synthesis block (S15–S22)

These run on data the earlier tasks already produced. Priority orders them
when several are unblocked at once.

| ID | Task (one session each) | Depends | Priority | Status | Results |
|----|-------------------------|---------|----------|--------|---------|
| S15 | **Method contribution** — what would domain search alone have missed, per superfamily (Q3); the recall curve as methods are added | S2, S3, S5 | high | pending | |
| S16 | **Annotation-quality audit** — how often a real calcium-channel locus is missing, fragmentary, split, unnamed or filed under the wrong family across RefSeq / Ensembl / UniProt / InterPro; the correction list | S5, S15 | high | pending | |
| S17 | **Where the boundary actually falls** — how many published "calcium channel" gene lists include Ca²⁺-activated channels, pumps or auxiliary subunits, and by how much that moves the count (Q1) | S2 | high | pending | |
| S18 | **Convergence audit** — Cav, ORAI, MCU and TRPV5/6 build Ca²⁺-selective pores from unrelated folds: is "unrelated" a fact or a detection limit (Q6) | S8, S12 | high | pending | |
| S19 | **Channelopathy map** — clinical variants of every family mapped onto the pore module and the constrained core; and how often a calcium-signalling disease is caused by something that is not a calcium channel (CASQ2, CALM1, TMEM38B) | S6, S12 | medium | pending | |
| S20 | **Auxiliary-subunit census** — the excluded 40 human genes: how often they are counted as calcium channels in published totals | S2 | medium | pending | |
| S21 | **Non-animal and viral calcium channels** — the plant, fungal, protist and viral census, and whether the animal families have relatives there | S3, S5 | medium | pending | |
| S22 | **Pharmacology overlay** — which families carry approved-drug targets, against family size and annotation quality; note that the α2δ subunit (a non-channel) is among the most-prescribed targets in the catalogue | S2, S19 | low | pending | |
| S14c | **Manuscript rewrite pass** — one full pass once every analysis has landed | S14a, S24 | medium | pending | |

---

## The questions this project answers

- **Q1** — How many human genes encode a Ca²⁺-conducting pore, and how much
  does that number move with the tier boundary?
- **Q2** — What fraction of published "calcium channel" totals are auxiliary
  subunits, pumps, sensors or Ca²⁺-activated channels?
- **Q3** — What would domain search alone have missed, per superfamily?
- **Q4** — Which lineages lack which families, and is Cav's absence from
  plants a loss or a never-had?
- **Q5** — Is the selectivity filter congruent with the pore-module tree, or
  has it changed within families?
- **Q6** — How many times has a Ca²⁺-selective pore evolved?
- **Q7** — How much of the calcium census rests on permeabilities the genome
  does not encode?

---

## Emergent tasks & new aims

Anything discovered mid-session that deserves its own work goes here rather
than expanding the task in progress.

| Added | From | Task | Status |
|-------|------|------|--------|
| 2026-08-20 | setup | Confirm the external drive is attached and `data_root.txt` points at it before S4/S5 | open |
| 2026-08-20 | setup | **The TRPV6 anchor is at D582, not the literature's D542.** The canonical UniProt entry is the 765 aa long isoform. Check whether the same offset affects any other position-based claim in the catalogue, and whether the short isoform is the one the functional literature used throughout | **half closed 2026-08-20** — `scripts/s0_anchors.py` now re-verifies all three anchors against live UniProt and exits non-zero on a drift; all three pass, and they are the catalogue's only position-based claims. The literature half — which isoform the functional papers numbered from — is a source question and moves to **S1b** |
| 2026-08-20 | setup | **45 exemplars carry no UniProt accession** and are resolved live on every run. Fold the S0-resolved accessions back into the catalogue files so the reference panel is reproducible offline | **closed 2026-08-20** — all 102 exemplars now declare an accession (`scripts/s0_fold_accessions.py` folded 42; three were declared by hand after review). The panel is reproducible offline and a pass no longer resolves ~90 symbols live |
| 2026-08-20 | setup | **The permeability values are the catalogue's weakest claims.** Every `P_Ca/P_Na` is `Provenance.LIT` written from memory and nothing checks it — no database holds these numbers. S1b exists for this and should run early, because the census tiers depend on them | open (S1b) |
| 2026-08-20 | setup | **Six Pfam accessions are `Provenance.CURATED`** — `PF04749`, `PF02714`, `PF13967`, `PF01452`, `PF07766`, `PF10613` — and are the most likely errors in the catalogue | **closed 2026-08-20** — all six resolve with matching short names and are observed on their families' exemplars. `PF10613` was the last `CURATED` signature in the catalogue and is now `DB`; **zero remain**. Note the real error was elsewhere: `PF00702`, which was *not* on this list |
| 2026-08-20 | setup | **The TRPV anchor may not discriminate.** TRPV1–4 also carry acidic residues in the outer pore, so projecting TRPV6's D582 may return D for all of them. If it does, HC7b has no positive test and that must be recorded as a limit rather than quietly dropped | **closed 2026-08-20 — it does not discriminate.** `scripts/s1_anchor_power.py` projected D582 onto all six human TRPVs: TRPV5 `D`, TRPV6 `D`, **and TRPV1 `D`, TRPV3 `D`, TRPV4 `D`**; only TRPV2 differs (`M`). HC7b's discriminator now reads "none from sequence - measured, not assumed" and `TRPV_CA_ANCHOR.calls` has been emptied so the anchor cannot name a family. The trpv_ca / trpv_ns boundary now rests entirely on P_Ca/P_Na, which raises the priority of **S1b** |
| 2026-08-20 | setup | **The nicotinic boundary splits sister subunits.** α7/α9/α10 are in the census and α4 is out, on a permeability ratio. Check whether a tier-1 nicotinic tree separates them at all — if it does not, the split is honest and uncomfortable; if it does, it is a real clade | open (S7) |
| 2026-08-20 | setup | **CatSper's filter is unread.** Four different subunits contribute one residue each, so no single-sequence projection can read it. A four-sequence joint projection might; that would close the last `[open]` in the four-repeat family | **half closed 2026-08-20 — the method now has evidence behind it.** S1 projected the Nav1.5 anchor onto all four subunits: CATSPER1 `---D`, CATSPER2 `--D-`, CATSPER3 `-D--`, CATSPER4 `--D-`. Each subunit carries an aspartate at a *different* repeat position and three of the four positions are covered between them, which is what a heterotetramer building one pore from four proteins should look like. The joint projection is now a concrete proposal | open (S9) |
| 2026-08-20 | S0 | **Three control families have no rule that can name them** — `assoc_release_reg`, `outofscope_tric`, `outofscope_connexin` (`results/s0_baseline/rule_targets.tsv`). `derived_rules()` only generates rules for *census* families, so a control is recognisable only if a hand-written hazard rule exists for it. All three are real confusions worth a hazard row: calsequestrin mutations cause the same disease as RYR2 mutations, TMEM38B causes a calcium-release disease with a potassium channel, and connexin shares CALHM's fold class. Until then they will classify as `unassigned` or by reference identity alone, and S1 must report that rather than score it as a miss | **closed 2026-08-20** — S1 reports them in their own section rather than scoring them. All three behaved correctly: CASQ2, TMEM38A and GJA1 were each left `unassigned`, which for a decoy is a success — the census asks whether a protein is a calcium channel and `unassigned` answers no. The hazard rows are still worth writing, but nothing was mis-scored |
| 2026-08-20 | S0 | Biopython is present in the `piezo1` env but absent from the base interpreter, so `src/analysis` and the GUI only run there. Either pin the env in a wrapper script or drop the Biopython dependency from `alignment.py` in favour of `src/utils/mafft.py` | open |
| 2026-08-20 | S23 | **A tier-2 `ca_release` tree from *full-length* exemplars runs in 110 s and is not a valid tier-2 result** — `run.py` says so itself: a 5,038 aa RyR aligned against a 2,700 aa IP3R is dominated by the cytoplasmic caps, and the pore module has to be extracted first (S6). The output was **deleted rather than committed**, on the same reasoning that deleted the stale `report.md` last session: an intermediate that can only mislead is not worth keeping. Build it properly in S8 | open (S6, S8) |
| 2026-08-20 | S23 | **The review's Figure 6 is deliberately absent** and its slot is reserved. After S6/S8, re-run `scripts/s0_review_fig_folds.py` and `scripts/s0_review_build.py --pdf` to fill it | open (S8) |
| 2026-08-20 | S23 | **Re-read review §2.4, §7.1 and §13 once S9 and S12 land.** The filter-congruence claim, the TRPV anchor's discriminating power and the "at least four unrelated folds" convergence count are all written as open there, and are the paragraphs those tasks will confirm or change | open (S9, S12) |
| 2026-08-20 | S23 | **A second correction-induced defect.** Demoting `PF16526` to its measured level left `PF00027` as the sole requirement of the generated CNG rule, which then named plant CNGC as animal CNG — the same shape as the HCN defect found in setup. Consider making `s0_rule_coverage.py` part of the self-test so no catalogue edit can land without it | open |

| 2026-08-20 | S1 | **`derived_rules()` must generate rules for control families too.** Measured: `PF18139` is declared at FAMILY level by both `trpm_ca` (census) and `outofscope_trpm_monovalent` (control) — correctly, both carry it — but the generator iterates `census_families()` only, so the shared domain yields one rule pointing at the census family and TRPM4 matches it with nothing to tie against. "The classifier named a Ca²⁺-impermeable channel as a calcium channel" is the most damaging error this project can make. Exposure measured across the whole catalogue: **1 family-level leak in 37 architecture matches into control families** (`results/benchmark_controls/rule_leakage.tsv`); the other 36 are superfamily-only and correct. This is the third instance of one shape (`PF00027`/CNGC, HCN, now `PF18139`), so the fix is the generator, not another hand-written hazard rule. Blast radius: every call in the S1 table, so it needs its own session and a re-run of S1 | open |
| 2026-08-20 | S1 | **The nicotinic boundary cannot be drawn from sequence, with a number.** CHRNA1 (out of census) was called `nachr_ca` by reference identity at margin +0.165, while CHRNA7 (in census) was left unassigned at margin +0.000 between `nachr_ca` and `outofscope_nachr_muscle`. This is the earlier "does a tier-1 nicotinic tree separate them at all" question, now with benchmark evidence that the reference tier does not. If S7's tree does not either, the α7/α9/α10 split is a permeability boundary with no sequence correlate and must be stated as one | open (S7) |
| 2026-08-20 | S1 | **HC13 is untested.** No panel member exercised "the two-pore *calcium* channel may be sodium-selective". TPCN1/TPCN2 are on the panel but the hazard's rule never fired on them. Either the panel needs a member that triggers it or the hazard needs a rule that can fire — a hazard with zero measurements is untested, not solved | open |
| 2026-08-20 | S1 | **`src/databases/interpro.py:fetch_uniprot_sequence` carries the same silent-degradation defect** that `src/utils/http.py` was written to fix — `except requests.RequestException: return ""`, and `return ""` on any non-200. It is a second, `requests`-based fetcher on the domain-scan path, so **S2 will run through it**. Route it through the retrying client (or give it the same 404-versus-transient distinction) before S2 starts | open (S2) |
| 2026-08-20 | S1 | **Make `s0_rule_coverage.py` a self-test step.** Raised after S23 and now reinforced by a third instance of the same defect. The self-test is what stops a catalogue edit from landing with a broken rule table, and this defect class has now cost three sessions | open |
---

## Decisions log

**D0 — This project inherits the PIEZO, IP3R and ion-channel projects'
methodological decisions.** They were paid for over 40+ sessions and are not
to be re-derived. D1–D30 below are those rules, restated. **D31** is new and
specific to a subject whose membership is a measured quantity. A session may
overturn one, but must say so explicitly here with its reason.

**D1 — Bulk storage lives on the external drive**, `data_root.txt`. Sessions
call `require_data_root()`; an unplugged drive stops the session rather than
filling the internal disk.

**D2 — The repository stays private until S14b**, which flips it public
alongside the Zenodo DOI.

**D3 — The discovery scorer needs an evidence gate.** A score ≥ 40 needs at
least one family-specific component; size and novelty alone cap at 39.

**D4 — An absence claim must pass two bars**: a genome-wide contiguity floor
*and* a local check that the locus's own neighbourhood is present.

**D5 — Bait panels are screened by label, not padded for breadth.**

**D6 — Never issue a database correction without the integrity veto.**

**D7 — Best-hit assignment needs a margin.** Two references within ~10 % of
each other is not a call. `DEFAULT_MARGIN = 0.10` in
`src/classify/reference.py`.

**D8 — Representatives are chosen per clade × per kingdom** by a rule in a
script, never "the longest sequence per species".

**D9 — Quote an annotation claim with its annotation source.**

**D10 — Iterative searches need a coded kill criterion.**

**D11 — Look at the figure.** Any session that changes a figure looks at it;
any session that writes a legend looks at the figure it describes.

**D12 — Every load-bearing number in the manuscript needs a claim row** in
`scripts/s14_claims.py`.

**D13 — Reports are rendered from the committed tables**, never written by
hand alongside them.

**D14 — Family assignment is a positive test at every stage.** Inherited
from the IP3R project, where ITPR/RYR was the single instance; here the
nineteen instances are `src/catalogue/hazards.py`.

**D15 — The species tree is an input, not a result.**

**D16 — Cross-family comparisons are paired within genome.**

**D17 — Permutation nulls are drawn from real genomic windows.**

**D18 — The project runs in the reused `piezo1` conda env**
(`/opt/anaconda3/envs/piezo1`) for anything needing Biopython, matplotlib,
BLAST+ or Foldseek. MAFFT, HMMER, trimAl and IQ-TREE 2 come from Homebrew and
work in any shell. The catalogue, classifier and phylogeny drivers
deliberately need neither — stdlib plus `requests` — so the session-protocol
checks run anywhere. Versions: `results/toolchain_manifest.txt`.

**D23 — The scope of "calcium channel" is declared, not assumed.** Seven
boundary questions, seven recorded answers, in `docs/scope_and_boundaries.md`.
Anything excluded stays in the catalogue with a status, so an exclusion is a
decision rather than an omission. The Ca²⁺-activated potassium channels are
the control that proves the boundary is enforced.

**D24 — Membership and mechanism are separate calls.** TRPM4 is in the TRPM
family by descent and is Ca²⁺-impermeable by measurement; MCUB is a pore
subunit that reduces conduction. The classifier reports the family; the
permeability is a separate, literature-derived field, and the two are never
merged into one label.

**D25 — A signature is evidence only at the level where it is diagnostic.**
`Signature.level` is `SUPERFAMILY` / `FAMILY` / `SUBFAMILY` / `ACCESSORY` /
`SHARED_WITH_DECOY`, and the rule engine will not make a family call on
superfamily evidence.

**D26 — The four-repeat families are separated by their selectivity filter.**
Projection from human Nav1.5 `Q14524` positions 372/898/1419/1711, verified
against the reference before every use. `src/classify/motifs.py`.

**D27 — The phylogeny is a forest, and non-alignable comparisons go to the
fold network.** `build_tier2()` raises `NotAlignable`; there is no
`build_tier3()`. A tier-2 tree is labelled a *pore-module tree* in every
output, and it shows the **whole** superfamily including its non-calcium
members — dropping them to make "the calcium channel tree" asserts a clade
that does not exist.

**D28 — A missing tool disables a test, loudly.** `MafftUnavailable` is
raised, not caught; a missing IQ-TREE writes the alignment and no tree, with
the reason in `TreeRun.note`. No silent fallback to a weaker method, ever.

**D29 — A benchmark drawn from the catalogue classifies leave-one-out.**
Scoring a protein against a reference set that contains it returns 100 %
identity to itself and measures nothing. `classify(..., leave_one_out=True)`
drops the query's own accession, and the overlap is reported rather than
quietly handled.

**D30 — Covered-only identity needs a coverage floor, measured on the
longer sequence.** Measured in the parent project: connexin-26 scored 61.3 %
identity to ryanodine receptor 2 — higher than to its own relative
connexin-43 — because an aligner placing 226 residues inside 4,967 selects
the 226 best-matching positions. Coverage of the *shorter* sequence does not
catch it. The reference tier drops any hit covering less than
`reference.MIN_COVERAGE` = 30 % of the longer sequence. This matters more
here than in the parent project, not less: the catalogue spans 175 aa
(rotavirus NSP4) to 5,038 aa (RYR1).

**D31 — Calcium membership is graded, and every grade carries its own
evidence.** *(New in this project.)* "Calcium channel" is a permeability
ratio, not a clade and not a motif. Every family therefore carries a
`Permeability` record naming its tier, the reported P_Ca/P_Na **as a string,
not a float**, the method that produced it, and its provenance. The census is
reported in tiers and a flat total is never quoted without them. Three
consequences the code enforces: `validate()` rejects a census family whose
calcium claim records no method; `validate()` rejects a channel record in the
`NOT_CALCIUM` tier — such a record is `OUT_OF_SCOPE`; and the classifier
emits a family call with **no permeability claim attached**, because for the
conditional families there is nothing in the sequence to call it from.

**D32 — An anchor that does not discriminate is retired as a test, not kept
as a caveat.** *(New in this project, S1, 2026-08-20.)* The project's
standing rule is that a hazard is closed only by a positive test. The
corollary it had not yet stated is what to do when the test is run and
**fails**. HC7b was closed by projecting TRPV6's outer-pore aspartate onto
its relatives; projected onto all six human TRPVs, five of them read `D` —
including three that are not Ca²⁺-selective. The response is not a note
saying the anchor should be interpreted with care. It is three concrete
changes: the hazard's `discriminator` is rewritten to say **"none from
sequence — measured, not assumed"** with the measurement and its date; the
anchor's `calls` map is **emptied**, so the code cannot make a family call
from it even if some future caller wires it in; and the projection is kept
and reported, because a residue that does not discriminate is still a
measurement worth having. A test that has been measured to fail and is left
in place with a warning attached is worse than no test, because the next
reader sees an anchor, a verification step and a hazard marked closed.

**D33 — A fetch failure is raised, never returned as an empty result.**
*(New in this project, S1, 2026-08-20.)* Every stdlib fetcher on the
classifier path used to be `except Exception: return ""`, which cannot
distinguish "this protein carries no Pfam domain" from "UniProt rate-limited
us". Both consequences were measured in the first S1 smoke run: an empty
`pfam_counts` makes a protein look like it carries nothing a calcium channel
carries and scores a positive as a miss, and an empty anchor sequence makes
`verify_anchor()` fail — which this project reads as *the anchor has
drifted*, a conclusion the TRPV6 D542/D582 finding proves is not
hypothetical. `src/utils/http.py` retries with backoff, distinguishes a
genuine 404 from a transient failure, and raises `FetchFailed`; every caller
records the failure rather than absorbing it, and a run reports its request
count and its unrecoverable failures. This is D28 ("a missing tool produces a
missing result and a note, never a silently weaker method") applied to the
network, which is the piece of the toolchain most likely to fail
intermittently and least likely to be noticed when it does.
