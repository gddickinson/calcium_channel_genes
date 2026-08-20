"""S1 — which control families can the architecture tier name as census ones?

TRPM4 is a Ca2+-**impermeable** member of the TRPM family, catalogued as a
control, and this benchmark called it `trpm_ca`. The mechanism is not a bad
domain annotation — the catalogue already records, correctly, that TRPM4 and
TRPM5 carry the same Pfam accessions as their Ca2+-permeable siblings. It is
`derived_rules()`:

    for fam in census_families():        # <- controls generate no rules

so a domain declared at `FAMILY` level by *both* a census family and a
control family produces exactly one rule, pointing at the census family, and
a control that carries the domain matches it with no competitor to tie
against. "Ties are ambiguity, never a coin toss" cannot help when the
catalogue was only allowed to enter one side.

This is the third time this shape has been found here: `PF00027` naming
plant CNGC as animal CNG, the HCN defect before it, and now `PF18139`. So
rather than fix the one instance, this script **measures the whole exposure**
— every control family whose declared domains satisfy some census family's
generated rule — and separates the two very different outcomes:

* a **superfamily-only** match (`target == ""`, priority 10) says "this is a
  P-loop channel", which for Nav, HCN and NALCN is simply true and is not an
  error;
* a **family-level** match names a control as a census family, and every one
  of those is a false positive waiting for a protein that carries the domain.

The count of the second kind is the number that belongs in the report.

    python3 scripts/s1_rule_leakage.py [--out results/benchmark_controls]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.s0_lib import write_tsv
from src.catalogue import CATALOGUE, control_families
from src.classify.rules import HAZARD_RULES, derived_rules

HEADER = ("control_family", "control_status", "rule", "rule_target",
          "rule_level", "requires", "priority", "hazard_rule_outranks",
          "severity")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path,
                    default=ROOT / "results" / "benchmark_controls")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    rules = derived_rules()
    rows: list[tuple] = []
    for ctl in control_families():
        # The declared architecture, as the catalogue states it: this asks what
        # the rules would do with a *perfectly annotated* member, which is the
        # upper bound on the tier's specificity.
        have = {s.accession: 9 for s in ctl.signatures}
        rescuers = [h.rid for h in HAZARD_RULES
                    if h.matches(have) and h.target == ctl.key]
        for r in rules:
            if not r.matches(have):
                continue
            level = "family" if r.target else "superfamily-only"
            severity = ("harmless — states the superfamily, which is true"
                        if not r.target else
                        "FALSE POSITIVE — names a control as a census family")
            rows.append((ctl.key, ctl.status.value, r.rid, r.target or "—",
                         level, "+".join(r.require), r.priority,
                         ",".join(rescuers) or "none", severity))

    write_tsv(args.out / "rule_leakage.tsv", HEADER, sorted(rows))
    fam_level = [r for r in rows if r[4] == "family"]
    print(f"[s1-leak] {len(rows)} architecture match(es) into "
          f"{len({r[0] for r in rows})} control famil(ies)")
    print(f"[s1-leak] {len(rows) - len(fam_level)} are superfamily-only "
          f"(correct: a sodium channel really is a P-loop channel)")
    print(f"[s1-leak] {len(fam_level)} name a control as a census family:")
    for r in fam_level:
        print(f"[s1-leak]     {r[0]} -> {r[3]} via {r[2]} [{r[5]}] "
              f"(hazard-rule rescue: {r[7]})")
    print(f"[s1-leak] → {args.out / 'rule_leakage.tsv'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
