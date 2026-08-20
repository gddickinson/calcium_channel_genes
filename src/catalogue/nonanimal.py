"""Calcium channels outside the animals - plants, fungi, protists and viruses.

A census restricted to human genes cannot make an evolutionary claim, and
calcium signalling is one of the places where the non-animal channels are
not simply the animal ones with different names. Plants have no voltage-
gated calcium channel of the Cav type at all; their equivalents are the
glutamate-receptor-like GLR proteins and the cyclic-nucleotide-gated CNGC
family, both of them relatives of animal channels that do something else.
Fungi kept a Cav homologue (CCH1) and lost the mitochondrial uniporter.
And several viruses encode their own calcium channels, which is the
strongest possible statement about how useful a calcium signal is.

Four families here, plus the viral one:

* **GLR** - about 20 genes in *Arabidopsis*, structurally ionotropic
  glutamate receptors, and the channels that carry the long-distance calcium
  wave a wounded leaf sends to an undamaged one.
* **CNGC** - about 20 genes, Ca2+-permeable, central to immunity and pollen
  tube growth.
* **MCA** - MCA1/MCA2, mechanosensitive and Ca2+-permeable, with no
  relationship to Piezo, MscS or OSCA. A fifth independent solution.
* **OSCA / TMEM63** - hyperosmolality-gated, present in plants *and* in
  animals (TMEM63A-C in human), which makes it the one mechanosensitive
  family in this catalogue that spans both kingdoms.
* **Viral** - rotavirus NSP4 releases ER calcium and is the enterotoxin;
  coronavirus ORF3a and E and picornavirus 2B do related jobs. They are
  unrelated to each other, so the superfamily is marked non-alignable.
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

#: Verified against InterPro 2026-08-20. The catalogue originally declared
#: `PF02714` as `RSN1_TM` and `PF13967` as `RSN1_7TM`; S0 found the two
#: **swapped**. `PF02714` is `RSN1_7TM`, "Calcium-dependent channel, 7TM
#: region" - the OSCA/TMEM63 membrane domain, historically DUF221 - and
#: `PF13967` is `RSN1_TM`, "Late exocytosis, associated with Golgi
#: transport". Both are carried by the same proteins, which is why the
#: mistake was invisible until a live check made it.
OSCA_7TM = Sig("pfam", "PF02714", "RSN1_7TM", L.SUPERFAMILY, 1, P.DB,
               "the OSCA/TMEM63 membrane domain; InterPro calls it "
               "'Calcium-dependent channel, 7TM region'")

SUPERFAMILIES: list[SF] = [
    SF("mca", "Plant MCA mechanosensitive Ca2+ channels", Fold.UNKNOWN, True,
       "full-length",
       (Sig("pfam", "PF04749", "PLAC8", L.SUPERFAMILY, 1, P.DB),),
       notes=("Two genes in *Arabidopsis* and no structural relative "
              "anywhere else in this catalogue. Fold recorded as UNKNOWN "
              "rather than guessed.")),
    SF("osca", "OSCA / TMEM63 hyperosmolality-gated channels", Fold.TMEM16,
       True, "the RSN1_7TM membrane domain", (OSCA_7TM,),
       notes=("Structurally a TMEM16-like fold - the same architecture as the "
              "anoctamins, which are Ca2+-*activated* chloride channels. One "
              "fold, two opposite relationships to calcium, and a good "
              "reason not to infer function from fold.")),
    SF("viroporin_ca", "Viral calcium-mobilising channels", Fold.VIROPORIN,
       False, "none - the member proteins are unrelated to each other",
       (), (),
       notes="A functional grouping, marked non-alignable so it is never treed."),
]

FAMILIES: list[CF] = [
    CF(
        key="glr_plant",
        name="Plant glutamate receptor-like channels (GLR)",
        superfamily="iglur", status=St.CHANNEL, fold=Fold.IGLUR,
        selectivity=Sel.CATION_NONSELECTIVE,
        gating=(G.LIGAND_EXTRACELLULAR, G.MECHANICAL),
        permeability=Perm(C.PERMEABLE, "Ca2+-permeable; ratio not systematically "
                          "measured across the family",
                          "Ca2+ imaging with genetically encoded sensors; "
                          "electrophysiology on a few members", P.LIT,
                          "the *glr3.3 glr3.6* double mutant loses the "
                          "wound-induced long-distance Ca2+ wave, which is "
                          "genetic evidence for the pathway rather than a "
                          "permeability ratio - and the catalogue records "
                          "which kind of evidence it has"),
        stoichiometry="tetramer", tm_per_subunit=3, pore_loops_per_subunit=1,
        # Measured 2026-08-20 (S0): GLR3.3 and GLR3.4 carry PF10613 as well,
        # which was observed but not declared. Recording it makes HC17
        # concrete - the plant channels carry all three of the domains the
        # animal iGluRs carry, and nothing in the architecture separates
        # them.
        signatures=(Sig("pfam", "PF00060", "Lig_chan", L.SUPERFAMILY, 1, P.DB),
                    Sig("pfam", "PF10613", "Lig_chan-Glu_bd", L.SUPERFAMILY,
                        1, P.DB),
                    Sig("pfam", "PF01094", "ANF_receptor", L.SHARED_WITH_DECOY,
                        1, P.DB)),
        exemplars=(Ex("At_GLR3.3", "GLR3.3", "Arabidopsis thaliana", "Q9C8E7"),
                   Ex("At_GLR3.4", "GLR3.4", "Arabidopsis thaliana", "Q8GXJ4")),
        other_genes=("GLR1.1", "GLR2.1", "GLR3.1", "GLR3.3", "GLR3.4",
                     "GLR3.5", "GLR3.6", "GLR3.7"),
        length_band_aa=(600, 1000),
        compartment="plasma membrane / vacuole -> cytosol",
        confusable_with=("ampa", "kainate", "nmda", "HC17"),
        provenance=P.LIT,
        notes=("Plants have ionotropic glutamate receptors and no synapses. "
               "The GLRs carry systemic wound signalling: damage to one leaf "
               "produces a calcium wave that reaches an untouched leaf in "
               "roughly a minute and switches on jasmonate defences there. "
               "In the catalogue because an evolutionary claim about calcium "
               "entry cannot be made from vertebrates alone."),
    ),
    CF(
        key="cngc_plant",
        name="Plant cyclic-nucleotide-gated channels (CNGC)",
        superfamily="ploop", status=St.CHANNEL, fold=Fold.P_LOOP,
        selectivity=Sel.CATION_NONSELECTIVE,
        gating=(G.CYCLIC_NUCLEOTIDE, G.CALCIUM),
        permeability=Perm(C.PERMEABLE, "Ca2+-permeable; several members "
                          "characterised individually",
                          "electrophysiology in heterologous systems; "
                          "Ca2+ imaging in planta", P.LIT,
                          "calmodulin-inhibited, so the channel is switched "
                          "off by the calcium it lets in - the same negative "
                          "feedback the animal CNG channels use"),
        stoichiometry="tetramer", tm_per_subunit=6, pore_loops_per_subunit=1,
        signatures=(Sig("pfam", "PF00520", "Ion_trans", L.SUPERFAMILY, 1, P.DB),
                    Sig("pfam", "PF00027", "cNMP_binding", L.ACCESSORY, 1, P.DB,
                        "**measured 2026-08-20: At_CNGC4 carries PF00520 and "
                        "NO cNMP_binding at all.** A family named for "
                        "cyclic-nucleotide gating whose exemplar has no "
                        "annotated cyclic-nucleotide-binding domain - so the "
                        "signature is ACCESSORY, not diagnostic: the animal "
                        "CNG and HCN families carry it too, so a rule built "
                        "on it named HCN as a plant channel until "
                        "`s0_rule_coverage.py` caught it (D25, HC16)")),
        exemplars=(Ex("At_CNGC2", "CNGC2", "Arabidopsis thaliana", "O65718"),
                   Ex("At_CNGC4", "CNGC4", "Arabidopsis thaliana", "Q94AS9")),
        other_genes=("CNGC1", "CNGC2", "CNGC4", "CNGC6", "CNGC14", "CNGC18"),
        length_band_aa=(600, 800),
        compartment="plasma membrane -> cytosol",
        confusable_with=("cng",),
        provenance=P.LIT,
        notes=("Twenty genes in *Arabidopsis*, doing in plants what Cav does "
               "in animals: CNGC2 and CNGC4 carry the immune calcium burst, "
               "CNGC18 the pollen tube tip gradient. Plants have no Cav "
               "homologue, so this family and GLR are the answer to 'what "
               "does a plant use instead' - and the answer is two families "
               "that in animals do something else entirely."),
    ),
    CF(
        key="mca_plant",
        name="Plant mechanosensitive Ca2+ channels (MCA1, MCA2)",
        superfamily="mca", status=St.CHANNEL, fold=Fold.UNKNOWN,
        selectivity=Sel.CATION_NONSELECTIVE, gating=(G.MECHANICAL,),
        permeability=Perm(C.PERMEABLE, "Ca2+-permeable; not quantified",
                          "complementation of a yeast mid1 mutant; "
                          "Ca2+ imaging in planta", P.LIT,
                          "identified by rescuing a *yeast* calcium-uptake "
                          "mutant with a plant cDNA library - a functional "
                          "assay across a kingdom boundary, and a reminder "
                          "that this family would never be found by "
                          "homology search"),
        stoichiometry="unknown", tm_per_subunit=1,
        signatures=(Sig("pfam", "PF04749", "PLAC8", L.FAMILY, 1, P.DB),
                    Sig("pfam", "PF19584", "MCAfunc", L.FAMILY, 1, P.DB,
                        "measured 2026-08-20 on At_MCA1; the family has two "
                        "domains, and this is the one that is not shared "
                        "with the wider PLAC8 family")),
        exemplars=(Ex("At_MCA1", "MCA1", "Arabidopsis thaliana", "Q8L7E9"),
                   Ex("At_MCA2", "MCA2", "Arabidopsis thaliana", "Q3EBY6")),
        other_genes=("MCA1", "MCA2"),
        length_band_aa=(400, 450),
        compartment="plasma membrane -> cytosol",
        provenance=P.LIT,
        notes=("The fifth independent mechanosensitive solution in this "
               "catalogue after Piezo, MscS, OSCA and TRP - and the one with "
               "no structure, no fold assignment and a single Pfam domain "
               "shared with a large family of plant proteins. Catalogued with "
               "`Fold.UNKNOWN` and `Provenance.CURATED` throughout, which is "
               "what an honest record of a poorly characterised family looks "
               "like."),
    ),
    CF(
        key="osca_tmem63",
        name="OSCA / TMEM63 hyperosmolality-gated channels",
        superfamily="osca", status=St.CHANNEL_CONTESTED, fold=Fold.TMEM16,
        selectivity=Sel.CATION_NONSELECTIVE, gating=(G.MECHANICAL,),
        permeability=Perm(C.PERMEABLE, "Ca2+-permeable in the plant OSCA1; "
                          "less well established for mammalian TMEM63",
                          "patch clamp; Ca2+ imaging", P.LIT,
                          "OSCA1 was found in a screen for *reduced "
                          "hyperosmolality-induced calcium increase*, so its "
                          "calcium role is what defined the family. The "
                          "mammalian orthologues are established as "
                          "mechanosensitive and their divalent permeability "
                          "is less thoroughly measured, which is why this "
                          "record is contested rather than plain"),
        stoichiometry="dimer (OSCA) or monomer (TMEM63)", tm_per_subunit=11,
        signatures=(OSCA_7TM,
                    Sig("pfam", "PF13967", "RSN1_TM", L.FAMILY, 1, P.DB,
                        "InterPro: 'Late exocytosis, associated with Golgi "
                        "transport' - a name unrelated to the function, on "
                        "the same proteins as PF02714"),
                    Sig("pfam", "PF14703", "PHM7_cyt", L.FAMILY, 1, P.DB,
                        "measured 2026-08-20 on both At_OSCA1.1 and "
                        "Hs_TMEM63A; the family carries three domains, not "
                        "two")),
        exemplars=(Ex("At_OSCA1.1", "OSCA1.1", "Arabidopsis thaliana", "Q9XEA1",
                      "UniProt's primary name for it is OSCA1 with OSCA1.1 "
                      "as a synonym, so the symbol resolves only by synonym "
                      "and the accession is declared instead"),
                   Ex("Hs_TMEM63A", "TMEM63A", "Homo sapiens", "O94886")),
        human_genes=("TMEM63A", "TMEM63B", "TMEM63C"),
        other_genes=("OSCA1.1", "OSCA1.2", "OSCA3.1"),
        length_band_aa=(700, 900),
        compartment="plasma membrane -> cytosol",
        confusable_with=("outofscope_anoctamin",),
        provenance=P.LIT,
        notes=("The same fold as the anoctamins, which are Ca2+-activated "
               "chloride channels: one architecture on both sides of this "
               "catalogue's boundary. TMEM63B variants cause a "
               "developmental and epileptic encephalopathy. Included with "
               "contested status rather than left out, because leaving it "
               "out would make the mechanosensitive part of the census look "
               "tidier than the evidence is."),
    ),
    CF(
        key="viroporin_ca",
        name="Viral calcium-mobilising viroporins (NSP4, ORF3a, E, 2B)",
        superfamily="viroporin_ca", status=St.CHANNEL, fold=Fold.VIROPORIN,
        selectivity=Sel.CATION_NONSELECTIVE, gating=(G.UNKNOWN,),
        permeability=Perm(C.RELEASE, "Ca2+-permeable; not quantified as a ratio",
                          "Ca2+ imaging in infected and transfected cells; "
                          "bilayer recording for some members", P.LIT,
                          "rotavirus NSP4 raises cytosolic Ca2+ by releasing "
                          "it from the ER, and the elevated Ca2+ is required "
                          "for viral replication and for the diarrhoea - one "
                          "of the few places where a channel's permeability "
                          "is also a disease mechanism at whole-organism "
                          "scale"),
        stoichiometry="tetramer (NSP4) / pentamer (E)", tm_per_subunit=1,
        signatures=(Sig("pfam", "PF01452", "Rota_NSP4", L.SUBFAMILY, 1,
                        P.DB),
                    Sig("pfam", "PF02723", "CoV_E", L.SUBFAMILY, 1, P.DB),
                    Sig("pfam", "PF11289", "bCoV_viroporin", L.SUBFAMILY, 1,
                        P.DB)),
        exemplars=(Ex("RV_NSP4", "NSP4", "Rotavirus A", "P04512",
                      "the SA11 strain the viroporin literature works in; "
                      "UniProt files every NSP4 under a strain node and "
                      "gives none of them a gene name, so this one cannot "
                      "be reached by symbol and must be declared"),
                   Ex("SARS2_E", "E",
                      "Severe acute respiratory syndrome coronavirus 2", "P0DTC4"),
                   Ex("SARS2_ORF3a", "ORF3a",
                      "Severe acute respiratory syndrome coronavirus 2", "A0A679G5L0")),
        other_genes=("NSP4", "E", "ORF3a", "2B"),
        length_band_aa=(60, 280),
        compartment="endoplasmic reticulum -> cytosol",
        provenance=P.LIT,
        notes=("In the catalogue with subfamily signatures rather than one "
               "family signature, because these are a convergent functional "
               "class: NSP4, ORF3a and 2B are no more related to each other "
               "than any of them is to a human channel. That is exactly what "
               "`alignable=False` on the superfamily records, and any "
               "pipeline claiming to find 'all calcium channels' in a "
               "sequence database will meet them."),
    ),
]
