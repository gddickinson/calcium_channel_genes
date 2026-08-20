"""The calcium-channel catalogue - this project's definition of its own subject.

Contents:
    schema.py         - ChannelFamily / Superfamily / Permeability / Hazard types
    ploop.py          - the P-loop superfamily: Cav1/2, Cav3, CatSper, CNG, TPC
    trp.py            - TRPV, TRPC, TRPM, TRPA, TRPML, TRPP
    release.py        - ITPR and RYR: the intracellular release channels
    store_operated.py - ORAI / CRAC
    organelle.py      - MCU and VDAC: the mitochondrial pathway
    lgic.py           - Ca2+-permeable nicotinic, AMPA, kainate, NMDA and P2X
    mechano.py        - Piezo
    largepore.py      - CALHM
    nonanimal.py      - plant GLR/CNGC/MCA, OSCA/TMEM63, viral viroporins
    controls_associated.py - auxiliary subunits: the CACN* trap, STIM, EMRE
    controls_excluded.py   - Nav, the Ca2+-activated channels, pumps,
                             exchangers, EF-hand sensors, CASR
    hazards.py        - the eighteen recorded ways to get a call wrong
    registry.py       - assembly, lookups, `census_by_tier()`, `validate()`

Import from `registry` (or from this package), never from a division file.

    from src.catalogue import CATALOGUE, census_families, validate
"""

from .hazards import HAZARD_BY_ID, HAZARDS
from .registry import (CATALOGUE, SUPERFAMILIES, census_by_tier,
                       census_families, control_families, exemplars, families,
                       families_by_ca_class, family, family_for_gene,
                       hazards_for, human_genes, pore_signatures,
                       reference_panel, shared_signatures, signature_index,
                       stats, superfamily, validate, with_resolved_exemplars)
from .schema import (CA_CENSUS_CLASSES, CENSUS_STATUSES, NOT_CALCIUM, CaClass,
                     ChannelFamily, Exemplar, Fold, Gating, Hazard, Level,
                     Permeability, Provenance, Selectivity, Signature, Status,
                     Superfamily)

__all__ = [
    "CATALOGUE", "SUPERFAMILIES", "HAZARDS", "HAZARD_BY_ID",
    "CENSUS_STATUSES", "CA_CENSUS_CLASSES", "NOT_CALCIUM",
    "ChannelFamily", "Superfamily", "Signature", "Exemplar", "Hazard",
    "Permeability", "CaClass",
    "Level", "Provenance", "Gating", "Selectivity", "Fold", "Status",
    "family", "superfamily", "families", "census_families",
    "control_families", "families_by_ca_class", "census_by_tier",
    "human_genes", "family_for_gene", "signature_index", "shared_signatures",
    "pore_signatures", "exemplars", "reference_panel", "hazards_for",
    "with_resolved_exemplars", "validate", "stats",
]
