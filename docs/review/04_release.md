## 4. Release from internal stores

Calcium entering from outside is only part of the signal, and often the
smaller part. The endoplasmic and sarcoplasmic reticulum hold free Ca²⁺ at
0.3–0.8 mM against a cytosol at 100 nM, and the channels that open onto that
gradient produce most of the calcium transients in most cells. They are
counted here in their own tier, with the compartment recorded, because the
same permeability ratio means something different on an organelle: what
matters is not how well IP₃R discriminates Ca²⁺ from K⁺ but the size of the
gradient it opens onto.

### 4.1 IP₃ receptors and ryanodine receptors

The two large release channels are the largest proteins in this review's
catalogue — RYR1 is 5,038 residues — and they are relatives. Both were cloned
in 1989: the ryanodine receptor from skeletal muscle
[takeshima1989] and the IP₃ receptor as the cerebellar P400 protein
[furuichi1989], with the similarity between them noticed immediately
[mignery1989]. Both are homotetramers with a small C-terminal pore module of
the P-loop kind and an enormous cytoplasmic cap that acts as a
signal-integration platform, resolved by cryo-EM in both families
[yan2015, desgeorges2016, fan2015].

Their physiology is organised by what opens them. IP₃ receptors are gated by
IP₃ produced downstream of phospholipase C, with cytosolic Ca²⁺ as a
co-agonist, giving the biphasic dependence that underlies calcium waves and
oscillations [berridge1993]. Ryanodine receptors are gated by calcium itself
— calcium-induced calcium release, demonstrated in skinned cardiac fibres
long before the protein was known [fabiato1983] — except in skeletal muscle,
where RyR1 is opened by direct mechanical coupling to Cav1.1 [rios1987,
lanner2010].

For a census, the pair are a domain-sharing hazard rather than a
discrimination problem: they share all four of `PF08709`, `PF01365`,
`PF08454` and `PF02815`, so architecture places a sequence in the pair
reliably and inside it not at all. One of those domains, the MIR domain
`PF02815`, is also carried by the O-mannosyltransferase POMT1, which is not a
channel — an illustration of why a domain hit is evidence about a superfamily
and not about a function.

### 4.2 Two-pore channels: counted, and contested

TPC1 and TPC2 sit in endosomal and lysosomal membranes and are structurally
the intermediate the four-repeat story predicts: two six-transmembrane
repeats rather than four, a plausible waypoint between a 6TM ancestor and the
duplicated Cav/Nav architecture.

Their permeability is genuinely disputed. They were identified as the NAADP
target releasing calcium from acidic stores [calcraft2009], and direct
endolysosomal patch clamp subsequently found a PI(3,5)P₂-activated,
Na⁺-selective current instead [wang2012]. This review counts them, in the
release tier, and records the dispute rather than resolving it by omission;
removing them costs the census two genes, and the catalogue is built so that
this is a one-line change and a recount.

### 4.3 TRPML and the lysosome

The mucolipins TRPML1–3 (`MCOLN1`–`MCOLN3`) are the lysosome's own release
channels, and TRPML1 loss causes mucolipidosis type IV. Their selectivity is
measured at lysosomal pH, near 4.6, which is part of why their reported
P_Ca/P_Na spans a wide range, and TRPML1 conducts Fe²⁺ as well
[dong2008, xu2015]. They belong to the TRP division by descent (§7) and are
placed in the release tier by compartment.

### 4.4 The regulators that are not channels

Around both large release channels sits a set of proteins that are required
for release and conduct nothing, and they are a good test of whether a gene
list is counting pores or counting participants. Calsequestrin is a luminal
calcium buffer whose occupancy sets how much RyR2 releases, and `CASQ2`
mutations cause catecholaminergic polymorphic ventricular tachycardia — the
same disease as `RYR2` mutations. FKBP12 and FKBP12.6 are immunophilins bound
to every RyR subunit. Triadin and junctin link the two.

The catalogue records these as channel-associated, and this project's own
architecture measurement found that they share no domain with one another:
`CASQ2` carries the calsequestrin domain alone, `FKBP1A` the FKBP domain
alone. A buffer and an immunophilin have in common only the channel they
regulate. TRIC channels (`TMEM38A`, `TMEM38B`) belong to the same category
from the other direction: they are potassium channels that provide the
counter-current for calcium release [yamazaki2011], and `TMEM38B` mutations
cause a calcium-release disease through a potassium channel.
