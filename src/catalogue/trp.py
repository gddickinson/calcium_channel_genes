"""The TRP division — the largest and least tidy part of the calcium census.

TRP channels are P-loop channels by descent and belong to the `ploop`
superfamily, but they get their own file because they carry three problems
none of the other divisions has.

**Pfam does not cover the TRP pore uniformly.** Measured against InterPro by
the parent project on 2026-08-19: TRPV1, TRPV5, TRPA1 and TRPM2 carry
`PF00520`, while TRPC3, TRPM8, MCOLN1, MCOLN2 and PKD2 carry none of it —
their pores are modelled by `PF08344`, `PF18139` and `PF08016` instead. A
census that enumerates P-loop channels by `PF00520` loses most of the TRP
division silently (hazard **HC7**), which for a calcium census means losing
most of the non-selective calcium entry pathways at once.

**Calcium permeability varies within a family, sometimes drastically.**
TRPV5 and TRPV6 are Ca2+-selective with P_Ca/P_Na above 100; TRPV1-TRPV4,
their close relatives with the same architecture, are non-selective with
ratios near 1-10 (hazard **HC7b**). TRPM4 and TRPM5 sit inside the TRPM
family and are *impermeable* to Ca2+ while being *activated* by it, so they
are catalogued in `controls.py` as out of scope with the reason attached
(hazard **HC15**). The families here are therefore split by measured
permeability where the split is load-bearing, following decision **D24**:
membership and mechanism are separate calls, and so are membership and
permeability.

**The N-terminal architectures are not alignable across the division.**
Ankyrin repeats, TRPM homology regions and the polycystin domain differ so
much that a full-length alignment is dominated by insertions, so TRP trees
are built on the pore module even at tier 1.
"""

from __future__ import annotations

from .ploop import ION_TRANS
from .schema import CaClass as C
from .schema import ChannelFamily as CF
from .schema import Exemplar as Ex
from .schema import Fold
from .schema import Gating as G
from .schema import Level as L
from .schema import Permeability as Perm
from .schema import Provenance as P
from .schema import Selectivity as Sel
from .schema import Signature as Sig
from .schema import Status as St

PKD_CHANNEL = Sig("pfam", "PF08016", "PKD_channel", L.SHARED_WITH_DECOY, 1, P.DB,
                  "carried by TRPP, by TRPML *and* by polycystin-1, which is "
                  "not a pore (HC9)")

