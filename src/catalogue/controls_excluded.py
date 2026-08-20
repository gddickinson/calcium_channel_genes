"""Everything the word *calcium* drags into a calcium-channel search.

Four kinds of record, and between them they outnumber the census.

`OUT_OF_SCOPE` - **genuine ion channels that are not calcium channels.**
Two groups. The first is the sodium and potassium channels of the P-loop
superfamily, which share the census families' fold, their Pfam accessions
and in the four-repeat case their entire architecture: Nav is the decoy
that makes the selectivity-filter test necessary. The second is the
Ca2+-*activated* channels - BK, SK, TMEM16A, TRPM4/5 - which are gated by
calcium and conduct potassium or chloride. They carry "calcium" in their
common names, in their Pfam entry names and in every review title, and a
keyword-driven census counts them (hazard **HC15**). The positive test is
the potassium filter: a TxGYG motif means the channel conducts K+, and a
channel that conducts K+ is not what this project counts.

`TRANSPORTER` - the pumps and exchangers that move calcium *against* its
gradient. SERCA, PMCA and SPCA hydrolyse ATP; NCX, NCKX and NCLX use the
sodium gradient; LETM1 uses protons. They are the other half of calcium
homeostasis and they are not channels, and the distinction is mechanistic
rather than architectural: they are catalogued so the boundary is a
decision (**D23**) rather than an omission.

`NON_CHANNEL_HOMOLOG` - proteins that carry a census family's diagnostic
domain, or its name, and have nothing to do with conduction. The
calcium-sensing receptor CASR is a G-protein-coupled receptor; calmodulin
binds calcium and conducts nothing; POMT1 carries the IP3R/RyR MIR domain.

`CHANNEL_ASSOCIATED` records live in `controls_associated.py`.
"""

from __future__ import annotations

from .schema import CaClass as C
from .schema import ChannelFamily as CF
from .schema import Exemplar as Ex
from .schema import Fold
from .schema import Gating as G
from .schema import Level as L
from .schema import NOT_CALCIUM
from .schema import Permeability as Perm
from .schema import Provenance as P
from .schema import Selectivity as Sel
from .schema import Signature as Sig
from .schema import Status as St
from .schema import Superfamily as SF

_NONE: tuple = ()

#: Ca2+-activated and does not conduct Ca2+ - the tier that exists so the
#: word "calcium" in a channel's name can be answered with a measurement.
_ACTIVATED = Perm(C.ACTIVATED, "0 - not measurably Ca2+-permeable",
                  "reversal potential", P.LIT,
                  "gated by cytosolic Ca2+; conducts something else")

SUPERFAMILIES: list[SF] = [
    SF("tmem16", "Anoctamins (TMEM16)", Fold.TMEM16, True, "full-length",
       (Sig("pfam", "PF04547", "Anoctamin", L.SUPERFAMILY, 1, P.DB),),
       notes=("The same fold as OSCA/TMEM63, which is in the census. One "
              "architecture, one side of the boundary each.")),
    SF("p_type_atpase", "P-type Ca2+-ATPases (SERCA, PMCA, SPCA)",
       Fold.P_TYPE_ATPASE, True, "the ATPase core",
       (Sig("pfam", "PF00122", "E1-E2_ATPase", L.SUPERFAMILY, 1, P.DB),)),
    SF("ca_exchanger", "Na+/Ca2+ exchangers (NCX, NCKX, NCLX)",
       Fold.CACA_EXCHANGER, True, "the alpha-repeat region",
       (Sig("pfam", "PF01699", "Na_Ca_ex", L.SUPERFAMILY, 1, P.DB),)),
    SF("ca_sensor", "EF-hand calcium sensors and buffers", Fold.EF_HAND, True,
       "the EF-hand pairs",
       (Sig("pfam", "PF13499", "EF-hand_7", L.SUPERFAMILY, 1, P.DB),),
       notes=("Not channels and not transporters: they bind calcium and pass "
              "the signal on. In the catalogue because 'calcium binding' and "
              "'calcium conducting' are one keyword apart (HC12).")),
]

