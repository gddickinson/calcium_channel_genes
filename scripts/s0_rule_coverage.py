"""S0 - which families can the architecture tier name, and which cannot?

Offline, no network, under a second. For every family the catalogue
declares, this feeds the family's **own declared architecture** back into
`match_architecture()` and records what comes out. It answers one question
before S1 spends an hour measuring it on real proteins:

    if a protein carried exactly the domains this family is declared to
    carry, would the architecture tier name the family?

A "no" is not a bug. It is the claim `docs/classification_rules.md` makes,
turned into a number: **domain architecture is not a family call** (**D25**),
and the families it cannot reach are supposed to be exactly the ones the
hazard registry says are architecturally indistinguishable from a sibling.
This script checks that correspondence. A family that fails here *without*
a hazard row is the interesting case - either the hazard is missing or the
signatures are wrong.

Two tables:

    rule_coverage.tsv    one row per family: declared architecture, what the
                         architecture tier made of it, and its hazards
    rule_targets.tsv     one row per family that no rule can name at all

    python3 scripts/s0_rule_coverage.py [--out results/s0_baseline]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.s0_lib import write_tsv
from src.catalogue import CATALOGUE, census_families, hazards_for
from src.classify.rules import all_rules, match_architecture


def outcome(family_key: str) -> tuple[str, str]:
    """`(verdict, detail)` for one family fed its own declared architecture."""
    fam = CATALOGUE[family_key]
    counts = {s.accession: s.copies for s in fam.signatures}
    if not counts:
        return "NO_SIGNATURES", ""
    m = match_architecture(counts)
    if m.family == family_key:
        return "named", m.family
    if m.family:
        return "NAMED_AS_ANOTHER_FAMILY", m.family
    if m.ambiguous:
        return ("ambiguous_with_sibling"
                if family_key in m.ambiguous else "AMBIGUOUS_WITHOUT_SELF",
                ",".join(m.ambiguous))
    if m.superfamily:
        return "superfamily_only", m.superfamily
    return "no_match", ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=ROOT / "results" / "s0_baseline")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    rules = all_rules()
    nameable = {r.target for r in rules if r.target}

    rows, unreachable = [], []
    for key, fam in CATALOGUE.items():
        verdict, detail = outcome(key)
        hz = ",".join(h.hid for h in hazards_for(key))
        rows.append((key, "census" if fam.census_member() else "control",
                     fam.superfamily, fam.architecture() or "(none)",
                     verdict, detail, hz,
                     "yes" if key in nameable else "no"))
        if key not in nameable:
            unreachable.append((key, "census" if fam.census_member()
                                else "control", fam.name, hz))

    write_tsv(args.out / "rule_coverage.tsv",
              ("family", "role", "superfamily", "declared_architecture",
               "verdict", "detail", "hazards", "any_rule_can_name_it"), rows)
    write_tsv(args.out / "rule_targets.tsv",
              ("family", "role", "name", "hazards"), unreachable)

    cens = census_families()
    named = [f for f in cens if outcome(f.key)[0] == "named"]
    unnamed = [f for f in cens if outcome(f.key)[0] != "named"]
    print(f"[coverage] {len(named)}/{len(cens)} census families are named by "
          f"the architecture tier from their own declared architecture")
    print(f"[coverage] {len(unnamed)} are not - these need the motif or "
          f"reference tier, and S1 measures whether they get there:")
    orphans = []
    for f in unnamed:
        hz = [h.hid for h in hazards_for(f.key)]
        print(f"[coverage]   {f.key:22s} {outcome(f.key)[0]:22s} "
              f"hazards: {','.join(hz) or 'NONE'}")
        if not hz:
            orphans.append(f.key)
    print(f"[coverage] wrote {args.out / 'rule_coverage.tsv'}")
    if orphans:
        # A family architecture cannot name and no hazard explains is the
        # one failure mode this script exists to surface.
        print(f"[coverage] ** {len(orphans)} unnameable famil(y/ies) with no "
              f"hazard row: {', '.join(orphans)} **")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
