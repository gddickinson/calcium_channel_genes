"""The review's source list - titles to resolve, not a bibliography.

Every entry is `(key, title)` or `(key, title, constraint)`, where the
constraint is extra Europe PMC query syntax - `AUTH:"Catterall WA" AND
PUB_YEAR:2011`. Short generic titles ("TRP channels", "Calcium signaling")
match hundreds of papers and the search ranks the wrong one; the constraint
is how a real paper with an unhelpfully short title gets resolved without
loosening the title match that keeps the bibliography honest. Nothing here
is a citation yet: the titles are *queries*, and `scripts/s0_review_refs.py`
resolves each one against Europe PMC and writes the verified metadata to
`results/s0_baseline/references.tsv`. A title that does not resolve, or that
resolves to something whose title does not match, is reported and **not**
written - so a misremembered paper becomes a build failure rather than a
fabricated reference.

This matters more than usual here. A review is the one artefact in a
publication project where an invented citation is both easy to produce and
almost impossible for a reader to catch, so the rule is absolute: the
bibliography is machine-generated from live records, and prose may cite only
keys that survived resolution (`scripts/s0_review_build.py --check`).

**This list is deliberately shorter than the parent project's.** A hundred
verified sources are worth more than two hundred half-remembered ones, and
the list is expected to grow section by section as the review is written -
each addition resolved before it can be cited.

Keys are stable and arbitrary. The build renumbers them into order of first
appearance, so adding a paper mid-section does not renumber the file.
"""

from __future__ import annotations

