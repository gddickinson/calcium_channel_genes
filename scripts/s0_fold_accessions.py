#!/usr/bin/env python3
"""S0 — fold the resolved UniProt accessions back into the catalogue.

45 of the catalogue's 102 exemplars carry no accession. They are written as
a gene symbol plus a species, and every verification pass resolves them live
— two or three UniProt requests each, roughly ninety requests per pass, and
a different answer possible on any given day if UniProt promotes a different
entry to canonical. That makes the classifier's reference panel a thing the
network decides rather than a thing the repository declares, which is the
opposite of what a reference panel is for.

This script reads `exemplars_resolved.tsv` and writes the accession S0
resolved into the `Ex(...)` call in the division file, so the panel becomes
reproducible offline and future passes stop re-asking a question already
answered.

**It only fills gaps.** An exemplar that already declares an accession is
never rewritten, because a disagreement between a declared accession and a
resolved one is a finding for a person to look at, not something a script
should quietly overwrite — the same reason `s0_catalogue_verify.py` reports
mismatches instead of fixing them. Rows whose resolved gene name disagrees
with the catalogue's are skipped by default and listed, for the same reason.

    python3 scripts/s0_fold_accessions.py --dry-run     # show what it would do
    python3 scripts/s0_fold_accessions.py               # write it
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.s0_lib import read_tsv                                # noqa: E402

CATALOGUE_DIR = ROOT / "src" / "catalogue"

#: A resolved row is safe to fold in when the accession was found and the
#: record agrees with the catalogue about what gene it is. `NO_GENE_NAME_IN
#: _UNIPROT` is included deliberately: UniProt carries no gene name at all
#: for many viral, prokaryotic and invertebrate entries, which is a property
#: of the record rather than a disagreement about identity.
SAFE = {"ok", "NO_GENE_NAME_IN_UNIPROT"}


def patch(text: str, label: str, gene: str, species: str, acc: str) -> tuple[str, bool]:
    """Fill the accession slot of one `Ex(...)` call, in either written form.

    Two forms occur in the division files — a three-argument call with the
    slot absent, and a five-argument call with the slot written as `""` in
    front of a note — and both may be split across lines.
    """
    lab, gen, sp = (re.escape(x) for x in (label, gene, species))
    head = rf'Ex\(\s*"{lab}",\s*"{gen}",\s*"{sp}"'

    # form B first: an explicit empty accession, with or without a note after
    m = re.search(head + r',\s*""', text)
    if m:
        return text[:m.start()] + m.group(0)[:-2] + f'"{acc}"' + text[m.end():], True

    # form A: the slot is absent and the call closes straight after species
    m = re.search(head + r'\s*\)', text)
    if m:
        closing = m.group(0)
        return (text[:m.start()] + closing[:closing.rindex(")")]
                + f', "{acc}")' + text[m.end():], True)

    return text, False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dir", type=Path, default=ROOT / "results" / "s0_baseline")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rows = read_tsv(args.dir / "exemplars_resolved.tsv")
    if not rows:
        print(f"[fold] no exemplars_resolved.tsv in {args.dir} — "
              f"run scripts/s0_catalogue_verify.py first")
        return 1

    gaps = [r for r in rows
            if not r["declared_accession"] and r["resolved_accession"]]
    skipped = [r for r in gaps if r["status"] not in SAFE]
    todo = [r for r in gaps if r["status"] in SAFE]

    files = {p: p.read_text() for p in sorted(CATALOGUE_DIR.glob("*.py"))}
    written, missed = 0, []
    for r in todo:
        for p, text in files.items():
            new, hit = patch(text, r["label"], r["gene"], r["species"],
                             r["resolved_accession"])
            if hit:
                files[p] = new
                written += 1
                print(f"  {p.name:24s} {r['label']:22s} -> "
                      f"{r['resolved_accession']}")
                break
        else:
            missed.append(r)

    if skipped:
        print(f"\n[fold] {len(skipped)} resolved exemplar(s) NOT folded in — "
              f"the record disagrees with the catalogue about which gene it "
              f"is, and that is a finding, not a gap:")
        for r in skipped:
            print(f"  {r['label']:22s} {r['gene']:12s} -> "
                  f"{r['resolved_accession']} ({r['resolved_gene'] or '—'}) "
                  f"{r['status']}")
    if missed:
        print(f"\n[fold] {len(missed)} exemplar(s) could not be located in "
              f"the catalogue source — the Ex(...) call is written in a form "
              f"this script does not recognise:")
        for r in missed:
            print(f"  {r['label']:22s} {r['family']}")

    if args.dry_run:
        print(f"\n[fold] dry run: {written} accession(s) would be written")
        return 0

    for p, text in files.items():
        if text != p.read_text():
            p.write_text(text)
    print(f"\n[fold] wrote {written} accession(s) into the catalogue. "
          f"Re-run `python3 -m src.catalogue` and `python3 scripts/selftest.py`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
