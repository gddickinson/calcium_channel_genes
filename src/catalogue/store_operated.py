"""Store-operated calcium entry: the ORAI channels.

ORAI1 is the most Ca2+-selective channel in the plasma membrane of any
animal cell, and it is gated by nothing that happens in that membrane. When
the ER empties, STIM1 - a single-pass ER protein with a luminal EF-hand -
loses its bound Ca2+, oligomerises, migrates to ER-plasma-membrane junctions
and grips ORAI's C-terminus across a ~15 nm gap. **The gate is in another
organelle**, which is why `Gating.STORE_DEPLETION` exists in this schema and
why STIM1 and STIM2 are catalogued as channel-associated rather than as
channels: they are the gate, not the pore, and counting them would count the
channel twice (hazard **HC5**).

The fold is its own: a hexamer with a single central pore, contributed by
one TM1 helix per subunit. Nothing else in this catalogue is built that way,
and there is no sequence-level relationship to the P-loop channels at all,
so `orai` is a superfamily with one family in it and the comparison to
everything else is a fold comparison (**D27**).
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

ORAI_SIG = Sig("pfam", "PF07856", "Orai-1", L.SUPERFAMILY, 1, P.DB)

SUPERFAMILIES: list[SF] = [
    SF("orai", "ORAI store-operated Ca2+ channels", Fold.ORAI, True,
       "full-length", (ORAI_SIG,),
       notes=("One family. Its relatives outside the animals are the "
              "*Drosophila* and *Dictyostelium* Orai proteins, which are in "
              "the family record rather than in families of their own.")),
]

FAMILIES: list[CF] = [
    CF(
        key="orai",
        name="ORAI / CRAC channels (ORAI1-3)",
        superfamily="orai", status=St.CHANNEL, fold=Fold.ORAI,
        selectivity=Sel.CA, gating=(G.STORE_DEPLETION,),
        permeability=Perm(C.SELECTIVE, ">1000", "reversal potential; the CRAC "
                          "current is essentially Ca2+-only under "
                          "physiological conditions", P.LIT,
                          "selectivity is set by a ring of six glutamates, "
                          "one per subunit: E106 in human ORAI1. E106Q "
                          "abolishes selectivity and E106D converts the "
                          "channel to a non-selective one, so the filter is a "
                          "single residue and its identity matters"),
        stoichiometry="hexamer, one central pore", tm_per_subunit=4,
        pore_loops_per_subunit=0,
        signatures=(Sig("pfam", "PF07856", "Orai-1", L.FAMILY, 1, P.DB),),
        exemplars=(Ex("Hs_ORAI1", "ORAI1", "Homo sapiens", "Q96D31"),
                   Ex("Hs_ORAI2", "ORAI2", "Homo sapiens", "Q96SN7"),
                   Ex("Dm_Orai", "Orai", "Drosophila melanogaster", "Q9U6B8")),
        human_genes=("ORAI1", "ORAI2", "ORAI3"),
        length_band_aa=(250, 310), filter_motif="E106 (ORAI1 numbering)",
        compartment="plasma membrane -> cytosol",
        confusable_with=("assoc_stim", "trpc", "HC5", "HC5b"),
        provenance=P.LIT,
        notes=("Found by two genome-wide RNAi screens in 2006, in "
               "*Drosophila* cells and in patients: ORAI1 R91W causes a "
               "severe combined immunodeficiency, and the T-cell defect is "
               "what made the current physiologically legible. Zero pore "
               "loops - the schema's `pore_loops_per_subunit` is 0 here and "
               "that is not a missing value. Note the naming trap in the "
               "other direction: ORAI's channel-forming role was for a "
               "decade attributed to TRPC1, and the TRPC/ORAI question is "
               "still live (HC5b)."),
    ),
]
