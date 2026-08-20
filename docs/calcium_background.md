# The biology this project rests on

Every statement is tagged with what it rests on:

- `[db]` — re-derived from a live database by an S0 script in this repo, or
  by the parent project (`../ion_channel_genes`) and inherited with its date.
- `[lit]` — established in the literature; the review's bibliography carries
  the resolved citation.
- `[open]` — a question this project answers, or leaves open and says so.

Read it before S1. The measured annotation facts near the bottom decide how
the census must be run.

---

## 1. Why calcium

Calcium is a signal because it is kept scarce. Cytosolic free Ca²⁺ sits near
100 nM against roughly 2 mM outside and ~0.5 mM in the ER, a gradient of four
orders of magnitude maintained by pumps and exchangers that do nothing else
`[lit]`. Opening a pore therefore produces an instant, large, local change,
and the cell reads it with EF-hand sensors that bind in the micromolar range.

Two consequences shape this catalogue:

1. **The gradient does the work a selectivity filter does elsewhere.** An IP3
   receptor with P_Ca/P_K around 6 is a perfectly good calcium-release channel
   because the ER gradient is enormous `[lit]`. Selectivity and physiological
   role are only loosely coupled.
2. **Calcium is toxic, so the pathways are heavily regulated and heavily
   duplicated.** Most census families carry Ca²⁺-dependent inactivation, and
   several are inhibited by the ion they conduct.

## 2. What a "calcium channel" is not a synonym for

`[lit]` Four distinct classes carry calcium in their names and are different
kinds of object. The catalogue separates all four:

| class | example | what it does |
|---|---|---|
| Ca²⁺ channel | CACNA1C | conducts Ca²⁺ down a gradient |
| Ca²⁺-activated channel | KCNMA1 (BK) | gated *by* Ca²⁺, conducts K⁺ |
| Ca²⁺ transporter | ATP2A1 (SERCA) | pumps Ca²⁺ against a gradient |
| Ca²⁺ sensor / buffer | CALM1 | binds Ca²⁺, conducts nothing |

## 3. Selectivity mechanisms — three unrelated solutions

`[lit]` **Cav: charged-ring, multi-ion.** Four glutamates (EEEE), one per
repeat, form a high-affinity site. Selectivity is achieved not by excluding
Na⁺ but by binding Ca²⁺ so tightly that micromolar Ca²⁺ blocks the Na⁺
current through the same pore; conduction then comes from ion–ion repulsion
in a single-file queue. The T-type channels read **EEDD** and are measurably
less selective.

`[lit]` **ORAI: one glutamate ring, six subunits.** E106 in human ORAI1.
E106Q abolishes selectivity; E106D converts the channel to a non-selective
one. P_Ca/P_Na exceeds 1000 — the most selective conductance in the plasma
membrane.

`[lit]` **MCU: the DIME motif.** A short acidic `WDxxE` ring in the inner
mitochondrial membrane, with nanomolar Ca²⁺ affinity. The most
Ca²⁺-selective channel measured anywhere, and the only one in this catalogue
whose filter is short enough to find with a regular expression `[db]`
(verified 2026-08-20: `WDIME` at position 260 of human MCU `Q8NE86`).

`[lit]` **TRPV5/6: an aspartate ring.** Four aspartates at the outer pore.
Neutralise them and the channel becomes non-selective. Its sister channels
TRPV1–4 share every Pfam accession and are non-selective.

## 4. The three timescales the census cannot see

`[lit]` Calcium permeability can be set after the genome has spoken:

1. **RNA editing.** ADAR2 converts the GRIA2 Q/R codon from glutamine to
   arginine; arginine at that position makes the AMPA receptor
   Ca²⁺-impermeable. Editing is near-complete in adult brain. ADAR2-null mice
   die of seizures and are rescued completely by a genomically edited GRIA2
   allele — the cleanest demonstration that the permeability is not in the
   DNA.
2. **Subunit composition.** NMDA receptors need GluN1 plus GluN2/GluN3;
   GluN3-containing receptors are much less Ca²⁺-permeable. TRPC1's behaviour
   differs alone and in TRPC1/TRPC4 or TRPC1/ORAI1 complexes.
3. **Splicing and use-dependence.** TRPV1's pore dilates during prolonged
   activation and its permeability changes with it; P2X7 dilates to pass
   molecules up to ~900 Da.

**This is the single most important limit on the method.** No sequence-level
approach can call these, and this project does not try (hazards **HC8**,
**HC16**).

