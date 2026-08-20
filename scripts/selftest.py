"""Offline self-test - the invariants that must hold before any session starts.

No network, no external binaries, under a second. It checks the things that
break silently when the catalogue is edited: that a hazard rule still fires
on the architecture it was written for, that the census still refuses to
count a channel with no calcium claim, that the phylogeny driver still
refuses the comparisons decision **D27** forbids, that a scope still derives
its sister panel from the hazard registry, and that the classifier still
never consults a gene symbol.

Run it after any catalogue edit, and as step 4a of the session protocol:

    python3 scripts/selftest.py

Exit code 0 means every invariant holds. Each failure prints what was
expected and what happened, because a self-test whose output is just a count
tells you nothing at the moment you need it.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.catalogue import (CATALOGUE, HAZARDS, CaClass, census_by_tier,
                           census_families, validate)
from src.classify import ChannelQuery, classify, ef_hand_hits, k_filter_hits
from src.classify.motifs import (FILTER_CALLS, MCU_DXXE_RE, TRPV_CA_ANCHOR,
                                 mcu_filter_hits)
from src.classify.rules import match_architecture
from src.phylo import NotAlignable, build_tier2, refused_superfamilies
from src.utils.mafft import (alignment_stats, percent_identity,
                             project_positions)
from src.utils.scope import scope_for

FAILURES: list[str] = []


def check(name: str, got, want) -> None:
    if got == want:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}\n         want {want!r}\n         got  {got!r}")
        FAILURES.append(name)


def check_true(name: str, cond, detail: str = "") -> None:
    check(name, bool(cond), True) if cond else (
        print(f"  FAIL {name}  {detail}"), FAILURES.append(name))


# ------------------------------------------------------------ catalogue
print("catalogue")
check("validate() is clean", validate(), [])
check("every hazard names known families",
      sorted({f for h in HAZARDS for f in h.families if f not in CATALOGUE}), [])
check("every hazard has a discriminator",
      [h.hid for h in HAZARDS if not h.discriminator.strip()], [])

# ---------------------------------------------- the calcium census (D31)
print("\nthe census is graded, and the grades carry evidence (D31)")
check("no census family makes an unevidenced calcium claim",
      [f.key for f in census_families() if not f.permeability.method], [])
check("no census family is in the NOT_CALCIUM tier",
      [f.key for f in census_families()
       if f.ca_class() is CaClass.NOT_CALCIUM], [])
tiers = census_by_tier()
check_true("all four census tiers are populated",
           all(t["families"] for t in tiers.values()), tiers)
check_true("the flat headline is never the whole story",
           sum(t["human_genes"] for t in tiers.values())
           > max(t["human_genes"] for t in tiers.values()), tiers)
# The Ca2+-activated channels are the reason the ACTIVATED tier exists.
check("BK is catalogued and not counted",
      CATALOGUE["outofscope_kca"].census_member(), False)
check("BK's exclusion is recorded as a measurement, not an omission",
      CATALOGUE["outofscope_kca"].ca_class(), CaClass.ACTIVATED)
check("TRPM4/5 sit outside the census their own family is in",
      (CATALOGUE["trpm_ca"].census_member(),
       CATALOGUE["outofscope_trpm_monovalent"].census_member()), (True, False))

# ------------------------------------------- architecture / hazard rules
print("\narchitecture rules - the hazard cases, by synthetic architecture")
CASES = [
    # (name, pfam counts, expected family, expected ambiguity)
    ("Cav1.2 (HC1)",   {"PF00520": 4, "PF08763": 1, "PF16905": 1}, "cav_hva", []),
    ("Cav3 (HC1)",     {"PF00520": 4}, "", []),          # the filter tier's job
    ("Nav (HC1)",      {"PF00520": 4, "PF06512": 1, "PF11933": 1},
     "outofscope_nav", []),
    ("CACNB1 (HC2)",   {"PF00625": 1}, "assoc_cav_aux", []),
    ("CACNG2 (HC2)",   {"PF00822": 1}, "assoc_cav_aux", []),
    ("RyR (HC3)",      {"PF08709": 1, "PF02026": 4, "PF02815": 1}, "ryr", []),
    ("ITPR (HC3)",     {"PF08709": 1, "PF02815": 1, "PF01365": 2}, "itpr", []),
    ("POMT (HC4)",     {"PF02815": 1, "PF02366": 1}, "nonchannel_pomt", []),
    ("ORAI1 (HC5)",    {"PF07856": 1}, "orai", []),
    ("STIM1 (HC5)",    {"PF16533": 1, "PF07647": 1}, "assoc_stim", []),
    ("MCU (HC6)",      {"PF04678": 1}, "mcu", []),
    ("MICU1 (HC6)",    {"PF13833": 1}, "assoc_mcu_reg", []),
    ("EMRE (HC6)",     {"PF10161": 1}, "assoc_mcu_reg", []),
    ("TRPML (HC9)",    {"PF08016": 1, "PF21381": 1}, "trpml", []),
    ("PKD1 (HC9)",     {"PF08016": 1, "PF00801": 15}, "assoc_polycystin1", []),
    ("CATSPERB (HC10)", {"PF15149": 1}, "assoc_catsper_aux", []),
    ("SERCA (HC11)",   {"PF00122": 1, "PF00689": 1}, "transporter_ca_atpase", []),
    ("NCX1 (HC11)",    {"PF01699": 1}, "transporter_ca_exchanger", []),
    ("CASR (HC12)",    {"PF01094": 1, "PF00003": 1}, "nonchannel_casr_gpcr", []),
    ("calmodulin (HC12)", {"PF13499": 1}, "nonchannel_efhand", []),
    ("BK (HC15)",      {"PF00520": 1, "PF03493": 1}, "outofscope_kca", []),
    # Measured in S0: KCNN2 shares no diagnostic domain with BK, so one rule
    # cannot reach both halves of the Ca2+-activated potassium family.
    ("SK2 (HC15)",     {"PF07885": 1, "PF03530": 1, "PF02888": 1},
     "outofscope_kca", []),
    # Measured in S0: TRPM7 carries no PF00520 either (HC7), and does carry
    # the fused alpha-kinase.
    ("TRPM7 (HC7)",    {"PF18139": 1, "PF16519": 1, "PF23317": 1,
                        "PF25508": 2, "PF02816": 1}, "trpm_ca", []),
    ("ANO1 (HC15)",    {"PF04547": 1, "PF16178": 1}, "outofscope_anoctamin", []),
    # PF00027 spans CNG, HCN and the plant CNGCs. Found by
    # scripts/s0_rule_coverage.py: without a positive HCN test, HCN's
    # architecture was named as a plant channel.
    ("HCN (HC16)",     {"PF00520": 1, "PF00027": 1, "PF08412": 1},
     "outofscope_hcn", []),
    ("CNG (HC16)",     {"PF00520": 1, "PF00027": 1, "PF16526": 1}, "cng", []),
    # PKD1 carries PF20519 as TRPP does; the fifteen PKD repeats have to
    # outrank the shared domain or a non-pore ties with a census family.
    ("PKD1 vs TRPP (HC9)",
     {"PF08016": 1, "PF20519": 1, "PF00801": 15}, "assoc_polycystin1", []),
]
for name, counts, want_family, want_ambig in CASES:
    m = match_architecture(counts)
    check(f"{name} family", m.family, want_family)
    if want_ambig:
        check(f"{name} ambiguity", sorted(m.ambiguous), sorted(want_ambig))

# The negative half of the auxiliary-subunit tests has to stay negative:
# a claudin fold *with* a pore model must not be filed as a TARP.
m = match_architecture({"PF00822": 1, "PF00520": 4, "PF08763": 1})
check("a pore model outranks the claudin/TARP rule (HC2)", m.family, "cav_hva")

# -------------------------------------------------------------- symbols
print("\nthe gene symbol is never consulted (HC2, HC10)")
counts = {"PF00625": 1}
a = classify(ChannelQuery("X1", gene_symbol="CACNA1C", pfam_counts=counts))
b = classify(ChannelQuery("X1", gene_symbol="", pfam_counts=counts))
c = classify(ChannelQuery("X1", gene_symbol="TOTAL_NONSENSE", pfam_counts=counts))
check("same call with, without and with a misleading symbol",
      {a.family, b.family, c.family}, {"assoc_cav_aux"})

# ---------------------------------------------------------------- motifs
print("\nmotifs")
check("TxGYG found in a KcsA-like filter",
      [m for _, m in k_filter_hits("AAATVGYGDLYP")], ["TVGYG"])
check("no K+ filter in a random stretch", k_filter_hits("MKKLLIVDDE"), [])
check("the MCU DIME motif is found where MCU carries it",
      [m for _, m in mcu_filter_hits("TWWEYSWDIMEPVTYFITY")], ["WDIME"])
check("no DIME motif in a calmodulin EF-hand",
      mcu_filter_hits("DKDGDGTITTKELGTVMRSL"), [])
check("the EF-hand loop of calmodulin is found",
      [m for _, m in ef_hand_hits("AEFKEAFSLFDKDGDGTITTKELGTVMRSL")],
      ["DKDGDGTITTKE"])
check("every filter string maps to a catalogued family",
      sorted({f for f, _ in FILTER_CALLS.values() if f not in CATALOGUE}), [])
check("EEDD is a calcium channel, not a non-call (HC14)",
      FILTER_CALLS["EEDD"][0], "cav_lva")
check("DEKA is called, and called as a sodium channel (HC1)",
      FILTER_CALLS["DEKA"][0], "outofscope_nav")
check("the TRPV anchor is a single position with a recorded expectation",
      (len(TRPV_CA_ANCHOR.positions), TRPV_CA_ANCHOR.expected), (1, "D"))

# ---------------------------------------------------------- alignment ops
print("\nalignment helpers")
check("projection maps reference positions onto the query",
      project_positions("AB-CD", "AXYCD", [1, 2, 3, 4]),
      {1: "A", 2: "X", 3: "C", 4: "D"})
check("covered-only identity ignores overhang",
      round(percent_identity("AAAA----", "AAAAKKKK", covered_only=True), 3), 1.0)
check("full-alignment identity does not",
      round(percent_identity("AAAA----", "AAAAKKKK", covered_only=False), 3), 0.5)
# The parent project's measured failure: a short sequence scattered through a
# long one keeps a high covered identity and near-total coverage *of itself*,
# and only coverage of the longer sequence exposes it (D30). With a 5,038 aa
# ryanodine receptor in the panel this matters more here, not less.
_id, _cs, _cl, _n = alignment_stats("A-A-A-A-", "AXAXAXAX")
check("coverage of the shorter sequence does not catch a cherry-picked hit",
      round(_cs, 3), 1.0)
check("coverage of the longer sequence does", round(_cl, 3), 0.5)

# -------------------------------------------------------------- phylogeny
print("\nphylogeny - D27")
refused = {k for k, _ in refused_superfamilies()}
check_true("some superfamilies are marked non-alignable", refused, "none marked")
for sf in sorted(refused):
    try:
        build_tier2(sf, [], ROOT / "results" / "_selftest")
        print(f"  FAIL tier-2 on {sf} was ACCEPTED")
        FAILURES.append(f"tier2-{sf}")
    except NotAlignable:
        print(f"  ok   tier-2 on {sf} refused")

# ------------------------------------------------------------------ scope
print("\nscope")
itpr = scope_for("itpr")
check("the ITPR scope derives its sister panel from the hazards",
      sorted(itpr.sister_family_keys), ["nonchannel_pomt", "ryr"])
check_true("the ITPR sister panel carries RyR gene symbols",
           "RYR1" in itpr.sister_genes, itpr.sister_genes)
cav = scope_for("cav_hva")
check_true("the Cav scope's sisters include the sodium channels",
           "outofscope_nav" in cav.sister_family_keys, cav.sister_family_keys)
check_true("...and the pumps that a keyword search would return",
           "transporter_ca_atpase" in cav.sister_family_keys,
           cav.sister_family_keys)
allsc = scope_for("all")
check_true("the whole-catalogue scope enumerates more than PF00520",
           len(allsc.pfam_ids) > 1 and "PF00520" in allsc.pfam_ids,
           allsc.pfam_ids[:5])

print()
if FAILURES:
    print(f"{len(FAILURES)} invariant(s) FAILED: {', '.join(FAILURES)}")
    sys.exit(1)
print("all invariants hold")
