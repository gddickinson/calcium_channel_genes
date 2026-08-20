"""Calcium channels of the mitochondrion: the uniporter and the porins.

Mitochondria take up calcium through a pathway that was described
electrophysiologically in the 1960s and had no molecular identity until
2011. Fifty years is the longest gap between a current and its gene in this
catalogue, and it is a direct consequence of where the channel lives: the
organelle channels were found by physiology on isolated membranes rather
than by patch clamp on cells, so they entered the literature later, with
less standard nomenclature, and several still have contested identities.
A census built from plasma-membrane-shaped assumptions - a signal peptide,
an extracellular ligand-binding domain, a voltage sensor - finds fewer of
them than exist.

Two channels, in the two mitochondrial membranes:

**MCU** in the inner membrane is the most Ca2+-selective channel measured
anywhere. Its filter is the acidic **DIME motif** (the `WDxxE` ring), and it
needs a driving force of about -180 mV to work against a matrix that already
holds calcium. Its regulators - MICU1-3, EMRE/SMDT1, MCUR1 - are catalogued
as channel-associated. MCUB is not: it is a pore subunit that assembles into
the same tetramer and reduces conduction, which makes "pore-forming" and
"conducting" two different questions (hazard **HC6**).

**VDAC** in the outer membrane is the only all-beta channel here: a
19-stranded barrel, voltage-gated, and the route calcium takes to reach the
uniporter at all. Its role in the mitochondrial permeability transition is
argued and is recorded as an open question rather than as a function.
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

MCU_SIG = Sig("pfam", "PF04678", "MCU", L.SUPERFAMILY, 1, P.DB)
PORIN_3 = Sig("pfam", "PF01459", "Porin_3", L.SUPERFAMILY, 1, P.DB)

SUPERFAMILIES: list[SF] = [
    SF("mcu", "Mitochondrial calcium uniporter", Fold.MCU, True, "full-length",
       (MCU_SIG,),
       notes=("Present in most eukaryotes and lost in *Saccharomyces "
              "cerevisiae*, which is why baker's yeast has no mitochondrial "
              "calcium uptake and why the gene took so long to find: the "
              "standard genetic model organism does not have it.")),
    SF("porin", "Eukaryotic porins (VDAC)", Fold.BETA_BARREL, True,
       "full-length", (PORIN_3,),
       notes=("Bacterial outer-membrane porins share the architecture and are "
              "catalogued out of scope: an ungated diffusion pore is not what "
              "this project counts, and that criterion is what keeps VDAC - "
              "voltage-gated, eukaryotic, regulated - inside.")),
]

FAMILIES: list[CF] = [
    CF(
        key="mcu",
        name="Mitochondrial calcium uniporter (MCU, MCUB)",
        superfamily="mcu", status=St.CHANNEL, fold=Fold.MCU,
        selectivity=Sel.CA, gating=(G.CALCIUM,),
        permeability=Perm(C.SELECTIVE, ">10000", "mitoplast patch clamp", P.LIT,
                          "the most Ca2+-selective conductance ever measured; "
                          "the pore binds Ca2+ with nanomolar affinity in a "
                          "carboxylate ring and monovalent flux is only "
                          "detectable when divalents are removed entirely"),
        stoichiometry="tetramer + MICU / EMRE regulators", tm_per_subunit=2,
        pore_loops_per_subunit=0,
        signatures=(Sig("pfam", "PF04678", "MCU", L.FAMILY, 1, P.DB),),
        exemplars=(Ex("Hs_MCU", "MCU", "Homo sapiens", "Q8NE86"),
                   Ex("Hs_MCUB", "MCUB", "Homo sapiens", "Q9NWR8",
                      "a pore subunit that lowers conduction - not a regulator")),
        human_genes=("MCU", "MCUB"),
        length_band_aa=(330, 360), filter_motif="WDxxE (the DIME motif)",
        compartment="cytosol -> mitochondrial matrix",
        confusable_with=("assoc_mcu_reg", "HC6"),
        provenance=P.LIT,
        notes=("Two genes, one of the largest gaps in the catalogue between "
               "physiological description (1961) and molecular identity "
               "(2011), and the only family here whose selectivity filter is "
               "short enough to find with a regular expression - which is why "
               "`src/classify/motifs.py` carries `MCU_DXXE_RE` as a positive "
               "test that needs no reference sequence. MCU knockout mice are "
               "viable, which was not what anyone expected of the pathway "
               "that couples workload to oxidative phosphorylation."),
    ),
    CF(
        key="vdac",
        name="Voltage-dependent anion channels (VDAC1-3)",
        superfamily="porin", status=St.CHANNEL, fold=Fold.BETA_BARREL,
        selectivity=Sel.ANION, gating=(G.VOLTAGE,),
        permeability=Perm(C.PERMEABLE, "not applicable - a wide aqueous pore",
                          "bilayer recording; Ca2+ flux measured directly",
                          P.LIT,
                          "anion-selective in its open state and freely "
                          "permeable to Ca2+ in both states; it is the route "
                          "calcium takes across the outer membrane to reach "
                          "MCU, and VDAC overexpression raises matrix Ca2+"),
        stoichiometry="monomer (19-stranded beta-barrel)", tm_per_subunit=19,
        signatures=(Sig("pfam", "PF01459", "Porin_3", L.FAMILY, 1, P.DB),),
        exemplars=(Ex("Hs_VDAC1", "VDAC1", "Homo sapiens", "P21796"),
                   Ex("Hs_VDAC2", "VDAC2", "Homo sapiens", "P45880")),
        human_genes=("VDAC1", "VDAC2", "VDAC3"),
        length_band_aa=(275, 300),
        compartment="cytosol -> mitochondrial intermembrane space",
        provenance=P.LIT,
        notes=("In the census as `PERMEABLE`, and the entry most likely to be "
               "argued with: VDAC is not a calcium channel in the sense Cav "
               "is, and the mitochondrial calcium pathway does not work "
               "without it. Catalogued with the permeability recorded and the "
               "objection written down, which is what the tiered census is "
               "for. An odd strand number (19) means one parallel beta-pair, "
               "unlike every bacterial porin."),
    ),
]
