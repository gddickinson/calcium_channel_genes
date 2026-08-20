# FINDINGS.md — the biological story, task by task

Plain language, findings before methods. Appended after every completed
task. Claims that a later task will confirm are marked *(pending: task)*.

---

## Setup, 2026-08-20 — what the subject turned out to be

The census is not one number, and that is the finding rather than an excuse.

**Calcium channels are not a family, a fold, or a motif.** Potassium
channels can be defined by a sequence: TxGYG. Sodium channels nearly so.
"Calcium channel" names a *permeability ratio* — how much better a pore
passes Ca²⁺ than Na⁺ — and that is measured, in a cell, at a divalent
concentration, sometimes per subunit combination. Pores that do it well have
arisen independently in at least four unrelated folds: the four-repeat
P-loop channels (Cav), the hexameric ORAI, the mitochondrial uniporter, and
the TRPV5/6 pair inside the TRP division.

So the catalogue counts in tiers, and the tiers are the result:

| tier | families | human genes |
|---|---|---|
| Ca²⁺-selective (P_Ca/P_Na ≳ 10) | 7 | 28 |
| store release | 5 | 11 |
| Ca²⁺-permeable, non-selective | 15 | 50 |
| conditional — set by editing or composition | 2 | 9 |
| **census total** | **29** | **98** |

A reader who thinks only selective pores count takes 28. A reader who counts
every physiologically important calcium entry route takes 98. Both numbers
are defensible; neither is quotable without the other three rows.
*(pending: S0 verifies the catalogue's accessions; S1b audits every
permeability value behind these tiers.)*

**The excluded set is bigger than the census.** The catalogue holds 245
human genes and counts 98. The other 147 are what a search for "calcium
channel" returns: sixteen `CACN`-prefixed auxiliary subunits (seven of which
are really AMPA-receptor subunits), the Ca²⁺-*activated* potassium and
chloride channels which conduct K⁺ and Cl⁻, nineteen pumps and exchangers,
the EF-hand sensors, the calcium-sensing receptor CASR — a GPCR — and the
sodium channels, which share Cav's fold and architecture and differ by four
residues in the filter.

That ratio is the argument for doing the census this way. A project that
listed only what it counted would look tidier and would be unfalsifiable.

**The boundary runs *inside* families, three times.** TRPV5/6 are
Ca²⁺-selective and their sisters TRPV1–4 are not. TRPM4 and TRPM5 sit inside
the TRPM family, carry the same Pfam accessions as their Ca²⁺-permeable
siblings, and are *activated by* calcium while excluding it. The nicotinic
α7 subunit reaches P_Ca/P_Na ≈ 10 and its sister α4 about 1. Splitting a
Pfam-identical family across the census boundary is uncomfortable and it is
what the measurements say.

**The literature's TRPV6 numbering does not match the database.** Verified
2026-08-20: the aspartate ring that makes TRPV5/TRPV6 calcium-selective is
cited as D542 throughout the functional literature. The canonical human
TRPV6 entry in UniProt (`Q9H1D0`) is 765 aa and carries the `TIIDGP` filter
at 579–584, putting that aspartate at **D582** — position 542 is a leucine.
The ~40-residue offset is the known long/short isoform difference (TRPV6 has
an upstream non-AUG start). An anchor copied from a paper would have
projected the wrong alignment column and returned a wrong answer silently
for every TRPV channel in the census. This is exactly what `verify_anchor()`
exists to catch, and it caught it on the first run.

**Three anchors verified, one regex validated.** Human Nav1.5 `Q14524` still
reads DEKA at 372/898/1419/1711, so the test that separates a calcium
channel from a sodium channel is sound. Human ORAI1 `Q96D31` position 106 is
the selectivity glutamate. The mitochondrial uniporter's DIME motif is at
position 260 of `Q8NE86` and is the only calcium filter in this catalogue
short enough to find with a regular expression — the most Ca²⁺-selective
channel known has the shortest filter. The EF-hand regex finds four loops in
calmodulin, four in calbindin, two in parvalbumin, two in MICU1, one in
STIM1, and none in CACNA1C or MCU: it separates the calcium-binding decoys
from the calcium-conducting census families rather than firing on everything
with calcium in its annotation.

