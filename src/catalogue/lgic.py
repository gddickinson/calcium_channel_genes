"""Ligand-gated channels that carry calcium - and the tier the genome cannot predict.

Three unrelated superfamilies, none of them a calcium channel by design and
all three of them major calcium entry routes: the pentameric Cys-loop
receptors, the tetrameric glutamate receptors, and the trimeric P2X
receptors. Their inclusion is the reason this catalogue has a `CONDITIONAL`
tier, because for most of them the answer to "does it conduct calcium" is
*it depends on the subunit composition*, and for one of them it depends on
something that is not in the genome at all.

**The AMPA receptor is the case that defines the problem.** GRIA2 is
transcribed with a glutamine codon at the Q/R site in the pore loop. ADAR2
edits that adenosine to inosine, the ribosome reads it as arginine, and an
arginine at that position makes the assembled channel Ca2+-**impermeable**.
Editing is essentially complete in adult brain, so almost every AMPA
receptor containing GRIA2 excludes calcium and every one lacking it admits
it. The gene sequence is identical either way. **No sequence-level method,
including every method in this project, can call the calcium permeability of
an AMPA receptor** - and a census that quietly assigned GRIA2 to either tier
would be asserting something it cannot know (hazard **HC8**). The catalogue
records the family as `CONDITIONAL` and the classifier emits no permeability
call.

The same shape recurs more mildly elsewhere: NMDA receptors are strongly
Ca2+-permeable but only assemble as GluN1 plus GluN2, so a single gene is
not a channel; nicotinic receptors range from a P_Ca/P_Na near 0.1 for
muscle-type to about 10 for the alpha7 homopentamer; P2X receptors span a
similar range across seven paralogues with one architecture.
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

NEUR_LBD = Sig("pfam", "PF02931", "Neur_chan_LBD", L.SUPERFAMILY, 1, P.DB,
               "the clamshell ligand-binding domain; a complete soluble "
               "protein in the molluscan acetylcholine-binding proteins")
NEUR_MEMB = Sig("pfam", "PF02932", "Neur_chan_memb", L.SUPERFAMILY, 1, P.DB,
                "the transmembrane region - the part that makes it a channel")
LIG_CHAN = Sig("pfam", "PF00060", "Lig_chan", L.SUPERFAMILY, 1, P.DB,
               "the iGluR pore region; the M2 re-entrant loop that carries "
               "the Q/R site sits inside it")
LIG_CHAN_GLU = Sig("pfam", "PF10613", "Lig_chan-Glu_bd", L.SUPERFAMILY, 1,
                   P.CURATED)
ANF_RECEPTOR = Sig("pfam", "PF01094", "ANF_receptor", L.SHARED_WITH_DECOY, 1,
                   P.DB,
                   "the ancestral periplasmic binding protein - also the "
                   "ligand-binding domain of every class C GPCR")
P2X_SIG = Sig("pfam", "PF00864", "P2X_receptor", L.SUPERFAMILY, 1, P.DB)

SUPERFAMILIES: list[SF] = [
    SF("cysloop", "Cys-loop (pentameric) ligand-gated ion channels",
       Fold.CYS_LOOP, True, "the LBD + TM region",
       (NEUR_LBD, NEUR_MEMB), ("nachr_ca",),
       notes=("Charge selectivity in this superfamily is set by a short ring "
              "at the M1-M2 boundary and flips between cation- and "
              "anion-selective with three substitutions, so nothing at the "
              "family level predicts it. The anion-selective members (GABA-A, "
              "glycine) are catalogued out of scope.")),
    SF("iglur", "Ionotropic glutamate receptors", Fold.IGLUR, True,
       "the pore region + M3 linker",
       (LIG_CHAN, LIG_CHAN_GLU, ANF_RECEPTOR), ("nmda",),
       notes=("An inverted potassium-channel pore under a two-lobed "
              "clamshell: the selectivity filter is upside-down relative to "
              "every P-loop channel, which is why the Q/R site sits where it "
              "does.")),
    SF("p2x", "P2X ATP-gated receptors", Fold.P2X, True, "full-length",
       (P2X_SIG,),
       notes="Trimeric, two TM helices per subunit, the 'dolphin' fold."),
]

FAMILIES: list[CF] = [
    CF(
        key="nachr_ca",
        name="Ca2+-permeable nicotinic receptors (alpha7, alpha9, alpha10)",
        superfamily="cysloop", status=St.CHANNEL, fold=Fold.CYS_LOOP,
        selectivity=Sel.CATION_NONSELECTIVE, gating=(G.LIGAND_EXTRACELLULAR,),
        permeability=Perm(C.PERMEABLE, "~10 (alpha7 homopentamer)",
                          "reversal potential; fractional Ca2+ current "
                          "(P_f ~ 10 % for alpha7)", P.LIT,
                          "the highest divalent permeability in the Cys-loop "
                          "superfamily, and the reason alpha7 signals rather "
                          "than merely depolarises. Muscle-type nicotinic "
                          "receptors, same fold and same two Pfam domains, "
                          "sit near P_Ca/P_Na 0.1"),
        stoichiometry="homopentamer (alpha7) or alpha9/alpha10 heteropentamer",
        tm_per_subunit=4,
        signatures=(NEUR_LBD, NEUR_MEMB),
        exemplars=(Ex("Hs_CHRNA7", "CHRNA7", "Homo sapiens"),
                   Ex("Hs_CHRNA9", "CHRNA9", "Homo sapiens")),
        human_genes=("CHRNA7", "CHRNA9", "CHRNA10"),
        length_band_aa=(430, 630),
        compartment="plasma membrane -> cytosol",
        iuphar_class="Nicotinic acetylcholine receptors",
        confusable_with=("outofscope_nachr_muscle", "HC16"),
        provenance=P.LIT,
        notes=("Split out of the nicotinic family by permeability, not by "
               "descent - the muscle and the other neuronal subunits are in "
               "controls.py as out of scope. The split is uncomfortable and "
               "recorded as such: alpha7 and alpha4 are sister subunits, and "
               "the census boundary runs between them. That is what it means "
               "for calcium to be a permeability rather than a clade."),
    ),
    CF(
        key="ampa",
        name="AMPA receptors (GRIA1-4)",
        superfamily="iglur", status=St.CHANNEL, fold=Fold.IGLUR,
        selectivity=Sel.CATION_NONSELECTIVE, gating=(G.LIGAND_EXTRACELLULAR,),
        permeability=Perm(C.CONDITIONAL,
                          "~1-3 without edited GluA2; ~0 with it",
                          "reversal potential; the difference is one "
                          "post-transcriptionally edited codon", P.LIT,
                          "ADAR2 edits the GRIA2 Q/R site from glutamine to "
                          "arginine in essentially all adult transcripts. The "
                          "genomic sequence encodes Q; the protein carries R. "
                          "No genome-based method can call this (HC8)"),
        stoichiometry="tetramer (dimer of dimers) + TARP / CNIH auxiliaries",
        tm_per_subunit=3, pore_loops_per_subunit=1,
        signatures=(LIG_CHAN, LIG_CHAN_GLU, ANF_RECEPTOR),
        exemplars=(Ex("Hs_GRIA1", "GRIA1", "Homo sapiens", "P42261"),
                   Ex("Hs_GRIA2", "GRIA2", "Homo sapiens", "",
                      "the edited subunit - the one that closes the pore to "
                      "calcium")),
        human_genes=("GRIA1", "GRIA2", "GRIA3", "GRIA4"),
        length_band_aa=(880, 910), filter_motif="Q/R site (GRIA2 Q607R, edited)",
        compartment="plasma membrane -> cytosol",
        confusable_with=("kainate", "nonchannel_casr_gpcr", "HC8"),
        provenance=P.LIT,
        notes=("Ca2+-permeable AMPA receptors carry synaptic plasticity, "
               "and their appearance after ischaemia or in ALS motor neurons "
               "is a proposed excitotoxic mechanism - so the tier this family "
               "sits in is not a technicality. ADAR2 knockout mice die of "
               "seizures, rescued completely by a GRIA2 allele with the "
               "edited codon written into the genome: the cleanest possible "
               "demonstration that the permeability is not in the DNA."),
    ),
    CF(
        key="kainate",
        name="Kainate receptors (GRIK1-5)",
        superfamily="iglur", status=St.CHANNEL, fold=Fold.IGLUR,
        selectivity=Sel.CATION_NONSELECTIVE, gating=(G.LIGAND_EXTRACELLULAR,),
        permeability=Perm(C.CONDITIONAL, "~0.2-2 depending on editing and subunit",
                          "reversal potential", P.LIT,
                          "GRIK1 and GRIK2 carry their own Q/R site and are "
                          "edited to varying and developmentally regulated "
                          "extents - unlike GRIA2, editing here is partial, "
                          "so the same transcript pool yields both "
                          "permeabilities at once"),
        stoichiometry="tetramer", tm_per_subunit=3, pore_loops_per_subunit=1,
        signatures=(LIG_CHAN, LIG_CHAN_GLU, ANF_RECEPTOR),
        exemplars=(Ex("Hs_GRIK1", "GRIK1", "Homo sapiens", "P39086"),
                   Ex("Hs_GRIK2", "GRIK2", "Homo sapiens")),
        human_genes=("GRIK1", "GRIK2", "GRIK3", "GRIK4", "GRIK5"),
        length_band_aa=(900, 980),
        compartment="plasma membrane -> cytosol",
        confusable_with=("ampa", "nonchannel_casr_gpcr", "HC8"),
        provenance=P.LIT,
    ),
    CF(
        key="nmda",
        name="NMDA receptors (GRIN1, GRIN2A-D, GRIN3A-B)",
        superfamily="iglur", status=St.CHANNEL, fold=Fold.IGLUR,
        selectivity=Sel.CATION_NONSELECTIVE,
        gating=(G.LIGAND_EXTRACELLULAR, G.VOLTAGE),
        permeability=Perm(C.SELECTIVE, "~10 (P_f ~ 12 %)",
                          "reversal potential; fractional Ca2+ current", P.LIT,
                          "an asparagine at the N site of the M2 loop - the "
                          "position equivalent to the AMPA Q/R site - sets "
                          "both the Ca2+ permeability and the Mg2+ block. "
                          "GluN3-containing receptors are much less "
                          "Ca2+-permeable, so the family spans tiers"),
        stoichiometry="obligate heterotetramer (2x GluN1 + 2x GluN2/GluN3)",
        tm_per_subunit=3, pore_loops_per_subunit=1,
        signatures=(LIG_CHAN, LIG_CHAN_GLU, ANF_RECEPTOR),
        exemplars=(Ex("Hs_GRIN1", "GRIN1", "Homo sapiens", "Q05586"),
                   Ex("Hs_GRIN2B", "GRIN2B", "Homo sapiens")),
        human_genes=("GRIN1", "GRIN2A", "GRIN2B", "GRIN2C", "GRIN2D",
                     "GRIN3A", "GRIN3B"),
        length_band_aa=(900, 1500), filter_motif="N site (GluN1 N598)",
        compartment="plasma membrane -> cytosol",
        confusable_with=("ampa", "nonchannel_casr_gpcr", "HC8"),
        provenance=P.LIT,
        notes=("The coincidence detector: glutamate binding opens it, "
               "depolarisation relieves the Mg2+ block, and only both "
               "together admit calcium. Listed as `SELECTIVE` on the "
               "P_Ca/P_Na ~ 10 criterion while being a non-selective cation "
               "channel by any structural description - a place where the "
               "tier boundary and the textbook label disagree, and the "
               "catalogue reports the number rather than the label. No "
               "single GRIN gene makes a channel, so the seven human genes "
               "are seven subunits and not seven channels; the census counts "
               "pore-forming genes and says so."),
    ),
    CF(
        key="p2x",
        name="P2X ATP-gated receptors (P2RX1-7)",
        superfamily="p2x", status=St.CHANNEL, fold=Fold.P2X,
        selectivity=Sel.CATION_NONSELECTIVE, gating=(G.LIGAND_EXTRACELLULAR,),
        permeability=Perm(C.PERMEABLE, "~0.5-4 (P2X1 and P2X4 highest)",
                          "reversal potential; fractional Ca2+ current", P.LIT,
                          "P2X7 additionally dilates under sustained "
                          "stimulation into a pore passing molecules up to "
                          "~900 Da, so its permeability is time-dependent and "
                          "no single ratio describes it"),
        stoichiometry="trimer", tm_per_subunit=2,
        signatures=(Sig("pfam", "PF00864", "P2X_receptor", L.FAMILY, 1, P.DB),),
        exemplars=(Ex("Hs_P2RX4", "P2RX4", "Homo sapiens"),
                   Ex("Hs_P2RX7", "P2RX7", "Homo sapiens", "Q99572")),
        human_genes=("P2RX1", "P2RX2", "P2RX3", "P2RX4", "P2RX5", "P2RX6",
                     "P2RX7"),
        length_band_aa=(380, 600),
        compartment="plasma membrane -> cytosol",
        provenance=P.LIT,
        notes=("The only extracellular-ATP-gated channels, and the cleanest "
               "single-family test of whether one Pfam accession plus one "
               "fold can predict a permeability: seven paralogues, one "
               "architecture, an order of magnitude of variation in "
               "P_Ca/P_Na. The answer is no, which is why the catalogue "
               "records permeability per family with its method attached."),
    ),
]
