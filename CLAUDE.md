# CLAUDE.md — Project-specific instructions

@INTERFACE.md

## ⚠ Publication project — read this first every session

This project is executing a multi-session publication plan. At the start of
EVERY session:

1. Read `PUBLICATION_ROADMAP.md` and follow its **Session protocol**
   exactly: open the dashboard (`python3 scripts/dashboard.py --open` plus a
   background `--watch`), `git pull`, verify the data root
   (`python3 -m src.utils.data_root --require` — it exits non-zero if the
   external drive is not attached, and **that is a stop, not a warning**),
   pick the single next task from the ledger (first `in_progress`, else
   first unblocked `pending`), announce it, and work only that task to its
   completion criteria.
2. Detailed task instructions live in `docs/session_briefs.md`.
3. At session end, without being asked: update the roadmap ledger +
   Results (+ Emergent tasks for anything new), append to `SESSION_LOG.md`,
   **append a biological-findings entry to `FINDINGS.md`** (plain-language
   summary of what the finished task changed biologically; mark unconfirmed
   claims *(pending: task)*), refresh `README.md`, then `git add -A`, commit
   (`S<n>: <one-line outcome>`), and push if a remote exists.
4. Bulk data (genomes, proteomes, HMM databases, structures) go under
   `get_data_root()` (`src/utils/data_root.py`) — never into the repo.

## Project summary

**Subject: every calcium channel.** The project identifies, classifies and
reconstructs the phylogeny of the pathways that carry Ca²⁺ down its gradient
through an open pore — across the ~17 superfamilies and ~98 human
pore-forming genes that the term covers, plus their relatives in plants,
fungi, protists and viruses.

Three deliverables, in order: a **census** (what exists, in a declared search
space, reported in tiers), a **classification** (what each thing is, by
positive tests with an audit trail), and a **phylogeny** (a forest of trees
plus a fold network, because the subject spans unrelated folds).

The subject is defined in `src/catalogue/` — 49 families, 17 superfamilies,
18 hazards — and nothing else in `src/` hard-codes a channel name.

## The four things that will bite you

**1. "Calcium channel" is a permeability, not a clade.** There is no motif
and no fold that defines the subject. Every family carries a `Permeability`
record with its P_Ca/P_Na as a **string**, the method that produced it, and
its provenance; the census is reported in four tiers and **a flat total is
never quoted without them** (**D31**). `python3 -m src.catalogue --tiers` is
the authoritative view.

**2. The nearest relative of a calcium channel is usually not one.** Cav
beside Nav (four residues in the filter), CNG beside HCN, TRPV6 beside
TRPV1, TRPM7 beside TRPM4. Domain architecture cannot make these calls —
assign by positive test (filter projection, reference margin, hazard rule)
and record which tier decided (**D25**, **D26**).

**3. The word "calcium" is this census's biggest error source.** The
Ca²⁺-*activated* channels (BK, SK, TMEM16A, TRPM4/5) conduct K⁺ or Cl⁻; the
Ca²⁺-ATPases and Na⁺/Ca²⁺ exchangers are transporters; the EF-hand sensors
and CASR bind or sense and conduct nothing; sixteen `CACN`-prefixed human
genes encode no pore and seven of those belong to the AMPA receptor. The
catalogue holds **245 human genes and counts 98**. The classifier never
consults a symbol (**HC2**, **HC10**), and neither should any analysis.

**4. There is no tree of calcium channels.** ORAI and a ryanodine receptor
share no alignable position. `src/phylo/forest.py:build_tier2` *refuses* to
build a tree across a superfamily marked `alignable=False` (**D27**). And
the specific trap here: a tier-2 `ploop` tree **contains the sodium channels
and the Ca²⁺-activated potassium channels**, because superfamilies are
defined by descent. Do not drop them to make "the calcium channel tree" —
that hides the non-monophyly and removes the outgroup that makes the tree
rootable.

## Provenance

The app (`src/core`, `src/databases`, `src/analysis`, `src/gui`,
`src/investigation`, `src/discovery`), the classifier and phylogeny
frameworks, the figure style, the dashboard, the manuscript-assembly and
claim-checking tooling and the session protocol are ported from
`../ion_channel_genes`, itself ported from `../ip3r_genes` and
`../piezo_genes`. Their `INTERFACE.md` files map reference implementations
for most tasks here.

