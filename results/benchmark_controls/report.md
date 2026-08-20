# S1 — classifier control benchmark

*Generated 2026-08-20 14:14:07 by `scripts/s1_report.py` from the tables in `results/benchmark_controls` (D13). Panel: `controls_benchmark`. 68/69 targets classified in 1425.1 s.*

## Headline

| measure | value |
|---|---|
| recall (positives called correctly) | **38/48** (79.2%) |
| specificity (decoys not called as channels) | **18/20** (90.0%) |
| hazards exercised | 18/19 |
| four-repeat anchor validates | yes |
| MAFFT | v7.526 (2024/Apr/26) |
| reference panel | 102 exemplar sequences |
| panel proteins that are themselves exemplars | 67 — classified leave-one-out |

**Leave-one-out matters here.** 67 of the 68 panel proteins are themselves catalogue exemplars — both are drawn from the same curated gene lists — so without excluding the query's own accession the reference tier would score almost the whole panel against itself at 100 % identity and the benchmark would measure nothing but that overlap (**D29**).

## Panel members that were not measured

1 of the 69 panel members could not be fetched, so they are **absent from both numbers above rather than scored as failures**. A rate-limited request is not a classifier error, and letting one look like one would understate recall for a reason that has nothing to do with the method.

| panel member | expected family | why |
|---|---|---|
| CHRNA7 | nachr_ca | evidence fetch: URLError |

## Which tier made the call

This is the number that says whether the classifier is doing anything a nearest-neighbour lookup could not. A call made by the architecture or hazard tier rests on domain composition and works on a sequence with no close relative in the panel; a call made only by the reference tier does not.

| decisive tier | n calls |
|---|---|
| hazard | 28 |
| reference | 20 |
| none | 12 |
| architecture | 5 |
| motif | 3 |

| confidence | n |
|---|---|
| gold | 28 |
| bronze | 23 |
| silver | 14 |
| unassigned | 3 |

## Per-family recall

18/25 **positive** families were called correctly for every member. The 20 decoy families are scored by specificity, not recall — a decoy left `unassigned` is a success, and listing it as a recall failure would invert the result.

**Positive families the classifier did not call correctly:**

| family | n | correct | recall | called instead |
|---|---|---|---|---|
| catsper | 2 | 0 | 0.000 | unassigned |
| cng | 2 | 1 | 0.500 | unassigned |
| nachr_ca | 1 | 0 | 0.000 | unassigned |
| nmda | 2 | 0 | 0.000 | unassigned |
| tpc | 2 | 0 | 0.000 | unassigned |
| trpa | 1 | 0 | 0.000 | unassigned |
| trpm_ca | 2 | 1 | 0.500 | outofscope_trpm_monovalent |

**Decoys:** 20 families; 18 were left unassigned or called as themselves, 2 were called as something else.

| decoy family | called instead |
|---|---|
| outofscope_nachr_muscle | nachr_ca |
| outofscope_trpm_monovalent | trpm_ca |

Full table: `recall.tsv`.

## The four-repeat filter: does it separate Cav from Nav?

This is the census's load-bearing test. Cav1/2, Cav3, Nav and NALCN share a domain architecture that no rule can tell apart; the four residues projected from the Nav1.5 anchor are the only positive evidence separating them, and every downstream count depends on them reading correctly.

| gene | expected | called | projected filter | decisive tier | reads its family's signature? |
|---|---|---|---|---|---|
| CACNA1C | cav_hva | cav_hva | `EEEE` | hazard | **yes** |
| CACNA1S | cav_hva | cav_hva | `EEEE` | hazard | **yes** |
| CACNA1G | cav_lva | cav_lva | `EEDD` | motif | **yes** |
| CACNA1H | cav_lva | cav_lva | `EEDD` | motif | **yes** |
| CATSPER1 | catsper | unassigned | `---D` | — | non-call — see below |
| CATSPER2 | catsper | unassigned | `--D-` | — | non-call — see below |
| TPCN1 | tpc | unassigned | `--PN` | — | non-call — see below |
| TPCN2 | tpc | unassigned | `--AN` | — | non-call — see below |
| SCN5A | outofscope_nav | outofscope_nav | `DEKA` | hazard | **yes** |
| NALCN | outofscope_nalcn | outofscope_nalcn | `EEKE` | motif | **yes** |

**6/6 — every panel member that produces a complete four-residue string reads exactly the filter its catalogue entry declares, and no string is shared between a calcium family and a non-calcium one.** The remaining 4 are structural non-calls rather than failures. The non-calls are the families that structurally cannot produce one: TPC has two repeats rather than four, and CatSper is a heterotetramer whose four *different* subunits contribute one filter residue each — CATSPER1 projects `---D`, CATSPER2 `--D-`, CATSPER3 `-D--` and CATSPER4 `--D-`, so no single-sequence projection can read a CatSper filter and the joint reading is a task, not a gap (`anchor_power.tsv`).

*(58 other panel members also produced a projected string. They are not shown: a TRPV or a ryanodine receptor aligned against Nav1.5 yields four residues from positions that are not its filter, and reading them as evidence is the mistake the `applies_to` field exists to prevent. They are in `calls.tsv`.)*

