"""Large-pore channels: CALHM, and the gap-junction proteins beside it.

CALHM1 is a voltage-gated, Ca2+-permeable channel whose *own* gating is
inhibited by extracellular calcium, so it opens when calcium falls - the
inverse of almost everything else in this catalogue. With CALHM3 it forms
the ATP-release channel of sweet, bitter and umami taste cells, which is a
calcium-permeable channel whose physiological output is a different
messenger entirely.

The superfamily is marked **`alignable=False`**, and that is the point of
the file. CALHM, the connexins, the innexin/pannexin clan and LRRC8 share a
fold class - four TM helices per subunit, large oligomers, wide pores - and
no alignable sequence positions between the groups. Putting them in one tree
would produce branch lengths measured on noise, so `build_tier2()` refuses
the comparison and the relationship goes to the fold network instead
(**D27**). The connexins themselves are catalogued here as contested:
undocked hemichannels do pass Ca2+, and whether that is a physiological
pathway or a pathological one is argued.
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

SUPERFAMILIES: list[SF] = [
    SF("largepore", "Large-pore channels (CALHM, connexin, pannexin, LRRC8)",
       Fold.CALHM, False,
       "none - one fold class, no alignable sequence positions between groups",
       (), (),
       notes=("Marked non-alignable so the phylogeny driver refuses to build "
              "a tree across it. Within-group trees (connexin to connexin) "
              "are tier-1 work and are fine; the between-group comparison is "
              "a structural one and belongs in the fold network.")),
]

FAMILIES: list[CF] = [
    CF(
        key="calhm",
        name="Calcium homeostasis modulators (CALHM1-CALHM6)",
        superfamily="largepore", status=St.CHANNEL_CONTESTED, fold=Fold.CALHM,
        selectivity=Sel.LARGE_PORE, gating=(G.VOLTAGE, G.CALCIUM),
        permeability=Perm(C.PERMEABLE, "Ca2+-permeable; ratio not well defined "
                          "for a wide pore",
                          "whole-cell recording and Ca2+ imaging in "
                          "heterologous expression", P.LIT,
                          "CALHM1 is *inhibited* by extracellular Ca2+ and "
                          "permeable to it - the channel opens when its own "
                          "permeant ion is scarce. Only CALHM1 and CALHM3 "
                          "have direct functional data; CALHM4-6 are curated "
                          "into the family by homology and are the reason "
                          "this record is CHANNEL_CONTESTED"),
        stoichiometry="octamer to undecamer", tm_per_subunit=4,
        signatures=(Sig("pfam", "PF14798", "Ca_hom_mod", L.FAMILY, 1, P.DB),),
        exemplars=(Ex("Hs_CALHM1", "CALHM1", "Homo sapiens", "Q8IU99"),
                   Ex("Hs_CALHM2", "CALHM2", "Homo sapiens", "Q9HA72")),
        human_genes=("CALHM1", "CALHM2", "CALHM3", "CALHM4", "CALHM5",
                     "CALHM6"),
        length_band_aa=(300, 400), filter_motif="none - a wide pore",
        compartment="plasma membrane -> cytosol",
        provenance=P.LIT,
        notes=("Named for calcium homeostasis before anyone showed it was a "
               "channel, which is the reverse of the usual naming hazard and "
               "just as misleading: the name asserts the function this "
               "catalogue is supposed to be testing. Oligomeric state varies "
               "by paralogue - CALHM2 is an undecamer - so stoichiometry is a "
               "per-protein property, not a family constant."),
    ),
]
