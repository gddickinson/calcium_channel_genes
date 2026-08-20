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
