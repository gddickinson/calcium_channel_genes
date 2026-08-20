"""The hazard registry - every recorded way to classify a calcium channel wrongly.

The grandparent project (`../ip3r_genes`) had exactly one of these. ITPR and
RYR share all four of their diagnostic Pfam domains, and when that project's
discovery scorer was first benchmarked it promoted **six out of six**
ryanodine-receptor decoys as candidate novel IP3 receptors. The fix - a
positive test on distances to a labelled sister-family bait - became its
decision D14 and is carried here as D14 too.

A calcium census has nineteen, and they come in two shapes.

**Architecture cannot resolve it.** Cav and Nav have the same fold, the same
`PF00520`x4 architecture and overlapping length bands (HC1). TRPV5 and TRPV1
share every Pfam accession and differ a hundredfold in P_Ca/P_Na (HC7b).
TRPM4 sits inside the TRPM family and excludes the ion its siblings conduct
(HC15). These are closed by positive tests on motifs and reference identity,
and where no such test exists the catalogue says so instead of guessing.

**The word *calcium* is the trap.** This is the shape a sodium or potassium
census does not have, and it is the larger half of this file. The
Ca2+-*activated* potassium and chloride channels are named for calcium and
conduct something else (HC15). The Ca2+-ATPases and Na+/Ca2+ exchangers move
calcium and are not channels (HC11). The calcium-sensing receptor is a GPCR
(HC12). Sixteen `CACN`-prefixed human genes encode auxiliary subunits, seven
of which are really AMPA-receptor subunits (HC2). Every one of these is
returned by a keyword search and by most annotation-driven pipelines.

Two rules govern this file.

1. **A hazard is only closed by a test, never by a caveat.** "Analysts
   should be careful of X" is not an entry; `discriminator` has to be
   something a script can run.
2. **The discriminator must be a positive test.** Never "it is not a Cav
   because its symbol says SCN5A" - always "the four filter residues read
   D/E/K/A, which is Nav's signature and not Cav's". Names are evidence
   about annotators, not about proteins, and an unnamed gene model in a new
   genome has none.

Severity is the cost of getting it wrong at census scale: `high` means the
hazard silently changes the headline count.
"""

from __future__ import annotations

from .schema import Hazard
from .schema import Provenance as P

