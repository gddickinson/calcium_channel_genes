## 2. Four filters, no common ancestor

If calcium channels formed a clade, they would share a filter. They do not.
The four best-characterised calcium-selective pores are built from four
different structural ideas, occupy four unrelated folds, and share no
alignable position with one another. This section takes them in turn, because
everything the census does downstream — the positive tests, the hazard rules,
the refusal to build one tree — follows from the fact that they are separate
inventions.

![](figures/fig1_folds.png)

**Figure 1 | The folds that build a calcium-permeable pore.** One subunit
each, drawn to a common scheme, for the folds represented in this review's
catalogue. Transmembrane helices are boxes and pore-forming re-entrant loops
are marked; the drawing is schematic and carries no data beyond the topology
and the counts shown. The point of the figure is the absence of a common
ancestor: no two of these can be aligned to one another, and the calcium
selectivity of each was arrived at independently.

### 2.1 The EEEE ring: four repeats, four glutamates

The voltage-gated calcium channel is a single polypeptide of four homologous
repeats, each contributing one re-entrant P-loop to a single central pore.
Mutagenesis of the L-type channel identified one glutamate per repeat as the
determinant of calcium selectivity, and neutralising them degrades
selectivity in proportion to the number changed: the filter is a ring of four
carboxylates, and it acts as a unit [yang1993]. The complementary experiment
is the more striking one. Substituting the corresponding residues of a sodium
channel — whose own ring reads DEKA — converts it into a calcium-selective
channel [heinemann1992]. Four side chains separate the two largest families
of voltage-gated cation channels in the human genome.

Structures later showed why the ring can be both selective and fast. The
bacterial channel CavAb, engineered from a sodium-channel scaffold, and the
rabbit Cav1.1 complex both resolve multiple Ca²⁺ ions bound in file within
the filter [tang2014, wu2016, wu2015]. Selectivity comes from a
high-affinity site that monovalents cannot compete for; throughput comes from
a second ion arriving and repelling the first. Tight binding and fast
conduction are reconciled by never having only one ion present.

The same locus separates four families that domain architecture cannot tell
apart at all, and this review's project reads it as a four-residue string
projected from human Nav1.5:

| filter | family | note |
|---|---|---|
| EEEE | Cav1, Cav2 | the high-voltage-activated locus |
| EEDD | Cav3 | the T-type locus |
| DEKA | Nav | a sodium channel |
| EEKE | NALCN | a sodium-leak channel [lu2007] |

![](figures/fig3_four_repeat_filter.png)

**Figure 3 | Four residues separate two superfamilies.** The four-repeat
selectivity locus, projected from human Nav1.5 `Q14524` onto each query by
alignment and read directly — rendered from `filter_four_repeat.tsv`. The
high-voltage-activated calcium channels read EEEE, the T-type channels EEDD,
the sodium channels DEKA and NALCN EEKE. Two rows carry the caution rather
than the result: TPC1 returns a partial signature because it has two repeats
rather than four, and CatSper1 returns a partial signature because its four
positions lie in four different proteins. A partial result is recorded as
partial, not discarded.

Cav3's EEDD is the reason the census cannot use "EEEE" as its test: the
T-type channels are calcium channels with a different ring
[perezreyes2003, cribbs1998]. CatSper, the sperm channel, shares the same
architecture again and cannot be read this way at all, because its four
pore-forming subunits are four separate genes contributing one residue each
[ren2001, cai2012].

### 2.2 ORAI: one glutamate, and a pore that is not a P-loop

The store-operated calcium current is the most calcium-selective conductance
in the plasma membrane, with P_Ca/P_Na above 1000, and it is carried by a
protein with no relationship to any voltage-gated channel. ORAI1 has four
transmembrane helices, no P-loop, and assembles as a hexamer; its filter is a
single glutamate, E106, contributed once per subunit
[prakriya2006, yeromin2006, vig2006, feske2006]. The *Drosophila* Orai
structure showed the ring directly, at the extracellular mouth of a long
pore lined by basic residues [hou2012]. Mutating E106 to glutamine abolishes
calcium selectivity outright.

Structurally this is the same trick as the EEEE ring — a ring of
carboxylates at the narrowest point — implemented in a fold that has nothing
in common with the P-loop channels. It is the clearest single case of
convergence in the subject.