**Some calcium permeability is not in the genome at all.** ADAR2 edits one
codon of the GRIA2 transcript from glutamine to arginine, and an arginine
there makes the assembled AMPA receptor calcium-impermeable. Editing is
essentially complete in adult brain, so almost every GRIA2-containing
receptor excludes calcium and every one lacking GRIA2 admits it — with
identical DNA either way. Nine human genes in this census sit in that
`conditional` tier. No sequence-level method can call them, this project
does not try, and the tier exists so that the amount of the count resting on
something the genome does not encode is visible rather than buried.

---

## S0 (partial), 2026-08-20 — what a live check did to a hand-written catalogue

S0 is not finished. It is far enough along to have changed the catalogue
eight times and the classifier three times, and every one of those changes
was invisible to the offline checks that passed before it.

**The literature's TRPV6 numbering is off by forty residues.** The aspartate
ring that makes TRPV5 and TRPV6 calcium-selective is cited as D542
throughout the functional literature. The canonical human TRPV6 entry
(`Q9H1D0`) is 765 aa and carries the `TIIDGP` filter at 579–584, so that
aspartate is **D582**; position 542 is a leucine. The offset is the known
long/short isoform difference — TRPV6 has an upstream non-AUG start. Had the
anchor been taken from the paper, every TRPV channel in the census would
have had the wrong alignment column read, and nothing would have said so.

