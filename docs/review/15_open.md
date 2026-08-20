## 15. What is unresolved

This section separates three kinds of uncertainty that are easy to conflate:
identities that are genuinely disputed in the literature, quantities this
project has not yet measured, and limits that no sequence-based method can
pass.

### 15.1 Contested identities

Recorded in the catalogue as contested rather than resolved by omission:

- **TPC1/TPC2** — named as calcium channels and reported as NAADP-gated
  calcium release from acidic stores [calcraft2009]; direct endolysosomal
  patch clamp finds a PI(3,5)P₂-activated, Na⁺-selective current
  [wang2012]. Counted, in the release tier, with the dispute recorded.
- **PKD2** — established in the ER and the primary cilium, disputed in the
  plasma membrane.
- **CALHM4–6** — curated into the family by homology; only CALHM1 and CALHM3
  have direct functional data [taruno2013, ma2018].
- **TMEM63A–C** — mechanosensitive for certain; divalent permeability less
  thoroughly established than in the plant OSCA1.
- **Connexin hemichannels** — excluded on the ground that the physiological
  state is the docked junction, which connects two cytosols rather than
  crossing a gradient. Undocked hemichannels do pass calcium, and the dissent
  is recorded rather than resolved by omission. CALHM1 shares structural
  features with connexins, pannexins and innexins, which is why the two sit
  adjacent in the catalogue [siebert2013].

### 15.2 The weakest claims in this review

Two classes of statement here rest on less than the rest.

**Every permeability ratio is a literature value, and no database holds one.**
The tiers that organise this entire review — selective, permeable,
conditional, release — are boundaries drawn on P_Ca/P_Na values that were
recorded by hand from the literature. Nothing in the verification described in
§12 checks them, because no database contains them. Tracing each one to a
resolved source with its method attached is a separate audit, and until it
runs, the tier boundaries rest on claims that nothing has checked
(*pending: S1b*). This is stated here as prominently as it is because a reader
should discount the tier assignments accordingly.

**Permeability ratios are not single numbers.** They are measured in a
particular cell, at a particular divalent concentration, and often per subunit
combination. The catalogue stores them as strings — `">1000"`, `"~1-10"`,
`"~0.5-4 (P2X1 and P2X4 highest)"` — because turning a range measured in one
cell type into a float would invent a precision nobody measured, and the
census boundary would then rest on it.

### 15.3 Limits no sequence method can pass

Three things are not recoverable from a genome, and this project does not
attempt them:

1. **RNA editing.** Whether an AMPA receptor conducts calcium is set by ADAR2
   on one `GRIA2` codon (§8.2).
2. **Subunit composition.** NMDA receptor permeability depends on whether
   GluN2 or GluN3 is present; TRPC1 behaves differently alone and in
   complexes.
3. **Use-dependent pore dilation.** TRPV1 and P2X7 change their permeation
   properties during prolonged activation (§8.4).

A census that reported a permeability for every gene would be asserting things
about these cases that no data supports. The catalogue therefore **never
predicts a permeability** — the classifier returns a family, a superfamily, a
status and an audit trail, and no calcium claim at all.

### 15.4 Open measurements

Finally, the results this review is waiting on, each attached to the task that
produces it:

| question | status |
|---|---|
| Per-family recall and per-hazard specificity of the classifier | *pending: S1* |
| Does the TRPV aspartate anchor actually separate TRPV5/6 from TRPV1–4? | *pending: S1* |
| Every P_Ca/P_Na traced to a source with its method | *pending: S1b* |
| What domain search alone would have missed, per superfamily | *pending: S15* |
| CatSper's filter, read by joint projection across four subunits | *pending: S9* |
| Is the filter congruent with the pore-module tree? | *pending: S9* |
| Do the nicotinic α7/α9/α10 subunits form a clade? | *pending: S7* |
| How many times has a Ca²⁺-selective pore evolved? | *pending: S12, S18* |
| Is Cav's absence from plants a loss or a never-had? | *pending: S5, S10* |
