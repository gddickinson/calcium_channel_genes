"""Real subunits of real calcium-channel complexes that do not line a pore.

Every protein in this file is physically part of a working calcium channel
and is not one. They are catalogued because a census that counts them is
wrong by a large margin, and because *the gene symbols are the trap*: eight
`CACNG` genes, four `CACNB`, four `CACNA2D`, five `CATSPER`-prefixed
accessories and two `STIM` sort inside the calcium-channel symbol space, and
a search by symbol prefix counts sixteen calcium-channel genes in the Cav
complex where there are ten pores.

The `CACNG` set is the worst of them, and it is worse than a naming
collision. CACNG1 is a genuine skeletal-muscle Cav subunit; **CACNG2-CACNG8
are TARPs - auxiliary subunits of AMPA receptors** with a claudin fold and
no role in voltage-gated calcium channels at all. The symbol asserts a
complex membership that the protein does not have (hazard **HC2**).

The other recurring shape here is the gate that is not a pore. STIM1 is the
ER calcium sensor that opens ORAI across a membrane junction; EMRE is
required for the uniporter to conduct and contributes no pore lining;
calsequestrin sets the luminal calcium the ryanodine receptor releases.
Counting any of them would count one channel twice.
"""

from __future__ import annotations

from .schema import ChannelFamily as CF
from .schema import Exemplar as Ex
from .schema import Fold
from .schema import Level as L
from .schema import NOT_CALCIUM
from .schema import Provenance as P
from .schema import Selectivity as Sel
from .schema import Signature as Sig
from .schema import Status as St

_NONE: tuple = ()

