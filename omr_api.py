#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Single-call interface to the detector.

    from omr_api import adjudicate_sheet

    result = adjudicate_sheet(key=[...], marks=[...], profile="balanced")
    print(result.summary())    # headline figures
    print(result.explain())    # gates, null models, per-question ledger

`key` is indexed by question, `marks` by physical row; use None for a blank
row. `profile` is "conservative", "balanced" or "sensitive".

For the full narrative report, use `omr_shift.Reporter`.
"""
from __future__ import annotations

import os
import sys
import warnings
from dataclasses import replace
from typing import Optional, Sequence

_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from omr_shift import (  # noqa: E402
    Adjudication, AdjudicationConfig, Adjudicator, Policy, ResponseSheet,
)

__all__ = ["adjudicate_sheet", "PROFILES"]

PROFILES = {p.label: p for p in Policy}


def _check(key: Sequence, marks: Sequence, max_displacement: int) -> None:
    """Raise on input that cannot be adjudicated; warn on input that is legal
    but usually a miscount."""
    if not key:
        raise ValueError("key is empty")
    if not marks:
        raise ValueError("marks is empty")

    if any(k is None for k in key):
        bad = [i + 1 for i, k in enumerate(key) if k is None]
        raise ValueError(
            f"the answer key has no entry for question(s) {bad[:5]}. Marks may "
            f"be blank; the key may not.")

    drift = len(marks) - len(key)
    if abs(drift) > max_displacement:
        raise ValueError(
            f"{len(marks)} marks for {len(key)} questions. A difference of "
            f"{drift:+d} exceeds max_displacement={max_displacement}, so no "
            f"admissible registration exists. Count the entries in `marks`, "
            f"including the None values for blank rows.")
    if drift:
        warnings.warn(
            f"{len(marks)} marks for {len(key)} questions ({drift:+d}). Legal, "
            f"and every offset in the result is relative to that difference. "
            f"Re-count `marks` if a short or long sheet was not intended.",
            stacklevel=3)

    alphabet = {k for k in key} | {m for m in marks if m is not None}
    odd = {s for s in alphabet if not isinstance(s, str) or len(s) != 1}
    if odd:
        raise ValueError(
            f"marks and key must be single characters, or None for a blank "
            f"row. Found: {sorted(odd, key=str)[:5]}")


def adjudicate_sheet(key: Sequence[str],
                     marks: Sequence[Optional[str]],
                     profile: str = "balanced",
                     candidate_id: str = "sheet",
                     external_ability: Optional[float] = None,
                     verbose: bool = False) -> Adjudication:
    """Adjudicate one sheet.

    key                 correct answer per question, in question order
    marks               what each physical row holds, in row order; None for a
                        blank row
    profile             "conservative", "balanced" or "sensitive"; sets the
                        acceptance level and the permutation draw count, which
                        move together
    external_ability    the candidate's ability from other subjects or prior
                        attainment, if the board has it; never fitted to this
                        sheet
    candidate_id        carried into the report

    Returns an `Adjudication`: `.accepted`, `.raw_score`, `.adjudicated_score`,
    `.verdict`, `.gates`, `.segments`, `.item_ledger`, `.evidence`,
    `.calibration`, plus `.summary()` and `.explain()`.
    """
    if profile not in PROFILES:
        raise ValueError(
            f"unknown profile {profile!r}. Choose one of {sorted(PROFILES)}.")
    pol = PROFILES[profile]

    base = AdjudicationConfig()
    _check(key, marks, base.max_displacement)

    cfg = replace(base,
                  permutation_alpha=pol.alpha,
                  n_permutations=pol.n_permutations,
                  external_ability=external_ability)

    sheet = ResponseSheet(tuple(key), tuple(marks), candidate_id=candidate_id)
    return Adjudicator(sheet, cfg).run(n_permutations=pol.n_permutations,
                                       verbose=verbose)


_POINTER = "result.explain() for gate values, null models and the ledger."


def _summary(self: Adjudication, pointer: bool = True) -> str:
    """Headline figures."""
    c, e = self.calibration, self.evidence
    n = self.sheet.n_questions
    L = []
    if self.sheet.n_rows != n:
        L.append(f"!! SHEET LENGTH    : {self.sheet.n_rows} marks for {n} "
                 f"questions ({self.sheet.n_rows - n:+d}); offsets are relative "
                 f"to that")
    L += [f"verdict            : {self.verdict}",
          f"score as marked    : {self.raw_score} / {n}",
          f"score after        : {self.adjudicated_score} / {n}",
          f"log10 Bayes factor : {e['log10_bayes_factor']:+.2f}",
          f"posterior P(shift) : {e['posterior_h1']:.4f}"]
    if c.get("computed", True):
        L.append(f"Monte Carlo p      : {c['p_value']:.4f}  "
                 f"(binding null: {c['decisive_null']})")
    else:
        L.append("Monte Carlo p      : not computed; a gate had already failed")
    L.append("gates              : " + ", ".join(
        f"{k}={'pass' if g['passed'] else 'FAIL'}" for k, g in self.gates.items()))
    disp = [s for s in self.segments if s.offset != 0]
    if disp:
        L.append("displaced blocks   : " + ", ".join(
            f"Q{s.q_start + 1}-Q{s.q_end + 1} at {s.offset:+d} "
            f"({s.n_correct}/{s.n_items} correct)" for s in disp))
    if pointer:
        L += ["", _POINTER]
    return "\n".join(L)


def _fmt(v) -> str:
    return f"{v:.4g}" if isinstance(v, float) else str(v)


def _explain(self: Adjudication, ledger: str = "changed") -> str:
    """Gate values, null models and the per-question ledger.

    ledger: "changed" for questions whose registration moved, "all" for every
    question, "none" to omit the table.
    """
    if ledger not in ("changed", "all", "none"):
        raise ValueError('ledger must be "changed", "all" or "none"')

    W = 78
    L = [self.summary(pointer=False), ""]

    L += ["-" * W, "GATES  (all must pass)", "-" * W]
    for name, g in self.gates.items():
        L.append(f"  {'pass' if g['passed'] else 'FAIL'}  {name:<19} "
                 f"{_fmt(g['value']):>10} vs {_fmt(g['threshold']):<8}  "
                 f"{g['description']}")

    c = self.calibration
    if c.get("computed", True) and c.get("nulls"):
        L += ["", "-" * W,
              "NULL MODELS  (the reported p is the worst of the three)", "-" * W,
              f"  observed statistic {c['observed_statistic']:.4f}"]
        for name, r in c["nulls"].items():
            L.append(f"  {name:<17} p={r['p_value']:.4f}  "
                     f"mean={r['null_mean']:.3f}  q99.9={r['null_q999']:.3f}  "
                     f"({r['n_draws']} draws)")

    if ledger != "none":
        rows = self.item_ledger
        if ledger == "changed":
            rows = [r for r in rows if r["original_row"] != r["final_row"]]
        heading = "re-registered only" if ledger == "changed" else "all questions"
        L += ["", "-" * W, f"PER-QUESTION LEDGER  ({heading})", "-" * W]
        if not rows:
            L.append("  no question changed registration")
        for r in rows:
            L.append(f"  Q{r['question']:>3}  key={r['key']}  "
                     f"row {str(r['original_row']):>4} -> {str(r['final_row']):<4} "
                     f"{r['change']:<5} conf={r['map_posterior']:.4f}  "
                     f"{r['reason']}")

    gained = sum(1 for r in self.item_ledger if r["change"] == "GAIN")
    lost = sum(1 for r in self.item_ledger if r["change"] == "LOSS")
    L += ["", "-" * W,
          f"  gained {gained}, lost {lost}, net {gained - lost:+d}. A loss is a "
          f"mark that was right before re-registration.",
          "-" * W]
    return "\n".join(L)


Adjudication.summary = _summary
Adjudication.explain = _explain


if __name__ == "__main__":
    from omr_shift import CASE_SHEET
    s = ResponseSheet.from_file(CASE_SHEET)
    print(adjudicate_sheet(list(s.key), list(s.marks),
                           candidate_id="CASE").explain())
