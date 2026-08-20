## 3. The voltage-gated calcium channels

### 3.1 Ten genes, three subfamilies, one architecture

The voltage-gated calcium channels are the family the term "calcium channel"
usually means, and the one whose pharmacology reaches furthest into clinical
practice. Ten human α₁ genes encode the pore, and they fall into three
subfamilies by sequence and by physiology [ertel2000, catterall2011]:

| subfamily | genes | current | activation |
|---|---|---|---|
| Cav1 | `CACNA1S`, `CACNA1C`, `CACNA1D`, `CACNA1F` | L-type | high-voltage |
| Cav2 | `CACNA1A`, `CACNA1B`, `CACNA1E` | P/Q-, N-, R-type | high-voltage |
| Cav3 | `CACNA1G`, `CACNA1H`, `CACNA1I` | T-type | low-voltage |

The purification that started the molecular era used the dihydropyridine
receptor of skeletal muscle, and the sequence that followed established the
four-repeat architecture [tanabe1987]; the cardiac L-type channel followed
[mikami1989], and the T-type channels last, a decade later
[cribbs1998, perezreyes2003]. Structures of the Cav1.1 complex resolved the
pore, the four voltage sensors and the auxiliary subunits together
[wu2015, wu2016].

Physiologically the split that matters is not Cav1 against Cav2 but
high-voltage against low-voltage. Cav1 and Cav2 open on strong
depolarisation and carry the calcium that triggers contraction and
transmitter release; Cav3 opens near rest, inactivates quickly, and supports
rhythmic firing and rebound bursts [perezreyes2003]. Cav1.1 in skeletal
muscle is the extreme case: it works largely as a voltage sensor
mechanically coupled to RyR1 rather than as a conduit, and calcium entry
through it is not what triggers contraction [rios1987].

### 3.2 The nearest relative is a sodium channel

Cav's closest architectural neighbours are not other calcium channels. The
four-repeat P-loop channels comprise the voltage-gated calcium channels, the
voltage-gated sodium channels, the sodium-leak channel NALCN and the sperm
channel CatSper, and they are indistinguishable by domain architecture
[catterall2012, payandeh2011, lu2007]. This project's own measurement makes
the point concretely: `PF00520` in four copies describes all of them equally
well, and CACNA1G carries `PF00520`×4 and nothing else — no Cav-specific
domain at all.

The consequence for any census is direct. A calcium channel here cannot be
recognised by what domains it carries; it has to be recognised by reading the
filter (§2.1). This is the single most important hazard in the subject, and
the reason the classification behind this review assigns by positive test
rather than by architecture.

A second, subtler consequence concerns trees. Because superfamilies are
defined by descent rather than by ion, a pore-module tree of the P-loop
superfamily *contains* the sodium channels and the Ca²⁺-activated potassium
channels. Dropping them to produce "the calcium channel tree" would hide the
non-monophyly and remove the outgroup that makes the tree rootable. The
protocol behind this review forbids it.

### 3.3 The subunits that are not channels

The high-voltage-activated channels are complexes: an α₁ pore with a
cytoplasmic β subunit, an extracellular-facing α2δ and, in some tissues, a γ
subunit [dolphin2016, dolphin2018]. None of them forms a pore, and all of
them carry `CACN` symbols. Sixteen human genes do — four `CACNB`, four
`CACNA2D`, eight `CACNG` — and this review's catalogue counts none of them.

Three facts make this more than nomenclature:

- **The β subunit is required for the channel to reach the membrane at all**,
  and shifts its voltage dependence by tens of millivolts. It is a MAGUK — a
  scaffold fold doing a channel job.
- **α2δ-1 is the gabapentin and pregabalin target.** An auxiliary subunit
  that conducts nothing is among the most-prescribed drug targets in the
  entire catalogue [zamponi2015, santos2017].
- **Seven of the eight `CACNG` genes are not calcium-channel subunits at
  all.** CACNG2–CACNG8 are TARPs: claudin-fold proteins that traffic and
  modulate AMPA receptors, with no role in voltage-gated calcium channels.
  Their symbols are a historical accident of the order of discovery, and they
  are counted as calcium-channel genes by any list built on symbol prefixes.

This project measured the architectures directly and found that the three
subunit types share no domain at all: `CACNB1` carries a guanylate-kinase
domain and a β-specific N-terminal domain, `CACNA2D1` a von Willebrand A
domain and the α2δ domain, `CACNG2` a claudin domain alone. The "family" is
three unrelated protein types grouped by the job they do.

### 3.4 CatSper, and a filter that cannot be read

CatSper is the principal calcium channel of sperm, required for
hyperactivated motility and for male fertility, and gated in human sperm by
progesterone acting through a lipid hydrolase rather than through a classical
receptor [ren2001, lishko2011, strunker2011]. It is a four-repeat channel
built the hard way: four distinct pore-forming genes, `CATSPER1`–`CATSPER4`,
each contributing one repeat, alongside several accessory subunits
[cai2012].

That construction defeats the test that works for every other four-repeat
family. A filter projection reads four positions from one sequence; CatSper's
four positions are in four different proteins, so no single-sequence
projection can recover the ring. The locus is recorded as unread rather than
guessed, and closing it would need a joint projection across all four
subunits (*pending: S9*).