## Do the other two anchors discriminate?

`classify()` runs exactly one anchor — the four-repeat locus. The TRPV and ORAI anchors are declared and verified but never projected onto anything, so `scripts/s1_anchor_power.py` projects each one over the families it claims to apply to and asks whether the residue it reads actually differs between permeability tiers. An anchor that reads the same residue for every member is not a test, and a hazard it was supposed to close stays open.

| anchor | reference | positions | projected | distinct strings | discriminates? |
|---|---|---|---|---|---|
| `four_repeat` | Hs_SCN5A Q14524 | 372/898/1419/1711 | 27 | 10 | **yes** |
| `trpv_ca_ring` | Hs_TRPV6 Q9H1D0 | 582 | 6 | 2 | **no** |
| `orai_e106` | Hs_ORAI1 Q96D31 | 106 | 3 | 1 | **no** |

- **`four_repeat`** — discriminates: no projected string is shared between permeability tiers
  - reads: ---D=CATSPER1; --AN=TPCN2; --D-=CATSPER2,CATSPER4; --PN=TPCN1; -D--=CATSPER3; DEKA=SCN1A,SCN2A,SCN3A,SCN4A,SCN5A,SCN8A,SCN9A,SCN10A,SCN11A; DENA=SCN7A; EEDD=CACNA1G,CACNA1H,CACNA1I; EEEE=CACNA1A,CACNA1B,CACNA1C,CACNA1D,CACNA1E,CACNA1F,CACNA1S; EEKE=NALCN
- **`trpv_ca_ring`** — DOES NOT discriminate: 'D' is read by members of more than one permeability tier
  - reads: D=TRPV5,TRPV6,TRPV1,TRPV3,TRPV4; M=TRPV2
- **`orai_e106`** — untested: every projected member is in one tier (ca_selective) — this panel cannot separate anything
  - reads: E=ORAI1,ORAI2,ORAI3

**1 anchor(s) were measured and do not separate the tiers they were written to separate.** That is recorded rather than quietly dropped: a hazard is only closed by a test, so the hazard this anchor was meant to close now says so in the registry and the anchor's call map has been emptied — it can no longer name a family.

**1 anchor(s) are untested, which is not the same as undiscriminating.** Every family in their scope sits in one permeability tier, so this panel has nothing for them to separate; measuring them needs a decoy that shares the fold, and that is a panel extension rather than a result.

## Per-hazard

A hazard is only closed by a test. `n touched` counts panel members whose classification involved that hazard's rule; a hazard with zero is not solved, it is **untested** by this panel.

| hazard | severity | n touched | correct | wrong | examples | what it is |
|---|---|---|---|---|---|---|
| HC1 | high | 6 | 6 | 0 | — | Cav, Nav, NALCN and CatSper share one domain architectur |
| HC2 | high | 5 | 5 | 0 | — | Sixteen human CACN* genes are auxiliary subunits, seven  |
| HC3 | high | 4 | 4 | 0 | — | IP3 receptors and ryanodine receptors share every diagno |
| HC4 | low | 5 | 5 | 0 | — | The MIR domain is shared with the O-mannosyltransferases |
| HC5 | medium | 3 | 3 | 0 | — | The gate is in another organelle: STIM is not ORAI |
| HC5b | low | 4 | 4 | 0 | — | Store-operated entry is a mechanism, not a family |
| HC6 | medium | 3 | 3 | 0 | — | A uniporter subunit can be a pore and still not conduct |
| HC7 | high | 12 | 11 | 1 | Q8TD43 | Most TRP families carry no `PF00520` at all |
| HC7b | high | 4 | 4 | 0 | — | Ca2+ selectivity varies a hundredfold inside one TRP fam |
| HC8 | high | 4 | 4 | 0 | — | Calcium permeability is not always in the genome |
| HC9 | medium | 5 | 5 | 0 | — | `PF08016` covers TRPML, TRPP *and* polycystin-1 |
| HC10 | medium | 1 | 1 | 0 | — | The CATSPER symbol root covers four pores and seven acce |
| HC11 | high | 4 | 4 | 0 | — | Calcium pumps and exchangers are calcium proteins and no |
| HC12 | high | 4 | 4 | 0 | — | 'Calcium binding' is one keyword away from 'calcium cond |
| HC13 | medium | 0 | 0 | 0 | — | The two-pore *calcium* channel may be sodium-selective |
| HC14 | high | 5 | 5 | 0 | — | The T-type filter reads EEDD, not EEEE |
| HC15 | high | 5 | 3 | 2 | O94759;Q8TD43 | Ca2+-activated channels are named for calcium and conduc |
| HC16 | high | 5 | 4 | 1 | P02708 | Ca2+ permeability varies across sister families with one |
| HC17 | medium | 4 | 4 | 0 | — | The plant glutamate receptor-like channels are architect |

**1 hazard(s) carry no measurement from this panel:** HC13. Extending the panel to exercise them is a task, not a footnote.

## The decoys no rule can name

