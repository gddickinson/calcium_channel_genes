"""Selectivity-filter tests - the discriminators that domain architecture cannot make.

Four motifs carry the work, and they divide into the two kinds of test this
project can run.

**Motifs that need no reference sequence.** Three of them, all matched by a
regular expression, all usable on a bare sequence from an unannotated
genome:

* `K_FILTER_RE` - T-x-G-Y-G, the backbone carbonyl cage of a potassium
  channel. In a calcium census it is a *negative* test used positively: a
  protein with this motif conducts K+, which settles the Ca2+-activated
  potassium channels (hazard **HC15**) without consulting a name.
* `MCU_DXXE_RE` - the `WDxxE` DIME motif of the mitochondrial uniporter.
  Verified 2026-08-20 against human MCU `Q8NE86`: **WDIME at position 260**.
  The most Ca2+-selective channel known has the shortest filter, and it is
  the only family in the catalogue callable from a five-residue regex.
* `EF_HAND_RE` - the canonical EF-hand loop. A positive detector for the
  decoys of hazard **HC12**, never evidence against a channel: STIM1 and
  MICU1 carry EF-hands and sit inside census complexes. Measured
  2026-08-20: 4 loops in calmodulin, 4 in calbindin, 2 in parvalbumin, and
  none in CACNA1C or MCU.

**Motifs that must be projected from a reference.** Two of them, because the
residues that matter are not in a conserved context and cannot be found by
pattern:

* **The four-repeat filter locus.** Cav, Nav, NALCN and CatSper have
  identical domain architectures (hazard **HC1**) and are separated by one
  residue contributed by each of the four repeats. Align the query to human
  Nav1.5 and read whatever falls on its D372, E898, K1419 and A1711.
  Verified 2026-08-20 against live UniProt `Q14524`: those positions read
  **DEKA**. This is the test that separates a calcium channel from a sodium
  channel, and the census turns on it.

      Cav1/Cav2 -> EEEE      Cav3 -> EEDD      NALCN -> EEKE      Nav -> DEKA

* **The TRPV aspartate ring.** TRPV5/TRPV6 are Ca2+-selective and TRPV1-4
  are not, with the same Pfam accessions and the same length band (hazard
  **HC7b**). The discriminator is one aspartate per subunit in the outer
  pore. **The literature's D542 does not validate against UniProt**:
  measured 2026-08-20, the canonical human TRPV6 entry `Q9H1D0` is 765 aa
  and carries the `TIIDGP` filter at 579-584, putting the aspartate at
  **D582**. The 40-residue offset is the known long/short TRPV6 isoform
  difference, and it is exactly the failure `verify_anchor()` exists to
  catch: an anchor taken from a paper's numbering would have projected the
  wrong column silently.

Every projection is checked against its own reference before it is trusted,
and a non-validating anchor refuses to project rather than returning a
guess (**D26**, **D28**).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from ..utils.mafft import (MafftUnavailable, align, mafft_available,
                           project_positions)

#: The K+ selectivity filter. Matches TVGYG (Kv, KcsA), TIGYG (Kir, KCNQ),
#: SVGFG (EAG) and the BK/SK variants. A hit means potassium, which in this
#: project means "not a calcium channel" (HC15).
K_FILTER_RE = re.compile(r"[TSAC][VILMTAF]G[YFL]G")

#: The mitochondrial uniporter's DIME motif. Verified on human MCU Q8NE86,
#: WDIME at 260 (2026-08-20).
MCU_DXXE_RE = re.compile(r"WD[ILVM][MILVF]E")

#: The canonical 12-residue EF-hand loop: D-x-D/N-x-D/N/S-G-x-I/V-x-x-x-E.
#: A decoy detector for HC12 and never evidence against a channel.
#:
#: Measured 2026-08-20 against live UniProt: 4 loops in calmodulin (P0DP23),
#: 4 in calbindin (P05937), 2 in parvalbumin (P20472), 2 in MICU1 (Q9BPX6),
#: 1 in STIM1 (Q13586) - and **0 in CACNA1C and 0 in MCU**. The last two are
#: what make it usable: the detector separates the calcium-binding decoys
#: from the calcium-conducting census families rather than firing on
#: everything with calcium in its annotation.
EF_HAND_RE = re.compile(r"D[A-Z][DN][A-Z][DNS]G[A-Z][IVL][A-Z]{3}E")

#: Motifs that are diagnostic on their own, with what they mean.
SIMPLE_MOTIFS: dict[str, tuple[re.Pattern, str]] = {
    "k_filter": (K_FILTER_RE,
                 "potassium selectivity filter (TxGYG) - not a Ca2+ channel"),
    "mcu_dxxe": (MCU_DXXE_RE,
                 "mitochondrial uniporter DIME motif (WDxxE)"),
    "ef_hand": (EF_HAND_RE,
                "EF-hand calcium-binding loop - binding, not conducting"),
}


@dataclass(frozen=True)
class FilterAnchor:
    """A reference protein plus the positions its selectivity filter occupies."""
    key: str
    reference_label: str
    reference_uniprot: str
    positions: tuple[int, ...]
    expected: str            # what the reference itself must read
    applies_to: tuple[str, ...]   # catalogue family keys this anchor can call
    calls: dict[str, tuple[str, str]] = field(default_factory=dict)
    note: str = ""


#: The four-repeat locus. Verified against UniProt Q14524 on 2026-08-20:
#: positions 372/898/1419/1711 of human Nav1.5 read D/E/K/A.
#:
#: Anything not in `calls` is a non-call, which is a legitimate answer: TPC1
#: projects to a two-residue string because it has two repeats, not four, and
#: that is information rather than failure.
FOUR_REPEAT_ANCHOR = FilterAnchor(
    key="four_repeat",
    reference_label="Hs_SCN5A",
    reference_uniprot="Q14524",
    positions=(372, 898, 1419, 1711),
    expected="DEKA",
    applies_to=("cav_hva", "cav_lva", "outofscope_nav", "outofscope_nalcn",
                "catsper", "tpc"),
    calls={
        "EEEE": ("cav_hva", "Cav1/Cav2 high-voltage-activated locus"),
        "EEDD": ("cav_lva", "Cav3 (T-type) locus - HC14"),
        "DEKA": ("outofscope_nav", "voltage-gated sodium channel locus"),
        "EEKE": ("outofscope_nalcn", "NALCN leak-channel locus"),
    },
    note=("hazard HC1; the reference is a sodium channel, because the "
          "decoy is what the calcium families have to be measured against"),
)

#: The TRPV Ca2+-selectivity aspartate. Verified against UniProt Q9H1D0 on
#: 2026-08-20: the canonical 765 aa human TRPV6 carries TIIDGP at 579-584,
#: so the aspartate is D582 and NOT the D542 of the literature's numbering.
TRPV_CA_ANCHOR = FilterAnchor(
    key="trpv_ca_ring",
    reference_label="Hs_TRPV6",
    reference_uniprot="Q9H1D0",
    positions=(582,),
    expected="D",
    applies_to=("trpv_ca", "trpv_ns"),
    calls={"D": ("trpv_ca", "outer-pore aspartate ring - Ca2+-selective TRPV")},
    note=("hazard HC7b; a D here does not by itself make a family call - "
          "TRPV1-4 also carry acidic residues in the outer pore - so the "
          "classifier treats it as supporting evidence and the S1 benchmark "
          "measures how far it actually separates the two groups"),
)

#: The ORAI selectivity filter. Verified against UniProt Q96D31 on
#: 2026-08-20: position 106 of human ORAI1 is E.
ORAI_ANCHOR = FilterAnchor(
    key="orai_e106",
    reference_label="Hs_ORAI1",
    reference_uniprot="Q96D31",
    positions=(106,),
    expected="E",
    applies_to=("orai",),
    calls={"E": ("orai", "the E106 glutamate ring of the CRAC pore")},
    note="one glutamate per subunit; E106Q abolishes Ca2+ selectivity",
)

ANCHORS: dict[str, FilterAnchor] = {
    a.key: a for a in (FOUR_REPEAT_ANCHOR, TRPV_CA_ANCHOR, ORAI_ANCHOR)
}

#: Backwards-compatible alias: the four-repeat map is the one the benchmark
#: and the self-test report on directly.
FILTER_CALLS: dict[str, tuple[str, str]] = FOUR_REPEAT_ANCHOR.calls


@dataclass
class MotifResult:
    """What the motif tier found, and what it could not look for."""
    filter_string: str = ""
    filter_family: str = ""
    filter_note: str = ""
    anchor_key: str = ""
    k_filter_hits: list[tuple[int, str]] = field(default_factory=list)
    mcu_hits: list[tuple[int, str]] = field(default_factory=list)
    ef_hand_hits: list[tuple[int, str]] = field(default_factory=list)
    available: bool = True
    message: str = ""

    def summary(self) -> str:
        bits = []
        if self.filter_string:
            bits.append(f"{self.anchor_key or 'filter'} {self.filter_string}"
                        + (f" -> {self.filter_family}" if self.filter_family
                           else " (no call)"))
        if self.k_filter_hits:
            pos = ", ".join(f"{p}:{m}" for p, m in self.k_filter_hits[:4])
            bits.append(f"{len(self.k_filter_hits)} K+ filter match(es) "
                        f"[{pos}] - potassium, not calcium")
        if self.mcu_hits:
            bits.append(f"MCU DIME motif at {self.mcu_hits[0][0]}")
        if self.ef_hand_hits:
            bits.append(f"{len(self.ef_hand_hits)} EF-hand loop(s) - "
                        f"Ca2+-binding evidence, not Ca2+-conducting")
        if not self.available:
            bits.append(f"unavailable - {self.message}")
        return "; ".join(bits) or "no motif evidence"


def _hits(pattern: re.Pattern, sequence: str) -> list[tuple[int, str]]:
    return [(m.start() + 1, m.group(0)) for m in pattern.finditer(sequence.upper())]


def k_filter_hits(sequence: str) -> list[tuple[int, str]]:
    """1-based positions and matched text of every TxGYG-like motif."""
    return _hits(K_FILTER_RE, sequence)


def mcu_filter_hits(sequence: str) -> list[tuple[int, str]]:
    """The uniporter DIME motif - the one Ca2+ filter a regex can find."""
    return _hits(MCU_DXXE_RE, sequence)


def ef_hand_hits(sequence: str) -> list[tuple[int, str]]:
    """Canonical EF-hand loops. Decoy evidence for HC12, never a veto."""
    return _hits(EF_HAND_RE, sequence)


def filter_signature(query_sequence: str, reference_sequence: str,
                     anchor: FilterAnchor = FOUR_REPEAT_ANCHOR) -> str:
    """Project the anchor positions of the reference onto the query.

    Returns the projected residues as a string (`-` where the query does not
    cover the position). Raises `MafftUnavailable` if MAFFT is not installed
    - the test has no weaker fallback and must not pretend otherwise
    (**D28**).
    """
    if not query_sequence or not reference_sequence:
        return ""
    rows = align([("ref", reference_sequence), ("qry", query_sequence)])
    projected = project_positions(rows["ref"], rows["qry"], list(anchor.positions))
    return "".join(projected[p] for p in anchor.positions)


def verify_anchor(reference_sequence: str,
                  anchor: FilterAnchor = FOUR_REPEAT_ANCHOR) -> bool:
    """Does the reference itself still read what the anchor claims?

    Run before trusting any projection. A UniProt sequence-version bump, or
    an isoform boundary moving, would otherwise turn every filter call
    silently wrong - and this is not hypothetical: the TRPV6 anchor in this
    module is at D582 rather than the literature's D542 precisely because
    the canonical entry is the long isoform. `scripts/s1_benchmark.py` calls
    this first and refuses to report filter results if it fails.
    """
    if len(reference_sequence) < max(anchor.positions):
        return False
    got = "".join(reference_sequence[p - 1] for p in anchor.positions)
    return got == anchor.expected


def scan(query_sequence: str, reference_sequence: str = "",
         anchor: FilterAnchor = FOUR_REPEAT_ANCHOR) -> MotifResult:
    """Run every motif test available for this query."""
    res = MotifResult(anchor_key=anchor.key,
                      k_filter_hits=k_filter_hits(query_sequence),
                      mcu_hits=mcu_filter_hits(query_sequence),
                      ef_hand_hits=ef_hand_hits(query_sequence))
    if not reference_sequence:
        return res
    if not mafft_available():
        res.available = False
        res.message = "mafft not on PATH; projected filter test skipped"
        return res
    if not verify_anchor(reference_sequence, anchor):
        res.available = False
        res.message = (f"anchor {anchor.key} does not validate against "
                       f"{anchor.reference_label} - refusing to project")
        return res
    try:
        sig = filter_signature(query_sequence, reference_sequence, anchor)
    except (MafftUnavailable, RuntimeError) as exc:
        res.available = False
        res.message = str(exc)[:200]
        return res
    res.filter_string = sig
    call = anchor.calls.get(sig)
    if call:
        res.filter_family, res.filter_note = call
    return res
