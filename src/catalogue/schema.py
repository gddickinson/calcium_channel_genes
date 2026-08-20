"""The types the calcium-channel catalogue is written in.

One `ChannelFamily` record per family, grouped into `Superfamily` records.
Everything the project treats as an *assertion about biology* lives in these
records, so a claim can be traced to one line of one file and checked
against a live database by `scripts/s0_catalogue_verify.py`.

Four ideas carry the design. The first three are inherited from the
ion-channel project this codebase is ported from; the fourth is what makes
this a calcium project rather than a search-and-replace of that one.

**Signatures have a level.** A Pfam accession is only evidence for the level
at which it is diagnostic. `PF00520` (Ion_trans) is carried by Cav, Nav,
NALCN, CatSper, TRP and CNG alike, so it is a `SUPERFAMILY` signature — it
says "P-loop channel", never "this is a calcium channel". Recording the
level in the data is what stops the classifier from making a family call on
superfamily evidence (decision **D25**).

**Status is not the same as membership.** A family is in the catalogue
because a search for calcium channels will hit it, not because it is one.
The Ca2+-*activated* potassium and chloride channels, the Ca2+ pumps and
exchangers, the EF-hand calcium sensors and the auxiliary subunits with
`CACN` in their symbols are all catalogued *and* marked, so an excluded
thing is excluded by a recorded decision rather than by never having been
considered.

**Nothing here is trusted until it is verified.** Every accession carries a
`Provenance` tag; `results/s0_baseline/catalogue_verification.tsv` records
what a live check made of it. Curated-but-unverified is a legitimate state,
silently-wrong is not.

**Calcium membership is graded, and the grade carries its own evidence.**
This is the difference from a sodium or potassium census. "Calcium channel"
is not a clade and not a domain signature: it is a *permeability ratio*,
measured per channel, per subunit composition, and in the case of the
AMPA receptors per RNA-editing state of one codon. So a family does not
simply have a `Selectivity`; it has a `Permeability` record naming its
`CaClass` tier, the reported P_Ca/P_Na, how that number was obtained and
where it came from. The census denominator is then a choice of tier that
the reader can see and disagree with, rather than a boundary buried in a
gene list (decision **D31**).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Level(str, Enum):
    """The taxonomic level at which a signature is diagnostic."""
    SUPERFAMILY = "superfamily"   # shared across the superfamily; never a family call
    FAMILY = "family"             # diagnostic for this family
    SUBFAMILY = "subfamily"       # diagnostic for a subset of the family
    ACCESSORY = "accessory"       # present, but common to unrelated proteins
    SHARED_WITH_DECOY = "shared_with_decoy"  # also carried by a known non-channel


class Provenance(str, Enum):
    """How far an assertion can be trusted, in the parent projects' grammar."""
    DB = "db"        # re-derived from a live database by an S0 script
    LIT = "lit"      # literature; audited in S0
    CURATED = "curated"   # hand-written here, not yet checked
    OPEN = "open"    # a question this project answers


class CaClass(str, Enum):
    """How a family relates to calcium — the census's membership tiers.

    The tiers are ordered by how much of the claim rests on the sequence and
    how much on a measurement made in a particular cell:

    * `SELECTIVE` — the pore discriminates strongly for Ca2+ (P_Ca/P_Na
      roughly > 10, usually far more). Cav, ORAI, TRPV5/6, MCU.
    * `PERMEABLE` — a non-selective cation channel that nonetheless carries a
      physiologically important Ca2+ current. Most TRPs, P2X, Piezo, CNG.
    * `CONDITIONAL` — Ca2+ permeability depends on something the genome does
      not show: subunit composition, alternative splicing, or RNA editing.
      The AMPA receptors are the canonical case and the reason this tier
      exists (hazard **HC8**).
    * `RELEASE` — releases Ca2+ from an intracellular store rather than
      admitting it across the plasma membrane. ITPR, RYR, and the organelle
      channels.
    * `ACTIVATED` — *gated by* calcium and does not conduct it. BK, SK, ANO1,
      TRPM4/5. In the catalogue precisely because a keyword census counts
      them (hazard **HC15**).
    * `NOT_CALCIUM` — conducts something else, or conducts nothing.
    """
    SELECTIVE = "ca_selective"
    PERMEABLE = "ca_permeable"
    CONDITIONAL = "ca_conditional"
    RELEASE = "ca_release"
    ACTIVATED = "ca_activated"
    NOT_CALCIUM = "not_calcium"


#: The tiers that count towards the calcium census (see `CENSUS_STATUSES`;
#: a family must satisfy both to be counted).
CA_CENSUS_CLASSES = (CaClass.SELECTIVE, CaClass.PERMEABLE,
                     CaClass.CONDITIONAL, CaClass.RELEASE)