### 2.3 The uniporter: the shortest filter, the highest selectivity

Mitochondrial calcium uptake was measured as a current in 2004 and shown to
be the most calcium-selective channel then known, with an estimated
P_Ca/P_Na above 10⁴ [kirichok2004]. The protein responsible was not
identified for another seven years, by two groups in the same year, using
comparative genomics built on the observation that yeast takes up no
mitochondrial calcium and lacks the gene
[baughman2011, destefani2011, perocchi2010].

MCU's filter is a five-residue motif, W-D-x-x-E, known as DIME and sitting in
a short loop between two transmembrane helices. Cryo-EM structures of fungal
and metazoan uniporters resolve the two acidic rings it forms
[baradaran2018]. It is the only family in this review's catalogue that can be
called from a bare regular expression on an unannotated sequence, and it
achieves the highest selectivity of any of them with the smallest filter.

The uniporter also supplies the subject's cleanest boundary case. EMRE is
required for conduction in metazoans and lines none of the pore
[sancak2013]; MICU1 is an EF-hand gatekeeper that holds the channel shut at
resting calcium [perocchi2010]. Both are excluded from the census. MCUB, by
contrast, assembles into the tetramer, contributes pore lining, and *reduces*
conduction — and is counted, because the question the catalogue asks is
whether a gene contributes pore lining, not whether it increases current.

### 2.4 The TRPV aspartate ring, and an anchor that had moved

TRPV5 and TRPV6 are the epithelial calcium channels of intestinal and renal
reabsorption, with P_Ca/P_Na above 100 [peng1999, hoenderop1999,
hoenderop2005]. Their close relatives TRPV1–TRPV4 are non-selective cation
channels. The discriminator is a ring of one aspartate per subunit in the
outer pore, resolved in the TRPV6 structure [saotome2016].

This filter is the one that cannot be found by pattern, because the residue
sits in no conserved context; it has to be projected from a reference
sequence. Doing so exposed a trap worth recording, because it is the kind
that fails silently. The literature numbers the TRPV6 aspartate D542. The
canonical human UniProt entry `Q9H1D0` is the 765-residue long isoform and
carries the filter `TIIDGP` at positions 579–584, putting the aspartate at
**D582** — a 40-residue offset. An anchor taken from a paper's numbering
would have aligned correctly, projected the wrong column, and returned a
confident answer about the wrong residue. Every projection anchor in this
project is therefore verified against its own reference before use, and a
non-validating anchor refuses to project rather than guessing. All three
anchors were re-verified against live UniProt on 2026-08-20: Nav1.5
`Q14524` reads DEKA at 372/898/1419/1711, ORAI1 `Q96D31` reads E at 106, and
TRPV6 reads D at 582.

A caution belongs with this one. TRPV1–TRPV4 also carry acidic residues in
the outer pore, so a projected aspartate is supporting evidence rather than a
family call, and how far the anchor actually separates the two groups is a
measurement the classifier benchmark makes rather than an assumption
(*pending: S1*).

### 2.5 The negative test used positively

One motif does more work in a calcium census than any of the above: the
potassium filter, T-x-G-Y-G. A protein carrying it conducts K⁺, which settles
the Ca²⁺-*activated* potassium channels — BK, SK — without consulting a name,
a symbol or an annotation. In a subject where the most common error is
admitting something because it has "calcium" in its title, a reference-free
regular expression that says "this conducts potassium" is the most reliable
exclusion available.

![](figures/fig2_potassium_filter.png)

**Figure 2 | The exclusion that needs no reference.** The T-x-G-Y-G
potassium filter located directly in each sequence with flanking context —
no alignment was performed — rendered from `filter_k.tsv`. In a calcium
census this is a negative test used positively: a protein carrying it
conducts K⁺, which removes the Ca²⁺-activated potassium channels from the
count without consulting a name, a symbol or an annotation.

The limits are equally worth stating. TRPM4 and TRPM5 are Ca²⁺-activated and
conduct monovalent cations rather than K⁺, so no potassium filter identifies
them; they share every Pfam accession and the same length band with the
Ca²⁺-permeable TRPMs, and nothing in their sequence separates them. That
split is a literature call, recorded as one, and the classifier is not
expected to make it.