## 5. Architecture and its limits

`[db]` (parent project, measured 2026-08-19 against InterPro)

- `PF00520` (Ion_trans) in four copies describes Cav, Nav, NALCN and CatSper
  equally well. CACNA1G (Cav3.1) carries `PF00520`×4 **and nothing else** —
  no Cav-specific domain at all.
- `PF08763` (Ca_chan_IQ) is present on Cav1/Cav2 and **absent** from Cav3.
- TRPV1, TRPV5, TRPA1 and TRPM2 carry `PF00520`; **TRPC3, TRPM8, MCOLN1,
  MCOLN2 and PKD2 carry none of it.** Their pores are modelled by `PF08344`,
  `PF18139` and `PF08016`.
- `PF08016` is carried by TRPML, TRPP **and** polycystin-1, which is not a
  pore.
- `PF02815` (MIR) is carried by ITPR, RYR **and** the O-mannosyltransferase
  POMT1.
- ITPR and RYR share all four of `PF08709`, `PF01365`, `PF08454`, `PF02815`;
  49 % of zebrafish `PF08709` records are ryanodine receptors.

`[db]` (this project, verified 2026-08-20 against live UniProt)

- Human Nav1.5 `Q14524` positions 372/898/1419/1711 read **DEKA**. The
  four-repeat projection anchor is valid.
- Human ORAI1 `Q96D31` position 106 is **E**.
- Human TRPV6 `Q9H1D0` is 765 aa and carries `TIIDGP` at 579–584, so its
  selectivity aspartate is **D582** — **not** the D542 of the literature's
  numbering, which refers to the short isoform. An anchor taken from a paper
  would have projected the wrong column silently.
- The canonical EF-hand regex finds 4 loops in calmodulin `P0DP23`, 4 in
  calbindin `P05937`, 2 in parvalbumin `P20472`, 2 in MICU1, 1 in STIM1 —
  and **0 in CACNA1C and 0 in MCU**.

## 6. Numbers worth remembering

`[lit]` / `[db]`

| quantity | value |
|---|---|
| cytosolic resting free Ca²⁺ | ~100 nM |
| extracellular Ca²⁺ | ~1.8–2 mM |
| ER/SR luminal free Ca²⁺ | ~0.3–0.8 mM |
| P_Ca/P_Na, ORAI1 | > 1000 |
| P_Ca/P_Na, Cav1.2 | > 1000 |
| P_Ca/P_Na, TRPV6 | > 100 |
| P_Ca/P_Na, nAChR α7 | ~10 |
| P_Ca/P_Na, nAChR muscle-type | ~0.1–1 |
| largest census protein | RYR1, 5,038 aa `[db]` |
| smallest census protein | rotavirus NSP4, ~175 aa `[lit]` |
| human genes catalogued / counted | 245 / 98 `[db]` |

## 7. Evolution — what is settled and what is not

`[lit]` The P-loop pore module is ancient and prokaryotic. The four-repeat
Cav/Nav architecture arose by two rounds of internal duplication from a
6TM ancestor, and the two-repeat TPC channels are the intermediate the story
predicts — `[open]` though their placement is a result this project's tier-2
trees are meant to produce, not an assumption.

`[lit]` Plants have no Cav homologue; fungi have CCH1 and no MCU. `[open]`
Whether MCU loss in *Saccharomyces* is one event or several, and how often
Ca²⁺ selectivity has been gained or lost within the TRP division, are
questions S10/S11 address.

`[open]` **How many times has a Ca²⁺-selective pore evolved?** The honest
current answer is "at least four, in unrelated folds (Cav, ORAI, MCU,
TRPV5/6)", and the number is a count of unconnected components in the tier-3
fold network rather than a clade count. It cannot be answered inside any one
tree.

## 8. Contested identities

`[open]` Recorded as contested in the catalogue rather than resolved by
omission:

- **TPC1/TPC2** — named calcium channels, and direct endolysosomal patch
  clamp finds a Na⁺-selective, PI(3,5)P₂-activated current (**HC13**).
- **PKD2** — established in the ER and the primary cilium, disputed in the
  plasma membrane.
- **CALHM4–6** — curated into the family by homology; only CALHM1 and CALHM3
  have direct functional data.
- **TMEM63A–C** — mechanosensitive for certain; divalent permeability less
  thoroughly measured than in the plant OSCA1.
- **Connexin hemichannels** — excluded, with the dissent recorded.