HAZARDS: list[Hazard] = [
    Hazard(
        "HC1", "Cav, Nav, NALCN and CatSper share one domain architecture",
        ("cav_hva", "cav_lva", "outofscope_nav", "outofscope_nalcn", "catsper"),
        shared_evidence=("`PF00520`x4 in a single chain, 1,600-2,500 aa, the "
                         "same 24-TM pseudo-tetramer built by two rounds of "
                         "internal duplication. Measured by the parent "
                         "project: CACNA1G (Cav3) carries Ion_trans x4 and "
                         "nothing else - no Cav-specific domain at all."),
        discriminator=("Read the four selectivity-filter residues off the "
                       "pore-module alignment: EEEE = Cav1/Cav2, EEDD = Cav3, "
                       "DEKA = Nav, EEKE = NALCN. Confirm with a reference "
                       "identity margin >= 0.10 (D7). This is the test the "
                       "whole census turns on: it is what separates a calcium "
                       "channel from a sodium channel."),
        test_owner="src/classify/motifs.py:filter_signature()",
        severity="high", provenance=P.DB,
    ),
    Hazard(
        "HC2", "Sixteen human CACN* genes are auxiliary subunits, seven of them "
               "belonging to a different channel entirely",
        ("assoc_cav_aux", "cav_hva", "ampa"),
        shared_evidence=("`CACNB1-4`, `CACNA2D1-4` and `CACNG1-8` all sort "
                         "inside the calcium-channel symbol space. CACNG2-8 "
                         "are TARPs: claudin-fold auxiliary subunits of AMPA "
                         "receptors, with no role in voltage-gated calcium "
                         "channels."),
        discriminator=("Membership requires a pore model (`PF00520` or a "
                       "catalogued pore signature). `PF00625` (guanylate "
                       "kinase) => CACNB; `PF08473` => alpha2delta; "
                       "`PF00822` (claudin) => gamma/TARP. Symbols are never "
                       "consulted - measured cost of getting this wrong: "
                       "+16 human genes on the Cav count alone."),
        test_owner="src/classify/rules.py:HAZARD_RULES",
        severity="high", provenance=P.DB,
    ),
    Hazard(
        "HC3", "IP3 receptors and ryanodine receptors share every diagnostic domain",
        ("itpr", "ryr"),
        shared_evidence=("`PF08709`, `PF01365`, `PF08454`, `PF02815` are all "
                         "carried by both. The grandparent project measured "
                         "49 % of zebrafish `PF08709` records to be RyRs."),
        discriminator=("`PF02026` (the RyR repeat, x4) and `PF06459` are "
                       "present in RYR and absent from ITPR; confirm with the "
                       "labelled-bait identity margin (D14). Length (2.7 kaa "
                       "vs 5.0 kaa) supports the call and never makes it."),
        test_owner="src/classify/rules.py + src/discovery/candidates.py",
        severity="high", provenance=P.DB,
    ),
    Hazard(
        "HC4", "The MIR domain is shared with the O-mannosyltransferases",
        ("itpr", "ryr", "nonchannel_pomt"),
        shared_evidence="Measured: POMT1 carries `PF02815`, as ITPR and RYR do.",
        discriminator=("`PF02366` (PMT) present => mannosyltransferase. "
                       "Inherited from the grandparent project's S1 decoy "
                       "panel."),
        test_owner="src/classify/rules.py:HAZARD_RULES",
        severity="low", provenance=P.DB,
    ),
    Hazard(
        "HC5", "The gate is in another organelle: STIM is not ORAI",
        ("orai", "assoc_stim"),
        shared_evidence=("STIM1 and ORAI1 produce the same current, the same "
                         "immunodeficiency when lost, and the same hits in a "
                         "search for 'store-operated calcium channel'. STIM1 "
                         "carries an EF-hand and a single TM helix."),
        discriminator=("`PF07856` (Orai-1) => pore. `PF16533` (SOAR) or "
                       "`PF07647` (SAM_2) without a pore model => STIM. A "
                       "protein required for a current is not thereby a "
                       "channel."),
        test_owner="src/classify/rules.py:HAZARD_RULES",
        severity="medium", provenance=P.DB,
    ),
    Hazard(
        "HC5b", "Store-operated entry is a mechanism, not a family",
        ("orai", "trpc"),
        shared_evidence=("TRPC1 was the candidate SOCE channel for a decade "
                         "before ORAI1 was found, and TRPC1/ORAI1 complexes "
                         "are still argued to carry part of the native "
                         "current. Both families answer to the same "
                         "physiological description."),
        discriminator=("Membership is by pore evidence and family signature "
                       "(`PF07856` vs `PF08344`), never by the mechanism a "
                       "paper attributes to the protein. The mechanism is "
                       "recorded as a separate literature-derived field "
                       "(D24), and where the literature disagrees the "
                       "catalogue records the disagreement."),
        test_owner="src/catalogue (Permeability.note) - no sequence test",
        severity="low", provenance=P.LIT,
    ),
    Hazard(
        "HC6", "A uniporter subunit can be a pore and still not conduct",
        ("mcu", "assoc_mcu_reg"),
        shared_evidence=("MCU, MCUB, MICU1-3, EMRE and MCUR1 are all "
                         "'the uniporter' in the literature. MCUB assembles "
                         "into the same tetramer as MCU and lowers its "
                         "conductance; EMRE is required for conduction and "
                         "lines no part of the pore."),
        discriminator=("`PF04678` (MCU) => pore subunit, MCUB included. "
                       "`PF13833` (EF-hand_8) or `PF10161` (DDDD) without "
                       "`PF04678` => regulator. 'Pore-forming' and 'required "
                       "for conduction' are two different questions and the "
                       "catalogue answers the first."),
        test_owner="src/classify/rules.py:HAZARD_RULES",
        severity="medium", provenance=P.DB,
    ),
    Hazard(
        "HC7", "Most TRP families carry no `PF00520` at all",
        ("trpc", "trpm_ca", "trpml", "trpp", "trpv_ca", "trpv_ns", "trpa"),
        shared_evidence=("Measured by the parent project 2026-08-19: TRPV1, "
                         "TRPV5, TRPA1 and TRPM2 carry `PF00520`; TRPC3, "
                         "TRPM8, MCOLN1/2 and PKD2 carry none. Their pores "
                         "are modelled by `PF08344`, `PF18139` and `PF08016` "
                         "instead."),
        discriminator=("The census enumerates from the union of every "
                       "catalogued pore model, never from `PF00520` alone; "
                       "recall per TRP family is a reported S1 metric. For a "
                       "calcium census the cost is concentrated: the TRP "
                       "division is most of the non-selective calcium entry "
                       "in the catalogue."),
        test_owner="src/catalogue/registry.py:pore_signatures()",
        severity="high", provenance=P.DB,
    ),
    Hazard(
        "HC7b", "Ca2+ selectivity varies a hundredfold inside one TRP family",
        ("trpv_ca", "trpv_ns"),
        shared_evidence=("TRPV5/TRPV6 and TRPV1-TRPV4 carry the same Pfam "
                         "accessions, sit in the same length band, and are "
                         "sister groups by sequence. P_Ca/P_Na is >100 for "
                         "the first pair and ~1-10 for the second."),
        discriminator=("The outer-pore aspartate ring - D542 in human TRPV6, "
                       "D541 in TRPV5 - projected from the TRPV6 reference by "
                       "alignment, exactly as the four-repeat filter is "
                       "projected from Nav1.5. Verified against the reference "
                       "before use; a non-validating anchor refuses to "
                       "project rather than returning a guess."),
        test_owner="src/classify/motifs.py:TRPV_CA_ANCHOR",
        severity="high", provenance=P.LIT,
    ),
    Hazard(
        "HC8", "Calcium permeability is not always in the genome",
        ("ampa", "kainate", "nmda"),
        shared_evidence=("ADAR2 edits the GRIA2 Q/R codon from glutamine to "
                         "arginine post-transcriptionally, and an arginine "
                         "there makes the assembled AMPA receptor "
                         "Ca2+-impermeable. Editing is near-complete in adult "
                         "brain. The genomic sequence is identical in both "
                         "cases. GRIK1/GRIK2 are edited partially and "
                         "developmentally."),
        discriminator=("**None.** No sequence-level method can call this, and "
                       "this project's classifier emits no permeability "
                       "call. The families are recorded in the `CONDITIONAL` "
                       "tier and the census reports that tier separately, so "
                       "a reader can see exactly how much of the count rests "
                       "on something the genome does not encode."),
        test_owner="(no test - a declared limit of the method)",
        severity="high", provenance=P.LIT,
    ),
    Hazard(
        "HC9", "`PF08016` covers TRPML, TRPP *and* polycystin-1",
        ("trpml", "trpp", "assoc_polycystin1"),
        shared_evidence=("Measured: MCOLN1, PKD2 and PKD1 all carry `PF08016` "
                         "(Polycystin cation channel). PKD1 is not a pore."),
        discriminator=("`PF21381` (MCLN_ECD) => TRPML; `PF20519` without a "
                       "long PKD-repeat ectodomain => TRPP; `PF00801`x>=5 "
                       "=> polycystin-1, which is catalogued as "
                       "channel-associated."),
        test_owner="src/classify/rules.py:HAZARD_RULES",
        severity="medium", provenance=P.DB,
    ),
    Hazard(
        "HC10", "The CATSPER symbol root covers four pores and seven accessories",
        ("catsper", "assoc_catsper_aux"),
        shared_evidence=("CATSPER1-4 are pore subunits; CATSPERB, CATSPERG, "
                         "CATSPERD, CATSPERE, CATSPERZ, EFCAB9 and TMEM249 "
                         "are not. Symbol-prefix matching returns eleven "
                         "genes and one channel."),
        discriminator=("`PF00520` present => pore subunit. `PF15149` "
                       "(CATSPERB_C) or an EF-hand without a pore model => "
                       "accessory."),
        test_owner="src/classify/rules.py:HAZARD_RULES",
        severity="medium", provenance=P.DB,
    ),
    Hazard(
        "HC11", "Calcium pumps and exchangers are calcium proteins and not channels",
        ("transporter_ca_atpase", "transporter_ca_exchanger", "cav_hva"),
        shared_evidence=("ATP2A/ATP2B/ATP2C, SLC8A/SLC8B/SLC24A and LETM1 are "
                         "annotated for calcium transport, appear under every "
                         "calcium-handling GO term, and move more calcium per "
                         "cell than most census families."),
        discriminator=("`PF00122` + `PF00689` (P-type ATPase core) => pump; "
                       "`PF01699` (Na_Ca_ex) => exchanger. A channel call "
                       "requires a catalogued pore signature and is never "
                       "made from a transport annotation. Membership and "
                       "mechanism are separate calls (D24)."),
        test_owner="src/classify/rules.py:HAZARD_RULES",
        severity="high", provenance=P.DB,
    ),
    Hazard(
        "HC12", "'Calcium binding' is one keyword away from 'calcium conducting'",
        ("nonchannel_efhand", "nonchannel_casr_gpcr", "assoc_stim",
         "assoc_mcu_reg"),
        shared_evidence=("Roughly 250 human proteins carry an EF-hand; CASR "
                         "is named the calcium-sensing receptor and is a "
                         "GPCR; STIM1, MICU1 and EFCAB9 are EF-hand proteins "
                         "physically inside calcium channel complexes. "
                         "CALM1-3 mutations cause arrhythmias "
                         "indistinguishable from RYR2 channelopathies."),
        discriminator=("`PF00036`/`PF13499` (EF-hand) or `PF00003` (7tm_3) "
                       "without a catalogued pore signature => not a "
                       "channel. The EF-hand regex in "
                       "`src/classify/motifs.py` is a positive detector for "
                       "the decoy, not evidence against a channel: several "
                       "census families carry EF-hands too."),
        test_owner="src/classify/rules.py + src/classify/motifs.py:EF_HAND_RE",
        severity="high", provenance=P.DB,
    ),
    Hazard(
        "HC13", "The two-pore *calcium* channel may be sodium-selective",
        ("tpc",),
        shared_evidence=("TPCN1/TPCN2 were named as calcium channels and "
                         "characterised as NAADP-gated Ca2+-release channels. "
                         "Direct patch clamp of enlarged endolysosomes finds "
                         "a PI(3,5)P2-activated, Na+-selective current. Both "
                         "results reproduce."),
        discriminator=("**None at the sequence level.** The family is "
                       "catalogued `CHANNEL_CONTESTED` with both readings "
                       "recorded in `Permeability.note`, and it is counted in "
                       "the census with the contested flag so that removing "
                       "it is one line and a recount. A catalogue that "
                       "resolved a live dispute by omission would be hiding "
                       "the most interesting record it has."),
        test_owner="(no test - recorded as contested)",
        severity="medium", provenance=P.LIT,
    ),
    Hazard(
        "HC14", "The T-type filter reads EEDD, not EEEE",
        ("cav_lva", "cav_hva", "outofscope_nav"),
        shared_evidence=("Cav3 channels carry `PF00520`x4 and no "
                         "Cav-specific Pfam domain - not even `PF08763` "
                         "(Ca_chan_IQ), which Cav1 and Cav2 have. Their "
                         "filter substitutes aspartate for glutamate in "
                         "repeats III and IV."),
        discriminator=("`FILTER_CALLS` maps **both** EEEE and EEDD onto the "
                       "calcium families and records which subfamily each "
                       "belongs to. A rule written to recognise 'four "
                       "glutamates' misses every T-type channel; a rule "
                       "written to recognise 'the calcium filter' has to "
                       "enumerate the strings that are it."),
        test_owner="src/classify/motifs.py:FILTER_CALLS",
        severity="high", provenance=P.DB,
    ),
    Hazard(
        "HC15", "Ca2+-activated channels are named for calcium and conduct "
                "potassium or chloride",
        ("outofscope_kca", "outofscope_anoctamin",
         "outofscope_trpm_monovalent", "trpm_ca"),
        shared_evidence=("BK (KCNMA1), SK (KCNN1-4), TMEM16A/B and TRPM4/5 "
                         "are gated by cytosolic Ca2+ and are called calcium-"
                         "activated in their IUPHAR class names. TRPM4/5 sit "
                         "inside the TRPM family, carry the same Pfam "
                         "accessions as their Ca2+-permeable siblings, and "
                         "exclude Ca2+."),
        discriminator=("A TxGYG match => potassium filter => not a calcium "
                       "channel. `PF04547` (Anoctamin) => TMEM16, and the "
                       "channel/scramblase and Cl-/Ca2+ questions are then "
                       "literature calls. **TRPM4 versus TRPM7 has no "
                       "sequence discriminator at all** and is recorded as a "
                       "literature split with `Provenance.LIT`, which is what "
                       "an honest limit looks like."),
        test_owner="src/classify/motifs.py:K_FILTER_RE + the catalogue",
        severity="high", provenance=P.DB,
    ),
    Hazard(
        "HC16", "Ca2+ permeability varies across sister families with one architecture",
        ("cng", "outofscope_hcn", "cngc_plant", "nachr_ca",
         "outofscope_nachr_muscle", "p2x"),
        shared_evidence=("`PF00027` (cNMP_binding) spans the animal CNG "
                         "channels, the HCN channels and the plant CNGCs - "
                         "three families, two of them in this census and one "
                         "not, differing ten- to twentyfold in fractional "
                         "Ca2+ current. Measured 2026-08-20 by "
                         "`scripts/s0_rule_coverage.py`: a rule resting on "
                         "`PF00027` named HCN as a plant channel. The "
                         "nicotinic alpha7 subunit reaches P_Ca/P_Na ~10 and "
                         "its sister alpha4 ~1; the seven P2X paralogues span "
                         "an order of magnitude with one accession between "
                         "them."),
        discriminator=("For the *family* call: `PF08412` (Ion_trans_N) => "
                       "HCN, and `PF16526` (CLZ) with `PF00027` => animal "
                       "CNG. `PF00027` alone is ACCESSORY-level evidence and "
                       "names nothing - the plant CNGCs have no diagnostic "
                       "domain at all and correctly fall to the reference "
                       "tier. For the *permeability*: **none from "
                       "sequence.** Permeability is recorded as a "
                       "family-level literature attribute with its "
                       "measurement method (`Permeability`), never predicted "
                       "per sequence, and the classifier emits a family call "
                       "with no permeability claim attached. The census "
                       "boundary is therefore visible as data rather than "
                       "buried in a gene list (D31)."),
        test_owner="(no test - a declared limit of the method)",
        severity="high", provenance=P.LIT,
    ),
    Hazard(
        "HC17", "The plant glutamate receptor-like channels are architecturally "
                "identical to the animal ionotropic glutamate receptors",
        ("glr_plant", "ampa", "kainate", "nmda"),
        shared_evidence=("`PF00060` (Lig_chan) and `PF01094` (ANF_receptor) "
                         "are carried by the *Arabidopsis* GLRs and by every "
                         "animal iGluR. There is no plant-specific accession "
                         "and no animal-specific one, so the architecture "
                         "tier returns the superfamily and declines to name a "
                         "family - correctly."),
        discriminator=("Reference identity to the exemplar panel with the D7 "
                       "margin, and tier-1 clade membership: the plant GLRs "
                       "are a distinct clade, not a subgroup of any animal "
                       "family. **Species is not the test** - a plant "
                       "sequence in a metagenome has no organism label, and "
                       "assigning by taxonomy would make the census unable to "
                       "place the very sequences it exists to place."),
        test_owner="src/classify/reference.py + src/phylo/forest.py",
        severity="medium", provenance=P.DB,
        notes=("Added 2026-08-20 by `scripts/s0_rule_coverage.py`, which "
               "found `glr_plant` to be the one census family the "
               "architecture tier cannot name and no hazard explained. That "
               "is precisely the gap the script exists to surface: an "
               "unnameable family without a hazard row means either the "
               "hazard is missing or the signatures are wrong."),
    ),
]

HAZARD_BY_ID: dict[str, Hazard] = {h.hid: h for h in HAZARDS}
