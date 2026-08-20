# What counts as a calcium channel

**Decision D23.** The scope is declared, not assumed. Seven boundary
questions, seven recorded answers, and anything excluded stays in the
catalogue with a `Status` that says why — so an exclusion is a decision a
reader can disagree with rather than an omission they cannot see.

This document is the reason the census has a denominator. Every count this
project reports is a count *under these answers*, and changing one of them
changes the number in a way the reader can compute.

---

## The problem, stated once

A potassium census can be defined structurally: the TxGYG filter is a
sequence motif, and the channels that have it are the channels that conduct
K⁺. A sodium census is nearly as clean. **A calcium census has no such
handle.**

"Calcium channel" names a *permeability ratio*, and permeability ratios are
measured, per channel, in a particular cell, at a particular divalent
concentration, sometimes per subunit combination — and in one important case
per RNA-editing state of a single codon. The pores that conduct calcium have
arisen independently in at least a dozen unrelated folds, and the nearest
sequence relative of a calcium channel is very often not one:

| this is a calcium channel | its nearest relative is not | they differ by |
|---|---|---|
| Cav1.2 (CACNA1C) | Nav1.5 (SCN5A) | four residues in the filter |
| CNGA1 | HCN1 | ~20-fold in fractional Ca²⁺ current |
| TRPV6 | TRPV1 | one aspartate ring |
| TRPM7 | TRPM4 | no sequence discriminator known |
| nAChR α7 | nAChR α4 | ~10-fold in P_Ca/P_Na |
| MCU | MCUB (a pore that barely conducts) | conduction, not architecture |

So the boundary cannot be inherited from the fold, and it cannot be inferred
from the sequence. It has to be **declared, tiered and evidenced**, which is
what `Permeability` in `src/catalogue/schema.py` does and what decision
**D31** commits to.

---

## Q1 — Must a calcium channel be selective for Ca²⁺?

**No — but the census is reported in tiers, and never as one number.**

Requiring selectivity (say P_Ca/P_Na > 10) would exclude most TRP channels,
every Ca²⁺-permeable AMPA receptor, P2X, Piezo and CNG: that is, most of the
calcium entry in most non-excitable cells. Admitting everything with any
measurable Ca²⁺ permeability would admit the muscle nicotinic receptor and,
at the limit, any large pore.

The catalogue therefore records a `CaClass` per family with its P_Ca/P_Na
**as reported** and the method that produced it:

| tier | criterion | families | human genes |
|---|---|---|---|
| `ca_selective` | pore discriminates for Ca²⁺, roughly P_Ca/P_Na > 10 | 7 | 28 |
| `ca_release` | releases Ca²⁺ from an intracellular store | 5 | 11 |
| `ca_permeable` | non-selective, carries a physiologically important Ca²⁺ current | 15 | 50 |
| `ca_conditional` | permeability set by editing, splicing or subunit composition | 2 | 9 |

(Counts as of the catalogue's current state; `python3 -m src.catalogue
--tiers` is authoritative.)

**A reader who wants a stricter census takes the top row. A reader who wants
the broadest takes all four.** Both are supported, both are visible, and
neither is hidden inside a gene list. That is the whole point of the tiering.

The ratio is stored as a **string** — `">1000"`, `"~1-10"`, `"~0.5-4 (P2X1
and P2X4 highest)"` — because that is the shape the literature has. Turning
a range measured in one cell type into a float would invent a precision
nobody measured, and the census boundary would then rest on it.

## Q2 — Do pumps and exchangers count?

**No.** A channel conducts down an electrochemical gradient through a pore
that is open at both ends at once. SERCA, PMCA and SPCA hydrolyse ATP; NCX,
NCKX and NCLX are coupled to the sodium gradient; LETM1 to protons. All are
catalogued with `Status.TRANSPORTER` and 19 human genes.

This is the same call as the parent project's **D24** — membership and
mechanism are separate — and it excludes proteins that move more calcium per
cell than most census families do. It is a decision about what kind of
object is being counted, not a claim about importance.

## Q3 — Do intracellular release channels count?

**Yes**, as their own tier, with the compartment recorded.

ITPR, RYR, TRPML, TPC and the viral viroporins do not admit calcium to the
cell; they move it from a store into the cytosol. Physiologically that is
often the larger signal. The `compartment` field on every family records the
direction (`"endoplasmic reticulum -> cytosol"`), because the same
permeability means something different on an organelle: TRPML's selectivity
is measured at lysosomal pH 4.6, and IP3R's modest P_Ca/P_K matters less than
the 5,000-fold gradient it opens onto.

