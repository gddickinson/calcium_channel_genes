## 7. The TRP division: one superfamily, every answer

The TRP channels are where the difficulty of a calcium census is most
concentrated. They are a single superfamily by descent, they span the whole
range from Ca²⁺-selective to Ca²⁺-impermeable, and the boundary between those
states falls *inside* families rather than between them. The founding member
was found in a *Drosophila* phototransduction mutant, and the mammalian
division has grown to some 28 human genes across six families
[clapham2003, ramsey2006]. They are also, as a group, heavily represented in
inherited disease, across a range of organ systems that reflects how widely
the division is deployed rather than any shared mechanism [nilius2007]. Their permeabilities were surveyed early and the
survey's conclusion has held: TRP selectivity is a spectrum, and it is not
predictable from family membership [owsianik2006].

### 7.1 TRPV: a family split by one residue ring

TRPV1 is the capsaicin and heat receptor, the founding member of the
mammalian nociceptive TRPs and a non-selective cation channel
[caterina1997]. TRPV5 and TRPV6 are its close relatives and are
Ca²⁺-selective epithelial channels responsible for the apical step of
transcellular calcium reabsorption in kidney and intestine
[peng1999, hoenderop1999, hoenderop2005, saotome2016].

This review's catalogue therefore splits TRPV into two families on measured
permeability rather than on sequence similarity — a selective pair and a
non-selective remainder — and records that they carry the same Pfam
accessions and occupy the same length band. The split is honest and
uncomfortable: it is a division of a natural sequence group by a functional
measurement, and the only positive test available for it is the projected
aspartate ring of §2.4, whose discriminating power is itself something to be
measured rather than assumed.

### 7.2 TRPM: Ca²⁺-permeable and Ca²⁺-activated in the same family

TRPM is the same problem again, and worse. TRPM2, TRPM3, TRPM6 and TRPM7 are
Ca²⁺-permeable; TRPM4 and TRPM5 are Ca²⁺-*activated* channels that conduct
monovalent cations and no calcium at all
[launay2002, hofmann2003]. TRPM6 and TRPM7 in fact prefer Mg²⁺ and Zn²⁺ to
Ca²⁺, and carry a fused α-kinase domain — a channel with an enzyme bolted on,
which is exactly what a one-domain-of-interest assumption misfiles.

The census excludes TRPM4 and TRPM5 and counts the rest. There is no sequence
test that makes this call: the potassium filter does not fire on them, they
share every Pfam accession with their Ca²⁺-permeable relatives, and they sit
in the same length band. The exclusion is a literature call, is recorded as
one, and is precisely the kind of boundary that a census must be able to
state it cannot derive.

### 7.3 The rest of the division

TRPC is the closest to the *Drosophila* founder and is the family most
dependent on assembly: TRPC1 behaves differently alone than in TRPC1/TRPC4 or
TRPC1/ORAI1 complexes, so its permeability is a property of the complex
rather than of the gene. TRPA1 is a single human gene and a chemical irritant
sensor. TRPML (§4.3) and TRPP are intracellular. PKD2 is the contested case:
established in the ER and the primary cilium, disputed in the plasma
membrane, and counted with the dispute recorded.

### 7.4 What the annotation does to this division

The TRP channels are the clearest demonstration in this review that domain
annotation does not partition the subject the way the textbooks do. Measured
against InterPro:

- `PF00520` (Ion_trans), the canonical P-loop pore model, is carried by
  TRPV1, TRPV5, TRPA1 and TRPM2 — and **not** by TRPC3, TRPM8, MCOLN1,
  MCOLN2 or PKD2. Their pores are modelled by `PF08344`, `PF18139` and
  `PF08016` instead. A census that enumerates P-loop channels by `PF00520`
  loses most of the TRP division without reporting a gap.
- `PF16519` (TRPM_tetra), a tetramerisation domain *named for* TRPM, is
  annotated on TRPM7 and is absent from TRPM2, TRPM8, TRPM4 and TRPM5
  (measured 2026-08-20). It is carried by a minority of the family it is
  named after.
- `PF08016` (PKD_channel) is carried by TRPML, TRPP **and** polycystin-1 —
  which forms no pore on its own.

None of these is a database error. They are what a set of models built from
the best-studied members of each family looks like when it is asked about the
members nobody studied, and they are the reason the census behind this review
runs profile-HMM and genomic sweeps in addition to domain enumeration
(*pending: S2, S3, S5*).
