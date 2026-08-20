## 8. Ligand-gated calcium entry, and a permeability not in the genome

Three unrelated superfamilies of ligand-gated channels carry physiologically
important calcium currents: the ionotropic glutamate receptors, the Cys-loop
nicotinic receptors, and P2X. They have nothing in common structurally, and
each provides a different reason why calcium permeability resists
sequence-based prediction.

### 8.1 NMDA receptors: selective, and obligately heteromeric

NMDA receptors are the most calcium-permeable of the glutamate receptors,
with a fractional calcium current near 12 %, and their calcium entry is the
trigger for most forms of synaptic plasticity [traynelis2010, mayer2006].
They are counted in the selective tier.

They also make the sharpest case for the census counting *genes* rather than
*channels*. Seven human `GRIN` genes encode NMDA receptor subunits and not
one of them makes a channel alone: the receptor is an obligate heterotetramer
of GluN1 with GluN2 or GluN3 subunits, and GluN3-containing receptors are far
less calcium-permeable than GluN2-containing ones. Counting genes is
reproducible; counting "channels" would require deciding which subunit
combinations exist in which cells, which is not a genomic question. The
census counts genes and says so.

### 8.2 AMPA and kainate receptors: the permeability ADAR2 decides

AMPA receptors are the clearest case in all of calcium biology of a
functional property that the genome does not encode. A receptor containing an
edited GluA2 subunit is calcium-impermeable; the same receptor without it is
calcium-permeable. The difference is a single codon in `GRIA2`, changing a
glutamine to an arginine in the pore-lining M2 loop, and the change is made
post-transcriptionally by the RNA editing enzyme ADAR2
[sommer1991, hume1991, burnashev1992].

The genetics are unambiguous about which state matters. Mice lacking ADAR2
die young with seizures, and the phenotype is rescued completely by a
knock-in allele encoding the edited residue directly — the enzyme's only
essential substrate, in that context, is that one codon [higuchi2000].

For a sequence-based census this is a hard limit rather than a difficulty.
The genomic `GRIA2` sequence encodes the calcium-permeable form; editing is
close to complete in adult brain; and no method operating on genomes or
proteomes can recover the distinction. The catalogue therefore places AMPA
and kainate receptors in a **conditional** tier, records the mechanism, and
records that there is no test. A census that quoted a single number for
"calcium-permeable human genes" without that tier would be asserting
something about nine genes that nothing in the data supports.

### 8.3 Nicotinic receptors: a boundary that splits sisters

The Cys-loop nicotinic acetylcholine receptors span an order of magnitude in
calcium permeability. The α7 homopentamer reaches P_Ca/P_Na near 10 and
carries calcium entry sufficient to trigger downstream signalling; the
muscle-type receptor is near 0.1–1 [fucile2004]. The catalogue counts α7, α9
and α10 and excludes the rest.

This is the census's most uncomfortable boundary, and it is worth stating
plainly rather than smoothing over. It divides a single natural sequence
family by a measured ratio, placing sister subunits on opposite sides. If a
tree of the nicotinic subunits does not separate them, the split is honest
and awkward; if it does, it is a real clade. Which of those is true is a
result to be produced, not assumed (*pending: S7*).

### 8.4 P2X: a third fold, and a pore that changes size

P2X receptors are ATP-gated trimers with two transmembrane helices per
subunit and no relationship to either of the families above; the zebrafish
P2X4 structure established the fold [kawate2009, north2002]. The seven human
paralogues span roughly an order of magnitude in calcium permeability, with
P2X1 and P2X4 highest [egan2004].

P2X7 adds a further complication of the kind that defeats any static
description: on prolonged activation its pore dilates and begins to pass
molecules up to about 900 Da. A permeability measured at one moment of
activation is not the permeability at another, which is one more reason the
catalogue stores these ratios as strings with their conditions attached
rather than as numbers.