## Q4 — Do Ca²⁺-*activated* channels count?

**No**, and they are catalogued as `OUT_OF_SCOPE` with `CaClass.ACTIVATED`
so the exclusion is visible.

BK (KCNMA1), the SK channels (KCNN1-4), TMEM16A/B and TRPM4/TRPM5 are gated
by cytosolic Ca²⁺ and conduct K⁺ or Cl⁻ or monovalent cations. They carry
"calcium" in their common names, in their IUPHAR class names and in most
review titles, and a keyword-driven census counts them (hazard **HC15**).

The positive test is the potassium filter: a TxGYG match means the channel
conducts K⁺. **TRPM4 versus TRPM7 has no such test** — they share every Pfam
accession and sit in the same length band — so that split is recorded as a
literature call with `Provenance.LIT` and the classifier is not expected to
make it from sequence. Recording the limit is the point.

## Q5 — Do auxiliary subunits and gates count?

**No.** `Status.CHANNEL_ASSOCIATED`, 40 human genes, and the largest single
source of inflation in published totals.

Sixteen human genes carry a `CACN` symbol prefix and encode no pore
(hazard **HC2**), and seven of those — CACNG2 to CACNG8 — are TARPs, AMPA
receptor subunits with a claudin fold and no role in voltage-gated calcium
channels at all. Five more carry the `CATSPER` root, beside two further
accessories (**HC10**). STIM1 is the
gate that opens ORAI from another organelle; EMRE is required for the
uniporter to conduct and lines none of its pore.

The boundary case that defines the rule is **MCUB**: a subunit that
assembles into the uniporter tetramer and *reduces* conduction. It is in the
census, because the question the catalogue asks is "does this gene
contribute pore lining", not "does this gene increase current" (**HC6**).

## Q6 — Are non-animal and viral channels in scope?

**Yes.** A census restricted to human genes cannot make an evolutionary
claim, and the non-animal calcium channels are not the animal ones renamed.

Plants have **no Cav homologue at all**; their voltage- and ligand-gated
calcium entry runs through the glutamate-receptor-like GLR family and the
cyclic-nucleotide-gated CNGC family — both relatives of animal channels that
do something else. Fungi kept a Cav homologue (CCH1) and lost MCU, which is
why *Saccharomyces cerevisiae* has no mitochondrial calcium uptake and part
of why the uniporter took fifty years to identify. Rotavirus NSP4 is a
genuine ER calcium-release channel and the enterotoxin.

## Q7 — What is the census counting: genes, pores, or channels?

**Pore-forming genes**, and the difference is stated wherever it matters.

Seven human `GRIN` genes encode NMDA receptor subunits, and no single one of
them makes a channel: the receptor is an obligate heterotetramer of GluN1
plus GluN2 or GluN3. Four `CATSPER` genes make one heterotetrameric channel.
Counting genes is reproducible and counting "channels" is not, so the census
counts genes and says so — and a claim about the *number of distinct calcium
channels* in a cell is a different claim this project does not make.

---

## The consequence: the excluded set is larger than the census

The catalogue holds **245 human genes** and counts **98**. The 147 it does
not count are not an afterthought; they are what a search for "calcium
channel" returns, and every one of them has a recorded reason and, wherever
a test exists, a positive test that identifies it as something else.

That ratio is the strongest argument for doing the census this way. A
project that simply listed what it counted would look tidier and would be
unfalsifiable.

---

## What would change these answers

Each of these is a live disagreement, and each can be acted on by editing
one field:

- **The connexin/pannexin hemichannels** are excluded on the ground that the
  physiological state is the docked junction. Undocked hemichannels do pass
  Ca²⁺. Moving `outofscope_connexin` to `CHANNEL_CONTESTED` with a
  `PERMEABLE` class adds 16 human genes.
- **TPC** is counted and may be Na⁺-selective (**HC13**). Removing it costs 2.
- **VDAC** is counted as `ca_permeable` and is not a calcium channel in the
  sense Cav is. Removing it costs 3.
- **The nicotinic boundary** currently runs between α7/α9/α10 and the rest,
  which splits sister subunits. A stricter reading removes 3.
- **The `ca_conditional` tier** could reasonably be excluded entirely on the
  ground that the genome does not encode the permeability. That costs 9.

The catalogue is designed so that each of these is one line and a recount.