`derived_rules()` generates a rule from every **census** family's declared architecture, so a control family is recognisable only if somebody wrote a hazard rule for it by hand. S0 measured which ones have none (`results/s0_baseline/rule_targets.tsv`). Those decoys cannot be *named*; they can only be left `unassigned` or placed by reference identity. Leaving them unassigned is the correct outcome — the census asks whether a protein is a calcium channel, and `unassigned` answers no — so this section reports them rather than scoring them as misses.

| control family | panel member | called | confidence | rejected as a channel? |
|---|---|---|---|---|
| `assoc_release_reg` | CASQ2 | unassigned | unassigned | yes |
| `outofscope_connexin` | GJA1 | unassigned | unassigned | yes |
| `outofscope_tric` | TMEM38A | unassigned | unassigned | yes |

## How a decoy gets named as a calcium channel

One decoy was not merely accepted — it was **named**. TRPM4 is a Ca²⁺-impermeable member of the TRPM family and the architecture tier called it `trpm_ca` outright. The cause is not a bad annotation: the catalogue records, correctly, that TRPM4 and TRPM5 carry the same Pfam accessions as their Ca²⁺-permeable siblings. It is `derived_rules()`, which iterates `census_families()` only, so a domain declared at family level by both a census family and a control family yields exactly one rule — pointing at the census family — and the control matches it with nothing to tie against. "Ties are ambiguity, never a coin toss" cannot fire when only one side was allowed to enter.

`scripts/s1_rule_leakage.py` measures the whole exposure rather than the one instance: **37 architecture matches into 6 control families, of which 36 are superfamily-only** — a sodium channel really is a P-loop channel, and saying so is correct — **and 1 names a control as a census family**.

| control family | named as | via rule | requires | priority | hazard rule that would outrank it |
|---|---|---|---|---|---|
| `outofscope_trpm_monovalent` | `trpm_ca` | `cat-trpm_ca` | `PF18139` | 40 | none |

This is the third instance of one shape — `PF00027` naming plant CNGC as animal CNG, the HCN defect before it, now `PF18139`. The fix is not another hand-written hazard rule; it is letting control families generate rules so the shared domain produces a tie. That is a change to the rule generator with a blast radius across every call in this table, so it is recorded as an emergent task with the measurement attached rather than made inside a benchmark session.

## Panel coverage

25/29 census families have at least one member in this panel. Coverage counts what the panel **contains**, not what the classifier managed to call — counting calls would hide a family whose every member was left `unassigned` behind a coverage gap, which is the opposite of reporting it.

| family | superfamily | human genes | in panel | called as |
|---|---|---|---|---|
| `cav_hva` | ploop | 7 | 2 | 2 |
| `cav_lva` | ploop | 3 | 2 | 2 |
| `catsper` | ploop | 4 | 2 | 0 |
| `cng` | ploop | 6 | 2 | 1 |
| `tpc` | ploop | 2 | 2 | 0 |
| `trpv_ca` | ploop | 2 | 2 | 2 |
| `trpv_ns` | ploop | 4 | 2 | 2 |
| `trpc` | ploop | 6 | 2 | 2 |
| `trpm_ca` | ploop | 6 | 2 | 2 |
| `trpa` | ploop | 1 | 1 | 0 |
| `trpml` | ploop | 3 | 2 | 2 |
| `trpp` | ploop | 3 | 2 | 2 |
| `itpr` | ca_release | 3 | 2 | 2 |
| `ryr` | ca_release | 3 | 2 | 2 |
| `orai` | orai | 3 | 2 | 2 |
| `mcu` | mcu | 2 | 2 | 2 |
| `vdac` | porin | 3 | 2 | 2 |
| `nachr_ca` | cysloop | 3 | 1 | 1 |
| `ampa` | iglur | 4 | 2 | 2 |
| `kainate` | iglur | 5 | 2 | 2 |
| `nmda` | iglur | 7 | 2 | 0 |
| `p2x` | p2x | 7 | 2 | 2 |
| `piezo` | piezo | 2 | 2 | 2 |
| `calhm` | largepore | 6 | 2 | 2 |
| `osca_tmem63` | osca | 3 | 2 | 2 |

**Families with no panel member: `glr_plant`, `cngc_plant`, `mca_plant`, `viroporin_ca`.** These are the census's non-human families — the plant glutamate-receptor-like channels, the plant CNGCs, plant MCA and the viral viroporins — plus any human family the preset omits. A benchmark built from human gene symbols cannot measure them, and a census that spans plants, fungi, protists and viruses cannot claim their recall from this table. They are S3's and S21's to measure.

## Every call

`calls.tsv` carries one row per protein with the full evidence string from every tier, including the tiers that did not decide. The point of keeping the losing evidence is that a wrong call is diagnosable without re-running anything.

**1 call(s) had disagreeing tiers:**

| protein | gene | expected | called | confidence | conflict |
|---|---|---|---|---|---|
| O94759 | TRPM2 | trpm_ca | outofscope_trpm_monovalent | silver | architecture=trpm_ca;reference=outofscope_trpm_monovalent |

