# What the harvested data can answer

The analysis menu behind S15–S22, and — as importantly — the analyses
deliberately not attempted.

## Available once S2/S3 land (the census)

- **The tier curve.** How the human count moves as the boundary moves from
  `ca_selective` to all four tiers. The headline of Q1, and the one figure
  that makes the project's method visible.
- **Published-total reconciliation.** For each published "calcium channel"
  gene list, how many of its entries this catalogue classifies as auxiliary
  subunits, pumps, sensors or Ca²⁺-activated channels (Q2, S17).
- **Method contribution.** Recall per superfamily as methods are added:
  domain search → profile HMM → genomic sweep (Q3, S15).
- **Annotation quality.** How often a real locus is missing, fragmentary,
  split, unnamed or misfiled, per database (S16).

## Available once S5/S10 land (the lineage panel)

- **Presence/absence per family per lineage**, with every absence passing
  both D4 bars.
- **The two sharp cases**: MCU's absence from *Saccharomyces cerevisiae*,
  and Cav's absence from plants. Both are well known and neither has been
  tested here; a census that assumed them would be citing rather than
  measuring.
- **Ancestral repertoire reconstruction** on the species tree (D15: the tree
  is an input).

## Available once S7/S8/S12 land (the forest and the network)

- **Filter congruence** (Q5): does the selectivity filter track the
  pore-module tree, or has it changed within families? Cav3's EEDD against
  Cav1/2's EEEE is the first test case.
- **Convergence count** (Q6): unconnected components of the fold network.
- **The duplication order** that built the 24TM Cav from a 6TM ancestor, and
  where TPC's two-repeat architecture falls (S11).

## Deliberately not attempted

- **Predicting P_Ca/P_Na from sequence.** The AMPA receptors settle this:
  the same genomic codon gives a Ca²⁺-permeable or Ca²⁺-impermeable channel
  depending on ADAR2 (**HC8**). A predictor trained on family labels would
  learn the labels, and its errors would be invisible.
- **Predicting selectivity or gating** at all. Both are literature
  attributes of a family (**HC16**).
- **A single tree of the calcium channels.** Forbidden by **D27** and by the
  code.
- **Separating TRPM4/5 from TRPM7 by sequence.** No discriminator is known;
  the split is `Provenance.LIT` and stays that way until someone finds one.
- **Counting "channels" rather than pore-forming genes.** Seven `GRIN` genes
  make no defined number of channels (**Q7**).
- **Resolving the TPC dispute.** Both readings reproduce; the catalogue
  records the disagreement (**HC13**).
