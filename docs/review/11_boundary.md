## 11. What the word "calcium" costs

The largest source of error in a calcium census is not a difficult
phylogenetic call. It is the word. "Calcium" attaches to proteins that are
gated by calcium, that pump calcium, that exchange calcium, that bind
calcium, that sense calcium, and that assemble with calcium channels — and to
almost none of these does it attach because they conduct calcium down a
gradient through a pore. This section works through the excluded set, because
in this project the excluded set is a deliverable rather than housekeeping:
the catalogue holds **245 human genes and counts 98**, and the 147 it does
not count are what a search for "calcium channel" returns.

### 11.1 Gated by calcium, conducting something else

The Ca²⁺-*activated* channels are the most-cited contaminant.

| family | genes | conducts |
|---|---|---|
| BK | `KCNMA1` | K⁺ |
| SK / IK | `KCNN1`–`KCNN4` | K⁺ |
| TMEM16A/B | `ANO1`, `ANO2` | Cl⁻ |
| TRPM4/5 | `TRPM4`, `TRPM5` | monovalent cations |

They are opened by cytosolic calcium and they carry no calcium current. They
appear in IUPHAR class names, in review titles and in gene-set annotations
with "calcium" in them, and a keyword-driven list counts every one.

For the potassium channels a positive test exists and is decisive: the
T-x-G-Y-G filter says the protein conducts K⁺, without reference to a name or
a symbol. For TRPM4 and TRPM5 no such test exists (§7.2), and the exclusion is
recorded as a literature call.

### 11.2 Transporters

Nineteen human genes move calcium across membranes by mechanisms that are not
conduction:

- **P-type ATPases** — SERCA (`ATP2A1`–`ATP2A3`), PMCA (`ATP2B1`–`ATP2B4`)
  and SPCA (`ATP2C1`, `ATP2C2`) — hydrolyse ATP and move calcium against its
  gradient through an alternating-access cycle. SERCA is among the
  best-characterised membrane proteins in structural biology
  [toyoshima2000, brini2009].
- **Na⁺/Ca²⁺ exchangers** — NCX (`SLC8A1`–`SLC8A3`), NCKX (`SLC24A1`–
  `SLC24A5`) and NCLX (`SLC8B1`) — couple calcium movement to the sodium
  gradient [blaustein1999, palty2010].

These are excluded on mechanism, not on importance; several move more calcium
per cell than most census families do. The distinction being drawn is between
a pore that is open at both ends at once and a cycle that is not.

### 11.3 Sensors and buffers, which conduct nothing

Calmodulin, calbindin, parvalbumin, the S100 proteins and the calcium-sensing
receptor CASR all bind or sense calcium and none conducts it
[brown1993, brown2001]. They are catalogued as non-channel homologues, and
they matter to a census for a specific reason: they are what an EF-hand-driven
or annotation-driven search returns.

The positive test here is the EF-hand itself, used as a *detector of decoys*
rather than as a veto (§5.2).

### 11.4 The subunits

Forty human genes encode proteins that assemble with calcium channels and
form no pore: the Cav β, α2δ and γ subunits, the CatSper accessories, STIM1
and STIM2, the uniporter regulators MICU1–3, EMRE and MCUR1, the release
regulators calsequestrin, FKBP12/12.6, triadin and junctin, and polycystin-1.

Sixteen of them carry a `CACN` symbol prefix, and seven of those sixteen —
CACNG2 to CACNG8 — are AMPA receptor subunits with no role in voltage-gated
calcium channels at all (§3.3). Any census assembled from symbol prefixes
counts all sixteen, and any census assembled from protein-complex membership
counts all forty.

### 11.5 The rule, and why it is a rule

Across every case above, the catalogue's requirement is the same: **a family
is excluded by a positive test, never by a caveat and never by a symbol.**
Not "this is not a Cav because the symbol says `SCN5A`", but "the filter
reads DEKA". Not "TRPM4 is probably not in scope", but either a test or an
explicit statement that no test exists and the call is a literature one.

The reason is that a census whose exclusions are unexamined is
unfalsifiable. Listing 98 genes and moving on would look tidier and would
give a reader nothing to check. Listing 245 with a recorded reason for each of
the 147 exclusions makes every one of them arguable — and each is designed to
be reversible by editing a single field and recounting. Moving the connexin
hemichannels into scope adds 16 genes; removing TPC costs 2; removing VDAC
costs 3; tightening the nicotinic boundary costs 3; dropping the conditional
tier entirely costs 9.