**Port the method; never port a result.** Cav, ITPR, RYR, TRP, ORAI and MCU
appear in the parent's catalogue as a handful of its ninety families, and its
census of them is an external check on ours rather than an input to it. The
measured annotation facts inherited from the parent (`PF00520` coverage of
TRP, the ITPR/RYR domain overlap) are cited with the parent's measurement
date and are re-verified by this project's S0.

## Conventions

- Every `.py` < 500 lines (split if it would exceed). Read `INTERFACE.md`
  before opening source files.
- The subject is defined in **one** place, `src/catalogue/`. A new family is
  an edit to one division file plus, at most, a hazard row. Never hard-code a
  gene name, Pfam id or size band anywhere else; read it from the catalogue
  through `src/utils/scope.py`.
- Every assertion in the catalogue carries a `Provenance` — `DB`
  (re-derived from a live database by an S0 script), `LIT`, `CURATED`
  (written by hand, not yet checked) or `OPEN`. Curated-but-unchecked is a
  legitimate state; silently wrong is not.
- **A permeability claim carries its method.** `validate()` rejects a census
  family whose `Permeability.method` is empty, and a channel record in the
  `NOT_CALCIUM` tier — such a record is `OUT_OF_SCOPE`.
- A hazard is only closed by a **test**, never by a caveat, and the test must
  be a **positive** one: never "it is not a Cav because the symbol says
  SCN5A", always "the filter reads DEKA".
- Every projection anchor is checked by `verify_anchor()` before use. The
  TRPV6 anchor sits at **D582**, not the literature's D542, because the
  canonical UniProt entry is the long isoform — that is what the check is
  for.
- Each database client subclasses `src/databases/base.py:DatabaseClient` and
  normalises its records into `ProteinVariant`; new clients register in
  `src/databases/__init__.py:AVAILABLE_CLIENTS`.
- The GUI never makes network calls on the main thread — everything goes
  through `SearchOrchestrator` → worker threads → `queue.Queue` →
  `MainWindow._drain_queue` (polled with `root.after()`).
- Analysis scripts live in `scripts/s<n>_*.py`, one task per prefix, and
  render their `report.md` purely from their committed tables so report and
  data cannot drift (**D13**).
- A missing tool produces a missing result and a note, never a silently
  weaker method (**D28**). `MafftUnavailable` is raised, not caught.

## Running

```
python3 -m src.catalogue --tiers                  # the census, by permeability tier
python3 run.py --catalogue --scope ploop          # what the catalogue claims
python3 run.py --classify CACNA1C,CACNB1,CALM1    # classify, with audit trail
python3 run.py --classify-preset controls_benchmark --save-results
python3 run.py --phylo cav_hva                    # tier 1 tree
python3 run.py --phylo largepore --tier 2         # refused, with the reason
python3 scripts/selftest.py                       # offline invariants, <1 s
python3 scripts/s0_catalogue_verify.py            # re-derive every claim
python3 scripts/dashboard.py --open
```

The catalogue, classification and phylogeny commands need only the standard
library plus `requests`. The search / analysis / GUI paths need Biopython and
matplotlib, which live in the `piezo1` conda env — run those with
`/opt/anaconda3/envs/piezo1/bin/python` (**D18**).

## Adding a family to the catalogue

1. Add a `ChannelFamily` to the right `src/catalogue/<division>.py`, with
   `Provenance.CURATED` on anything you have not checked and a
   `Permeability` record whose `method` says how the number was obtained.
2. If it shares a signature with something it could be confused with, add a
   `Hazard` naming the discriminating test.
3. `python3 -m src.catalogue` and `python3 scripts/selftest.py` — both clean.
4. `python3 scripts/s0_catalogue_verify.py` — then read
   `results/s0_baseline/report.md` and fix what it flags.
5. Update `INTERFACE.md`.

## Adding a family that is *not* a calcium channel

Do this whenever a search returns something that looks like one. Give it a
`Status` (`OUT_OF_SCOPE`, `TRANSPORTER`, `NON_CHANNEL_HOMOLOG`,
`CHANNEL_ASSOCIATED`), leave its `Permeability` as `NOT_CALCIUM` (or
`ACTIVATED` where it is gated by calcium), and write the positive test that
identifies it as something else into a hazard row. **The excluded set is a
deliverable, not housekeeping**: it is currently 147 of the catalogue's 245
human genes and it is what makes the census falsifiable.
