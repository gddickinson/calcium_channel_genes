# Why the phylogeny is a forest

**Decision D27.** There is no alignment that contains an ORAI channel and a
ryanodine receptor, and `src/phylo/forest.py` refuses to build one.

This is a stronger statement in a calcium project than in the ion-channel
project it is ported from. There, the superfamilies were defined by fold and
the non-homology between them was a structural fact. **Here the subject
itself is a functional class assembled across folds**: "the calcium
channels" is a statement about permeability, and the pores that have it have
arisen independently at least a dozen times. A single tree of the subject
would not merely be badly rooted — it would be a category error rendered in
Newick.

---

## The three tiers

**Tier 1 — within a family.** Full-length alignment, rooted on the sister
family inside the same superfamily. Conventional, uncontroversial, and where
nearly every biologically useful result lives.

**Tier 2 — within a superfamily.** Pore-module alignment only
(`src/phylo/modules.py`), rooted on the superfamily's declared outgroup. The
tree is labelled a *pore-module tree* in every output, because that is what
it is.

**Tier 3 — between superfamilies.** Refused. `build_tier2()` raises
`NotAlignable` for any superfamily the catalogue marks `alignable=False`,
and there is no `build_tier3()`. Cross-superfamily comparison goes to
`src/phylo/network.py`, which produces a fold-similarity network with no
branch lengths and no support values.

## The trap specific to this project

A tier-2 tree of the `ploop` superfamily **necessarily contains the sodium
channels and the Ca²⁺-activated potassium channels.** Superfamilies in this
catalogue are defined by descent, not by ion, and Cav's nearest relatives are
Nav and NALCN.

The temptation is to drop the non-calcium members and present "the calcium
channel tree". That is exactly the error the protocol forbids: it removes
the outgroup that makes the tree rootable, it hides the fact that the
calcium channels are not monophyletic within their own superfamily, and it
produces a figure that asserts a clade that does not exist. **Every tier-2
figure shows the whole superfamily, with the census tier as a colour.**

## Rooting

| superfamily | rooted on | note |
|---|---|---|
| `ploop` | prokaryotic P-loop channels | the outgroup is a **sodium** channel; rooting a calcium tree requires a non-calcium channel, and that is recorded rather than hidden |
| `ca_release` | ITPR | RYR is the derived, larger family |
| `iglur` | non-vertebrate GLR / prokaryotic relatives | |
| `cysloop` | prokaryotic pentamers | |
| `orai`, `mcu`, `piezo`, `mca` | — | one family each; nothing to root against inside the catalogue |
| `largepore`, `viroporin_ca` | — | `alignable=False`; tier 2 refused |

## What replaces the tree nobody can build

The tier-3 network (`src/phylo/network.py`). Nodes are superfamilies, edges
are measured structural similarity (Foldseek TM-score between representative
predicted structures), and:

- **no edge ever carries a branch length or a bootstrap value**;
- **an unmeasured pair is recorded as unmeasured**, never as unrelated —
  `UNCONNECTED` names the superfamilies with no asserted relative anywhere in
  this catalogue, because "no relative measured" and "no relative exists" are
  different claims;
- the literature-asserted edges are seeded as `measured=False` and are
  replaced, not confirmed, by the S12 measurements.

The question **"how many times has a Ca²⁺-selective pore evolved?"** is
answered here, as a count of unconnected components plus a statement of what
was measured — and not inside any tree.

## Tools (D28)

MAFFT → trimAl → IQ-TREE 2 with ModelFinder and 1000 ultrafast bootstrap
replicates. Every command is recorded in `TreeRun` and written to
`run.json` beside the tree. A missing tool disables the step **loudly**:
`MafftUnavailable` is raised, a missing IQ-TREE writes the alignment and no
tree with the reason in `TreeRun.note`. There is no silent fallback to a
weaker method, ever — two incomparable methods in one figure is the failure
this prevents.
