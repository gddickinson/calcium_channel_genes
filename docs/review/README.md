# The review's source files

`docs/channel_review_2026.md` is **generated**. Never edit it.

Edit the numbered section files in this directory and re-run:

```bash
python3 scripts/s0_review_refs.py        # resolve every source against Europe PMC
python3 scripts/s0_review_build.py --check
python3 scripts/s0_review_build.py --pdf
```

## How citations work

Cite by stable key, in square brackets, comma-separated for multiples:

```
The EEEE locus was identified by mutagenesis [yang1993], and the
structural basis followed two decades later [wu2016, tang2014].
```

Keys come from `scripts/review_sources.py` and are resolved against Europe
PMC by `s0_review_refs.py`, which writes
`results/s0_baseline/references.tsv`. A record is accepted only if its
returned title is ≥ 90 % similar to the one requested, so a misremembered
paper fails loudly instead of becoming a plausible bibliography entry.

**A cited key with no verified reference is a build error.** The build
renumbers keys into order of first appearance, so adding a paper mid-section
does not renumber anything.

## Planned sections (task S23)

| file | covers |
|------|--------|
| `00_frontmatter.md` | title, abstract, keywords |
| `01_introduction.md` | why calcium; why "calcium channel" is not a clade |
| `02_selectivity.md` | the four unrelated filter mechanisms: EEEE, E106, DIME, the aspartate ring |
| `03_cav.md` | the voltage-gated calcium channels, and Nav as their nearest relative |
| `04_release.md` | ITPR, RYR, TPC, TRPML — release from stores |
| `05_soce.md` | ORAI and STIM: a gate in another organelle |
| `06_mitochondrial.md` | MCU, VDAC, and fifty years between current and gene |
| `07_trp.md` | the TRP division, and permeability varying within a family |
| `08_ligand_gated.md` | AMPA/kainate/NMDA, nicotinic α7, P2X — and RNA editing |
| `09_mechano.md` | Piezo, OSCA/TMEM63, plant MCA |
| `10_nonanimal.md` | plants without Cav; fungi without MCU; viral viroporins |
| `11_boundary.md` | Ca²⁺-activated channels, pumps, exchangers, sensors — what the word costs |
| `12_annotation.md` | what the databases record — this project's own measurements |
| `13_evolution.md` | how many times a Ca²⁺-selective pore has evolved |
| `14_disease.md` | channelopathies, and the ones caused by non-channels |
| `15_open.md` | what is unresolved |
| `16_methods.md` | how the census, classification and phylogeny were done |

Nothing here is written yet. **Do not write the review before S0 and S9 have
run** — its measured sections are supposed to report this project's own
results, not restate the literature.
