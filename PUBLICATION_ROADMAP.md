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
| S0 | Catalogue verification + scope confirmation: re-derive every Pfam accession, exemplar, architecture, anchor and taxon id against live databases; build the reference panel | — | **in_progress** | Five passes run; **eight catalogue corrections and three classifier defects came out of them** (see `FINDINGS.md`). Pfam stage **clean on the final pass: 84 accessions, 0 missing, 0 name mismatches**; taxonomy clean (52/52); 101/102 exemplars resolved. **NOT complete**: the exemplar-architecture stage was throttled and stopped, and `results/s0_baseline/` is mixed-provenance — see `results/s0_baseline/PROVENANCE.md` for which table came from which pass and the exact resume command. |
| S1 | Classifier control benchmark: positives from every census family, one decoy per control family; per-family recall, per-hazard specificity, per-tier attribution | S0 | pending | |
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
| S23 | **Literature review** — `docs/review/*.md` written, every citation resolved against Europe PMC before it can be used, figures rendered from committed tables | S0, S9 | pending | |
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
| 2026-08-20 | setup | **The TRPV6 anchor is at D582, not the literature's D542.** The canonical UniProt entry is the 765 aa long isoform. Check whether the same offset affects any other position-based claim in the catalogue, and whether the short isoform is the one the functional literature used throughout | open (S0) |
| 2026-08-20 | setup | **45 exemplars carry no UniProt accession** and are resolved live on every run. Fold the S0-resolved accessions back into the catalogue files so the reference panel is reproducible offline | open (S0) |
| 2026-08-20 | setup | **The permeability values are the catalogue's weakest claims.** Every `P_Ca/P_Na` is `Provenance.LIT` written from memory and nothing checks it — no database holds these numbers. S1b exists for this and should run early, because the census tiers depend on them | open (S1b) |
| 2026-08-20 | setup | **Six Pfam accessions are `Provenance.CURATED`** — `PF04749`, `PF02714`, `PF13967`, `PF01452`, `PF07766`, `PF10613` — and are the most likely errors in the catalogue | open (S0) |
| 2026-08-20 | setup | **The TRPV anchor may not discriminate.** TRPV1–4 also carry acidic residues in the outer pore, so projecting TRPV6's D582 may return D for all of them. If it does, HC7b has no positive test and that must be recorded as a limit rather than quietly dropped | open (S1) |
| 2026-08-20 | setup | **The nicotinic boundary splits sister subunits.** α7/α9/α10 are in the census and α4 is out, on a permeability ratio. Check whether a tier-1 nicotinic tree separates them at all — if it does not, the split is honest and uncomfortable; if it does, it is a real clade | open (S7) |
| 2026-08-20 | setup | **CatSper's filter is unread.** Four different subunits contribute one residue each, so no single-sequence projection can read it. A four-sequence joint projection might; that would close the last `[open]` in the four-repeat family | open (S9) |
| 2026-08-20 | S0 | **Three control families have no rule that can name them** — `assoc_release_reg`, `outofscope_tric`, `outofscope_connexin` (`results/s0_baseline/rule_targets.tsv`). `derived_rules()` only generates rules for *census* families, so a control is recognisable only if a hand-written hazard rule exists for it. All three are real confusions worth a hazard row: calsequestrin mutations cause the same disease as RYR2 mutations, TMEM38B causes a calcium-release disease with a potassium channel, and connexin shares CALHM's fold class. Until then they will classify as `unassigned` or by reference identity alone, and S1 must report that rather than score it as a miss | open (S1) |
| 2026-08-20 | S0 | Biopython is present in the `piezo1` env but absent from the base interpreter, so `src/analysis` and the GUI only run there. Either pin the env in a wrapper script or drop the Biopython dependency from `alignment.py` in favour of `src/utils/mafft.py` | open |

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
