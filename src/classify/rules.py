"""The architecture tier - domain-composition rules, and the hazard rules that override them.

A rule fires on the *multiset* of domain accessions a protein carries: which
signatures are present, and in how many copies. That is enough to make a
confident call for maybe two thirds of the catalogue and is provably not
enough for the rest, which is the point of keeping the rules in a table that
records their own priority.

Rules come from two places.

**Derived rules** are generated from the catalogue itself: a family's
`FAMILY`- and `SUBFAMILY`-level signatures become its requirement, and a
family with only `SUPERFAMILY` signatures generates a superfamily-level rule
that deliberately declines to name a family. Nothing is hand-maintained
twice - edit the catalogue and the rules follow.

**Hazard rules** are hand-written, sit at higher priority, and exist because
a hazard is only closed by a test. Each one names its `HC` number, so
`scripts/s1_benchmark.py` can report per-hazard precision and recall, and so
that deleting a rule is visibly deleting a test.

Half of these rules exist to keep something *out* of the census. That is the
shape of a calcium project: the pumps, the exchangers, the EF-hand sensors,
the sixteen `CACN`-prefixed auxiliary subunits and the Ca2+-activated
potassium and chloride channels all arrive with calcium annotations
attached, and each needs a positive test that says what it is instead.
`_CENSUS_SIGNATURES` is derived from the catalogue's own pore models so that
"carries no pore" is a claim about this catalogue rather than a hard-coded
list that will drift away from it.

Ties are not resolved. Two rules of equal priority naming different families
produce an `ambiguous` result carrying both, which the classifier hands to
the reference and motif tiers. Silently picking the first match would turn
the whole hazard registry into decoration.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..catalogue import CATALOGUE, Level, census_families, pore_signatures

# Priorities. Higher wins; equal-and-different is ambiguity, not a coin toss.
P_HAZARD = 100
P_FAMILY_STRONG = 50    # two or more family-level signatures
P_FAMILY = 40           # one family-level signature
P_SUPERFAMILY = 10      # superfamily evidence only - no family call

#: Every family- or superfamily-level signature any census family declares.
#: Used by the rules that have to say "and carries nothing a calcium channel
#: carries" - HC2, HC10, HC12 - so the negative half of those tests tracks
#: the catalogue instead of drifting from a hard-coded list. Deliberately
#: broader than "pore models": `PF00027` (the cyclic-nucleotide-binding
#: domain) is not a pore, and a protein carrying it is not something these
#: rules should be filing as an auxiliary subunit on negative evidence.
_CENSUS_SIGNATURES: tuple[str, ...] = tuple(
    sorted({s.accession for s in pore_signatures()}))


@dataclass(frozen=True)
class ArchitectureRule:
    rid: str
    target: str                       # catalogue family key ("" = superfamily only)
    superfamily: str
    require: tuple[str, ...] = ()     # accessions that must be present
    min_copies: tuple[tuple[str, int], ...] = ()   # (accession, minimum copies)
    forbid: tuple[str, ...] = ()      # accessions that must be absent
    priority: int = P_FAMILY
    hazard: str = ""
    rationale: str = ""

    def matches(self, counts: dict[str, int]) -> bool:
        if any(a not in counts for a in self.require):
            return False
        if any(counts.get(a, 0) < n for a, n in self.min_copies):
            return False
        if any(a in counts for a in self.forbid):
            return False
        return bool(self.require or self.min_copies)

    def describe(self) -> str:
        bits = []
        if self.require:
            bits.append("+".join(self.require))
        for a, n in self.min_copies:
            bits.append(f"{a}×≥{n}")
        if self.forbid:
            bits.append("without " + "/".join(self.forbid))
        return " ".join(bits)


# --------------------------------------------------------- hazard rules
HAZARD_RULES: list[ArchitectureRule] = [
    # HC1 - the four-repeat families are architecturally identical.
    ArchitectureRule("HC1-fourrepeat", "", "ploop",
                     min_copies=(("PF00520", 4),),
                     forbid=("PF06512", "PF08763"),
                     priority=P_HAZARD, hazard="HC1",
                     rationale="four repeats with no family-specific domain: "
                               "Cav3, NALCN and CatSper are indistinguishable "
                               "here - hand to the motif tier"),
    ArchitectureRule("HC1-nav", "outofscope_nav", "ploop",
                     ("PF00520", "PF06512"), priority=P_HAZARD, hazard="HC1",
                     rationale="Na_trans_assoc is the one Nav-specific domain; "
                               "a sodium channel is not a calcium channel"),
    ArchitectureRule("HC1-cav", "cav_hva", "ploop", ("PF00520", "PF08763"),
                     priority=P_HAZARD, hazard="HC1",
                     rationale="the Ca_chan_IQ calmodulin site is on Cav1/Cav2 "
                               "and measured absent from Cav3"),
    # HC2 - sixteen human CACN* genes are auxiliary subunits.
    ArchitectureRule("HC2-cacnb", "assoc_cav_aux", "ploop", ("PF00625",),
                     forbid=_CENSUS_SIGNATURES, priority=P_HAZARD, hazard="HC2",
                     rationale="a guanylate-kinase (MAGUK) fold carrying no "
                               "census-family signature => the Cav beta subunit"),
    ArchitectureRule("HC2-a2d", "assoc_cav_aux", "ploop", ("PF08473",),
                     priority=P_HAZARD, hazard="HC2",
                     rationale="VGCC_alpha2 => alpha2delta, the gabapentin "
                               "target and not a pore"),
    ArchitectureRule("HC2-tarp", "assoc_cav_aux", "ploop", ("PF00822",),
                     forbid=_CENSUS_SIGNATURES, priority=P_HAZARD, hazard="HC2",
                     rationale="a claudin fold with no channel signature => a gamma/TARP "
                               "subunit; CACNG2-8 belong to the AMPA receptor"),
    # HC3 - ITPR versus RYR (inherited decision D14).
    ArchitectureRule("HC3-ryr", "ryr", "ca_release", ("PF08709", "PF02026"),
                     priority=P_HAZARD, hazard="HC3",
                     rationale="the RyR repeat is present in RYR and absent "
                               "from ITPR"),
    ArchitectureRule("HC3-itpr", "itpr", "ca_release", ("PF08709",),
                     forbid=("PF02026", "PF06459"), priority=P_HAZARD,
                     hazard="HC3",
                     rationale="IP3R core without any RyR-specific domain"),
    # HC4 - MIR is shared with the O-mannosyltransferases.
    ArchitectureRule("HC4-pomt", "nonchannel_pomt", "ca_release",
                     ("PF02815", "PF02366"), priority=P_HAZARD, hazard="HC4",
                     rationale="MIR + mannosyltransferase => POMT"),
    # HC5 - the gate is in another organelle.
    ArchitectureRule("HC5-orai", "orai", "orai", ("PF07856",),
                     priority=P_HAZARD, hazard="HC5",
                     rationale="Orai-1 => the CRAC pore"),
    ArchitectureRule("HC5-stim", "assoc_stim", "orai", ("PF16533",),
                     forbid=("PF07856",), priority=P_HAZARD, hazard="HC5",
                     rationale="the ORAI-activating region without the pore "
                               "=> STIM: a gate, not a channel"),
    # HC6 - pore subunit versus regulator in the uniporter complex.
    ArchitectureRule("HC6-mcu", "mcu", "mcu", ("PF04678",),
                     priority=P_HAZARD, hazard="HC6",
                     rationale="the MCU model marks a pore subunit, MCUB "
                               "included"),
    ArchitectureRule("HC6-micu", "assoc_mcu_reg", "mcu", ("PF13833",),
                     forbid=("PF04678",), priority=P_HAZARD, hazard="HC6",
                     rationale="an EF-hand gatekeeper with no pore => MICU"),
    ArchitectureRule("HC6-emre", "assoc_mcu_reg", "mcu", ("PF10161",),
                     forbid=("PF04678",), priority=P_HAZARD, hazard="HC6",
                     rationale="EMRE: required for conduction, lines no pore"),
    # HC9 - PF08016 covers TRPML, TRPP and polycystin-1.
    ArchitectureRule("HC9-pkd1", "assoc_polycystin1", "ploop", ("PF08016",),
                     min_copies=(("PF00801", 5),), priority=P_HAZARD,
                     hazard="HC9",
                     rationale="a long PKD-repeat ectodomain => polycystin-1"),
    ArchitectureRule("HC9-trpml", "trpml", "ploop", ("PF08016", "PF21381"),
                     priority=P_HAZARD, hazard="HC9",
                     rationale="the mucolipin extracytosolic domain"),
    ArchitectureRule("HC9-trpp", "trpp", "ploop", ("PF08016", "PF20519"),
                     forbid=("PF21381",), priority=P_HAZARD, hazard="HC9",
                     rationale="polycystin domain without the mucolipin domain"),
    # HC10 - the CATSPER symbol root covers four pores and seven accessories.
    ArchitectureRule("HC10-catsper-aux", "assoc_catsper_aux", "ploop",
                     ("PF15149",), forbid=_CENSUS_SIGNATURES,
                     priority=P_HAZARD, hazard="HC10",
                     rationale="CATSPERB_C with no channel signature => an accessory subunit"),
    # HC11 - pumps and exchangers move calcium and are not channels.
    ArchitectureRule("HC11-pump", "transporter_ca_atpase", "p_type_atpase",
                     ("PF00122", "PF00689"), priority=P_HAZARD, hazard="HC11",
                     rationale="the P-type ATPase core => SERCA/PMCA/SPCA"),
    ArchitectureRule("HC11-exchanger", "transporter_ca_exchanger",
                     "ca_exchanger", ("PF01699",), priority=P_HAZARD,
                     hazard="HC11",
                     rationale="the Na_Ca_ex alpha-repeats => NCX/NCKX/NCLX"),
    # HC12 - calcium binding is one keyword away from calcium conducting.
    ArchitectureRule("HC12-casr", "nonchannel_casr_gpcr", "iglur",
                     ("PF01094", "PF00003"), priority=P_HAZARD, hazard="HC12",
                     rationale="clamshell + 7tm_3 => a class C GPCR; CASR "
                               "senses calcium and conducts nothing"),
    ArchitectureRule("HC12-efhand", "nonchannel_efhand", "ca_sensor",
                     ("PF13499",), forbid=_CENSUS_SIGNATURES,
                     priority=P_HAZARD, hazard="HC12",
                     rationale="an EF-hand with no channel signature => a calcium "
                               "sensor or buffer, not a channel"),
    # HC15 - Ca2+-activated channels conduct potassium or chloride.
    ArchitectureRule("HC15-bk", "outofscope_kca", "ploop", ("PF03493",),
                     priority=P_HAZARD, hazard="HC15",
                     rationale="BK_channel_a => a Ca2+-activated potassium "
                               "channel; confirm with the TxGYG filter"),
    ArchitectureRule("HC15-ano", "outofscope_anoctamin", "tmem16",
                     ("PF04547",), priority=P_HAZARD, hazard="HC15",
                     rationale="the anoctamin fold => a Ca2+-activated "
                               "chloride channel"),
]


# -------------------------------------------------------- derived rules
def derived_rules() -> list[ArchitectureRule]:
    """Rules generated from the catalogue's own signature declarations.

    Two rules per family where the catalogue supports them, and the split
    matters. A **family rule** requires only the `FAMILY`-level signatures,
    because those are the ones every member is expected to carry. A
    **subfamily rule** additionally requires the `SUBFAMILY`-level ones and
    sits at higher priority, so a protein that has them gets the more
    specific call and a protein that does not is still matched.

    Measured in the parent project: with `SUBFAMILY` signatures folded
    into the family requirement, `kv_shaker` required `PF02214` + `PF03521`
    (the Kv2-only model) and KCNA1 — a Kv1 — fell through to `kv_modifier`,
    whose rule needs `PF02214` alone. The correct architecture-tier answer
    for KCNA1 is *ambiguous between `kv_shaker` and `kv_modifier`*, which is
    what this generator now produces: the two families really are
    architecturally identical, and the reference tier is what separates them.

    Copy-number requirements are **not** generated here. They are brittle at
    family scale — measured: OTOP1 carries `PF03189`×3 and OTOP2 ×2 — so the
    two places where copy number is genuinely diagnostic (`PF07885`×2 for
    K2P, `PF00520`×4 for the four-repeat channels) are hazard rules instead,
    where the number is stated with the measurement behind it.
    """
    out: list[ArchitectureRule] = []
    for fam in census_families():
        family_sigs = tuple(s.accession for s in fam.signatures
                            if s.level is Level.FAMILY)
        subfamily_sigs = tuple(s.accession for s in fam.signatures
                               if s.level is Level.SUBFAMILY)
        if family_sigs:
            out.append(ArchitectureRule(
                f"cat-{fam.key}", fam.key, fam.superfamily, family_sigs,
                priority=(P_FAMILY_STRONG if len(family_sigs) > 1 else P_FAMILY),
                rationale=f"family-level signatures of {fam.name}"))
            if subfamily_sigs:
                out.append(ArchitectureRule(
                    f"cat-sub-{fam.key}", fam.key, fam.superfamily,
                    family_sigs + subfamily_sigs,
                    priority=P_FAMILY_STRONG + 5,
                    rationale=f"family + subfamily signatures of {fam.name}"))
            continue
        if subfamily_sigs:
            out.append(ArchitectureRule(
                f"cat-sub-{fam.key}", fam.key, fam.superfamily, subfamily_sigs,
                priority=P_FAMILY,
                rationale=f"subfamily signatures of {fam.name}"))
            continue
        shared = [s.accession for s in fam.signatures
                  if s.level is Level.SUPERFAMILY]
        if shared:
            out.append(ArchitectureRule(
                f"cat-sf-{fam.key}", "", fam.superfamily, tuple(shared[:1]),
                priority=P_SUPERFAMILY,
                rationale=(f"{fam.name} carries superfamily evidence only — "
                           f"no family call is possible from architecture")))
    return out


def all_rules() -> list[ArchitectureRule]:
    return HAZARD_RULES + derived_rules()


# ------------------------------------------------------------- matching
@dataclass
class RuleMatch:
    """The architecture tier's verdict."""
    family: str = ""
    superfamily: str = ""
    ambiguous: list[str] = field(default_factory=list)
    fired: list[ArchitectureRule] = field(default_factory=list)
    hazards: list[str] = field(default_factory=list)

    def called(self) -> bool:
        return bool(self.family)

    def summary(self) -> str:
        if self.family:
            head = f"family {self.family}"
        elif self.ambiguous:
            head = "ambiguous between " + ", ".join(sorted(self.ambiguous))
        elif self.superfamily:
            head = f"superfamily {self.superfamily} only"
        else:
            head = "no architecture match"
        rules = ", ".join(f"{r.rid}[{r.describe()}]" for r in self.fired[:4])
        return f"{head} — {rules}" if rules else head


