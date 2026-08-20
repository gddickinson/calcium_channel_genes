# The calcium channels: one permeability, many origins

*A review of the pathways that carry Ca²⁺ down its gradient through an open
pore — their filters, their folds, their evolution, and what the sequence
databases do and do not record about them.*

**Generated file — do not edit.** The text lives in `docs/review/*.md` and is
assembled by `scripts/s0_review_build.py`. Citations are written as stable
keys and renumbered on build; every reference was resolved against Europe PMC
by `scripts/s0_review_refs.py`, and a cited key with no verified record is a
build error rather than a silent entry in the bibliography.

---

## Summary

Calcium is the only ion whose channels are named for what they let through
rather than for what they are. Potassium channels can be defined
structurally: the T-x-G-Y-G filter is a sequence motif, and the proteins that
carry it are the proteins that conduct K⁺. Sodium channels are nearly as
clean. **A calcium census has no such handle.** "Calcium channel" names a
permeability ratio — a quantity measured in a particular cell, at a
particular divalent concentration, sometimes per subunit combination, and in
one important case per RNA-editing state of a single codon.

This review is organised around that fact and its consequences. The pores
that conduct Ca²⁺ have arisen independently in a large number of unrelated
folds, so there is no alignment containing a ryanodine receptor and an ORAI
channel and therefore no tree of calcium channels. What there is instead is a
set of independent inventions that converged on the same physical problem:
how to select a divalent ion that is thirty thousand times less abundant than
sodium in the cytosol's own gradient, and still conduct it at a rate near
diffusion.

We take the solutions one at a time — the four-repeat voltage-gated pore, the
CRAC channel's single glutamate ring, the uniporter's five-residue filter,
the epithelial TRPV aspartates, the intracellular release channels, the
ligand-gated receptors, the mechanosensors, and the plant, fungal and viral
channels that are not the animal ones renamed — and ask of each what is
genuinely shared and what merely looks shared.

Two questions then have to be answered before anything can be counted. The
first is where the boundary of the subject falls, because the word "calcium"
attaches to Ca²⁺-*activated* channels that conduct K⁺ or Cl⁻, to pumps and
exchangers that are not channels, to EF-hand sensors that conduct nothing,
and to sixteen human genes whose symbols begin `CACN` and which encode no
pore at all. The second is what the annotation databases actually record,
which turns out to be less than a census needs and to fail in ways that are
systematic rather than random.

## Scope, and what "the census" means here

Every count in this review is a count under the boundary decisions recorded
in `docs/scope_and_boundaries.md`, and is reported in tiers rather than as a
single headline number. The catalogue behind it holds **245 human genes and
counts 98**: 28 in the selective tier, 50 permeable, 9 conditional and 11
release. The 147 it does not count are catalogued too, each with a recorded
reason and, wherever a test exists, a positive test identifying it as
something else. That ratio is the point. A review that listed only what it
counted would look tidier and would be impossible to check.

## Figures

| | |
|---|---|
| **1** | the folds that build a calcium-permeable pore, one subunit each — *schematic* |
| **2** | the potassium filter across the P-loop branch — *measured, no alignment used* |
| **3** | the four-repeat locus: EEEE / EEDD / DEKA / EEKE — *measured, projected from Nav1.5* |
| **4** | length range by superfamily — *measured* |
| **5** | which families carry which shared domain, and which cross the census boundary — *measured* |
| **6** | a rooted ML tree of the intracellular release channels — *not yet rendered; awaits the pore-module extraction of S6 and the tier-2 build of S8* |
| **7** | the forest, and the superfamilies that get no tree — *schematic of a rule* |
| **8** | the architecture traps, to scale — *measured* |

Seven of the eight are rendered; figures rendered from committed tables
carry the table they came from in their legend, and the schematics say so and
display no data beyond the counts in them. **Figure 6 is deliberately
absent.** A tier-2 tree requires the pore module to be extracted first,
because a full-length alignment of a 5,038-residue ryanodine receptor against
a 2,700-residue IP₃ receptor is dominated by the cytoplasmic caps rather than
by the pore. Running the command on full-length sequences produces a tree,
and the tooling itself reports that the result is a quick look rather than
the tier-2 result. Substituting it here would be the kind of quiet
methodological downgrade this project forbids, so the figure waits for S6 and
S8.

## Key points

- **Calcium-channel membership is a permeability, not a clade.** There is no
  motif and no fold that defines the subject, so the census is reported in
  four evidence tiers and a flat total is never quoted without them.
- **The nearest relative of a calcium channel is usually not one.** Cav sits
  beside Nav and is separated from it by four residues; CNG beside HCN;
  TRPV6 beside TRPV1; TRPM7 beside TRPM4. Domain architecture cannot make
  any of these calls.
- **Ca²⁺ selectivity has been invented repeatedly in unrelated folds.** The
  four best-characterised solutions — the EEEE ring, ORAI's E106, the
  uniporter's DIME motif and the TRPV aspartate ring — share no alignable
  position with one another.
- **Some permeabilities are not in the genome.** Whether an AMPA receptor
  conducts Ca²⁺ is decided by ADAR2 editing of a single GRIA2 codon, and no
  sequence-level method can recover it.
- **The word "calcium" is the census's largest error source.** The
  Ca²⁺-activated channels conduct K⁺ or Cl⁻; the pumps and exchangers are
  transporters; the EF-hand sensors conduct nothing; and of the sixteen
  `CACN`-prefixed human genes that encode no pore, seven belong to the AMPA
  receptor.
- **Domain annotation does not partition the subject the way the textbooks
  do**, and a census built on the obvious accessions loses whole divisions
  without saying so.
