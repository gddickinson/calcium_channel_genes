"""Piezo - calcium entry driven by membrane tension.

Piezo1 and Piezo2 are non-selective cation channels, so they are in the
census as `PERMEABLE` rather than `SELECTIVE`; but they are the principal
mechanically gated calcium entry pathway in vertebrates, and in most of the
cell types where they matter - endothelium under shear, red cells, the
Merkel cell, the baroreceptor terminal - the calcium is the signal.

The architecture is unlike anything else here: a trimer of 38 transmembrane
helices per subunit arranged as a three-bladed propeller that curves the
membrane into a dome, with the pore on the axis. Force-from-lipid gating is
a mechanism rather than a clade, and the prokaryotic and plant
mechanosensitive channels share no residue with Piezo, so the superfamily
holds one family and the comparison to anything else is structural.

Piezo is also why the length band matters in this catalogue: at 2,521 aa
(PIEZO1, measured by the grandparent project `../piezo_genes`) it sits in the
same band as the IP3 receptors and well above every other plasma-membrane
channel, so a size filter designed for one family excludes the other.
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

PIEZO_CAP = Sig("pfam", "PF12166", "Piezo_cap", L.SUPERFAMILY, 1, P.DB,
                "the extracellular cap over the pore")

SUPERFAMILIES: list[SF] = [
    SF("piezo", "Piezo mechanosensitive channels", Fold.PIEZO, True,
       "full-length (only two paralogues)", (PIEZO_CAP,),
       notes=("No detectable relationship to MscL, MscS, the plant MCA "
              "proteins or TMEM63/OSCA - four independent solutions to "
              "turning tension into an open pore.")),
]

FAMILIES: list[CF] = [
    CF(
        key="piezo",
        name="Piezo mechanosensitive channels (PIEZO1, PIEZO2)",
        superfamily="piezo", status=St.CHANNEL, fold=Fold.PIEZO,
        selectivity=Sel.CATION_NONSELECTIVE, gating=(G.MECHANICAL,),
        permeability=Perm(C.PERMEABLE, "~1-6", "reversal potential; "
                          "Ca2+ imaging in the cell types where it is native",
                          P.LIT,
                          "modestly Ca2+-preferring and rapidly "
                          "inactivating, so the calcium signal it produces is "
                          "shaped as much by inactivation kinetics as by "
                          "permeability"),
        stoichiometry="trimer", tm_per_subunit=38,
        signatures=(PIEZO_CAP,
                    Sig("pfam", "PF15917", "Piezo_TM25-28", L.FAMILY, 1, P.DB),
                    Sig("pfam", "PF24871", "Piezo_TM1-24", L.FAMILY, 1, P.DB),
                    Sig("pfam", "PF23188", "THU_Piezo1", L.FAMILY, 1, P.DB),
                    Sig("pfam", "PF24874", "Piezo_THU9_anchor", L.FAMILY, 1,
                        P.DB)),
        exemplars=(Ex("Hs_PIEZO1", "PIEZO1", "Homo sapiens", "Q92508"),
                   Ex("Hs_PIEZO2", "PIEZO2", "Homo sapiens")),
        human_genes=("PIEZO1", "PIEZO2"),
        length_band_aa=(2500, 2850), filter_motif="[open]",
        compartment="plasma membrane -> cytosol",
        provenance=P.LIT,
        notes=("38 TM helices per subunit - the largest TM count of any known "
               "channel. PIEZO1 loss-of-function causes lymphatic dysplasia "
               "and gain-of-function causes hereditary xerocytosis; PIEZO2 "
               "carries touch and proprioception. The grandparent project of "
               "this codebase is a full census of exactly this family, so its "
               "results are the natural external check on ours - and, as "
               "everywhere else in this lineage, never an input."),
    ),
]