def match_architecture(counts: dict[str, int],
                       rules: list[ArchitectureRule] | None = None) -> RuleMatch:
    """Match a `{accession: copies}` multiset against the rule table."""
    rules = rules if rules is not None else all_rules()
    fired = [r for r in rules if r.matches(counts)]
    if not fired:
        return RuleMatch()
    best = max(r.priority for r in fired)
    top = [r for r in fired if r.priority == best]
    targets = {r.target for r in top if r.target}
    sfs = {r.superfamily for r in top if r.superfamily}
    res = RuleMatch(
        superfamily=(next(iter(sfs)) if len(sfs) == 1 else ""),
        fired=sorted(fired, key=lambda r: -r.priority),
        hazards=sorted({r.hazard for r in fired if r.hazard}),
    )
    if len(targets) == 1:
        res.family = next(iter(targets))
    elif len(targets) > 1:
        res.ambiguous = sorted(targets)
    return res


def topology_check(family_key: str, tm_count: int | None,
                   pore_loops: int | None = None) -> tuple[bool, str]:
    """Is an observed topology consistent with the family's declared one?

    Hazard **H8**: which Pfam pore model matched does *not* track the number
    of transmembrane helices — the 6TM SK channels are annotated with the 2TM
    model — so topology is taken from UniProt features or a prediction and
    compared here, never inferred from the domain hit.
    """
    fam = CATALOGUE.get(family_key)
    if fam is None or tm_count is None or not fam.tm_per_subunit:
        return True, "no topology expectation recorded"
    expected = fam.tm_per_subunit
    tol = max(2, expected // 4)
    ok = abs(tm_count - expected) <= tol
    detail = (f"{tm_count} TM observed vs {expected} expected "
              f"(±{tol}) for {fam.key}")
    if pore_loops is not None and fam.pore_loops_per_subunit:
        ok = ok and pore_loops == fam.pore_loops_per_subunit
        detail += f"; {pore_loops} pore loop(s) vs {fam.pore_loops_per_subunit}"
    return ok, detail
