# How a protein gets classified

The classifier answers one question: **which catalogue family does this
protein belong to?** It deliberately does not answer "does it conduct
calcium" — that is a family attribute with a measurement behind it, not a
prediction (hazards **HC8**, **HC16**).

Three tiers run on every query and all three are recorded, whether or not
they agreed.

---

## Tier 1 — architecture (`src/classify/rules.py`)

Fires on the multiset of Pfam accessions a protein carries: which
signatures, in how many copies.

**Derived rules** are generated from the catalogue itself. A family's
`FAMILY`- and `SUBFAMILY`-level signatures become its requirement; a family
with only `SUPERFAMILY`-level signatures generates a rule that names the
superfamily and *declines to name a family*. Nothing is maintained twice.

**Hazard rules** are hand-written, sit at priority 100, and each names its
`HC` number so the benchmark can report per-hazard precision. Deleting one
is visibly deleting a test.

Half the hazard rules exist to keep something **out** of the census, which
is the shape of a calcium project: `PF00625` without any census-family
signature is a Cav β subunit; `PF00122` + `PF00689` is a P-type pump;
`PF13499` without a census-family signature is an EF-hand sensor. The
negative half of those tests is computed from the catalogue
(`_CENSUS_SIGNATURES`) so it cannot drift away from it.

**Ties are not resolved.** Two rules of equal priority naming different
families produce `ambiguous`, carrying both. Silently picking the first
match would turn the hazard registry into decoration.

The designed non-answer: `PF00520`×4 with no family-specific domain fires
`HC1-fourrepeat`, which names no family at all and hands the query to the
motif tier. That is Cav3, NALCN and CatSper, and it is the correct
architecture-tier answer for them.

## Tier 2 — motifs (`src/classify/motifs.py`)

Two kinds of test.

**Reference-free regexes**, usable on a bare sequence from an unannotated
genome:

| motif | means |
|---|---|
| `K_FILTER_RE` — TxGYG | conducts K⁺, so not a calcium channel (**HC15**) |
| `MCU_DXXE_RE` — WDxxE | the uniporter's DIME filter |
| `EF_HAND_RE` | a calcium-binding loop — evidence for a **decoy**, never against a channel (**HC12**) |

**Projected anchors**, where the residues that matter have no conserved
context and must be read off an alignment to a verified reference:

| anchor | reference | positions | calls |
|---|---|---|---|
| `four_repeat` | Nav1.5 `Q14524` | 372/898/1419/1711 | EEEE→Cav1/2, EEDD→Cav3, DEKA→Nav, EEKE→NALCN |
| `trpv_ca_ring` | TRPV6 `Q9H1D0` | 582 | D→Ca²⁺-selective TRPV |
| `orai_e106` | ORAI1 `Q96D31` | 106 | E→the CRAC filter |

Every anchor is checked against its own reference by `verify_anchor()`
before it is trusted, and a non-validating anchor **refuses to project**
rather than returning a guess (**D26**, **D28**). This is not hypothetical:
the TRPV6 anchor sits at D582 and not the literature's D542 because the
canonical UniProt entry is the long isoform, and an anchor copied from a
paper would have read the wrong column silently.

A non-call is a legitimate answer. TPC1 projects a short string because it
has two repeats, not four; CatSper's filter is built from four *different*
subunits and is recorded as `[open]`.

## Tier 3 — reference identity (`src/classify/reference.py`)

Best-hit identity against the exemplar panel, with:

- **D7** — a margin. Two references within 10 % of each other is not a call.
- **D29** — leave-one-out. A benchmark drawn from the catalogue scores
  against a panel that contains it, and scoring a protein against itself
  measures nothing.
- **D30** — a coverage floor of 30 % **of the longer sequence**. Covered-only
  identity without it is unsafe across a catalogue whose members differ
  30-fold in length: an aligner placing 250 residues inside a 5,038 aa
  ryanodine receptor selects the 250 best-matching columns and the metric
  then scores exactly those. Coverage of the *shorter* sequence does not
  catch it.

## Combination

Precedence: **hazard > motif > reference > architecture**. Every tier's
finding is recorded in `ChannelCall.evidence` even when it lost, and
disagreements are recorded in `conflicts` rather than discarded.

Confidence:

| tier | meaning |
|---|---|
| gold | two or more independent tiers agree |
| silver | one tier calls it, nothing contradicts |
| bronze | superfamily only, or a derived rule alone |
| unassigned | no tier could call it |

**`unassigned` is a result, not a failure.** Records the classifier cannot
call stay in the census with that label; they are never dropped.

## What the classifier deliberately does not do

- **It never consults a gene symbol.** `CACNB1`, `CACNG2`, `CATSPERB` and
  `CASR` all sort inside the calcium-channel symbol space and none is a
  pore; an unnamed gene model in a new genome has no symbol at all. The
  symbol is carried on the query and never read (**HC2**, **HC10**;
  locked by `scripts/selftest.py`).
- **It never predicts calcium permeability.** See **HC8** and **HC16**.
- **It never predicts selectivity or gating.** Both are literature attributes
  of a family.
- **It does not split TRPM4/5 from TRPM7.** There is no sequence
  discriminator; the split is `Provenance.LIT` and the limit is recorded
  (**HC15**).