class Gating(str, Enum):
    VOLTAGE = "voltage"
    LIGAND_EXTRACELLULAR = "ligand_extracellular"
    LIGAND_INTRACELLULAR = "ligand_intracellular"
    CYCLIC_NUCLEOTIDE = "cyclic_nucleotide"
    STORE_DEPLETION = "store_depletion"   # ORAI: the gate is in another organelle
    CALCIUM = "calcium"                   # Ca2+-dependent activation or inactivation
    MECHANICAL = "mechanical"
    THERMAL = "thermal"
    PROTON = "proton"
    LIPID = "lipid"
    PHOSPHORYLATION = "phosphorylation"
    MEMBRANE_APPOSITION = "membrane_apposition"   # RyR1 by Cav1.1, mechanically
    LEAK = "leak"
    UNKNOWN = "unknown"


class Selectivity(str, Enum):
    CA = "Ca2+"
    NA = "Na+"
    K = "K+"
    ANION = "anion"
    CATION_NONSELECTIVE = "cation_nonselective"
    MONOVALENT_CATION = "monovalent_cation"   # TRPM4/5: cation, but not divalent
    LARGE_PORE = "large_pore"
    UNKNOWN = "unknown"


class Fold(str, Enum):
    """Structural fold of the pore-forming module.

    The fold, not the sequence, is what makes two families comparable at all
    — and folds shared without detectable sequence homology are exactly the
    cases the phylogeny protocol forbids putting in one tree (**D27**).
    """
    P_LOOP = "p_loop"                 # VGIC superfamily: S5-P-S6 pore module
    CYS_LOOP = "cys_loop"             # pentameric LGIC
    IGLUR = "iglur"                   # tetrameric LGIC, clamshell + inverted pore
    P2X = "p2x"                       # trimeric, dolphin fold
    ORAI = "orai"                     # hexameric CRAC
    MCU = "mcu"                       # mitochondrial Ca2+ uniporter
    BETA_BARREL = "beta_barrel"       # VDAC
    PIEZO = "piezo"                   # three-bladed propeller
    CALHM = "calhm"                   # octa/undecameric large pore
    CONNEXIN = "connexin"             # hexameric hemichannel
    INNEXIN = "innexin"               # octameric; pannexin fold
    TMEM16 = "tmem16"                 # anoctamin channel/scramblase fold
    TRIC = "tric"                     # trimeric intracellular cation
    P_TYPE_ATPASE = "p_type_atpase"   # SERCA, PMCA, SPCA — pumps
    CACA_EXCHANGER = "ca_exchanger"   # NCX / NCKX / NCLX
    EF_HAND = "ef_hand"               # the sensors: calmodulin and relatives
    VIROPORIN = "viroporin"
    UNKNOWN = "unknown"


class Status(str, Enum):
    """Why a record is in the catalogue."""
    CHANNEL = "channel"                       # pore-forming; in the census
    CHANNEL_CONTESTED = "channel_contested"   # channel or Ca2+ role disputed; in, flagged
    CHANNEL_ASSOCIATED = "channel_associated" # auxiliary subunit; not a pore
    TRANSPORTER = "transporter"               # pump or exchanger, not a channel
    NON_CHANNEL_HOMOLOG = "non_channel_homolog"  # shares a signature, is not a channel
    OUT_OF_SCOPE = "out_of_scope"             # a real ion channel, but not a Ca2+ channel


#: Statuses that count towards the census denominator. A family must also
#: carry a `CaClass` in `CA_CENSUS_CLASSES` — a channel that is not a
#: calcium channel is `OUT_OF_SCOPE` and a channel whose calcium role is
#: disputed is `CHANNEL_CONTESTED` and stays in, flagged.
CENSUS_STATUSES = (Status.CHANNEL, Status.CHANNEL_CONTESTED)


@dataclass(frozen=True)
class Permeability:
    """What is actually known about a family's calcium permeability.

    `p_ca_over_p_na` is recorded **as reported**, as a string — ">1000",
    "~10", "0.1–4 depending on subunit" — because that is the shape the
    literature has. Turning a range measured in one cell type at one
    divalent concentration into a float would invent a precision nobody
    measured, and the census's boundary would then rest on it.

    `method` names how the number was obtained, because reversal-potential
    ratios, fractional-current (P_f) measurements and Ca2+-imaging estimates
    are not the same quantity and the literature quotes all three.
    """
    ca_class: CaClass
    p_ca_over_p_na: str = ""
    method: str = ""
    provenance: Provenance = Provenance.LIT
    note: str = ""

    def census_member(self) -> bool:
        return self.ca_class in CA_CENSUS_CLASSES

    def describe(self) -> str:
        bits = [self.ca_class.value]
        if self.p_ca_over_p_na:
            bits.append(f"P_Ca/P_Na {self.p_ca_over_p_na}")
        if self.method:
            bits.append(self.method)
        return "; ".join(bits)


#: The default for control families — no calcium claim is being made.
NOT_CALCIUM = Permeability(CaClass.NOT_CALCIUM, provenance=Provenance.CURATED)


@dataclass(frozen=True)
class Signature:
    """One domain signature, with the level at which it means something."""
    db: str                 # "pfam" | "interpro"
    accession: str          # "PF00520"
    name: str               # "Ion_trans"
    level: Level = Level.FAMILY
    copies: int = 1         # expected copies per subunit (4 for Cav/Nav)
    provenance: Provenance = Provenance.CURATED
    note: str = ""

    def key(self) -> str:
        return f"{self.db}:{self.accession}"


