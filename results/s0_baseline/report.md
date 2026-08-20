# S0 — catalogue verification baseline

*Generated 2026-08-20 10:53:14 by `scripts/s0_report.py` from the tables in `results/s0_baseline`. Nothing here is hand-written (D13). 533 live requests, 0 failure(s), 721.8 s.*

## What the catalogue claims

| quantity | n |
|---|---|
| superfamilies | 17 |
| families total | 49 |
| families census | 29 |
| families control | 20 |
| human genes census | 98 |
| human genes catalogued | 245 |
| genes ca selective | 28 |
| genes ca permeable | 50 |
| genes ca conditional | 9 |
| genes ca release | 11 |
| exemplars | 102 |
| exemplars with accession | 102 |
| signatures | 87 |
| shared signatures | 18 |
| hazards | 19 |

The census denominator is **98 human genes encoding a Ca2+-conducting pore** across **29 families** in **17 superfamilies**, with **20 further families catalogued specifically so they can be excluded** — auxiliary subunits, Ca2+ pumps and exchangers, EF-hand sensors and channels that are gated by calcium without conducting it.

**That denominator is never quoted flat (D31).** Calcium membership is a permeability, not a clade, so the census is reported in tiers and a reader can see exactly how much of the count rests on non-selective channels and on families whose permeability the genome does not encode:

| tier | families | human genes |
|---|---|---|
| ca_selective | 7 | 28 |
| ca_permeable | 15 | 50 |
| ca_conditional | 2 | 9 |
| ca_release | 5 | 11 |

## 1. Internal consistency

`src.catalogue.validate()` is clean: every family points at a superfamily that exists, no human gene is claimed by two census families, every exemplar is resolvable, every `confusable_with` and every hazard family reference matches a catalogue key.

## 2. Pfam accessions

87 distinct accessions declared across the catalogue; **87 verified (100 %)**, 0 missing from InterPro, 0 carrying a different short name.

**The ten largest search spaces** — how many UniProt proteins carry each signature. This is the census's raw denominator, and the reason S2 is a task of its own:

| accession | name | UniProt proteins | families |
|---|---|---|---|
| PF12796 | Ank_2 | 542,446 | 4 |
| PF13499 | EF-hand_7 | 239,776 | 1 |
| PF00023 | Ank | 210,168 | 2 |
| PF00520 | Ion_trans | 206,115 | 17 |
| PF00122 | E1-E2_ATPase | 198,722 | 1 |
| PF00027 | cNMP_binding | 184,852 | 3 |
| PF13246 | Cation_ATPase | 118,075 | 1 |
| PF00622 | SPRY | 113,796 | 1 |
| PF01094 | ANF_receptor | 101,599 | 5 |
| PF00254 | FKBP_C | 99,670 | 1 |

## 3. Exemplars

102 exemplars declared; 100 resolved cleanly, 0 unresolvable, 0 with a declared accession that names a different gene, 0 where UniProt's primary symbol differs from the catalogue's.

| status | n |
|---|---|
| ok | 100 |
| DECLARED_GENE_IS_SYNONYM | 1 |
| NO_GENE_NAME_IN_UNIPROT | 1 |

Every exemplar that did not resolve cleanly:

| family | label | gene | species | declared | resolved | resolved gene | status |
|---|---|---|---|---|---|---|---|
| osca_tmem63 | At_OSCA1.1 | OSCA1.1 | Arabidopsis thaliana | Q9XEA1 | Q9XEA1 | OSCA1 | DECLARED_GENE_IS_SYNONYM |
| viroporin_ca | RV_NSP4 | NSP4 | Rotavirus A | P04512 | P04512 | — | NO_GENE_NAME_IN_UNIPROT |

`reference_panel.fasta` holds 102 sequences — the panel the classifier's reference tier scores against.

## 4. Declared architecture vs observed

102 exemplars had their Pfam architecture re-derived. **72 match the catalogue's declaration exactly, 30 differ only at signatures the catalogue does not promise every member carries, and 0 are missing a signature declared at `FAMILY` level.**

The split matters and is the reason this table is not one column (**D25**). A `FAMILY`-level signature is a claim that *every* member carries it, so its absence from an exemplar is a catalogue error. A `SUBFAMILY` signature says only that some members carry it, and `ACCESSORY` and `SUPERFAMILY` signatures make no per-member promise at all — reporting those absences as mismatches would bury the real errors in noise. Hazard **HC7** is the canonical case: most TRP families carry no `PF00520`, which is a fact about Pfam's coverage and not a fault in the catalogue.

**Expected absences** (subfamily-, accessory- or superfamily-level only):

