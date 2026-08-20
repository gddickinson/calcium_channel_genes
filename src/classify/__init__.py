"""Classification of a protein into the calcium-channel catalogue.

Contents:
    rules.py       - the architecture tier: domain-composition rules derived
                     from the catalogue, plus the hand-written hazard rules
                     (half of which exist to keep something out of the census)
    motifs.py      - the motif tier: three reference-free regexes (the K+
                     filter, the MCU DIME motif, the EF-hand loop) and three
                     projected anchors (the four-repeat Cav/Nav filter, the
                     TRPV aspartate ring, the ORAI E106 glutamate)
    reference.py   - the reference tier: best-hit identity to the exemplar
                     panel with a margin (D7) and a coverage floor (D30)
    classifier.py  - combines the tiers into one `ChannelCall` with an audit
                     trail and a confidence tier
    report.py      - benchmark tables: confusion matrix, per-family recall,
                     per-hazard precision

The classifier emits a **family** call. It deliberately emits no calcium
permeability call, because for the conditional families there is nothing in
the sequence to call it from (hazards **HC8**, **HC16**); permeability is a
catalogue attribute with its measurement method attached, not a prediction.

    from src.classify import ChannelQuery, classify, ReferenceSet
"""

from .classifier import (ChannelCall, ChannelQuery, Evidence, classify,
                         classify_all)
from .motifs import (ANCHORS, EF_HAND_RE, FOUR_REPEAT_ANCHOR, K_FILTER_RE,
                     MCU_DXXE_RE, ORAI_ANCHOR, TRPV_CA_ANCHOR, MotifResult,
                     ef_hand_hits, k_filter_hits, mcu_filter_hits,
                     verify_anchor)
from .reference import ReferenceResult, ReferenceSet, fetch_uniprot_sequence
from .rules import (ArchitectureRule, HAZARD_RULES, RuleMatch, all_rules,
                    derived_rules, match_architecture, topology_check)

__all__ = [
    "ChannelQuery", "ChannelCall", "Evidence", "classify", "classify_all",
    "ArchitectureRule", "HAZARD_RULES", "RuleMatch", "all_rules",
    "derived_rules", "match_architecture", "topology_check",
    "MotifResult", "ANCHORS", "FOUR_REPEAT_ANCHOR", "TRPV_CA_ANCHOR",
    "ORAI_ANCHOR", "K_FILTER_RE", "MCU_DXXE_RE", "EF_HAND_RE",
    "k_filter_hits", "mcu_filter_hits", "ef_hand_hits", "verify_anchor",
    "ReferenceSet", "ReferenceResult", "fetch_uniprot_sequence",
]
