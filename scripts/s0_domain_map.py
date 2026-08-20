"""Fetch per-residue domain positions for the review's figure exemplars.

`exemplar_architecture.tsv` records *which* domains a protein carries.
Drawing an architecture — a scale diagram of where each domain sits along
the chain — needs *where*, so this fetches the InterPro match coordinates
for a named subset of proteins and writes them to a committed table.

The subset is deliberately small and explicit: these are the proteins the
review's figures compare, and each one is there to make a specific point
(the four-repeat families that domain composition cannot separate, CFTR
against the ABC transporter that regulates a channel, the anoctamin channel
against the anoctamin scramblase, the three families that share `PF08016`).

    python3 scripts/s0_domain_map.py [--out results/s0_baseline]

Output: `domain_positions.tsv` — accession, gene, length, pfam, name, start,
end, copy index. The figures are rendered from that table, never from a
live fetch, so a figure cannot disagree with the data behind it (D13).
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.s0_lib import INTERPRO, Fetcher, write_tsv

#: (accession, gene, why it is in a figure)
FIGURE_PROTEINS: list[tuple[str, str, str]] = [
    # the four-repeat families - identical architecture, different ions
    ("Q13936", "CACNA1C", "Cav1: Ion_trans x4 + Ca_chan_IQ"),
    ("O43497", "CACNA1G", "Cav3: Ion_trans x4 and nothing else"),
    ("Q14524", "SCN5A", "Nav: the same architecture, a sodium channel"),
    ("Q8IZF0", "NALCN", "leak: Ion_trans x4 and nothing else"),
    ("Q8NEC5", "CATSPER1", "one 6TM subunit of a heterotetramer"),
    # the TRPV pair - the boundary inside a family
    ("Q9H1D0", "TRPV6", "Ca2+-selective; the D582 aspartate ring"),
    ("Q8NER1", "TRPV1", "the same accessions, non-selective"),
    # the TRPM pair - the boundary inside a family, with no discriminator
    ("Q96QT4", "TRPM7", "Ca2+-permeable chanzyme"),
    ("Q8TD43", "TRPM4", "Ca2+-activated and Ca2+-impermeable"),
    # the PF08016 trio
    ("Q9GZU1", "MCOLN1", "TRPML"),
    ("Q13563", "PKD2", "TRPP"),
    ("P98161", "PKD1", "polycystin-1: same domain, not a pore"),
    # a pore, a gate and a sensor - all three are SOCE hits
    ("Q96D31", "ORAI1", "the CRAC pore - and, at 301 aa, near the "
                        "small end of the census's 17-fold length range"),
    ("Q13586", "STIM1", "the gate, in another organelle"),
    ("P0DP23", "CALM1", "EF-hands, no membrane domain at all"),
    # the uniporter: a pore subunit and a regulator
    ("Q8NE86", "MCU", "the DIME pore"),
    ("Q9BPX6", "MICU1", "EF-hand gatekeeper, no pore"),
    # calcium in the name, not in the pore
    ("Q12791", "KCNMA1", "BK: Ca2+-activated, conducts K+"),
    ("O14983", "ATP2A1", "SERCA: a pump"),
    ("P41180", "CASR", "the calcium-sensing receptor, a GPCR"),
    ("Q9Y698", "CACNG2", "a CACN symbol on an AMPA-receptor subunit"),
    # scale
    ("P21817", "RYR1", "5,038 aa - the largest protein in the catalogue"),
]


def positions(f: Fetcher, accession: str) -> list[tuple]:
    d = f.json(f"{INTERPRO}/entry/pfam/protein/uniprot/{accession}/?page_size=100")
    if not d:
        return []
    out = []
    for entry in d.get("results", []):
        m = entry["metadata"]
        name = m.get("name")
        short = name.get("short") if isinstance(name, dict) else name
        for prot in entry.get("proteins", []):
            for i, loc in enumerate(prot.get("entry_protein_locations", []) or [], 1):
                frags = loc.get("fragments") or []
                if not frags:
                    continue
                out.append((m["accession"], short or "",
                            int(frags[0]["start"]), int(frags[-1]["end"]), i))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=ROOT / "results" / "s0_baseline")
    args = ap.parse_args()

    f = Fetcher()
    rows = []
    for i, (acc, gene, why) in enumerate(FIGURE_PROTEINS, 1):
        meta = f.json(f"https://rest.uniprot.org/uniprotkb/{acc}.json"
                      f"?fields=accession,length")
        length = ((meta or {}).get("sequence") or {}).get("length", 0)
        hits = positions(f, acc)
        for pfam, short, start, end, copy in sorted(hits, key=lambda h: h[2]):
            rows.append((acc, gene, length, pfam, short, start, end, copy, why))
        print(f"[domains] [{i}/{len(FIGURE_PROTEINS)}] {gene:9s} {acc} "
              f"{length or '?':>5} aa  {len(hits)} match(es)", flush=True)
        time.sleep(0.1)

    write_tsv(args.out / "domain_positions.tsv",
              ("accession", "gene", "length_aa", "pfam", "pfam_name",
               "start", "end", "copy", "role"), rows)
    print(f"[domains] {len(rows)} matches across {len(FIGURE_PROTEINS)} "
          f"proteins → {args.out / 'domain_positions.tsv'}")
    return 1 if f.failures else 0


if __name__ == "__main__":
    sys.exit(main())
