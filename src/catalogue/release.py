"""The intracellular Ca2+-release channels: IP3 receptors and ryanodine receptors.

These two families are the reason most cells can raise cytosolic calcium
without opening anything in the plasma membrane, and they are the largest
proteins in the catalogue by an order of magnitude: 2,700 aa for an IP3
receptor, 5,038 aa for RyR1. Almost all of that is a cytosolic solenoid that
receives regulatory input; the channel itself is a P-loop pore module of a
few hundred residues at the C-terminus, structurally a relative of the
potassium channels.

**ITPR and RYR are inherited work.** The grandparent project of this
codebase (`../ip3r_genes`) is a full census of the IP3 receptors, and it
established by measurement that the two families share all four of their
diagnostic Pfam domains (`PF08709`, `PF01365`, `PF08454`, `PF02815`), that
49 % of zebrafish `PF08709` records are ryanodine receptors, and that a
discovery scorer without a positive ITPR/RYR test promotes every RyR decoy.
That result is carried here as hazard **HC3** and as decision **D14**.

The superfamily is kept separate from `ploop` even though the pore module is
a P-loop pore, because a 5,000-residue release channel and a 400-residue
inward rectifier cannot be aligned full-length in any meaningful way. Tier 2
aligns the pore module and every output says so (**D27**).
"""

from __future__ import annotations

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
from .schema import Superfamily as SF

INS145 = Sig("pfam", "PF08709", "Ins145_P3_rec", L.SUPERFAMILY, 1, P.DB,
             "carried by ITPR *and* RYR - Pfam's name says 'IP3/ryanodine' (HC3)")
RIH = Sig("pfam", "PF01365", "RYDR_ITPR", L.SUPERFAMILY, 2, P.DB)
RIH_ASSOC = Sig("pfam", "PF08454", "RIH_assoc", L.SUPERFAMILY, 1, P.DB)
MIR = Sig("pfam", "PF02815", "MIR", L.SHARED_WITH_DECOY, 1, P.DB,
          "also carried by the protein O-mannosyltransferases POMT1/2 (HC4)")

SUPERFAMILIES: list[SF] = [
    SF("ca_release", "Intracellular Ca2+-release channels (ITPR, RYR)",
       Fold.P_LOOP, True, "the C-terminal pore module + RIH domains",
       (INS145, RIH, RIH_ASSOC, MIR), ("itpr",),
       notes=("The pore module is a P-loop channel, so this is a division "
              "*inside* the P-loop clan structurally. It is kept as its own "
              "superfamily because the 2,700-5,000 aa cytosolic solenoid "
              "makes full-length alignment to a 600 aa TRP channel "
              "meaningless.")),
]

FAMILIES: list[CF] = [
    CF(
        key="itpr",
        name="Inositol 1,4,5-trisphosphate receptors (ITPR1-3)",
        superfamily="ca_release", status=St.CHANNEL, fold=Fold.P_LOOP,
        selectivity=Sel.CA, gating=(G.LIGAND_INTRACELLULAR, G.CALCIUM),
        permeability=Perm(C.RELEASE, "~6 (Ca2+ over K+)",
                          "single-channel recording from reconstituted ER "
                          "membranes and nuclear patches", P.LIT,
                          "only modestly selective, and it does not need to "
                          "be: the ER lumen holds ~0.5 mM Ca2+ against ~100 nM "
                          "cytosolic, so the gradient does the work the "
                          "filter does elsewhere"),
        stoichiometry="tetramer", tm_per_subunit=6, pore_loops_per_subunit=1,
        signatures=(INS145, RIH, RIH_ASSOC, MIR,
                    Sig("pfam", "PF00520", "Ion_trans", L.SUPERFAMILY, 1, P.DB)),
        exemplars=(Ex("Hs_ITPR1", "ITPR1", "Homo sapiens", "Q14643"),
                   Ex("Hs_ITPR2", "ITPR2", "Homo sapiens", "Q14571"),
                   Ex("Hs_ITPR3", "ITPR3", "Homo sapiens", "Q14573")),
        human_genes=("ITPR1", "ITPR2", "ITPR3"),
        length_band_aa=(2000, 3600),
        compartment="endoplasmic reticulum -> cytosol",
        confusable_with=("ryr", "nonchannel_pomt", "HC3", "HC4"),
        provenance=P.DB,
        notes=("Measured lengths 2,758 / 2,701 / 2,671 aa. Gated by IP3 "
               "*and* by cytosolic Ca2+ - the biphasic dependence that makes "
               "calcium waves and oscillations possible, and the reason "
               "'ligand-gated' understates it. ITPR1 variants cause SCA15/"
               "SCA29 and Gillespie syndrome. Fully censused by the "
               "grandparent project, whose results are this project's "
               "external check on the release branch and never an input to "
               "it."),
    ),
    CF(
        key="ryr",
        name="Ryanodine receptors (RYR1-3)",
        superfamily="ca_release", status=St.CHANNEL, fold=Fold.P_LOOP,
        selectivity=Sel.CA,
        gating=(G.CALCIUM, G.MEMBRANE_APPOSITION, G.LIGAND_INTRACELLULAR),
        permeability=Perm(C.RELEASE, "~6-7 (Ca2+ over K+)",
                          "single-channel recording in planar bilayers", P.LIT,
                          "conductance is enormous - several hundred pS for "
                          "K+ - which is what a channel optimised for flux "
                          "rather than selectivity looks like"),
        stoichiometry="tetramer", tm_per_subunit=6, pore_loops_per_subunit=1,
        signatures=(INS145, RIH, RIH_ASSOC, MIR,
                    Sig("pfam", "PF02026", "RyR", L.FAMILY, 4, P.DB,
                        "the RyR repeat - the one domain ITPR does not carry"),
                    Sig("pfam", "PF06459", "RR_TM4-6", L.FAMILY, 1, P.DB),
                    Sig("pfam", "PF00622", "SPRY", L.ACCESSORY, 3, P.DB),
                    Sig("pfam", "PF00520", "Ion_trans", L.SUPERFAMILY, 1, P.DB)),
        exemplars=(Ex("Hs_RYR1", "RYR1", "Homo sapiens", "P21817"),
                   Ex("Hs_RYR2", "RYR2", "Homo sapiens", "Q92736"),
                   Ex("Hs_RYR3", "RYR3", "Homo sapiens", "Q15413")),
        human_genes=("RYR1", "RYR2", "RYR3"),
        length_band_aa=(4800, 5100),
        compartment="sarcoplasmic / endoplasmic reticulum -> cytosol",
        confusable_with=("itpr", "nonchannel_pomt", "HC3", "HC4"),
        provenance=P.DB,
        notes=("5,038 aa (measured) - the largest ion channel known and the "
               "largest single-chain protein in the catalogue. RYR1 in "
               "skeletal muscle is gated by a *mechanical* interaction with "
               "Cav1.1 rather than by the calcium Cav1.1 conducts, which is "
               "why `MEMBRANE_APPOSITION` exists as a gating mode: the two "
               "best-known calcium channels in physiology are coupled "
               "without calcium passing between them. RYR2 in heart is gated "
               "by Ca2+-induced Ca2+ release instead. RYR1 variants cause "
               "malignant hyperthermia and central core disease; RYR2 causes "
               "CPVT. `PF02026` is the positive discriminator against ITPR."),
    ),
]
