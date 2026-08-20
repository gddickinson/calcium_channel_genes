## 13. How many times has a calcium-selective pore evolved?

### 13.1 The question, and why it has no single answer yet

Calcium signalling is old. It is present in bacteria, and the core logic —
keep cytosolic calcium low, then use its controlled entry as a signal — is
shared across the tree, which suggests it was established very early
[case2007, verkhratsky2014]. But the *channels* are not one story, and the
question in this section's title is deliberately awkward because it cannot be
answered inside any single tree.

The honest current answer is **at least four, in unrelated folds**: the EEEE
ring of the voltage-gated channels, ORAI's E106, the uniporter's DIME motif,
and the TRPV5/6 aspartate ring. These four share no alignable position with
one another, so "four" is a count of unconnected components in a structural
network, not a count of clades.

That framing carries an important caveat, and this review states it rather
than hiding it. "Unrelated" may be a fact about the proteins or a fact about
the detection limit of the methods used to compare them. Distinguishing those
two possibilities requires structural comparison — all-against-all structural
alignment across the fold network, rather than sequence similarity — and it is
an open result here (*pending: S12, S18*).

### 13.2 What is settled

**The P-loop pore module is ancient and prokaryotic.** The voltage-gated
superfamily descends from a prokaryotic ancestor, and bacterial channels
remain the structural prototypes and the outgroups that root the trees
[payandeh2011].

**The four-repeat architecture arose by internal duplication.** Cav and Nav
are single polypeptides of four homologous repeats, built from a
six-transmembrane ancestor by two rounds of internal duplication. The
two-repeat two-pore channels are the intermediate the story predicts. Their
placement is a result this project's pore-module trees are meant to produce
rather than an assumption they start from (*pending: S7, S8, S11*).

**Cav is animal, and does not exist in plants.** The four subunits of the
voltage-gated calcium channel complex have distinct evolutionary histories,
with ancient roots, increasing complexity and multiple independent losses
across lineages [moran2014]. Plants have no Cav homologue at all; fungi kept
one and lost the uniporter (§10).

**Repertoires differ profoundly across eukaryotes.** Surveys of algal and
other photosynthetic-eukaryote genomes find calcium channel complements that
match neither the plant nor the animal pattern [verret2010].

### 13.3 What is open, and how this project intends to close it

Four questions are live, and each is stated here with the evidence that would
settle it:

1. **Is Cav's absence from plants a loss or a never-had?** Answerable only
   against a declared lineage panel with a genomic sweep behind it, so that an
   absence is a claim about a search space rather than about the limits of a
   proteome download (*pending: S5, S10*).
2. **Is MCU loss in fungi one event or several?** Ancestral reconstruction
   across the panel (*pending: S10*).
3. **Is the selectivity filter congruent with the pore-module tree?** That is,
   has calcium selectivity been gained and lost *within* families, as the TRPV
   and TRPM splits suggest? This is the question that would turn the TRP
   division from a taxonomic problem into an evolutionary result
   (*pending: S9*).
4. **Are the four folds genuinely unrelated?** (*pending: S12, S18*.)

### 13.4 A methodological point about trees

Because superfamilies are defined by descent and not by ion, a pore-module
tree of the P-loop superfamily contains the voltage-gated sodium channels and
the Ca²⁺-activated potassium channels alongside the calcium channels. There is
a standing temptation to prune them and present "the calcium channel tree".
Doing so would hide the non-monophyly that is the single most important fact
about the subject, and would remove the outgroup that makes the tree rootable.

![](figures/fig7_forest.png)

**Figure 7 | A forest, and the trees that are refused.** The phylogenetic
units this project will build: tier-1 trees within families, tier-2
pore-module trees across alignable superfamilies including their non-calcium
members, and the superfamilies for which no tree is built at all because no
alignment across them exists. The figure is a schematic of a rule rather than
a result — it displays which units exist, not any inference from them.

The protocol behind this review therefore builds a forest — trees within
families and within alignable superfamilies, keeping every member — and
refuses outright to build a tree across a superfamily marked non-alignable.
The refusal is implemented in code rather than left to discipline: a request
for a tree spanning the CALHM large pores or the viral viroporins raises an
error and reports why.
