## 1. Why calcium, and why it is hard to count

### 1.1 An ion chosen for its scarcity

Calcium signalling begins with an accident of chemistry that life turned into
an advantage. Ringer found in 1883 that a frog heart would not keep beating
in saline made without calcium, and that restoring it restored contraction
[ringer1883]. Seventy years later Fatt and Katz recorded, in crustacean
muscle, an action potential that persisted when sodium was removed and that
was carried instead by calcium — the first evidence of a voltage-gated
calcium conductance [fatt1953]. The two observations bracket what makes the
ion useful: it is required, and it is separately controllable.

The reason is a gradient maintained at metabolic cost. Cytosolic free Ca²⁺
rests near 100 nM against roughly 2 mM outside and 0.3–0.8 mM in the
endoplasmic reticulum, a ratio of about ten thousand to one — steeper than
any other physiological ion gradient. A cell that opens a calcium-permeable
pore therefore gets a large, fast, local signal from a very small number of
ions, and one that can be terminated by buffering and pumping rather than by
bulk transport. Calcium is a second messenger because it is scarce, and the
machinery that keeps it scarce is what makes the message legible
[berridge2000, clapham2007, carafoli2002, bootman2020].

The techniques that made these currents legible were developed on other ions
and inherited. The Hodgkin–Huxley description of the squid axon established
that a membrane current could be decomposed into independent, voltage-
dependent conductances and modelled quantitatively before any channel protein
was known [hodgkin1952], and single-channel recording made the discrete
conducting unit directly visible [neher1976]. Both were applied to calcium
currents almost immediately, and the vocabulary of this review — selectivity
ratios, activation thresholds, single-channel conductance — is theirs.

That scarcity sets the engineering problem the rest of this review is about.
A calcium-selective pore must discriminate Ca²⁺ from Na⁺ and K⁺ that are
present at a hundred to a thousand times its concentration, and must do so
while conducting at rates approaching free diffusion. High selectivity
normally means tight binding, and tight binding normally means slow release.
The resolution — a pore that binds calcium tightly enough to exclude
monovalents but holds more than one ion at a time, so that electrostatic
repulsion between them restores a high throughput rate — was worked out for
the L-type channel and remains the general principle
[sather2003, yang1993]. Nearly every solution described below is a variation
on it.

### 1.2 A functional class, not a clade

The term "calcium channel" was never a phylogenetic claim. It describes
behaviour, and the behaviour has been arrived at many times. This review's
catalogue places the pore-forming calcium channels in **17 superfamilies**,
several of which share no alignable position with any other: the P-loop
channels, the TRP division, the intracellular release channels, ORAI, the
mitochondrial uniporter, VDAC, the Cys-loop receptors, the ionotropic
glutamate receptors, P2X, Piezo, the OSCA/TMEM63 mechanosensors, the CALHM
large pores and the viral viroporins, among others.

This has a consequence that organises the entire project behind this review:
**there is no tree of calcium channels.** An alignment column that contains a
residue of a ryanodine receptor and a residue of ORAI1 does not exist, and a
tree built across them would be a picture of an alignment artefact. What can
be built is a *forest* — trees within families and within superfamilies,
where descent is real — plus a structural network between the folds, which
carries no branch lengths and no support values because it is not a
phylogeny. Any sentence beginning "calcium channels evolved…" is therefore
either about one superfamily or is wrong.

Three long-standing observations make the same point from the other
direction, and each is a place where the obvious grouping misleads:

- **Cav and Nav are the same architecture.** Both are single polypeptides of
  four homologous six-transmembrane repeats surrounding one pore. They are
  separated by the four residues that each repeat contributes to the
  selectivity filter — EEEE in Cav1/Cav2 against DEKA in Nav — and a single
  substitution in the sodium channel confers calcium selectivity on it
  [heinemann1992].
- **Calcium permeability varies within families.** TRPV5 and TRPV6 are
  Ca²⁺-selective and their close relatives TRPV1–TRPV4 are not; the nicotinic
  α7 subunit reaches P_Ca/P_Na near 10 while its sister α4 is near 1
  [owsianik2006, fucile2004].
- **Calcium permeability is sometimes not encoded at all.** An AMPA receptor
  containing an edited GluA2 subunit is calcium-impermeable; the same gene,
  unedited, is not. The decision is made post-transcriptionally by ADAR2 on a
  single codon [sommer1991, higuchi2000].

### 1.3 A definition, and its five edges

Throughout this review a calcium channel is:

> a protein assembly forming a **gated aqueous pore** that conducts Ca²⁺
> across a membrane **down its electrochemical gradient**, without a coupled
> conformational transport cycle.

Each clause marks a boundary that published gene lists draw differently, and
each is worth stating because the disagreements account for most of the
variation between counts.

1. **Selectivity is not required, but it is graded.** Demanding
   P_Ca/P_Na > 10 would exclude most TRP channels, every Ca²⁺-permeable AMPA
   receptor, P2X, Piezo and CNG — that is, most of the calcium entry in most
   non-excitable cells. Admitting anything with a measurable Ca²⁺ current
   would admit the muscle nicotinic receptor and, in the limit, any large
   pore. This review therefore reports four tiers with the evidence for each
   attached, and never a single number.
2. **Gating *by* calcium is not membership.** BK and SK channels, TMEM16A and
   TRPM4/TRPM5 are opened by cytosolic Ca²⁺ and conduct K⁺, Cl⁻ or
   monovalent cations [launay2002, hofmann2003]. They carry "calcium" in
   their names and in most review titles, and they are the single most common
   contaminant of keyword-built lists.
3. **Transport is not conduction.** SERCA, PMCA and SPCA hydrolyse ATP; NCX,
   NCKX and NCLX are coupled to the sodium gradient
   [toyoshima2000, brini2009, blaustein1999]. They move more calcium per cell
   than most channels do, and they are excluded on mechanism, not importance.
4. **Auxiliary subunits are not pores.** The Cav β, α2δ and γ subunits, STIM1
   and EMRE are each required for a calcium channel to work and none of them
   lines a pore [dolphin2016]. They are the largest single source of
   inflation in published totals.
5. **Release from a store counts, and is recorded as such.** IP₃ receptors,
   ryanodine receptors, TRPML and the two-pore channels do not admit calcium
   to the cell; they move it from an internal store into the cytosol, which
   is often the larger signal [berridge1993, fabiato1983].

### 1.4 What follows

Sections 2–10 take the pores themselves: first the selectivity filters,
because they are what the census ultimately turns on, then the families
grouped by where their calcium comes from — the plasma membrane, the internal
stores, the mitochondrion — and by what opens them. Section 11 works through
the boundary explicitly, and is where the excluded set is argued rather than
assumed. Section 12 reports what the annotation databases record, measured
against live services rather than recalled. Sections 13–15 turn to evolution,
disease and what remains unresolved, and section 16 states the methods.