| family | exemplar | declared but not observed |
|---|---|---|
| cav_hva | Hs_CACNA1S | PF16885 |
| cav_hva | Hs_CACNA1A | PF16885 |
| cng | Hs_CNGB1 | PF16526 |
| trpv_ns | Hs_TRPV4 | PF12796 |
| trpc | Dm_trp | PF23317 |
| trpm_ca | Hs_TRPM8 | PF00520,PF02816,PF16519 |
| trpm_ca | Hs_TRPM2 | PF02816,PF16519,PF23317 |
| trpm_ca | Hs_TRPM7 | PF00520 |
| cngc_plant | At_CNGC4 | PF00027 |
| viroporin_ca | RV_NSP4 | PF02723,PF11289 |
| viroporin_ca | SARS2_E | PF01452,PF11289 |
| viroporin_ca | SARS2_ORF3a | PF01452,PF02723 |
| assoc_cav_aux | Hs_CACNB1 | PF00092,PF00822,PF08473 |
| assoc_cav_aux | Hs_CACNA2D1 | PF00625,PF00822,PF12052 |
| assoc_cav_aux | Hs_CACNG2 | PF00092,PF00625,PF08473,PF12052 |
| assoc_stim | Hs_STIM1 | PF13202 |
| assoc_stim | Hs_STIM2 | PF13202 |
| assoc_mcu_reg | Hs_MICU1 | PF10161 |
| assoc_mcu_reg | Hs_SMDT1 | PF13833 |
| assoc_release_reg | Hs_CASQ2 | PF00254 |
| assoc_release_reg | Hs_FKBP1A | PF01216 |
| outofscope_kca | Hs_KCNMA1 | PF02254,PF02888,PF03530,PF07885 |
| outofscope_kca | Hs_KCNN2 | PF00520,PF02254,PF03493 |
| outofscope_connexin | Hs_GJA1 | PF00876 |
| outofscope_connexin | Hs_PANX1 | PF00029 |
| transporter_ca_exchanger | Hs_SLC8A1 | PF07766 |
| transporter_ca_exchanger | Hs_SLC8B1 | PF07766 |
| transporter_ca_exchanger | Hs_LETM1 | PF01699 |
| nonchannel_efhand | Hs_CALM1 | PF00036 |
| nonchannel_efhand | Hs_PVALB | PF00036 |

## 5. Projection anchors

3 anchors re-verified against live UniProt; 3 read what the catalogue claims, 0 do not. Every filter call this project makes is a projection from one of these references, so an anchor that has drifted makes each of those calls silently wrong — and `verify_anchor()` refuses to project rather than guess (**D26**, **D28**). The TRPV6 row is why the check exists: the aspartate is at **D582**, not the literature's D542, because the canonical entry is the long isoform.

| anchor | reference | accession | positions | expected | observed | length aa | context | verified |
|---|---|---|---|---|---|---|---|---|
| four_repeat | Hs_SCN5A | Q14524 | 372/898/1419/1711 | DEKA | DEKA | 2016 | 368-LMTQDCWER-376; 894-ILCGEWIET-902; 1415-VATFKGWMD-1423; 1707-ITTSAGWDG-1715 | yes |
| trpv_ca_ring | Hs_TRPV6 | Q9H1D0 | 582 | D | D | 765 | 578-LTIIDGPAN-586 | yes |
| orai_e106 | Hs_ORAI1 | Q96D31 | 106 | E | E | 301 | 102-VAMVEVQLD-110 | yes |

## 6. Shared signatures — the hazard registry's evidence

18 signatures are carried by more than one family. **10 of them cross the census boundary** — a domain that is evidence for a calcium-channel family and is also carried by something the census does not count: a sodium channel, a Ca2+-activated channel, a pump, an auxiliary subunit or a sensor. This table is the hazard registry's empirical basis, and every row in it is a place where architecture alone cannot decide membership (**D25**).

| accession | families | statuses |
|---|---|---|
| PF00520 | cav_hva,cav_lva,catsper,cng,tpc,trpv_ca,trpv_ns,trpm_ca,trpa,itpr,ryr,cngc_plant | channel,channel_contested,out_of_scope |
| PF01094 | ampa,kainate,nmda,glr_plant,nonchannel_casr_gpcr | channel,non_channel_homolog |
| PF00060 | ampa,kainate,nmda,glr_plant | channel |
| PF10613 | ampa,kainate,nmda,glr_plant | channel |
| PF12796 | trpv_ca,trpv_ns,trpc,trpa | channel |
| PF00027 | cng,cngc_plant,outofscope_hcn | channel,out_of_scope |
| PF02815 | itpr,ryr,nonchannel_pomt | channel,non_channel_homolog |
| PF08016 | trpml,trpp,assoc_polycystin1 | channel,channel_associated |
| PF00023 | trpv_ca,trpv_ns | channel |
| PF01365 | itpr,ryr | channel |
| PF02931 | nachr_ca,outofscope_nachr_muscle | channel,out_of_scope |
| PF02932 | nachr_ca,outofscope_nachr_muscle | channel,out_of_scope |
| PF08454 | itpr,ryr | channel |
| PF08709 | itpr,ryr | channel |
| PF18139 | trpm_ca,outofscope_trpm_monovalent | channel,out_of_scope |

## 7. Taxonomy

53 taxon ids checked against the UniProt taxonomy service; 53 confirmed, 0 mismatched.

## 8. What this does not verify

- **Family membership.** That `CACNA1C` belongs to `cav_hva` is a literature assignment. S1 tests whether the classifier reproduces it; nothing here tests whether it is right.
- **Calcium permeability.** Every P_Ca/P_Na in the catalogue is a literature value with a method attached, and none of it is recoverable from sequence (hazards **HC8**, **HC16**). No database check can confirm a permeability, and this project never predicts one. Auditing those numbers against their sources is S1b's job, not S0's.
- **The tier boundaries.** Whether a P_Ca/P_Na of 3 counts as `ca_permeable` is a decision recorded in `docs/scope_and_boundaries.md`, not a fact. S0 checks that every census family carries evidence for the tier it claims; it cannot check that the tier is the right one.
- **Completeness.** A verified catalogue is not a complete one. Whether these are the right human genes is the question S2 answers, and it is answered against a declared search space, never against "all calcium channels".