SOURCES: list[tuple[str, ...]] = [
    # ------------------------------------------------------- foundations
    ("ringer1883", "A further Contribution regarding the influence of the different Constituents of the Blood on the Contraction of the Heart"),
    ("fatt1953", "The electrical properties of crustacean muscle fibres"),
    ("hodgkin1952", "A quantitative description of membrane current and its application to conduction and excitation in nerve"),
    ("neher1976", "Single-channel currents recorded from membrane of denervated frog muscle fibres"),
    ("berridge2000", "The versatility and universality of calcium signalling"),
    ("clapham2007", "Calcium signaling", 'AUTH:"Clapham DE" AND PUB_YEAR:2007'),
    ("carafoli2002", "Calcium signaling: a tale for all seasons"),
    ("bootman2020", "Fundamentals of Cellular Calcium Signaling: A Primer"),
    # -------------------------------------- voltage-gated calcium channels
    ("tanabe1987", "Primary structure of the receptor for calcium channel blockers from skeletal muscle"),
    ("mikami1989", "Primary structure and functional expression of the cardiac dihydropyridine-sensitive calcium channel"),
    ("ertel2000", "Nomenclature of voltage-gated calcium channels"),
    ("catterall2011", "Voltage-gated calcium channels", 'AUTH:"Catterall WA" AND PUB_YEAR:2011'),
    ("zamponi2015", "The physiology, pathology, and pharmacology of voltage-gated calcium channels and their future therapeutic potential"),
    ("dolphin2016", "Voltage-gated calcium channels and their auxiliary subunits: physiology and pathophysiology and pharmacology"),
    ("dolphin2018", "Presynaptic calcium channels: specialized control of synaptic neurotransmitter release"),
    ("wu2016", "Structure of the voltage-gated calcium channel Ca(v)1.1 at 3.6 Å resolution"),
    ("wu2015", "Structure of the voltage-gated calcium channel Cav1.1 complex"),
    ("rios1987", "Involvement of dihydropyridine receptors in excitation-contraction coupling in skeletal muscle"),
    # ---------------------------------------------- selectivity and filter
    ("yang1993", "Molecular determinants of Ca2+ selectivity and ion permeation in L-type Ca2+ channels"),
    ("sather2003", "Permeation and selectivity in calcium channels"),
    ("heinemann1992", "Calcium channel characteristics conferred on the sodium channel by single mutations"),
    ("tang2014", "Structural basis for Ca2+ selectivity of a voltage-gated calcium channel"),
    ("payandeh2011", "The crystal structure of a voltage-gated sodium channel"),
    ("catterall2012", "Voltage-gated sodium channels at 60: structure, function and pathophysiology"),
    ("lu2007", "The neuronal channel NALCN contributes resting sodium permeability and is required for normal respiratory rhythm"),
    # --------------------------------------------------- T-type and CatSper
    ("perezreyes2003", "Molecular physiology of low-voltage-activated T-type calcium channels"),
    ("cribbs1998", "Cloning and characterization of alpha1H from human heart, a member of the T-type Ca2+ channel gene family"),
    ("ren2001", "A sperm ion channel required for sperm motility and male fertility"),
    ("lishko2011", "Progesterone activates the principal Ca2+ channel of human sperm"),
    ("strunker2011", "The CatSper channel mediates progesterone-induced Ca2+ influx in human sperm"),
    ("cai2012", "Evolutionary genomics reveals lineage-specific gene loss and rapid evolution of a sperm-specific ion channel complex: CatSpers and CatSperbeta"),
    # --------------------------------------------- store-operated entry
    ("roos2005", "STIM1, an essential and conserved component of store-operated Ca2+ channel function"),
    ("liou2005", "STIM is a Ca2+ sensor essential for Ca2+-store-depletion-triggered Ca2+ influx"),
    ("feske2006", "A mutation in Orai1 causes immune deficiency by abrogating CRAC channel function"),
    ("vig2006", "CRACM1 is a plasma membrane protein essential for store-operated Ca2+ entry"),
    ("zhang2006", "Genome-wide RNAi screen of Ca2+ influx identifies genes that regulate Ca2+ release-activated Ca2+ channel activity"),
    ("prakriya2006", "Orai1 is an essential pore subunit of the CRAC channel"),
    ("yeromin2006", "Molecular identification of the CRAC channel by altered ion selectivity in a mutant of Orai"),
    ("hou2012", "Crystal structure of the calcium release-activated calcium channel Orai"),
    ("prakriya2015", "Store-Operated Calcium Channels", 'AUTH:"Prakriya M" AND PUB_YEAR:2015'),
    ("hogan2015", "Store-operated calcium entry: Mechanisms and modulation"),
    # ------------------------------------------- intracellular release
    ("furuichi1989", "Primary structure and functional expression of the inositol 1,4,5-trisphosphate-binding protein P400"),
    ("mignery1989", "Putative receptor for inositol 1,4,5-trisphosphate similar to ryanodine receptor"),
    ("takeshima1989", "Primary structure and expression from complementary DNA of skeletal muscle ryanodine receptor"),
    ("berridge1993", "Inositol trisphosphate and calcium signalling"),
    ("fabiato1983", "Calcium-induced release of calcium from the cardiac sarcoplasmic reticulum"),
    ("desgeorges2016", "Structural Basis for Gating and Activation of RyR1"),
    ("fan2015", "Gating machinery of InsP3R channels revealed by electron cryomicroscopy"),
    ("yan2015", "Structure of the rabbit ryanodine receptor RyR1 at near-atomic resolution"),
    ("lanner2010", "Ryanodine receptors: structure, expression, molecular details, and function in calcium release"),
    ("yamazaki2011", "TRIC-A channels in vascular smooth muscle contribute to blood pressure maintenance"),
    # ---------------------------------------------------- mitochondrial
    ("kirichok2004", "The mitochondrial calcium uniporter is a highly selective ion channel"),
    ("perocchi2010", "MICU1 encodes a mitochondrial EF hand protein required for Ca(2+) uptake"),
    ("baughman2011", "Integrative genomics identifies MCU as an essential component of the mitochondrial calcium uniporter"),
    ("destefani2011", "A forty-kilodalton protein of the inner membrane is the mitochondrial calcium uniporter"),
    ("sancak2013", "EMRE is an essential component of the mitochondrial calcium uniporter complex"),
    ("baradaran2018", "Cryo-EM structures of fungal and metazoan mitochondrial calcium uniporters"),
    ("colombini2004", "VDAC: the channel at the interface between mitochondria and the cytosol"),
    ("rapizzi2002", "Recombinant expression of the voltage-dependent anion channel enhances the transfer of Ca2+ microdomains to mitochondria"),
    ("shoshanbarmatz2010", "VDAC, a multi-functional mitochondrial protein regulating cell life and death"),
    ("palty2010", "NCLX is an essential component of mitochondrial Na+/Ca2+ exchange"),
    ("jiang2009", "Genome-wide RNAi screen identifies Letm1 as a mitochondrial Ca2+/H+ antiporter"),
    # ------------------------------------------------------------- TRP
    ("caterina1997", "The capsaicin receptor: a heat-activated ion channel in the pain pathway"),
    ("clapham2003", "TRP channels as cellular sensors"),
    ("ramsey2006", "An introduction to TRP channels"),
    ("owsianik2006", "Permeation and selectivity of TRP channels"),
    ("nilius2007", "Transient receptor potential cation channels in disease"),
    ("peng1999", "Molecular cloning and characterization of a channel-like transporter mediating intestinal calcium absorption"),
    ("hoenderop1999", "Molecular identification of the apical Ca2+ channel in 1, 25-dihydroxyvitamin D3-responsive epithelia"),
    ("hoenderop2005", "Calcium absorption across epithelia"),
    ("saotome2016", "Crystal structure of the epithelial calcium channel TRPV6"),
    ("launay2002", "TRPM4 is a Ca2+-activated nonselective cation channel mediating cell membrane depolarization"),
    ("hofmann2003", "TRPM5 is a voltage-modulated and Ca(2+)-activated monovalent selective cation channel"),
    ("dong2008", "The type IV mucolipidosis-associated protein TRPML1 is an endolysosomal iron release channel"),
    ("xu2015", "Lysosomal physiology"),
    # ------------------------------------------------- two-pore channels
    ("calcraft2009", "NAADP mobilizes calcium from acidic organelles through two-pore channels"),
    ("wang2012", "TPC proteins are phosphoinositide-activated sodium-selective ion channels in endosomes and lysosomes"),
    # --------------------------------------------- ligand-gated and editing
    ("sommer1991", "RNA editing in brain controls a determinant of ion flow in glutamate-gated channels"),
    ("hume1991", "Identification of a site in glutamate receptor subunits that controls calcium permeability"),
    ("burnashev1992", "Divalent ion permeability of AMPA receptor channels is dominated by the edited form of a single subunit"),
    ("higuchi2000", "Point mutation in an AMPA receptor gene rescues lethality in mice deficient in the RNA-editing enzyme ADAR2"),
    ("traynelis2010", "Glutamate receptor ion channels: structure, regulation, and function"),
    ("mayer2006", "Glutamate receptors at atomic resolution"),
    ("fucile2004", "Ca2+ permeability of nicotinic acetylcholine receptors"),
    ("north2002", "Molecular physiology of P2X receptors"),
    ("egan2004", "Contribution of calcium ions to P2X channel responses"),
    ("kawate2009", "Crystal structure of the ATP-gated P2X(4) ion channel in the closed state"),
    # ------------------------------------------------- mechanotransduction
    ("coste2010", "Piezo1 and Piezo2 are essential components of distinct mechanically activated cation channels"),
    ("ge2015", "Architecture of the mammalian mechanosensitive Piezo1 channel"),
    ("kefauver2020", "Discoveries in structure and physiology of mechanically activated ion channels"),
    ("yuan2014", "OSCA1 mediates osmotic-stress-evoked Ca2+ increases vital for osmosensing in Arabidopsis"),
    ("nakagawa2007", "Arabidopsis plasma membrane protein crucial for Ca2+ influx and touch sensing in roots"),
    # ------------------------------------------------------- large pores
    ("taruno2013", "CALHM1 ion channel mediates purinergic neurotransmission of sweet, bitter and umami tastes"),
    ("siebert2013", "Structural and functional similarities of calcium homeostasis modulator 1 (CALHM1) ion channel with connexins, pannexins, and innexins"),
    ("ma2018", "CALHM3 is essential for rapid ion channel-mediated purinergic neurotransmission of GPCR-mediated tastes"),
    # ------------------------------------------ pumps, exchangers, sensors
    ("toyoshima2000", "Crystal structure of the calcium pump of sarcoplasmic reticulum at 2.6 A resolution"),
    ("brini2009", "Calcium pumps in health and disease"),
    ("blaustein1999", "Sodium/calcium exchange: its physiological implications"),
    ("brown1993", "Cloning and characterization of an extracellular Ca(2+)-sensing receptor from bovine parathyroid"),
    ("brown2001", "Extracellular calcium sensing and extracellular calcium signaling"),
    # -------------------------------------------- evolution and non-animals
    ("case2007", "Evolution of calcium homeostasis: from birth of the first cell to an omnipresent signalling system"),
    ("verkhratsky2014", "Calcium signalling and calcium channels: evolution and general principles"),
    ("moran2014", "The evolution of the four subunits of voltage-gated calcium channels: ancient roots, increasing complexity, and multiple losses"),
    ("verret2010", "Calcium channels in photosynthetic eukaryotes: implications for evolution of calcium-based signalling"),
    ("toyota2018", "Glutamate triggers long-distance, calcium-based plant defense signaling"),
    ("mousavi2013", "GLUTAMATE RECEPTOR-LIKE genes mediate leaf-to-leaf wound signalling"),
    ("hedrich2012", "Ion channels in plants"),
    # ----------------------------------------------- disease, pharmacology
    ("ashcroft2006", "From molecule to malady"),
    ("kullmann2010", "Neurological channelopathies"),
    ("bagal2013", "Ion channels as therapeutic targets: a drug discovery perspective"),
    ("santos2017", "A comprehensive map of molecular drug targets"),
    ("alexander2023", "THE CONCISE GUIDE TO PHARMACOLOGY 2023/24: Ion channels"),
    # ------------------------------------------------ databases and tools
    ("paysanlafosse2023", "InterPro in 2022"),
    ("mistry2021", "Pfam: The protein families database in 2021"),
    ("uniprot2023", "UniProt: the Universal Protein Knowledgebase in 2023"),
    ("katoh2013", "MAFFT multiple sequence alignment software version 7: improvements in performance and usability"),
    ("minh2020", "IQ-TREE 2: New Models and Efficient Methods for Phylogenetic Inference in the Genomic Era"),
    ("kalyaanamoorthy2017", "ModelFinder: fast model selection for accurate phylogenetic estimates"),
    ("capellagutierrez2009", "trimAl: a tool for automated alignment trimming in large-scale phylogenetic analyses"),
    ("vankempen2024", "Fast and accurate protein structure search with Foldseek"),
    ("jumper2021", "Highly accurate protein structure prediction with AlphaFold"),
    ("eddy2011", "Accelerated Profile HMM Searches"),
]
