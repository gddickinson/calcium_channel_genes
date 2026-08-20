# Session briefs — what each ledger task actually does

One brief per task: goal, steps, completion criteria, outputs. Read the
brief for the task you are about to work, then work only that task
(`PUBLICATION_ROADMAP.md`, session protocol step 6).

---

## S0 — Catalogue verification baseline

**Goal.** Re-derive every claim the catalogue makes against live databases,
and report the mismatches without fixing them.

**Steps**
1. `python3 -m src.catalogue` and `python3 scripts/selftest.py` — both clean.
2. `python3 scripts/s0_catalogue_verify.py` (add `--quick` to skip protein
   counts on a first pass). Writes six TSVs plus `reference_panel.fasta`
   into `results/s0_baseline/`.
3. Re-verify the three projection anchors explicitly: Nav1.5 `Q14524` must
   read `DEKA` at 372/898/1419/1711; TRPV6 `Q9H1D0` must read `D` at 582;
   ORAI1 `Q96D31` must read `E` at 106. A failure here is a stop, not a
   warning — every filter call downstream depends on it.
4. Read `exemplar_architecture.tsv` line by line. Each difference between
   declared and observed signatures is either an expected subfamily-level
   absence (record it in the family's `notes`) or a catalogue correction.
5. `python3 scripts/s0_report.py` then `python3 scripts/s0_figures.py`.

**Completion criteria**
- Every Pfam accession resolves and its short name matches what the
  catalogue wrote, or the mismatch is recorded.
- Every exemplar resolves to an accession; the 45 that carry none in the
  code are resolved live and the table is committed.
- Every taxon id resolves.
- `reference_panel.fasta` exists and covers every census family.
- `report.md` renders from the tables, with zero hand-written numbers.

**Watch for.** The six `Provenance.CURATED` accessions (`PF04749`,
`PF02714`, `PF13967`, `PF01452`, `PF07766`, `PF10613`) are the most likely
errors in the file. And **S0 does not verify the permeability values** — no
database holds them; that is S1b.

---

## S1 — Classifier control benchmark

**Goal.** Measure the classifier on a panel of positives and the decoys that
look like them, and attribute every correct call to the tier that made it.

**Steps**
1. `python3 scripts/s1_toolchain.py` — every external binary probed and
   recorded before anything depends on it (**D28**).
2. `python3 run.py --classify-preset controls_benchmark --save-results`.
3. `python3 scripts/s1_benchmark.py` then `python3 scripts/s1_report.py`.

**Completion criteria**
- Per-family recall, per-hazard specificity, and the **per-tier
  attribution** are all reported.
- `verify_anchor()` passed before any filter result was reported.
- Every one of the eighteen hazards is either exercised by a panel member or
  listed as untested. **A hazard no panel member exercises is untested, not
  solved.**
- Leave-one-out is on (**D29**) and the panel/exemplar overlap is reported.

**The three results that matter most.**
1. **The per-tier breakdown.** If most correct calls come from the reference
   tier, the classifier is a nearest-neighbour lookup and will fail on
   exactly the sequences a census exists for.
2. **Does the four-repeat filter separate Cav from Nav?** This is the
   census's load-bearing test. Anything below 100 % on the panel needs an
   explanation before S2 runs.
3. **Does the TRPV anchor discriminate at all?** TRPV1–4 carry acidic
   residues in the outer pore too. If projecting TRPV6's D582 returns `D`
   for all of them, HC7b has no positive test — record that, do not quietly
   drop it.

---

## S1b — Permeability audit

**Goal.** The catalogue's weakest claims, checked. Every `P_Ca/P_Na` string
traced to a resolved reference with the method that produced it.

**Steps**
1. For each census family, find the primary measurement behind its
   `Permeability.p_ca_over_p_na`, resolve it through
   `scripts/s0_review_refs.py`, and record the reference key in
   `Permeability.note`.
2. Where the literature reports a range or disagrees, keep the range —
   collapsing it to a point value is the failure this audit exists to
   prevent.
3. Re-examine the tier boundaries against what the audit found, and record
   any family that moves tier, with the reason, in `FINDINGS.md`.

**Completion criteria.** Every census family's permeability claim carries a
resolved reference key or is explicitly marked `Provenance.OPEN`. No claim
remains `LIT`-without-a-source.

---

## S2 — Uncapped enumeration

**Goal.** The census's search space, enumerated rather than sampled.

**Steps.** `run_domain_scan()` over the union of every catalogued pore
signature (**never `PF00520` alone** — hazard HC7), paginating to InterPro's
own count with `strict` failure, then a positive family call on every
record.

**Completion criteria.** Every record classified or explicitly
`unassigned`; the count of records the enumeration returned that the
classifier could not place is reported as a number, not hidden.

**Watch for.** `PF00520` returns the sodium channels and the Ca²⁺-activated
potassium channels alongside the calcium channels. Separating them is the
classifier's job, and the fraction of the returned set that is *not* a
calcium channel is itself a headline result (Q2).

---

## S4 / S5 — Proteome and genome scope

Bulk tasks. **Neither can start until the external drive is attached**
(`python3 -m src.utils.data_root --require`). S4 declares the
reference-proteome manifest — the census denominator. S5 sweeps the genomes
for what the proteomes miss, and every absence claim must pass both D4 bars.

---

## S7 / S8 — The forest

**S7** builds a tier-1 tree per census family. **S8** builds a tier-2
pore-module tree per alignable superfamily and the tier-3 fold network for
the refused ones.

**The rule that will be tempting to break.** A tier-2 `ploop` tree contains
the sodium channels and the Ca²⁺-activated potassium channels, because the
superfamily is defined by descent. Do not drop them to make "the calcium
channel tree" — that hides the non-monophyly which is one of this project's
findings, and it removes the outgroup that makes the tree rootable
(**D27**).

---

## S12 — Structures, and Q6

**Goal.** How many times has a Ca²⁺-selective pore evolved?

The answer is a count of unconnected components in the tier-3 fold network
plus a statement of what was measured — **not** a clade count, and not
obtainable from any tree. `UNCONNECTED` in `src/phylo/network.py` names the
superfamilies with no asserted relative; each needs a measured Foldseek
result before it can be called unrelated rather than unmeasured.

---

## S23 — The literature review

**Goal.** `docs/channel_review_2026.md`, generated.

**Steps.** Write `docs/review/*.md`. Cite by stable key (`[catterall2011]`).
Run `python3 scripts/s0_review_refs.py` to resolve every source against
Europe PMC; then `python3 scripts/s0_review_build.py --check` and, when
clean, `--pdf`.

**The absolute rule.** A cited key with no verified reference is a build
error. The bibliography is machine-generated from live records and prose may
cite only keys that survived resolution. Never hand-edit
`docs/channel_review_2026.md` — it is generated.

---

## S14a / S14b — Manuscript and deposit

`scripts/s14_assemble.py` runs the ordered stages and exits non-zero on a
failed claim. Every load-bearing number needs a claim row in
`scripts/s14_claims.py` (**D12**). S14b is human-gated: Zenodo DOI, the D2
private→public flip, preprint upload.