@dataclass(frozen=True)
class Exemplar:
    """A reference protein for a family: the thing new sequences are scored against.

    `uniprot` may be empty when the record is curated from a gene symbol
    alone; `scripts/s0_catalogue_verify.py` resolves and fills the gap in
    `results/s0_baseline/exemplars_resolved.tsv` rather than editing code.
    """
    label: str              # "Hs_CACNA1C"
    gene: str               # "CACNA1C"
    species: str            # "Homo sapiens"
    uniprot: str = ""       # "Q13936"
    note: str = ""


@dataclass(frozen=True)
class ChannelFamily:
    """One family of the catalogue."""
    key: str                       # "cav_hva"
    name: str                      # "High-voltage-activated calcium channels"
    superfamily: str               # key into SUPERFAMILIES
    status: Status
    fold: Fold
    selectivity: Selectivity
    gating: tuple[Gating, ...]
    permeability: Permeability = NOT_CALCIUM
    stoichiometry: str = "tetramer"
    tm_per_subunit: int = 0        # 0 = not applicable / unknown
    pore_loops_per_subunit: int = 0
    signatures: tuple[Signature, ...] = ()
    exemplars: tuple[Exemplar, ...] = ()
    human_genes: tuple[str, ...] = ()
    other_genes: tuple[str, ...] = ()      # non-human members worth naming
    length_band_aa: tuple[int, int] = (0, 0)
    filter_motif: str = ""         # selectivity-filter signature, if one exists
    compartment: str = ""          # where the Ca2+ comes from or goes to
    iuphar_class: str = ""         # the IUPHAR/BPS name, where there is one
    confusable_with: tuple[str, ...] = ()  # family keys / hazard ids
    provenance: Provenance = Provenance.CURATED
    notes: str = ""

    def census_member(self) -> bool:
        """In the calcium census: a channel *and* a calcium-carrying one."""
        return (self.status in CENSUS_STATUSES
                and self.permeability.census_member())

    def ca_class(self) -> CaClass:
        return self.permeability.ca_class

    def diagnostic_signatures(self) -> tuple[Signature, ...]:
        return tuple(s for s in self.signatures
                     if s.level in (Level.FAMILY, Level.SUBFAMILY))

    def superfamily_signatures(self) -> tuple[Signature, ...]:
        return tuple(s for s in self.signatures if s.level is Level.SUPERFAMILY)

    def architecture(self) -> str:
        """The domain pattern, with the non-diagnostic parts marked.

        Signatures shared with a known decoy are shown in brackets: they are
        part of the architecture and are not evidence for the family, and a
        display that omitted them would make the family look more
        distinguishable than it is. `PF08016` on TRPP is the case in point —
        it is also on TRPML and on polycystin-1, which is not a pore.
        """
        parts = []
        for s in self.signatures:
            if s.level is Level.ACCESSORY:
                continue
            token = f"{s.accession}x{s.copies}" if s.copies > 1 else s.accession
            parts.append(f"[{token}]" if s.level is Level.SHARED_WITH_DECOY
                         else token)
        return " + ".join(parts)


@dataclass(frozen=True)
class Superfamily:
    """A group of families with a common pore fold and a common ancestor.

    Superfamilies are defined **by descent, not by ion**. `ploop` therefore
    holds the calcium channels of the voltage-gated-like superfamily *and*
    the sodium and potassium channels that share their fold, because that is
    what the phylogeny is about and because the sodium channels are this
    project's most important decoys. Which member conducts calcium is a
    property of the family, in `Permeability` (**D24**).

    `alignable` is the load-bearing field: it says whether the member
    families can be put in one sequence alignment at all. Where it is False
    the relationship is structural only, and the phylogeny protocol routes
    the comparison to the fold network instead of to a tree (**D27**).
    """
    key: str
    name: str
    fold: Fold
    alignable: bool = True
    anchor_module: str = ""        # the region a cross-family alignment uses
    shared_signatures: tuple[Signature, ...] = ()
    root_with: tuple[str, ...] = ()   # outgroup family keys for rooting
    notes: str = ""


@dataclass(frozen=True)
class Hazard:
    """A recorded way to get the classification wrong.

    The grandparent project (`../ip3r_genes`) carried exactly one of these —
    ITPR versus RYR — and it was load-bearing enough to become decision D14
    there. A calcium census has its own set, and they are of two kinds: the
    ones domain architecture cannot resolve (Cav versus Nav), and the ones
    where the *word calcium* is the trap (Ca2+-activated potassium channels,
    Ca2+ pumps, Ca2+-binding proteins, `CACNG` subunits that are really AMPA
    receptor auxiliaries). Every hazard names the discriminating test the
    classifier must apply, and `scripts/s1_benchmark.py` measures whether
    that test works.
    """
    hid: str                       # "HC1"
    title: str
    families: tuple[str, ...]      # catalogue keys involved
    shared_evidence: str           # what makes them look alike
    discriminator: str             # the positive test that separates them
    test_owner: str = ""           # which module implements the test
    severity: str = "high"         # high | medium | low
    provenance: Provenance = Provenance.CURATED
    notes: str = ""