**Two Pfam accessions were swapped, and four more names were wrong.**
`PF02714` is `RSN1_7TM` ("Calcium-dependent channel, 7TM region") and
`PF13967` is `RSN1_TM` ("Late exocytosis, associated with Golgi
transport"); the catalogue had them the other way round. Both are carried by
the same OSCA/TMEM63 proteins, which is why the mistake was undetectable
without a live check. `PF01452`, `PF07766`, `PF02888` and `PF19584` were
also named wrongly. All six were among the accessions marked
`Provenance.CURATED` — the tag did its job.

**Four families do not carry what the catalogue said they carry.** TRPM7
carries no `PF00520` at all, extending to a second family a finding the
parent project had made only for TRPM8; it does carry a fused alpha-kinase.
OSCA/TMEM63 carry a third domain (`PF14703`) nobody had declared, and plant
MCA1 a second (`PF19584`). And **plant CNGC4 carries no
cyclic-nucleotide-binding domain at all** — a family named for
cyclic-nucleotide gating whose exemplar has no annotated cyclic-nucleotide
site.

**The Ca²⁺-activated potassium channels are two families wearing one name.**
KCNN2 (SK2) carries `PF07885`, `PF03530` and `PF02888`, and **none** of
BK's domains. One architecture rule cannot reach both halves, so hazard
HC15 now has two.

**Domain architecture can name 17 of the 29 census families, and that is the
finding, not a shortfall.** `scripts/s0_rule_coverage.py` feeds every family
its own declared architecture back through the rule table. The twelve it
cannot name are precisely the ones the hazard registry already says are
architecturally indistinguishable from a sibling: the T-type calcium
channels and CatSper (identical to the sodium channels), TRPV5/6 against
TRPV1–4, the nicotinic α7 subunit against its own family, and all four
glutamate-receptor families against each other. The claim that domain
architecture is not a family call is now a number.

That script also found three defects in one run:

- **A missing hazard.** The plant glutamate receptor-like channels carry the
  same two domains as every animal iGluR and nothing distinguishes them.
  There was no hazard row saying so. There is now (**HC17**).
- **HCN was being classified as a plant channel.** Demoting plant CNGC's
  `PF00027` after the CNGC4 measurement left that accession as the sole
  requirement of the generated plant rule — and HCN carries it too. The
  correction created the bug. `PF00027` spans animal CNG, HCN *and* plant
  CNGC, so it is now `ACCESSORY` and names nothing; HCN gets a positive test
  of its own.
- **Polycystin-1 tied with TRPP.** PKD1 carries `PF20519` exactly as TRPP
  does, so both rules fired at equal priority and the honest tie would have
  let a protein that forms no pore into the census by ambiguity. Fifteen PKD
  repeats now outrank one shared domain.

All three are locked into the self-test, which is at 61 invariants.

**What is still unknown.** The exemplar-architecture stage has not been
re-run since the corrections, so the list of families whose declared
signatures are not all observed is stale. The permeability values behind
every census tier remain unaudited — no database holds them, and task S1b
exists for exactly that. *(pending: S0 completion, S1b.)*

---

## S0 complete — the catalogue now says only things that check out (2026-08-20)

**What changed biologically.** Nothing about which genes are calcium
channels: the census still counts 98 human genes out of 245 catalogued, in
four tiers. What changed is that the catalogue's claims about *what these
proteins are made of* are now measured rather than remembered, and the
measurement corrected eleven families.

**The corrections divide into three kinds, and the third is the interesting
one.**

*A wrong accession that no name check could catch.* Pfam holds two families
with the identical description "haloacid dehalogenase-like hydrolase",
`PF00702` and `PF08282`. The catalogue had declared `PF00702` for the P-type
Ca²⁺-ATPases. Neither SERCA nor PMCA carries it; both carry `PF08282`. The
accession existed and its short name matched what had been written, so every
check short of asking whether the family's own members carry the domain would
have passed.

*Domains that are named for a family and carried by a minority of it.*
`PF16519` is called TRPM_tetra. It is annotated on TRPM7 and absent from
TRPM2, TRPM8, TRPM4 and TRPM5. Together with the already-known absence of the
canonical pore model `PF00520` from TRPM8 and TRPM7, the TRP division is
annotated so unevenly that no single domain enumerates it — which is the
strongest argument yet for the profile-HMM and genomic sweeps that S3 and S5
will add. `PF16526` (CNG), `PF23317` (TRPC) and `PF00036` (the EF-hand
sensors) are the same story at smaller scale.

*Families that are not families.* Several catalogued groups are defined by
the job their members do, and the catalogue had declared the union of their
members' domains as though every member carried all of them. Measured, the
Cav auxiliary subunits share nothing at all: the β subunit is a MAGUK, α2δ
carries a von Willebrand A domain, and the γ subunits are claudins. The same
is true of the uniporter regulators (MICU1's EF-hands against EMRE's own
domain), the release regulators (calsequestrin against FKBP), and connexin
against pannexin. **A buffer and an immunophilin have in common only the
channel they regulate**, and the catalogue now says so.

**One correction created a defect, which is worth recording as a rule.** The
cyclic-nucleotide-binding domain `PF00027` spans animal CNG, HCN and the
plant CNGCs — the hazard registry had said so since setup — and the catalogue
simultaneously declared it a family-level signature of animal CNG. The
contradiction was invisible because a second requirement masked it.
Correcting that second requirement to its measured level removed the mask,
and the generated rule immediately named the plant CNGC channels as animal
CNG channels. Only a coverage test that re-derives every rule after every
edit catches this, and this is the second time in two sessions that a
correction has produced a defect.

**A gene symbol is not an identifier.** `GRIK5` carries `GRIK2` in its
UniProt synonym list, so a symbol lookup for GRIK2 returned GRIK5 — a
different, longer protein — and the classifier's reference panel had been
carrying it under the label `Hs_GRIK2`. The project's rule is never to
consult a gene symbol when classifying; the classifier obeyed it and the code
that built its references quietly did not. All 102 exemplars now declare a
UniProt accession explicitly, so the panel no longer depends on what a
lookup returns on a given day.

**The filters read what they should.** All three projection anchors were
re-verified against live UniProt — Nav1.5 `Q14524` reads DEKA, TRPV6
`Q9H1D0` reads D at 582, ORAI1 `Q96D31` reads E at 106 — and the filter
atlas then read the four-repeat locus across nine channels independently:
EEEE for Cav1/Cav2, EEDD for Cav3, DEKA for the sodium channels, EEKE for
NALCN. TPC1 and CatSper1 returned partial signatures, exactly as predicted:
TPC1 has two repeats rather than four, and CatSper's four positions lie in
four different proteins. A partial answer recorded as partial is the point.

**What is still unknown.** The permeability values behind every census tier
remain unaudited — no database holds a P_Ca/P_Na, and the tier boundaries
rest on literature claims nothing has checked *(pending: S1b)*. Whether the
TRPV aspartate anchor actually separates TRPV5/6 from TRPV1–4 is unmeasured
*(pending: S1)*.

---

## S23 — the literature review, written (2026-08-20)

**What it is.** `docs/channel_review_2026.md`: 17 sections, ~13,000 words,
122 references, seven figures rendered from committed tables. It is generated
from `docs/review/*.md` and never hand-edited.

**The claim it is organised around** is the one the project has been arguing
from the start, now stated at length: calcium-channel membership is a
measured permeability rather than a clade, so there is no motif and no fold
that defines the subject and no single tree that can contain it. The review
takes the four best-characterised calcium-selective filters — the EEEE ring,
ORAI's E106, the uniporter's DIME motif, the TRPV aspartate ring — and shows
that they share no alignable position, which makes "how many times has a
Ca²⁺-selective pore evolved" a count of unconnected components in a
structural network rather than a clade count.

**Every citation was verified before it could be used.** All 122 source
titles were resolved against Europe PMC, and a record is accepted only if the
returned title is at least 90 % similar to the one requested. Three failed on
the first pass and were corrected against the live records rather than
guessed at: the Cav1.1 structure paper is indexed as "Ca(v)1.1", the
Prakriya store-operated review needed an author constraint to beat a hundred
generically titled papers, and the TRPV5 identification paper is indexed with
a space inside "1, 25-dihydroxyvitamin". A misremembered title fails the
build rather than becoming a plausible bibliography entry.

**What it does not claim.** The measured sections report S0's results only.
Everything resting on the census sweeps, the classifier benchmark, the
phylogenies or the structural comparison is marked in the text with the task
that will produce it, and section 15 lists those nine open measurements
explicitly. The review states in its own methods that it establishes the
catalogue's claims are internally correct, not that the catalogue is
complete.

---

## S1 — the classifier, measured against the things it should reject (2026-08-20)

**The headline.** On a panel of 49 positives (one or two human members of
every census family with a human gene) and 20 decoys (one per control
family), the classifier recalls **38/48 (79.2 %)** and rejects **18/20
(90 %)**. Eighteen of the nineteen hazards were exercised. One positive,
CHRNA7, could not be fetched from UniProt after four attempts and is reported
as missing rather than scored as a failure — which is why the denominator is
48 and not 49. Both numbers are lower than a benchmark usually reports, and
the reason is the interesting part: almost every miss is the classifier
**refusing to guess**, not the classifier guessing wrong.

**Nine of the ten recall failures are abstentions.** CatSper, TPC, TRPA,
NMDA, CNGB1 and the α9 nicotinic subunit were left `unassigned` because the
nearest reference sequence belonged to another family by less than the 10 %
margin the project requires before it will make a call (D7). CATSPER1's
nearest neighbour in the whole panel is a **sodium channel**, at 28.6 %
identity. A classifier that reported 95 % recall on this panel would be one
that had stopped requiring a margin.

**The load-bearing test holds: the four-repeat filter separates Cav from Nav
perfectly.** Projected from the Nav1.5 anchor across all 27 human
four-repeat channels: every one of the seven Cav1/Cav2 genes reads `EEEE`,
all three Cav3 genes read `EEDD`, NALCN reads `EEKE`, and eight of the nine
sodium channels read `DEKA`. No string is shared between a calcium family
and a non-calcium one. The ninth sodium channel, SCN7A — Na_x, the atypical
member that is not voltage-gated — reads `DENA`, a lysine-to-asparagine
difference at repeat III that is a real property of that protein rather than
a projection error.

**And CatSper's filter is readable after all, but not from one sequence.**
The four CatSper subunits project to `---D`, `--D-`, `-D--` and `--D-`: each
subunit carries an aspartate at a *different* repeat position, which is
exactly what a heterotetramer assembling one pore from four different
proteins should look like. Three of the four repeat positions are covered
between them. A joint four-sequence projection is now a concrete proposal
rather than a hope *(pending: S9)*.

**The TRPV aspartate ring is not a test, and now the catalogue says so.**
This was the session's most consequential negative result. Hazard HC7b —
"Ca²⁺ selectivity varies a hundredfold inside one TRP family" — was closed
by projecting TRPV6's outer-pore aspartate onto its relatives. Projected onto
all six human TRPVs, **five of them read `D`**: TRPV5 and TRPV6, which are
the Ca²⁺-selective pair, but also TRPV1, TRPV3 and TRPV4, which are not.
Only TRPV2 reads anything else. The residue does not separate the groups it
was supposed to separate. HC7b's discriminator has been rewritten to say
"none from sequence", and the anchor's call map has been **emptied** so it
can no longer name a family — it stays as supporting evidence. The
trpv_ca / trpv_ns boundary rests entirely on measured permeability
*(pending: S1b)*.

**A decoy was not merely accepted — it was named.** TRPM4 is Ca²⁺-impermeable
and the architecture tier called it `trpm_ca` outright. The catalogue is
right that TRPM4 carries the same domains as its Ca²⁺-permeable siblings; the
fault is that rules are generated only for census families, so a domain both
sides declare produces one rule pointing at the census family and nothing to
tie against. Measured across the whole catalogue, this is **1 leak of its
kind in 37 architecture matches into control families** — the other 36 say
only "this is a P-loop channel", which is true. It is the third appearance of
one defect shape (after `PF00027` and HCN), and the fix is to let control
families generate rules *(pending: emergent task)*.

**The nicotinic boundary cannot be drawn from sequence, and the classifier
gets it exactly backwards.** CHRNA1, a muscle subunit that is *out* of the
census, was called `nachr_ca` by reference identity at a comfortable margin
of +0.165. CHRNA9, which *is* in the census, was left unassigned at a margin
of +0.004 — ambiguous between `nachr_ca` and `outofscope_nachr_muscle`. Both
proteins have the same nearest neighbour (TRPV6's panel-mate Hs_CHRNA7) at
almost the same identity, 39.2 % and 39.3 %. So the decoy got the confident
call and the real member got the abstention. The α7/α9/α10 versus muscle
split is a permeability split, and no sequence tier reproduces it. This is
the same shape as HC16's declared limit, now with a number attached.

**What the tiers actually contributed.** Hazard rules made 28 of the calls,
reference identity 20, architecture 5 and the motif tier 3, with 12 proteins
undecided. The classifier is therefore not a nearest-neighbour lookup — most
correct calls come from hand-written positive tests that would work on a
sequence with no relative in the panel — but the reference tier is what
carries the families whose architectures are identical, and those are
exactly the families where it fails.

**What is still unknown.** HC13 — whether the two-pore channel is in fact
sodium-selective — was exercised by nothing on this panel and remains
untested. The ORAI anchor is untested rather than undiscriminating: every
family in its scope is Ca²⁺-selective, so this panel has nothing for it to
separate. And the permeability values that every tier boundary depends on
are still unaudited *(pending: S1b)*.
