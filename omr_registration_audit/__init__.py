#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detecting registration errors in OMR answer sheets.

    from omr_registration_audit import adjudicate_sheet

    result = adjudicate_sheet(key=[...], marks=[...], profile="balanced")
    print(result.summary())    # headline figures
    print(result.explain())    # gates, null models, per-question ledger

`key` is indexed by question, `marks` by physical row; use None for a blank
row. `profile` is "conservative", "balanced" or "sensitive".

For a whole sitting:

    from omr_registration_audit import screen_cohort

    report = screen_cohort(sheets, q=0.05)
    print(report.text())

Lower-level pieces — `AdjudicationConfig`, `Adjudicator`, `ResponseSheet`,
`CohortScreen` — are exported here for callers who need to set thresholds,
priors or an external ability estimate directly.
"""
from __future__ import annotations

from .core import (
    # configuration and policy
    AdjudicationConfig,
    Policy,
    # the sheet and the pipeline
    ResponseSheet,
    ScoringModel,
    BandedPairHMM,
    EvidenceEngine,
    SegmentAnalyzer,
    CoherenceScanStatistic,
    NullCalibrator,
    Adjudicator,
    Adjudication,
    Alignment,
    Segment,
    Reporter,
    # cohort layer
    CohortScreen,
    CohortReport,
    CohortDecision,
    # helpers a caller may reasonably want
    binom_sf,
    clopper_pearson_upper,
    logsumexp,
    CASE_SHEET,
    load_case_records,
    STATE_M,
    STATE_X,
    STATE_Y,
    STATE_NAMES,
)
from .api import adjudicate_sheet, screen_cohort, PROFILES

__version__ = "0.1.0"

__all__ = [
    "adjudicate_sheet",
    "screen_cohort",
    "PROFILES",
    "AdjudicationConfig",
    "Policy",
    "ResponseSheet",
    "ScoringModel",
    "BandedPairHMM",
    "EvidenceEngine",
    "SegmentAnalyzer",
    "CoherenceScanStatistic",
    "NullCalibrator",
    "Adjudicator",
    "Adjudication",
    "Alignment",
    "Segment",
    "Reporter",
    "CohortScreen",
    "CohortReport",
    "CohortDecision",
    "binom_sf",
    "clopper_pearson_upper",
    "logsumexp",
    "CASE_SHEET",
    "load_case_records",
    "STATE_M",
    "STATE_X",
    "STATE_Y",
    "STATE_NAMES",
    "__version__",
]
