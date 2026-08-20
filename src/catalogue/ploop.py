"""The voltage-gated-like (P-loop) superfamily — its calcium-carrying branches.

This is the superfamily that gave the field the phrase "calcium channel",
and it is also where a calcium census runs out of domain architecture
fastest. `PF00520` (Ion_trans) in four copies within one chain describes the
calcium channels, the sodium channels, NALCN and the CatSper subunits
equally well: four homologous 6TM repeats built by two rounds of internal
duplication from a Kv-like ancestor. Pfam cannot tell them apart, InterPro's
family entries largely restate the gene names they were built from, and the
length bands overlap.

**The discrimination is the selectivity filter** — one residue contributed
by each of the four repeats:

    Cav1, Cav2    E / E / E / E      the high-voltage-activated locus
    Cav3          E / E / D / D      the T-type locus
    Nav           D / E / K / A      the DEKA locus  (not a calcium channel)
    NALCN         E / E / K / E      a Nav-like lysine in repeat III

Those four residues are the difference between a calcium channel and a
sodium channel with an identical domain architecture, and the whole census
turns on being able to read them. They cannot be found by a regular
expression — the surrounding sequence is not conserved enough — but they can
be *projected from a reference*: align the query to human Nav1.5 and read
whatever falls on its D372, E898, K1419 and A1711 (`src/classify/motifs.py`,
decision **D26**).

The superfamily is declared **by descent, not by ion**. `PLOOP_SUPERFAMILY`
therefore contains the sodium channels and the calcium-activated potassium
channels as well, catalogued in `controls.py` with `OUT_OF_SCOPE` status.
Keeping them here is what lets the tier-2 pore-module tree be rooted at all,
and it is what makes the decoys available to the benchmark.
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

#: The pore module of the whole superfamily. Never a family-level call.
ION_TRANS = Sig("pfam", "PF00520", "Ion_trans", L.SUPERFAMILY, 1, P.DB,
                "carried by Cav, Nav, NALCN, CatSper, TRP, CNG and HCN alike")
ION_TRANS_4 = Sig("pfam", "PF00520", "Ion_trans", L.SUPERFAMILY, 4, P.DB,
                  "four repeats in one chain: Cav, Nav, NALCN — identical (HC1)")

PLOOP_SUPERFAMILY = SF(
    "ploop", "Voltage-gated-like (P-loop) channel superfamily", Fold.P_LOOP,
    True, "the S5-P-S6 pore module",
    (ION_TRANS, Sig("pfam", "PF07885", "Ion_trans_2", L.SUPERFAMILY, 1, P.DB)),
    ("prok_ploop",),
    notes=("Declared by descent, not by ion. The sodium channels, NALCN and "
           "the Ca2+-activated potassium channels are members of this "
           "superfamily and are not calcium channels; they are catalogued in "
           "controls.py and are the benchmark's most informative decoys."),
)

SUPERFAMILIES: list[SF] = [PLOOP_SUPERFAMILY]

FAMILIES: list[CF] = [
    CF(
        key="cav_hva",
        name="High-voltage-activated calcium channels (Cav1, Cav2)",
        superfamily="ploop", status=St.CHANNEL, fold=Fold.P_LOOP,
        selectivity=Sel.CA, gating=(G.VOLTAGE, G.CALCIUM),
        permeability=Perm(C.SELECTIVE, ">1000", "reversal potential in "
                          "bi-ionic solutions", P.LIT,
                          "selectivity comes from ion-ion repulsion in a "
                          "single-file pore, not from a size filter: the "
                          "channel binds Ca2+ so tightly that micromolar Ca2+ "
                          "blocks the Na+ current through the same pore"),
        stoichiometry="pseudo-tetramer (four repeats in one chain) + beta + alpha2delta",
        tm_per_subunit=24, pore_loops_per_subunit=4,
        signatures=(ION_TRANS_4,
                    Sig("pfam", "PF08763", "Ca_chan_IQ", L.FAMILY, 1, P.DB,
                        "the calmodulin-binding IQ motif; measured present on "
                        "Cav1/Cav2 and ABSENT from CACNA1G (Cav3)"),
                    Sig("pfam", "PF16905", "GPHH", L.FAMILY, 1, P.DB),
                    Sig("pfam", "PF16885", "CAC1F_C", L.SUBFAMILY, 1, P.DB)),
        exemplars=(Ex("Hs_CACNA1C", "CACNA1C", "Homo sapiens", "Q13936",
                      "Cav1.2 — the L-type channel of heart and brain"),
                   Ex("Hs_CACNA1S", "CACNA1S", "Homo sapiens", "",
                      "Cav1.1 — the skeletal-muscle voltage sensor for RyR1"),
                   Ex("Hs_CACNA1A", "CACNA1A", "Homo sapiens", "", "Cav2.1, P/Q-type")),
        human_genes=("CACNA1A", "CACNA1B", "CACNA1C", "CACNA1D", "CACNA1E",
                     "CACNA1F", "CACNA1S"),
        length_band_aa=(1900, 2500), filter_motif="EEEE",
        compartment="plasma membrane -> cytosol",
        iuphar_class="Voltage-gated calcium channels",
        confusable_with=("outofscope_nav", "outofscope_nalcn", "cav_lva",
                         "assoc_cav_aux", "HC1", "HC2"),
        provenance=P.LIT,
        notes=("The prototype: the channel that couples depolarisation to "
               "secretion, contraction and transcription. Cav1.1 is the "
               "extreme case of a channel whose day job is not conduction — "
               "in skeletal muscle it works as RyR1's voltage sensor through "
               "a mechanical link, and the calcium it conducts is not needed "
               "for the contraction it triggers. CACNA1C variants cause "
               "Timothy syndrome; CACNA1A causes familial hemiplegic "
               "migraine and SCA6; CACNA1F causes X-linked congenital "
               "stationary night blindness."),
    ),
    CF(
        key="cav_lva",
        name="Low-voltage-activated (T-type) calcium channels (Cav3)",
        superfamily="ploop", status=St.CHANNEL, fold=Fold.P_LOOP,
        selectivity=Sel.CA, gating=(G.VOLTAGE,),
        permeability=Perm(C.SELECTIVE, "~10-100", "reversal potential", P.LIT,
                          "measurably less Ca2+-selective than Cav1/Cav2 and "
                          "with a smaller unitary conductance — consistent "
                          "with the EEDD filter rather than EEEE"),
        stoichiometry="pseudo-tetramer; no obligate auxiliary subunits",
        tm_per_subunit=24, pore_loops_per_subunit=4,
        signatures=(ION_TRANS_4,),
        exemplars=(Ex("Hs_CACNA1G", "CACNA1G", "Homo sapiens", "",
                      "Cav3.1 — measured to carry Ion_trans x4 and nothing else"),
                   Ex("Hs_CACNA1H", "CACNA1H", "Homo sapiens", "", "Cav3.2")),
        human_genes=("CACNA1G", "CACNA1H", "CACNA1I"),
        length_band_aa=(2100, 2500), filter_motif="EEDD",
        compartment="plasma membrane -> cytosol",
        iuphar_class="Voltage-gated calcium channels",
        confusable_with=("cav_hva", "outofscope_nav", "HC1", "HC14"),
        provenance=P.LIT,
        notes=("Split from Cav1/Cav2 as its own family rather than folded in "
               "as a subfamily, because the split is what two of this "
               "project's hazards are about. Cav3 carries **no** "
               "Cav-specific Pfam domain — architecture alone cannot tell it "
               "from a sodium channel (HC1) — and its filter reads EEDD, not "
               "EEEE, so a rule written to recognise 'the calcium filter' as "
               "four glutamates misses every T-type channel (HC14). T-type "
               "channels open near rest and drive thalamic burst firing; "
               "CACNA1H variants are found in childhood absence epilepsy."),
    ),
    CF(
        key="catsper",
        name="CatSper sperm-specific calcium channels",
        superfamily="ploop", status=St.CHANNEL, fold=Fold.P_LOOP,
        selectivity=Sel.CA, gating=(G.VOLTAGE, G.PROTON, G.LIGAND_EXTRACELLULAR),
        permeability=Perm(C.SELECTIVE, "high; not quantified per subunit",
                          "whole-cell recording from spermatozoa", P.LIT,
                          "the only Ca2+ channel measurable in mature human "
                          "sperm; gated by intracellular alkalinisation and, "
                          "in human, by progesterone"),
        stoichiometry="heterotetramer of four distinct 6TM subunits",
        tm_per_subunit=6, pore_loops_per_subunit=1,
        signatures=(ION_TRANS,),
        exemplars=(Ex("Hs_CATSPER1", "CATSPER1", "Homo sapiens"),
                   Ex("Hs_CATSPER2", "CATSPER2", "Homo sapiens")),
        human_genes=("CATSPER1", "CATSPER2", "CATSPER3", "CATSPER4"),
        length_band_aa=(400, 800), filter_motif="[open]",
        compartment="plasma membrane -> cytosol",
        confusable_with=("cav_hva", "assoc_catsper_aux", "HC1", "HC10"),
        provenance=P.LIT,
        notes=("The only heterotetramer in the superfamily assembled from "
               "four *different* genes, so its selectivity filter is built "
               "from four non-identical contributions and no single-sequence "
               "motif test can read it — recorded as `[open]` rather than "
               "guessed. Each subunit is 6TM, so a naive architecture rule "
               "files them with the potassium branch. The auxiliary subunits "
               "(CATSPERB/G/D/E/Z, EFCAB9, TMEM249) are in controls.py: nine "
               "more genes carrying the CATSPER symbol root and no pore."),
    ),
    CF(
        key="cng",
        name="Cyclic-nucleotide-gated channels (CNG)",
        superfamily="ploop", status=St.CHANNEL, fold=Fold.P_LOOP,
        selectivity=Sel.CATION_NONSELECTIVE,
        gating=(G.CYCLIC_NUCLEOTIDE,),
        permeability=Perm(C.PERMEABLE, "~3-10 (CNGA1, rod)",
                          "fractional Ca2+ current and reversal potential",
                          P.LIT,
                          "in the rod outer segment roughly 15 % of the dark "
                          "current is carried by Ca2+, and that fraction is "
                          "the signal that adapts the photoreceptor"),
        tm_per_subunit=6, pore_loops_per_subunit=1,
        signatures=(ION_TRANS,
                    Sig("pfam", "PF00027", "cNMP_binding", L.FAMILY, 1, P.DB),
                    Sig("pfam", "PF16526", "CLZ", L.FAMILY, 1, P.DB)),
        exemplars=(Ex("Hs_CNGA1", "CNGA1", "Homo sapiens", "P29973"),
                   Ex("Hs_CNGB1", "CNGB1", "Homo sapiens")),
        human_genes=("CNGA1", "CNGA2", "CNGA3", "CNGA4", "CNGB1", "CNGB3"),
        length_band_aa=(550, 1400), filter_motif="[open]",
        compartment="plasma membrane -> cytosol",
        confusable_with=("outofscope_hcn", "HC16"),
        provenance=P.LIT,
        notes=("A borderline census member and a deliberate one: CNG channels "
               "are not selective for Ca2+ and are nonetheless the calcium "
               "entry pathway of vision and olfaction. Their close relatives "
               "the HCN channels conduct almost no Ca2+ and are catalogued "
               "out of scope — same fold, same CNBD, opposite answer. The "
               "pair is the clearest illustration of why this catalogue "
               "records a permeability rather than inheriting one."),
    ),
    CF(
        key="tpc",
        name="Two-pore channels (TPC1, TPC2)",
        superfamily="ploop", status=St.CHANNEL_CONTESTED, fold=Fold.P_LOOP,
        selectivity=Sel.NA, gating=(G.VOLTAGE, G.LIGAND_INTRACELLULAR, G.LIPID),
        permeability=Perm(C.RELEASE, "contested: reported both as Na+-selective "
                          "and as a NAADP-gated Ca2+-release channel",
                          "patch clamp of enlarged endolysosomes vs Ca2+ imaging",
                          P.LIT,
                          "the direct-recording work finds a "
                          "PI(3,5)P2-activated, Na+-selective current; the "
                          "NAADP literature finds Ca2+ release. Both are "
                          "reproducible and the catalogue records the "
                          "disagreement rather than choosing (HC13)"),
        stoichiometry="dimer of two-repeat subunits",
        tm_per_subunit=12, pore_loops_per_subunit=2,
        signatures=(Sig("pfam", "PF00520", "Ion_trans", L.SUPERFAMILY, 2, P.DB,
                        "two repeats — not one and not four"),),
        exemplars=(Ex("Hs_TPCN1", "TPCN1", "Homo sapiens"),
                   Ex("Hs_TPCN2", "TPCN2", "Homo sapiens"),
                   Ex("At_TPC1", "TPC1", "Arabidopsis thaliana", "",
                      "the vacuolar SV channel — Ca2+-activated and "
                      "Ca2+-permeable, unlike its animal relatives")),
        human_genes=("TPCN1", "TPCN2"),
        length_band_aa=(750, 900), filter_motif="[open]",
        compartment="endolysosome -> cytosol",
        confusable_with=("cav_hva", "HC1", "HC13"),
        provenance=P.LIT,
        notes=("Named 'two-pore *calcium* channel' and possibly not a calcium "
               "channel — the single most instructive record in the "
               "catalogue. In the census as CHANNEL_CONTESTED with the "
               "argument attached, because a catalogue that resolves a live "
               "dispute by omission is not a catalogue. Also the "
               "evolutionary intermediate the 6TM -> 12TM -> 24TM story "
               "predicts, which is why its position in the tier-2 tree is a "
               "result the roadmap wants (S7/S8) rather than an assumption."),
    ),
]