FAMILIES: list[CF] = [
    # ------------------------------- P-loop channels that are not Ca channels
    CF(
        key="outofscope_nav",
        name="Voltage-gated sodium channels (Nav1.1-1.9, Nax)",
        superfamily="ploop", status=St.OUT_OF_SCOPE, fold=Fold.P_LOOP,
        selectivity=Sel.NA, gating=(G.VOLTAGE,),
        permeability=Perm(C.NOT_CALCIUM, "<0.1", "reversal potential", P.LIT,
                          "the DEKA filter excludes divalents; the lysine of "
                          "repeat III is the residue that does it"),
        stoichiometry="pseudo-tetramer (four repeats in one chain)",
        tm_per_subunit=24, pore_loops_per_subunit=4,
        signatures=(Sig("pfam", "PF00520", "Ion_trans", L.SUPERFAMILY, 4, P.DB),
                    Sig("pfam", "PF06512", "Na_trans_assoc", L.FAMILY, 1, P.DB,
                        "the one architectural feature that is Nav-specific"),
                    Sig("pfam", "PF11933", "Na_trans_cytopl", L.FAMILY, 1, P.DB)),
        exemplars=(Ex("Hs_SCN5A", "SCN5A", "Homo sapiens", "Q14524",
                      "the four-repeat filter anchor: D372/E898/K1419/A1711"),
                   Ex("Hs_SCN1A", "SCN1A", "Homo sapiens", "P35498")),
        human_genes=("SCN1A", "SCN2A", "SCN3A", "SCN4A", "SCN5A", "SCN7A",
                     "SCN8A", "SCN9A", "SCN10A", "SCN11A"),
        length_band_aa=(1600, 2100), filter_motif="DEKA",
        confusable_with=("cav_hva", "cav_lva", "HC1"),
        provenance=P.DB,
        notes=("**The most important record in this file.** Nav and Cav have "
               "the same fold, the same `PF00520`x4 architecture, overlapping "
               "length bands and a shared ancestor, and they differ by four "
               "residues. Human Nav1.5 is also the *reference* the "
               "four-repeat filter is projected from, so this family is "
               "simultaneously the census's principal decoy and its "
               "measuring instrument."),
    ),
    CF(
        key="outofscope_nalcn",
        name="NALCN sodium leak channel",
        superfamily="ploop", status=St.OUT_OF_SCOPE, fold=Fold.P_LOOP,
        selectivity=Sel.CATION_NONSELECTIVE, gating=(G.LEAK,),
        permeability=Perm(C.NOT_CALCIUM, "low; not a physiological Ca2+ route",
                          "reversal potential", P.LIT,
                          "the EEKE filter has three of Cav's four glutamates "
                          "and a Nav-like lysine in repeat III"),
        stoichiometry="pseudo-tetramer + FAM155/UNC79/UNC80",
        tm_per_subunit=24, pore_loops_per_subunit=4,
        signatures=(Sig("pfam", "PF00520", "Ion_trans", L.SUPERFAMILY, 4, P.DB),),
        exemplars=(Ex("Hs_NALCN", "NALCN", "Homo sapiens", "Q8IZF0"),),
        human_genes=("NALCN",),
        length_band_aa=(1600, 1800), filter_motif="EEKE",
        confusable_with=("cav_hva", "outofscope_nav", "HC1"),
        provenance=P.DB,
        notes=("One residue away from Cav's filter and not a calcium channel. "
               "The single strongest argument that the filter test has to "
               "read all four positions and not look for 'glutamates'."),
    ),
    CF(
        key="outofscope_hcn",
        name="Hyperpolarisation-activated cyclic-nucleotide-gated channels (HCN)",
        superfamily="ploop", status=St.OUT_OF_SCOPE, fold=Fold.P_LOOP,
        selectivity=Sel.CATION_NONSELECTIVE,
        gating=(G.VOLTAGE, G.CYCLIC_NUCLEOTIDE),
        permeability=Perm(C.NOT_CALCIUM, "~0.5 % of the current is Ca2+",
                          "fractional Ca2+ current", P.LIT,
                          "a Na+/K+ current with a CIGYG-like filter; its "
                          "sister family CNG is in the census"),
        tm_per_subunit=6, pore_loops_per_subunit=1,
        signatures=(Sig("pfam", "PF00520", "Ion_trans", L.SUPERFAMILY, 1, P.DB),
                    Sig("pfam", "PF00027", "cNMP_binding", L.FAMILY, 1, P.DB),
                    Sig("pfam", "PF08412", "Ion_trans_N", L.FAMILY, 1, P.DB)),
        exemplars=(Ex("Hs_HCN1", "HCN1", "Homo sapiens", "O60741"),),
        human_genes=("HCN1", "HCN2", "HCN3", "HCN4"),
        length_band_aa=(750, 1250), filter_motif="CIGYG",
        confusable_with=("cng", "HC16"),
        provenance=P.DB,
        notes=("The nearest relative of CNG, sharing the pore module and the "
               "cyclic-nucleotide-binding domain, and on the other side of "
               "the boundary. The CNG/HCN pair is this catalogue's cleanest "
               "demonstration that permeability is not inherited with "
               "architecture."),
    ),
    CF(
        key="outofscope_kca",
        name="Ca2+-activated potassium channels (BK, SK, IK)",
        superfamily="ploop", status=St.OUT_OF_SCOPE, fold=Fold.P_LOOP,
        selectivity=Sel.K, gating=(G.CALCIUM, G.VOLTAGE),
        permeability=_ACTIVATED,
        tm_per_subunit=6, pore_loops_per_subunit=1,
        signatures=(Sig("pfam", "PF00520", "Ion_trans", L.SUPERFAMILY, 1, P.DB),
                    Sig("pfam", "PF07885", "Ion_trans_2", L.SUPERFAMILY, 1, P.DB,
                        "measured on KCNN2 - the 2TM pore model on a 6TM "
                        "channel"),
                    Sig("pfam", "PF03493", "BK_channel_a", L.SUBFAMILY, 1, P.DB,
                        "BK only"),
                    Sig("pfam", "PF02254", "TrkA_N", L.SUBFAMILY, 2, P.DB,
                        "the RCK domains that bind Ca2+ - a Ca2+ sensor "
                        "inside a potassium channel. BK only"),
                    Sig("pfam", "PF03530", "SK_channel", L.SUBFAMILY, 1, P.DB,
                        "SK only"),
                    Sig("pfam", "PF02888", "CaMBD", L.SUBFAMILY, 1, P.DB,
                        "**measured 2026-08-20: KCNN2 carries PF07885, "
                        "PF03530 and PF02888 and NONE of BK's domains.** The "
                        "two halves of this family share no diagnostic "
                        "signature, so one architecture rule cannot reach "
                        "both - which is why HC15 needs two")),
        exemplars=(Ex("Hs_KCNMA1", "KCNMA1", "Homo sapiens", "Q12791", "BK"),
                   Ex("Hs_KCNN2", "KCNN2", "Homo sapiens", "Q9H2S1", "SK2")),
        human_genes=("KCNMA1", "KCNN1", "KCNN2", "KCNN3", "KCNN4", "KCNU1"),
        length_band_aa=(400, 1250), filter_motif="TxGYG",
        confusable_with=("cav_hva", "HC15"),
        provenance=P.DB,
        notes=("Called 'calcium-activated' everywhere including their IUPHAR "
               "class name, and they conduct potassium. BK is physically "
               "coupled to Cav in a nanodomain, so it is both a decoy and a "
               "genuine part of calcium signalling. The positive test is the "
               "TxGYG filter, which needs no reference sequence and is the "
               "one motif test in this project that works on a bare sequence "
               "from an unannotated genome (HC15)."),
    ),
    CF(
        key="outofscope_trpm_monovalent",
        name="Ca2+-activated monovalent TRP channels (TRPM4, TRPM5)",
        superfamily="ploop", status=St.OUT_OF_SCOPE, fold=Fold.P_LOOP,
        selectivity=Sel.MONOVALENT_CATION, gating=(G.CALCIUM, G.VOLTAGE),
        permeability=_ACTIVATED,
        tm_per_subunit=6, pore_loops_per_subunit=1,
        # PF16519 was declared here and is carried by *neither* TRPM4 nor
        # TRPM5 (measured 2026-08-20, S0) - InterPro annotates it on TRPM7
        # but not on the monovalent pair - so it is not a signature of this
        # family and has been removed rather than demoted.
        signatures=(Sig("pfam", "PF18139", "LSDAT_euk", L.FAMILY, 1, P.DB),
                    Sig("pfam", "PF25508", "TRPM2", L.FAMILY, 1, P.DB,
                        "the Pfam family is named for TRPM2 but is annotated "
                        "on TRPM4 and TRPM5 as well"),
                    Sig("pfam", "PF00520", "Ion_trans", L.SUPERFAMILY, 1, P.DB)),
        exemplars=(Ex("Hs_TRPM4", "TRPM4", "Homo sapiens", "Q8TD43"),
                   Ex("Hs_TRPM5", "TRPM5", "Homo sapiens", "Q9NZQ8")),
        human_genes=("TRPM4", "TRPM5"),
        length_band_aa=(1100, 1250), filter_motif="[open]",
        confusable_with=("trpm_ca", "HC15"),
        provenance=P.DB,
        notes=("The hardest exclusion in the catalogue: TRPM4 and TRPM5 are "
               "inside the TRPM family by descent, carry the same Pfam "
               "accessions as their Ca2+-permeable siblings, sit in the same "
               "length band - and are activated by cytosolic Ca2+ while "
               "excluding it. There is no architectural discriminator, so "
               "this split is `Provenance.LIT` and the classifier is not "
               "expected to make it from sequence. Recording that limit is "
               "the point (HC15)."),
    ),
    CF(
        key="outofscope_anoctamin",
        name="Ca2+-activated chloride channels (TMEM16A, TMEM16B)",
        superfamily="tmem16", status=St.OUT_OF_SCOPE, fold=Fold.TMEM16,
        selectivity=Sel.ANION, gating=(G.CALCIUM,),
        permeability=_ACTIVATED, stoichiometry="dimer", tm_per_subunit=10,
        signatures=(Sig("pfam", "PF04547", "Anoctamin", L.FAMILY, 1, P.DB),
                    Sig("pfam", "PF16178", "Anoct_dimer", L.FAMILY, 1, P.DB)),
        exemplars=(Ex("Hs_ANO1", "ANO1", "Homo sapiens", "Q5XXA6"),
                   Ex("Hs_ANO2", "ANO2", "Homo sapiens", "Q9NQ90")),
        human_genes=("ANO1", "ANO2"),
        confusable_with=("osca_tmem63", "HC15"),
        provenance=P.DB,
        notes=("Two Ca2+ ions bind directly within the membrane domain and "
               "open a chloride pore - the most direct calcium gating "
               "mechanism known, in a channel that conducts no calcium. Same "
               "fold as OSCA/TMEM63, which is in the census."),
    ),
    CF(
        key="outofscope_nachr_muscle",
        name="Low-Ca2+ nicotinic and anion-selective Cys-loop receptors",
        superfamily="cysloop", status=St.OUT_OF_SCOPE, fold=Fold.CYS_LOOP,
        selectivity=Sel.CATION_NONSELECTIVE,
        gating=(G.LIGAND_EXTRACELLULAR,),
        permeability=Perm(C.NOT_CALCIUM, "~0.1-1 (muscle-type); 0 for the "
                          "anion-selective members", "reversal potential",
                          P.LIT,
                          "below the census floor. The alpha7, alpha9 and "
                          "alpha10 subunits of the same superfamily reach "
                          "~10 and are in the census"),
        stoichiometry="pentamer", tm_per_subunit=4,
        signatures=(Sig("pfam", "PF02931", "Neur_chan_LBD", L.SUPERFAMILY, 1,
                        P.DB),
                    Sig("pfam", "PF02932", "Neur_chan_memb", L.SUPERFAMILY, 1,
                        P.DB)),
        exemplars=(Ex("Hs_CHRNA1", "CHRNA1", "Homo sapiens", "P02708"),
                   Ex("Hs_GABRA1", "GABRA1", "Homo sapiens", "P14867")),
        human_genes=("CHRNA1", "CHRNA2", "CHRNA3", "CHRNA4", "CHRNA5",
                     "CHRNA6", "CHRNB1", "CHRNB2", "CHRNB3", "CHRNB4",
                     "CHRND", "CHRNE", "CHRNG",
                     "GABRA1", "GABRB3", "GABRG2", "GLRA1", "GLRB",
                     "HTR3A"),
        confusable_with=("nachr_ca", "HC16"),
        provenance=P.CURATED,
        notes=("The census boundary runs *inside* the nicotinic receptors: "
               "alpha7 is in, alpha4 is out, and they are sister subunits "
               "with the same two Pfam domains. Recorded here as one control "
               "family rather than as a faithful reconstruction of the "
               "Cys-loop superfamily, which is the parent project's subject "
               "(`../ion_channel_genes`) and not this one's."),
    ),
    CF(
        key="outofscope_tric",
        name="Trimeric intracellular cation channels (TMEM38A/B)",
        superfamily="", status=St.OUT_OF_SCOPE, fold=Fold.TRIC,
        selectivity=Sel.K, gating=(G.VOLTAGE, G.CALCIUM),
        permeability=Perm(C.NOT_CALCIUM, "K+-selective", "bilayer recording",
                          P.LIT,
                          "the counter-ion channel that lets the SR release "
                          "calcium without building an opposing voltage"),
        stoichiometry="trimer", tm_per_subunit=7,
        signatures=(Sig("pfam", "PF05197", "TRIC", L.FAMILY, 1, P.DB),),
        exemplars=(Ex("Hs_TMEM38A", "TMEM38A", "Homo sapiens", "Q9H6F2"),),
        human_genes=("TMEM38A", "TMEM38B"),
        confusable_with=("ryr",),
        provenance=P.DB,
        notes=("A channel whose entire function is to make a calcium channel "
               "work, and which conducts potassium. TMEM38B mutations cause "
               "a recessive osteogenesis imperfecta - a calcium-release "
               "disease caused by a potassium channel."),
    ),
    CF(
        key="outofscope_connexin",
        name="Connexin and pannexin hemichannels",
        superfamily="largepore", status=St.OUT_OF_SCOPE, fold=Fold.CONNEXIN,
        selectivity=Sel.LARGE_PORE, gating=(G.VOLTAGE, G.CALCIUM, G.PROTON),
        permeability=Perm(C.NOT_CALCIUM,
                          "undocked hemichannels are Ca2+-permeable; the "
                          "docked junction is not a transmembrane Ca2+ route",
                          "dye flux and Ca2+ imaging", P.LIT,
                          "excluded on the ground that the physiological "
                          "state is the docked junction, which connects two "
                          "cytosols rather than crossing a gradient. The "
                          "dissent is real and is recorded here rather than "
                          "resolved by omission"),
        stoichiometry="hexamer (connexin) / heptamer (pannexin)",
        tm_per_subunit=4,
        # Connexins and pannexins are unrelated in sequence and converge on
        # a hemichannel: measured 2026-08-20 (S0), GJA1 carries PF00029 and
        # PANX1 carries PF00876, and neither carries the other.
        signatures=(Sig("pfam", "PF00029", "Connexin", L.SUBFAMILY, 1, P.DB,
                        "connexins only"),
                    Sig("pfam", "PF00876", "Innexin", L.SUBFAMILY, 1, P.DB,
                        "pannexins only - named for the invertebrate innexins "
                        "they descend from")),
        exemplars=(Ex("Hs_GJA1", "GJA1", "Homo sapiens", "P17302", "Cx43"),
                   Ex("Hs_PANX1", "PANX1", "Homo sapiens", "Q96RD7")),
        human_genes=("GJA1", "GJA3", "GJA4", "GJA5", "GJA8", "GJB1", "GJB2",
                     "GJB3", "GJB4", "GJB6", "GJC1", "GJC2", "GJD2",
                     "PANX1", "PANX2", "PANX3"),
        confusable_with=("calhm",),
        provenance=P.CURATED,
        notes=("Marked out of scope with the argument attached, and CALHM - "
               "the same fold class, the same superfamily record - is in the "
               "census. Any reader who disagrees can move one line and "
               "recount; that is what a declared boundary is for (D23)."),
    ),
    # --------------------------------------------------- pumps and exchangers
    CF(
        key="transporter_ca_atpase",
        name="P-type Ca2+-ATPases (SERCA, PMCA, SPCA)",
        superfamily="p_type_atpase", status=St.TRANSPORTER,
        fold=Fold.P_TYPE_ATPASE, selectivity=Sel.CA, gating=_NONE,
        permeability=NOT_CALCIUM, tm_per_subunit=10,
        # PF00702 was declared here and is carried by neither SERCA nor
        # PMCA. Pfam holds *two* families with the long name "haloacid
        # dehalogenase-like hydrolase" - PF00702 and PF08282 - and it is
        # PF08282 that InterPro annotates on the P-type Ca2+-ATPases
        # (measured 2026-08-20, S0). A hand-picked choice between two
        # identically named accessions is exactly what S0 exists to catch.
        signatures=(Sig("pfam", "PF00122", "E1-E2_ATPase", L.FAMILY, 1, P.DB),
                    Sig("pfam", "PF00689", "Cation_ATPase_C", L.FAMILY, 1, P.DB),
                    Sig("pfam", "PF00690", "Cation_ATPase_N", L.FAMILY, 1, P.DB),
                    Sig("pfam", "PF08282", "Hydrolase_3", L.FAMILY, 1, P.DB),
                    Sig("pfam", "PF13246", "Cation_ATPase", L.FAMILY, 1, P.DB)),
        exemplars=(Ex("Hs_ATP2A1", "ATP2A1", "Homo sapiens", "O14983", "SERCA1"),
                   Ex("Hs_ATP2B1", "ATP2B1", "Homo sapiens", "P20020", "PMCA1")),
        human_genes=("ATP2A1", "ATP2A2", "ATP2A3", "ATP2B1", "ATP2B2",
                     "ATP2B3", "ATP2B4", "ATP2C1", "ATP2C2"),
        length_band_aa=(900, 1250),
        confusable_with=("HC11",),
        provenance=P.DB,
        notes=("The other half of calcium homeostasis: every channel in the "
               "census is eventually reversed by one of these. SERCA is the "
               "best-characterised P-type pump in structural biology and the "
               "thapsigargin target; ATP2A1 mutations cause Brody myopathy "
               "and ATP2C1 causes Hailey-Hailey disease. Transporter by "
               "mechanism, calcium by substrate, and not a channel (D24)."),
    ),
    CF(
        key="transporter_ca_exchanger",
        name="Na+/Ca2+ exchangers (NCX, NCKX, NCLX) and LETM1",
        superfamily="ca_exchanger", status=St.TRANSPORTER,
        fold=Fold.CACA_EXCHANGER, selectivity=Sel.CA, gating=_NONE,
        permeability=NOT_CALCIUM, tm_per_subunit=10,
        # LETM1 is in this family by function and carries no Na_Ca_ex domain
        # (measured 2026-08-20, S0), so PF01699 is diagnostic for the NCX /
        # NCKX / NCLX part of it and not for the family.
        signatures=(Sig("pfam", "PF01699", "Na_Ca_ex", L.SUBFAMILY, 2, P.DB,
                        "NCX/NCKX/NCLX only, and in two copies - the "
                        "exchanger is an internally duplicated fold"),
                    Sig("pfam", "PF07766", "LETM1_RBD", L.SUBFAMILY, 1, P.DB,
                        "LETM1 only")),
        exemplars=(Ex("Hs_SLC8A1", "SLC8A1", "Homo sapiens", "P32418", "NCX1"),
                   Ex("Hs_SLC8B1", "SLC8B1", "Homo sapiens", "Q6J4K2", "NCLX"),
                   Ex("Hs_LETM1", "LETM1", "Homo sapiens", "O95202")),
        human_genes=("SLC8A1", "SLC8A2", "SLC8A3", "SLC8B1",
                     "SLC24A1", "SLC24A2", "SLC24A3", "SLC24A4", "SLC24A5",
                     "LETM1"),
        provenance=P.DB,
        notes=("Electrogenic, reversible and fast - NCX1 can run either way "
               "depending on membrane potential, so 'a calcium efflux "
               "pathway' is a statement about conditions rather than about "
               "the protein. NCLX (SLC8B1) is the mitochondrial exit route "
               "for the calcium MCU brings in, which makes this family the "
               "direct counterpart of a census member."),
    ),
    # ----------------------------------------------- non-channel homologues
    CF(
        key="nonchannel_efhand",
        name="EF-hand calcium sensors and buffers (calmodulin, calbindin, S100)",
        superfamily="ca_sensor", status=St.NON_CHANNEL_HOMOLOG, fold=Fold.EF_HAND,
        selectivity=Sel.UNKNOWN, gating=_NONE, permeability=NOT_CALCIUM,
        stoichiometry="monomer or dimer", tm_per_subunit=0,
        # Pfam splits the EF-hand across many families and InterPro assigns
        # whichever scores best, so the accessions are alternatives rather
        # than a set: measured 2026-08-20 (S0), calmodulin carries PF13499x2
        # and no PF00036, parvalbumin PF13499x1, calbindin both. PF13499 is
        # the one every member has.
        signatures=(Sig("pfam", "PF13499", "EF-hand_7", L.FAMILY, 1, P.DB),
                    Sig("pfam", "PF00036", "EF-hand_1", L.SUBFAMILY, 1, P.DB,
                        "an alternative EF-hand model, not a second domain")),
        exemplars=(Ex("Hs_CALM1", "CALM1", "Homo sapiens", "P0DP23"),
                   Ex("Hs_CALB1", "CALB1", "Homo sapiens", "P05937"),
                   Ex("Hs_PVALB", "PVALB", "Homo sapiens", "P20472")),
        human_genes=("CALM1", "CALM2", "CALM3", "CALB1", "CALB2", "PVALB",
                     "S100A1", "S100B", "CETN2", "CIB1"),
        confusable_with=("assoc_stim", "assoc_mcu_reg", "HC12"),
        provenance=P.DB,
        notes=("Roughly 250 human proteins carry an EF-hand and none of them "
               "is a channel. They are in the catalogue because a search for "
               "'calcium' in UniProt returns them in bulk, because calmodulin "
               "is bound to a large fraction of the census families as a "
               "regulator, and because CALM1-3 mutations cause "
               "arrhythmias that look exactly like RYR2 channelopathies "
               "(HC12). Ten representatives, not the full set - this is a "
               "decoy panel, not a census of the EF-hand superfamily."),
    ),
    CF(
        key="nonchannel_casr_gpcr",
        name="Class C GPCRs including the calcium-sensing receptor (CASR)",
        superfamily="iglur", status=St.NON_CHANNEL_HOMOLOG, fold=Fold.UNKNOWN,
        selectivity=Sel.UNKNOWN, gating=_NONE, permeability=NOT_CALCIUM,
        tm_per_subunit=7,
        signatures=(Sig("pfam", "PF01094", "ANF_receptor", L.SHARED_WITH_DECOY,
                        1, P.DB,
                        "measured on GRM1 - the same model as the iGluR "
                        "clamshell"),
                    Sig("pfam", "PF00003", "7tm_3", L.FAMILY, 1, P.DB)),
        exemplars=(Ex("Hs_CASR", "CASR", "Homo sapiens", "P41180"),
                   Ex("Hs_GRM1", "GRM1", "Homo sapiens", "Q13255")),
        human_genes=("CASR", "GPRC6A", "GRM1", "GRM2", "GRM3", "GRM4", "GRM5",
                     "GRM6", "GRM7", "GRM8", "GABBR1", "GABBR2",
                     "TAS1R1", "TAS1R3"),
        confusable_with=("nmda", "ampa", "HC12"),
        provenance=P.DB,
        notes=("CASR is *the* calcium-sensing receptor: it detects "
               "extracellular Ca2+, sets parathyroid hormone secretion, and "
               "its mutations cause familial hypocalciuric hypercalcaemia. It "
               "is a G-protein-coupled receptor and conducts nothing. Two "
               "decoys in one record - the calcium name, and the `PF01094` "
               "clamshell it shares with the ionotropic glutamate receptors "
               "in the census."),
    ),
    CF(
        key="nonchannel_pomt",
        name="Protein O-mannosyltransferases (POMT1, POMT2)",
        superfamily="ca_release", status=St.NON_CHANNEL_HOMOLOG,
        fold=Fold.UNKNOWN, selectivity=Sel.UNKNOWN, gating=_NONE,
        permeability=NOT_CALCIUM,
        signatures=(Sig("pfam", "PF02815", "MIR", L.SHARED_WITH_DECOY, 1, P.DB,
                        "measured on POMT1 - the same model as ITPR/RYR"),
                    Sig("pfam", "PF02366", "PMT", L.FAMILY, 1, P.DB)),
        exemplars=(Ex("Hs_POMT1", "POMT1", "Homo sapiens", "Q9Y6A1"),),
        human_genes=("POMT1", "POMT2"),
        confusable_with=("itpr", "ryr", "HC4"),
        provenance=P.DB,
        notes=("Glycosyltransferases of the ER membrane carrying the MIR "
               "domain. Inherited as a control from the grandparent project, "
               "where they were the MIR-sharing decoy in the S1 benchmark."),
    ),
]