FAMILIES: list[CF] = [
    CF(
        key="trpv_ca",
        name="Ca2+-selective vanilloid channels (TRPV5, TRPV6)",
        superfamily="ploop", status=St.CHANNEL, fold=Fold.P_LOOP,
        selectivity=Sel.CA, gating=(G.CALCIUM, G.LIPID),
        permeability=Perm(C.SELECTIVE, ">100", "reversal potential", P.LIT,
                          "selectivity is set by a ring of four aspartates, "
                          "one per subunit, at the outer pore: D542 in human "
                          "TRPV6 and the equivalent D541 in TRPV5. Neutralise "
                          "it and the channel becomes non-selective"),
        tm_per_subunit=6, pore_loops_per_subunit=1,
        signatures=(ION_TRANS,
                    Sig("pfam", "PF00023", "Ank", L.ACCESSORY, 1, P.DB),
                    Sig("pfam", "PF12796", "Ank_2", L.ACCESSORY, 1, P.DB)),
        exemplars=(Ex("Hs_TRPV6", "TRPV6", "Homo sapiens", "",
                      "the intestinal Ca2+ uptake channel"),
                   Ex("Hs_TRPV5", "TRPV5", "Homo sapiens", "",
                      "the renal Ca2+ reabsorption channel")),
        human_genes=("TRPV5", "TRPV6"),
        length_band_aa=(700, 800), filter_motif="D542 (TRPV6 numbering)",
        compartment="plasma membrane -> cytosol",
        confusable_with=("trpv_ns", "HC7b"),
        provenance=P.LIT,
        notes=("Split from TRPV1-4 because the split is a hazard: the two "
               "groups share every Pfam accession, sit in the same length "
               "band and differ by roughly two orders of magnitude in "
               "P_Ca/P_Na. The discriminator is a single aspartate that no "
               "domain model records, so this is the TRP division's version "
               "of the Cav/Nav filter problem. TRPV6 is the rate-limiting "
               "step of dietary calcium absorption and is vitamin-D "
               "regulated; TRPV5 does the same job in the distal nephron."),
    ),
    CF(
        key="trpv_ns",
        name="Non-selective vanilloid channels (TRPV1-TRPV4)",
        superfamily="ploop", status=St.CHANNEL, fold=Fold.P_LOOP,
        selectivity=Sel.CATION_NONSELECTIVE,
        gating=(G.THERMAL, G.LIGAND_EXTRACELLULAR, G.PROTON, G.LIPID),
        permeability=Perm(C.PERMEABLE, "~1-10", "reversal potential; "
                          "fractional Ca2+ current", P.LIT,
                          "TRPV1's ratio is itself use-dependent — the pore "
                          "dilates during prolonged activation and the "
                          "permeability changes with it, so a single number "
                          "does not describe the channel"),
        tm_per_subunit=6, pore_loops_per_subunit=1,
        signatures=(ION_TRANS,
                    Sig("pfam", "PF00023", "Ank", L.ACCESSORY, 1, P.DB),
                    Sig("pfam", "PF12796", "Ank_2", L.ACCESSORY, 1, P.DB)),
        exemplars=(Ex("Hs_TRPV1", "TRPV1", "Homo sapiens", "Q8NER1",
                      "the capsaicin and noxious-heat receptor"),
                   Ex("Hs_TRPV4", "TRPV4", "Homo sapiens")),
        human_genes=("TRPV1", "TRPV2", "TRPV3", "TRPV4"),
        length_band_aa=(700, 900), filter_motif="[open]",
        compartment="plasma membrane -> cytosol",
        confusable_with=("trpv_ca", "HC7b"),
        provenance=P.LIT,
        notes=("In the census as `PERMEABLE`, not `SELECTIVE`: the calcium "
               "that enters through TRPV1 is what makes capsaicin desensitise "
               "the nociceptor, so the permeability is load-bearing "
               "physiologically even though the pore does not prefer Ca2+."),
    ),
    CF(
        key="trpc",
        name="TRPC - canonical transient receptor potential channels",
        superfamily="ploop", status=St.CHANNEL, fold=Fold.P_LOOP,
        selectivity=Sel.CATION_NONSELECTIVE,
        gating=(G.LIGAND_INTRACELLULAR, G.LIPID, G.STORE_DEPLETION),
        permeability=Perm(C.PERMEABLE, "~1-10 (varies by heteromer)",
                          "reversal potential", P.LIT,
                          "TRPC1 in particular behaves differently alone and "
                          "in TRPC1/TRPC4 or TRPC1/ORAI1 complexes, so the "
                          "ratio is a property of the assembly rather than of "
                          "the gene"),
        tm_per_subunit=6, pore_loops_per_subunit=1,
        signatures=(Sig("pfam", "PF08344", "TRP_2", L.FAMILY, 1, P.DB,
                        "TRPC's pore model; measured: TRPC3 carries NO "
                        "PF00520 at all"),
                    Sig("pfam", "PF23317", "YVC1_C", L.FAMILY, 1, P.DB),
                    Sig("pfam", "PF12796", "Ank_2", L.ACCESSORY, 1, P.DB)),
        exemplars=(Ex("Hs_TRPC3", "TRPC3", "Homo sapiens"),
                   Ex("Hs_TRPC6", "TRPC6", "Homo sapiens"),
                   Ex("Dm_trp", "trp", "Drosophila melanogaster", "P19334",
                      "the founding member of the whole TRP division, and a "
                      "Ca2+-selective channel: the fly's phototransduction "
                      "current is largely Ca2+")),
        human_genes=("TRPC1", "TRPC3", "TRPC4", "TRPC5", "TRPC6", "TRPC7"),
        other_genes=("TRPC2",),
        length_band_aa=(750, 1100), filter_motif="[open]",
        compartment="plasma membrane -> cytosol",
        confusable_with=("orai", "HC5b", "HC7"),
        provenance=P.LIT,
        notes=("The family that gave 'store-operated calcium entry' its first "
               "candidate and lost the title to ORAI — whether TRPC1 "
               "contributes to native SOCE is still argued, and the "
               "catalogue records the question rather than an answer. TRPC2 "
               "is a unitary pseudogene in human and a functional "
               "vomeronasal channel in mouse: a per-lineage presence call "
               "the census must make correctly."),
    ),
    CF(
        key="trpm_ca",
        name="Ca2+-permeable melastatin channels (TRPM1, 2, 3, 6, 7, 8)",
        superfamily="ploop", status=St.CHANNEL, fold=Fold.P_LOOP,
        selectivity=Sel.CATION_NONSELECTIVE,
        gating=(G.THERMAL, G.LIGAND_INTRACELLULAR, G.CALCIUM, G.LIPID),
        permeability=Perm(C.PERMEABLE, "~1-6; TRPM6/7 prefer Mg2+ and Zn2+",
                          "reversal potential; divalent permeability series",
                          P.LIT,
                          "TRPM6 and TRPM7 are the only channels in this "
                          "catalogue whose principal physiological divalent "
                          "is magnesium, and they are here because they carry "
                          "Ca2+ too - the permeability sequence is a "
                          "measurement, not a label"),
        tm_per_subunit=6, pore_loops_per_subunit=1,
        signatures=(Sig("pfam", "PF18139", "LSDAT_euk", L.FAMILY, 1, P.DB,
                        "the TRPM homology region; present across the family"),
                    Sig("pfam", "PF25508", "TRPM2", L.SUBFAMILY, 1, P.DB),
                    Sig("pfam", "PF16519", "TRPM_tetra", L.FAMILY, 1, P.DB),
                    Sig("pfam", "PF23317", "YVC1_C", L.FAMILY, 1, P.DB),
                    Sig("pfam", "PF00520", "Ion_trans", L.SUPERFAMILY, 1, P.DB,
                        "measured present on TRPM2, absent from TRPM8 - the "
                        "pore model does not cover the family uniformly")),
        exemplars=(Ex("Hs_TRPM8", "TRPM8", "Homo sapiens", "Q7Z2W7",
                      "the cold and menthol receptor"),
                   Ex("Hs_TRPM2", "TRPM2", "Homo sapiens", "",
                      "NUDT9 pyrophosphatase-fused; ADP-ribose gated"),
                   Ex("Hs_TRPM7", "TRPM7", "Homo sapiens", "",
                      "alpha-kinase-fused")),
        human_genes=("TRPM1", "TRPM2", "TRPM3", "TRPM6", "TRPM7", "TRPM8"),
        length_band_aa=(1100, 2100), filter_motif="[open]",
        compartment="plasma membrane -> cytosol",
        confusable_with=("outofscope_trpm_monovalent", "HC15"),
        provenance=P.LIT,
        notes=("TRPM2, TRPM6 and TRPM7 are chanzymes - a channel fused to an "
               "enzyme - so any classifier assuming one domain-of-interest "
               "per protein misfiles them. Their siblings TRPM4 and TRPM5 are "
               "in controls.py: same family by descent, Ca2+-activated and "
               "Ca2+-impermeable by measurement. Splitting one Pfam-identical "
               "family across the census boundary is the sharpest statement "
               "this catalogue makes about what a calcium channel is."),
    ),
    CF(
        key="trpa",
        name="TRPA1 - ankyrin transient receptor potential channel",
        superfamily="ploop", status=St.CHANNEL, fold=Fold.P_LOOP,
        selectivity=Sel.CATION_NONSELECTIVE,
        gating=(G.LIGAND_EXTRACELLULAR, G.THERMAL, G.MECHANICAL),
        permeability=Perm(C.PERMEABLE, "~5-8", "reversal potential", P.LIT,
                          "gated covalently: electrophiles such as allyl "
                          "isothiocyanate modify cysteines in the N-terminus, "
                          "so the ligand is consumed by the act of gating"),
        tm_per_subunit=6, pore_loops_per_subunit=1,
        signatures=(ION_TRANS,
                    Sig("pfam", "PF12796", "Ank_2", L.ACCESSORY, 4, P.DB),
                    Sig("pfam", "PF13637", "Ank_4", L.ACCESSORY, 1, P.DB)),
        exemplars=(Ex("Hs_TRPA1", "TRPA1", "Homo sapiens", "O75762"),),
        human_genes=("TRPA1",),
        length_band_aa=(1100, 1200), filter_motif="[open]",
        compartment="plasma membrane -> cytosol",
        provenance=P.LIT,
        notes=("~14-16 N-terminal ankyrin repeats, the longest in the "
               "catalogue. The wasabi and mustard-oil receptor, and a "
               "Ca2+ entry route in nociceptors that is itself potentiated "
               "by the Ca2+ it admits."),
    ),
    CF(
        key="trpml",
        name="TRPML - mucolipins",
        superfamily="ploop", status=St.CHANNEL, fold=Fold.P_LOOP,
        selectivity=Sel.CATION_NONSELECTIVE, gating=(G.LIPID, G.PROTON),
        permeability=Perm(C.RELEASE, "~1-30 (Ca2+ over Na+, lysosomal pH)",
                          "patch clamp of enlarged lysosomes", P.LIT,
                          "releases Ca2+ from the lysosome into the cytosol, "
                          "so its driving force and its selectivity are both "
                          "measured at pH 4.6 rather than 7.4"),
        tm_per_subunit=6, pore_loops_per_subunit=1,
        signatures=(PKD_CHANNEL,
                    Sig("pfam", "PF21381", "MCLN_ECD", L.FAMILY, 1, P.DB,
                        "the extracytosolic domain - what separates TRPML "
                        "from TRPP")),
        exemplars=(Ex("Hs_MCOLN1", "MCOLN1", "Homo sapiens", "Q9GZU1"),
                   Ex("Hs_MCOLN2", "MCOLN2", "Homo sapiens", "Q8IZK6")),
        human_genes=("MCOLN1", "MCOLN2", "MCOLN3"),
        length_band_aa=(550, 600), filter_motif="[open]",
        compartment="lysosome -> cytosol",
        confusable_with=("trpp", "assoc_polycystin1", "HC9"),
        provenance=P.LIT,
        notes=("PI(3,5)P2-gated. MCOLN1 loss causes mucolipidosis IV, and the "
               "lysosomal Ca2+ it releases drives fusion and autophagy - a "
               "reminder that the census's compartment field is not "
               "decoration: the same permeability means something different "
               "on an organelle than on the cell surface."),
    ),
    CF(
        key="trpp",
        name="TRPP / polycystin-2 channels (PKD2, PKD2L1, PKD2L2)",
        superfamily="ploop", status=St.CHANNEL, fold=Fold.P_LOOP,
        selectivity=Sel.CATION_NONSELECTIVE, gating=(G.MECHANICAL, G.CALCIUM),
        permeability=Perm(C.PERMEABLE, "~5 (PKD2L1); PKD2 contested",
                          "reversal potential in reconstituted and "
                          "primary-cilium recordings", P.LIT,
                          "PKD2's own conductance in the plasma membrane is "
                          "disputed; it is well established in the ER and in "
                          "the primary cilium, and the cilium recordings are "
                          "recent enough that the field has not settled"),
        tm_per_subunit=6, pore_loops_per_subunit=1,
        signatures=(PKD_CHANNEL,
                    Sig("pfam", "PF20519", "Polycystin_dom", L.SHARED_WITH_DECOY,
                        1, P.DB,
                        "also on PKD1 - the discriminator is PF21381's absence"),
                    Sig("pfam", "PF18109", "Fer4_24", L.SUBFAMILY, 1, P.DB)),
        exemplars=(Ex("Hs_PKD2", "PKD2", "Homo sapiens", "Q13563"),
                   Ex("Hs_PKD2L1", "PKD2L1", "Homo sapiens")),
        human_genes=("PKD2", "PKD2L1", "PKD2L2"),
        length_band_aa=(600, 900), filter_motif="[open]",
        compartment="primary cilium / ER -> cytosol",
        confusable_with=("trpml", "assoc_polycystin1", "HC9"),
        provenance=P.LIT,
        notes=("Assembles 3:1 with polycystin-1, an 11TM protein that "
               "contributes one pore-like segment and conducts nothing alone; "
               "PKD1 and its relatives are catalogued as channel-associated "
               "(HC9). PKD2 mutations cause autosomal dominant polycystic "
               "kidney disease, and whether the disease is a calcium-"
               "signalling failure is exactly the kind of claim this census "
               "is built to keep honest."),
    ),
]
