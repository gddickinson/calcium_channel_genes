"""Tier 3 - the fold-similarity network that replaces the tree nobody can build.

Between superfamilies there is no alignment and therefore no phylogeny. What
there *is* is measurable structural similarity: the ITPR/RYR pore module is
a P-loop channel bolted onto a giant solenoid; the iGluR pore is an inverted
P-loop; CALHM, connexin, pannexin and LRRC8 build the same class of large
pore with no detectable sequence relationship. Those relationships are real,
some of them are probably ancestral, and the evidence for them is structural
rather than sequential.

For a calcium census the network carries more of the argument than it does
in a single-superfamily project, because the subject spans folds. The
question "how many times has a calcium-selective pore evolved" cannot be
answered inside any one tree, and the honest answer is a count of
unconnected components in this network together with a statement of what was
measured and what was not.

So tier 3 is a **network**, and it is drawn and named as one: nodes are
families, edges are structural similarity (Foldseek TM-score or E-value
between representative predicted structures), and no edge is ever given a
branch length or a bootstrap value. The output is explicitly not a
phylogram, and the module has no code that could produce one.

Where structures are missing the edge is absent and recorded as absent - a
missing edge in this network means "not measured", never "not related", and
the manifest keeps the two apart.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from ..catalogue import CATALOGUE, SUPERFAMILIES


@dataclass
class FoldEdge:
    source: str            # family or superfamily key
    target: str
    metric: str            # "tm_score" | "foldseek_evalue" | "literature"
    value: float
    evidence: str = ""     # structure ids, tool version, or citation
    measured: bool = True

    def key(self) -> tuple[str, str]:
        return tuple(sorted((self.source, self.target)))


@dataclass
class FoldNetwork:
    level: str = "superfamily"     # or "family"
    nodes: list[str] = field(default_factory=list)
    edges: list[FoldEdge] = field(default_factory=list)
    unmeasured: list[tuple[str, str, str]] = field(default_factory=list)

    def add(self, edge: FoldEdge) -> None:
        self.edges.append(edge)

    def note_unmeasured(self, a: str, b: str, why: str) -> None:
        self.unmeasured.append((a, b, why))

    def neighbours(self, node: str) -> list[FoldEdge]:
        return [e for e in self.edges if node in (e.source, e.target)]

    def summary(self) -> str:
        return (f"fold network at {self.level} level: {len(self.nodes)} nodes, "
                f"{len(self.edges)} measured edge(s), "
                f"{len(self.unmeasured)} pair(s) not measured")

    def to_dict(self) -> dict:
        return {
            "level": self.level,
            "nodes": self.nodes,
            "edges": [e.__dict__ for e in self.edges],
            "unmeasured": self.unmeasured,
            "caveat": ("Edges are structural similarity, not phylogeny. No "
                       "branch lengths, no support values, no common "
                       "ancestor is implied by an edge (D27)."),
        }

    def write(self, path: Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2))
        return path

    def edge_table(self) -> list[tuple]:
        return [(e.source, e.target, e.metric, f"{e.value:.4g}",
                 "measured" if e.measured else "asserted", e.evidence)
                for e in sorted(self.edges, key=lambda e: -e.value)]


def seed_network(level: str = "superfamily") -> FoldNetwork:
    """A network with every node and no edges — the honest starting state.

    The literature-asserted relationships are added as `measured=False`
    edges by `scripts/s8_fold_network.py` only after it has said so; nothing
    is asserted here, because a network that ships with its conclusions
    already drawn is a diagram, not a measurement.
    """
    if level == "superfamily":
        nodes = sorted(SUPERFAMILIES)
    else:
        nodes = sorted(f.key for f in CATALOGUE.values() if f.census_member())
    return FoldNetwork(level=level, nodes=nodes)


#: Relationships the literature asserts and this project must test rather
#: than inherit. Each becomes a `measured=False` edge until S8 measures it.
LITERATURE_EDGES: list[tuple[str, str, str]] = [
    ("ca_release", "ploop",
     "the ITPR/RYR pore module is a P-loop channel carrying PF00520 - the "
     "clearest structural link across two superfamilies in this catalogue"),
    ("iglur", "ploop",
     "the iGluR pore module is an inverted P-loop, structurally equivalent "
     "to Kir; the Q/R site sits where a selectivity filter would"),
    ("osca", "tmem16",
     "OSCA/TMEM63 and the anoctamins share a 10-TM fold with the conduction "
     "groove in the same place - one architecture, and Ca2+-permeable on one "
     "side of this catalogue's boundary and Ca2+-activated on the other"),
    ("largepore", "largepore",
     "CALHM, connexin, pannexin/innexin and LRRC8 build convergent large "
     "pores; within-group sequence alignment works and between-group does "
     "not, which is why the superfamily is marked alignable=False"),
]

#: Superfamilies with no asserted structural relative anywhere in this
#: catalogue. They are listed because an unconnected node is a *result* -
#: "no relative measured" and "no relative exists" are different claims, and
#: a network that simply omitted them would blur the two.
UNCONNECTED: dict[str, str] = {
    "orai": ("the hexameric CRAC fold has no measured structural relative in "
             "this catalogue; whether one exists is an S12 question"),
    "mcu": ("the uniporter fold likewise stands alone here; its prokaryotic "
            "relatives are an S3/S12 question"),
    "piezo": ("the three-bladed propeller is unique among the census "
              "families - the mechanosensitive channels in this catalogue "
              "share a mechanism and no fold"),
    "mca": ("no structure and no fold assignment; recorded as unknown "
            "rather than guessed"),
}
