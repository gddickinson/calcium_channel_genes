## 12. What the databases record

Everything in this section was measured against live services rather than
recalled, by `scripts/s0_catalogue_verify.py`, `scripts/s0_rule_coverage.py`
and `scripts/s0_anchors.py`, and is committed as tables under
`results/s0_baseline/`. The purpose is not to criticise the resources — they
are the reason a census is possible at all
[paysanlafosse2023, mistry2021, uniprot2023] — but to establish what a census
built on them can and cannot claim.

### 12.1 The catalogue's own claims, re-derived

The catalogue is a file full of assertions: this Pfam accession exists and
means that; this gene symbol resolves to that protein in that organism; this
family's members carry these domains; this taxon id is that species. Written
by hand and checked by nothing, such a file is a liability. Re-deriving all of
it against live databases produced the following state:

| checked | n | result |
|---|---|---|
| Pfam accessions | 87 | all resolve; every short name matches |
| exemplar proteins | 102 | all resolve to a declared accession |
| taxon ids | 53 | all resolve |
| projection anchors | 3 | all read what the catalogue claims |
| declared architectures | 102 | 30 show an absence, all subfamily-level |

That table is the end state, and it is worth being explicit that it was not
the starting one. The verification found and corrected a series of errors, and
they are more interesting than the clean result.

### 12.2 Errors that a name check would not have caught

**Two Pfam families share a description.** `PF00702` and `PF08282` are both
called "haloacid dehalogenase-like hydrolase". The catalogue declared
`PF00702` for the P-type Ca²⁺-ATPases; InterPro annotates `PF08282` on both
SERCA and PMCA, and neither pump carries `PF00702`. The accession existed and
its name matched what had been written, so every check short of asking whether
the family's own members carry it would have passed.

**A domain named for a family is carried by a minority of it.** `PF16519`
(TRPM_tetra) is annotated on TRPM7 and is absent from TRPM2, TRPM8, TRPM4 and
TRPM5.

**A domain the hazard registry had already flagged was still being used to
name a family.** `PF00027` (cNMP_binding) spans the animal CNG channels, HCN
and the plant CNGCs — recorded as a hazard, and simultaneously declared as a
family-level signature of animal CNG. The contradiction was invisible while a
second requirement masked it. Correcting an unrelated over-claim removed that
mask, and the generated rule immediately named the plant CNGC channels as
animal CNG channels. The lesson generalises: a correction can create a defect,
and only a coverage test that re-derives every rule from the catalogue after
every edit will catch it.

**A "family" can have no shared domain at all.** Several catalogued groups are
defined by the job their members do rather than by descent, and the union of
their members' domains had been declared as though every member carried all of
them. Measured, they do not:

| group | members carry |
|---|---|
| Cav auxiliary subunits | β: guanylate kinase; α2δ: VWA; γ: claudin |
| uniporter regulators | MICU1: EF-hands; EMRE: `PF10161` alone |
| release regulators | CASQ2: calsequestrin; FKBP1A: FKBP |
| connexin / pannexin | GJA1: connexin; PANX1: innexin |

These are not annotation failures. They are the catalogue asserting a shared
architecture where the biology has convergence or mere co-membership, and the
correction is to record the level at which each signature is actually
diagnostic.

### 12.3 A gene symbol is not an identifier

The reference panel that the classifier scores against is built by resolving
gene symbols to UniProt entries. Symbols are recycled, and UniProt records
synonyms: `GRIK5` (`Q16478`, 980 aa) carries `GRIK2` in its synonym list, so a
symbol query for `GRIK2` returned two reviewed human entries and a
longest-wins tiebreak selected the wrong protein. The panel had been carrying
GRIK5's sequence under the label `Hs_GRIK2`.

This is worth stating in a review because it is a failure mode of the
*tooling*, not of the databases, and because the project's own rule — never
consult a gene symbol when classifying — had been obeyed by the classifier and
quietly broken by the code that built its references. Every exemplar in the
catalogue now declares an accession explicitly, and the panel no longer
depends on what a symbol lookup returns on a given day.

A related case is benign and equally instructive: *Arabidopsis* `OSCA1.1`
resolves only as a synonym of UniProt's `OSCA1`. Reporting that as "the
accession names the wrong gene" would be false, so the check distinguishes a
synonym match from a mismatch.

![](figures/fig4_length_range.png)

**Figure 4 | Thirty-fold, within one census.** Observed length range per
superfamily, from the catalogue's exemplars. The subject spans rotavirus
NSP4 at roughly 175 residues to RYR1 at 5,038 — a range no single size
filter can accommodate, and the reason the catalogue declares a size band per
family rather than one for the census.

### 12.4 Domain architecture is not a family call

The strongest quantitative statement this project can currently make about
annotation is a coverage measurement: feed every family its own declared
architecture back through the classifier's architecture tier, and ask whether
the family is named.

**17 of 29 census families are named. Twelve are not.** The twelve are not a
random sample — they are, almost exactly, the families the hazard registry
already identifies as architecturally indistinguishable from a sibling:

- the T-type calcium channels and CatSper, identical in architecture to the
  sodium channels (§3.2);
- both TRPV families, and TRPA, within the TRP division (§7.1);
- the nicotinic α7 group against the rest of its own family (§8.3);
- all four glutamate-receptor families — AMPA, kainate, NMDA and the plant
  GLRs — against one another (§8, §10.1);
- the two-pore channels and the plant CNGCs.

![](figures/fig8_architecture_traps.png)

**Figure 8 | The architecture traps, to scale.** The families that share an
architecture with something they are not, drawn with their declared domains
in proportion. Cav3 against Nav is the extreme case: identical domain content
in identical copy number, separated by the four residues of Figure 3.

"Domain architecture is not a family call" is a claim this review can attach a
number to, and the number is 12 of 29. What those twelve need is the motif
tier or the reference tier, and how far each gets there is measured by the
classifier benchmark rather than assumed (*pending: S1*).

### 12.5 Shared signatures, and the census boundary

Eighteen domain signatures in the catalogue are carried by more than one
family, and the interesting subset is those that cross the census boundary — a
domain that is evidence for a calcium-channel family and is also carried by
something the census does not count. `PF00520` in four copies spans Cav, Nav,
NALCN and CatSper. `PF02815` (MIR) spans ITPR, RYR and the
O-mannosyltransferase POMT1. `PF08016` spans TRPML, TRPP and polycystin-1.
`PF00027` spans CNG, HCN and plant CNGC.

![](figures/fig5_domain_matrix.png)

**Figure 5 | The domains that cross the boundary.** Every signature carried
by more than one catalogued family, with the families that carry it, and with
those crossing the census boundary marked — rendered from
`signature_sharing.tsv`. A marked row is a domain that is evidence for a
calcium-channel family and is also carried by something the census does not
count: a sodium channel, a Ca²⁺-activated channel, a pump, an auxiliary
subunit or a sensor.

Each of these is a place where architecture alone cannot decide membership,
and each is why the classification behind this review assigns by positive test
and records which tier of evidence decided.