FAMILIES: list[CF] = [
    CF(
        key="assoc_cav_aux",
        name="Cav auxiliary subunits (beta, alpha2delta, gamma/TARP)",
        superfamily="ploop", status=St.CHANNEL_ASSOCIATED, fold=Fold.UNKNOWN,
        selectivity=Sel.UNKNOWN, gating=_NONE, permeability=NOT_CALCIUM,
        stoichiometry="one beta + one alpha2delta per channel",
        # Measured 2026-08-20 (S0): no member carries all four. CACNB1 has
        # PF00625 + PF12052, CACNA2D1 has PF08473, CACNG2 has PF00822 alone.
        # This "family" is three unrelated protein types sharing a job, so
        # every signature in it is SUBFAMILY-level by construction (D25).
        signatures=(Sig("pfam", "PF00625", "Guanylate_kin", L.SUBFAMILY, 1, P.DB,
                        "beta only; CACNB is a MAGUK - a scaffold fold doing "
                        "a channel job"),
                    Sig("pfam", "PF12052", "VGCC_beta4Aa_N", L.SUBFAMILY, 1, P.DB,
                        "beta only"),
                    Sig("pfam", "PF08473", "VGCC_alpha2", L.SUBFAMILY, 1, P.DB,
                        "alpha2delta only"),
                    Sig("pfam", "PF00092", "VWA", L.SUBFAMILY, 1, P.DB,
                        "alpha2delta only; the von Willebrand A domain that "
                        "carries the gabapentin site"),
                    Sig("pfam", "PF00822", "PMP22_Claudin", L.SUBFAMILY, 1, P.DB,
                        "gamma/TARP only - the gamma subunits are claudins")),
        exemplars=(Ex("Hs_CACNB1", "CACNB1", "Homo sapiens", "Q02641"),
                   Ex("Hs_CACNA2D1", "CACNA2D1", "Homo sapiens", "P54289"),
                   Ex("Hs_CACNG2", "CACNG2", "Homo sapiens", "Q9Y698",
                      "stargazin - an AMPA-receptor subunit with a calcium-"
                      "channel symbol")),
        human_genes=("CACNB1", "CACNB2", "CACNB3", "CACNB4",
                     "CACNA2D1", "CACNA2D2", "CACNA2D3", "CACNA2D4",
                     "CACNG1", "CACNG2", "CACNG3", "CACNG4", "CACNG5",
                     "CACNG6", "CACNG7", "CACNG8"),
        confusable_with=("cav_hva", "ampa", "HC2"),
        provenance=P.DB,
        notes=("Sixteen genes whose symbols all begin CACN. The beta subunit "
               "is required for the pore to reach the membrane at all and "
               "shifts its voltage dependence by tens of millivolts; "
               "alpha2delta-1 (CACNA2D1) is the gabapentin and pregabalin "
               "target, so an auxiliary subunit is one of the most "
               "prescribed drug targets in the catalogue. None of them "
               "conducts calcium."),
    ),
    CF(
        key="assoc_catsper_aux",
        name="CatSper auxiliary subunits (CATSPERB/G/D/E/Z, EFCAB9, TMEM249)",
        superfamily="ploop", status=St.CHANNEL_ASSOCIATED, fold=Fold.UNKNOWN,
        selectivity=Sel.UNKNOWN, gating=_NONE, permeability=NOT_CALCIUM,
        signatures=(Sig("pfam", "PF15149", "CATSPERB_C", L.FAMILY, 1, P.DB),),
        exemplars=(Ex("Hs_CATSPERB", "CATSPERB", "Homo sapiens", "Q9H7T0"),),
        human_genes=("CATSPERB", "CATSPERG", "CATSPERD", "CATSPERE",
                     "CATSPERZ", "EFCAB9", "TMEM249"),
        confusable_with=("catsper", "HC10"),
        provenance=P.DB,
        notes=("Seven accessories to a four-subunit pore. Symbol-prefix "
               "matching returns eleven CatSper genes and one channel. "
               "EFCAB9 is an EF-hand protein that acts as the pH-tuned "
               "calcium sensor of the complex - a calcium-binding protein "
               "inside a calcium channel, and therefore a decoy for two "
               "hazards at once."),
    ),
    CF(
        key="assoc_stim",
        name="STIM proteins (STIM1, STIM2)",
        superfamily="orai", status=St.CHANNEL_ASSOCIATED, fold=Fold.UNKNOWN,
        selectivity=Sel.UNKNOWN, gating=_NONE, permeability=NOT_CALCIUM,
        tm_per_subunit=1,
        signatures=(Sig("pfam", "PF07647", "SAM_2", L.FAMILY, 1, P.DB),
                    Sig("pfam", "PF16533", "SOAR", L.FAMILY, 1, P.DB,
                        "the ORAI-activating region - Pfam models the gate"),
                    Sig("pfam", "PF13202", "EF-hand_5", L.ACCESSORY, 1, P.DB,
                        "the luminal EF-hand that senses store depletion")),
        exemplars=(Ex("Hs_STIM1", "STIM1", "Homo sapiens", "Q13586"),
                   Ex("Hs_STIM2", "STIM2", "Homo sapiens", "Q9P246")),
        human_genes=("STIM1", "STIM2"),
        confusable_with=("orai", "nonchannel_efhand", "HC5"),
        provenance=P.DB,
        notes=("The ER calcium sensor that gates ORAI across a ~15 nm "
               "junction. STIM1 loss causes the same immunodeficiency as "
               "ORAI1 loss, which is exactly why it gets counted: identical "
               "phenotype, identical pathway, and no pore. A gate is not a "
               "pore (HC5)."),
    ),
    CF(
        key="assoc_mcu_reg",
        name="Uniporter regulators (MICU1-3, EMRE/SMDT1, MCUR1)",
        superfamily="mcu", status=St.CHANNEL_ASSOCIATED, fold=Fold.UNKNOWN,
        selectivity=Sel.UNKNOWN, gating=_NONE, permeability=NOT_CALCIUM,
        # Measured 2026-08-20 (S0): MICU1 carries PF13833 and PF13202 and
        # no PF10161; SMDT1/EMRE carries PF10161 and nothing else. A
        # gatekeeper and a required subunit are not the same protein.
        signatures=(Sig("pfam", "PF13833", "EF-hand_8", L.SUBFAMILY, 1, P.DB,
                        "MICU1-3 only"),
                    Sig("pfam", "PF10161", "DDDD", L.SUBFAMILY, 1, P.DB,
                        "EMRE only; Pfam still calls it a putative "
                        "mitochondrial precursor protein")),
        exemplars=(Ex("Hs_MICU1", "MICU1", "Homo sapiens", "Q9BPX6"),
                   Ex("Hs_SMDT1", "SMDT1", "Homo sapiens", "Q9H4I9")),
        human_genes=("MICU1", "MICU2", "MICU3", "SMDT1", "MCUR1"),
        confusable_with=("mcu", "nonchannel_efhand", "HC6"),
        provenance=P.DB,
        notes=("EMRE is required for conduction in metazoans and lines no "
               "part of the pore; MICU1 is an EF-hand gatekeeper that keeps "
               "the uniporter shut at resting calcium. MCUB, by contrast, "
               "*is* a pore subunit and is in the census - so this family is "
               "the boundary case that makes 'pore-forming' and 'required "
               "for conduction' two separate questions (HC6)."),
    ),
    CF(
        key="assoc_release_reg",
        name="Ca2+-release channel regulators (calsequestrin, FKBP12/12.6, triadin, junctin)",
        superfamily="ca_release", status=St.CHANNEL_ASSOCIATED,
        fold=Fold.UNKNOWN, selectivity=Sel.UNKNOWN, gating=_NONE,
        permeability=NOT_CALCIUM,
        # Measured 2026-08-20 (S0): CASQ2 carries PF01216 alone and FKBP1A
        # PF00254 alone. A luminal buffer and an immunophilin share only the
        # channel they regulate.
        signatures=(Sig("pfam", "PF01216", "Calsequestrin", L.SUBFAMILY, 1, P.DB,
                        "CASQ1/CASQ2 only"),
                    Sig("pfam", "PF00254", "FKBP_C", L.SUBFAMILY, 1, P.DB,
                        "FKBP1A/FKBP1B only")),
        exemplars=(Ex("Hs_CASQ2", "CASQ2", "Homo sapiens", "O14958"),
                   Ex("Hs_FKBP1A", "FKBP1A", "Homo sapiens", "P62942",
                      "calstabin - the immunophilin bound to every RyR subunit")),
        human_genes=("CASQ1", "CASQ2", "FKBP1A", "FKBP1B", "TRDN", "ASPH"),
        confusable_with=("ryr", "itpr"),
        provenance=P.CURATED,
        notes=("Calsequestrin is a luminal calcium *buffer* whose occupancy "
               "sets how much the ryanodine receptor releases, and CASQ2 "
               "mutations cause CPVT - the same disease as RYR2 mutations. "
               "Identical phenotype through the store rather than through "
               "the pore, and a good illustration of why a "
               "channelopathy-driven gene list is not a channel census."),
    ),
    CF(
        key="assoc_polycystin1",
        name="Polycystin-1 family (PKD1, PKD1L1-3)",
        superfamily="ploop", status=St.CHANNEL_ASSOCIATED, fold=Fold.P_LOOP,
        selectivity=Sel.UNKNOWN, gating=_NONE, permeability=NOT_CALCIUM,
        stoichiometry="one per PKD2 trimer", tm_per_subunit=11,
        signatures=(Sig("pfam", "PF08016", "PKD_channel", L.SHARED_WITH_DECOY,
                        1, P.DB,
                        "measured on PKD1 - the same model as TRPP and TRPML"),
                    Sig("pfam", "PF20519", "Polycystin_dom", L.SHARED_WITH_DECOY,
                        1, P.DB),
                    Sig("pfam", "PF00801", "PKD", L.ACCESSORY, 15, P.DB)),
        exemplars=(Ex("Hs_PKD1", "PKD1", "Homo sapiens", "P98161"),),
        human_genes=("PKD1", "PKD1L1", "PKD1L2", "PKD1L3"),
        confusable_with=("trpp", "trpml", "HC9"),
        provenance=P.DB,
        notes=("4,303 aa with a 3,000-residue ectodomain and a channel-like "
               "C-terminus that contributes one subunit to a PKD2 trimer "
               "without conducting on its own. The commonest cause of "
               "autosomal dominant polycystic kidney disease. Whether the "
               "PKD1:PKD2 1:3 complex is one channel or a channel plus a "
               "receptor is unsettled, which is why this sits here with the "
               "argument written down rather than in the census."),
    ),
]
