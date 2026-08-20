## 16. Methods

This review is a component of a project that produces a census, a
classification and a phylogeny, and its measured statements come from that
project's committed outputs. This section states how they were produced and
what the reader is entitled to conclude from them.

### 16.1 The subject is defined in one place

Every family, signature, size band, permeability, exemplar and hazard is
declared in a single catalogue module, and nothing else in the codebase
hard-codes a gene name, a Pfam accession or a size band. Adding a family is an
edit to one file plus, at most, one hazard row. The catalogue currently holds
49 families in 17 superfamilies: 29 census families covering 98 human genes,
and 20 control families that exist so they can be excluded, covering the other
147.

Every assertion carries a provenance — re-derived from a live database,
taken from the literature, curated by hand and not yet checked, or explicitly
open. Curated-but-unchecked is a legitimate state; silently wrong is not. As
of this build, no signature in the catalogue remains in the unchecked state.

### 16.2 The census is reported in tiers

Membership is a measured permeability, so the census is reported as four tiers
with the evidence for each attached, and a flat total is never quoted without
them:

| tier | criterion | families | human genes |
|---|---|---|---|
| selective | pore discriminates for Ca²⁺, roughly P_Ca/P_Na > 10 | 7 | 28 |
| permeable | non-selective, physiologically important Ca²⁺ current | 15 | 50 |
| conditional | permeability set by editing, splicing or subunit composition | 2 | 9 |
| release | releases Ca²⁺ from an intracellular store | 5 | 11 |

Every family carries a permeability record whose ratio is stored as a string,
together with the method that produced it and its provenance; a census family
whose method field is empty fails validation.

### 16.3 Classification is by positive test, with an audit trail

A protein is classified by three tiers of evidence, in precedence order:

1. **Hazard rules** — hand-written tests for recorded ways of classifying
   wrongly, each naming the discriminating observation.
2. **Motifs** — three reference-free regular expressions (the potassium
   filter, the uniporter's DIME motif, the canonical EF-hand loop) and three
   projected anchors (the four-repeat locus from Nav1.5, the TRPV aspartate
   from TRPV6, the ORAI glutamate from ORAI1).
3. **Reference identity** — alignment against a panel of catalogued
   exemplars, scored over mutually covered columns only, with a required
   margin between the best and second-best family and a coverage floor.
4. **Domain architecture**, last, and never on its own where a hazard applies.

Ties are reported as ambiguity rather than resolved by a coin toss. The gene
symbol is carried through the whole pipeline and never consulted. **No
permeability is ever predicted.**

Every projected anchor is verified against its own reference before use, and a
non-validating anchor refuses to project rather than returning a guess. The
TRPV6 case in §2.4 is why.

### 16.4 The phylogeny is a forest, and sometimes a refusal

Three tiers, and no fourth:

- **Tier 1** — full-length trees within a family, rooted on the family's
  declared outgroup.
- **Tier 2** — pore-module trees across an alignable superfamily, including
  every member whether or not it conducts calcium.
- **Tier 3** — a structural network between folds, with no branch lengths and
  no support values. An unmeasured pair is recorded as unmeasured, never as
  unrelated.

A request for a tree spanning a superfamily the catalogue marks non-alignable
raises an error and reports the reason. There is no tier that builds one tree
of all calcium channels, because no such alignment exists.

Alignments use MAFFT and trimAl; trees use IQ-TREE 2 with ModelFinder and
ultrafast bootstrap; structural comparison uses Foldseek against AlphaFold
models [katoh2013, capellagutierrez2009, minh2020, kalyaanamoorthy2017,
vankempen2024, jumper2021]; profile searches use HMMER [eddy2011]. A missing
tool produces a missing result and a note, never a silently weaker method.

### 16.5 Reproducibility and the standing of the citations

Every analysis script renders its report purely from its own committed tables,
so a report cannot drift from the data it describes. Verification scripts
report mismatches and never edit the catalogue: a script that rewrites its own
inputs to make its checks pass is not a check.

The bibliography of this review is machine-generated. Each source title is
resolved against Europe PMC, and a record is accepted only if the returned
title is at least 90 % similar to the one requested, so a misremembered paper
fails loudly rather than becoming a plausible entry. **A cited key with no
verified reference is a build error.** Every citation in this document is
therefore one that a live literature service returned, not one that anybody
recalled.

### 16.6 What this review does not establish

The measured statements here are the catalogue-verification results of §12.
They establish that the catalogue's claims about accessions, exemplars,
architectures, anchors and taxa are correct as of the build date. They do
**not** establish that the catalogue is complete, that its family assignments
are right, or that its permeability values are accurate — those are the
census, the classifier benchmark and the permeability audit respectively, and
each is marked in the text where it is relied on.
