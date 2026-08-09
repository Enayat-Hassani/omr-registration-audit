# Assumptions tested

This file records design assumptions that were made explicit, tested in the
repository, and either retained, weakened, or removed. The measurements are
synthetic unless stated otherwise. They are evidence about this implementation,
not guarantees for operational use.

## A1. Ability can be estimated from the disputed sheet

This is not a safe input. Fitting ability to the same sheet whose registration is
being adjudicated is circular: a successful re-registration can manufacture the
high ability estimate that then appears to support it. The current case output
illustrates the problem: the sheet-implied ability is 0.2928, only modestly above
the four-option chance level of 0.25, and the value is explicitly diagnostic only.

The implementation therefore uses an external ability estimate when one exists,
or the prior mean otherwise. It floors the admissible range at chance and never
uses the disputed sheet’s fitted ability to decode or accept a registration.

## A2. The gates resist asserted ability

This assumption is only partly supported. The committed stress test escalates the
external prior concentration from 10 to 5,000 items. The Bayes-factor gate first
passes at concentration 120; the posterior gate first passes at 250. The
Monte Carlo p-value remains 0.8914 in all eight rows and never passes the 0.01
threshold, because that statistic uses no ability model.

The evidence and posterior gates can therefore be moved by a strong external
assertion. The ability-independent Monte Carlo gate is the main safeguard, but its
stability in this synthetic stress test does not prove safety against every real
failure mode.

## A3. Total score gain is a suitable test statistic

It is not. On the positive-control experiment, the p-values for a planted shift
were:

| Statistic | p-value |
|---|---:|
| Raw score gain | 0.143 |
| Viterbi score gain | 0.018 |
| Forward evidence ratio | 0.025 |
| Coherence scan | 0.0003 |

The implementation therefore gates on the most surprising contiguous block of
matches at a non-zero displacement, with multiplicity handled by the same search
in the null simulations. Score gain is not an acceptance criterion.

## A4. A richer response model should improve recovery

The repository does not support that conclusion. The IRT extension calibrates item
difficulty on 400 cohort sheets with correlation `r = 0.992`. On 40 shifted and
40 clean held-out sheets, constant-ability emissions had power 0.625 and IRT
emissions 0.650; both had zero false alarms.

When item difficulty is moved into the coherence statistic instead, the plain
statistic has power 0.773 and the weighted statistic 0.768 over 220 shifted and
220 clean paired sheets. McNemar’s exact two-sided p-value is 1.000.

The single-ability model is retained because these experiments do not show a
useful improvement. They do not show that richer inputs—scanner intensity,
erasures, timing, or cohort response frequencies—would be unhelpful.

## A5. Early and non-monotone mechanisms are unusable

The assumption is too broad. An early full shift is representable and is detected
well in the mechanism benchmark: the gated detector fires in 0.857 of 14 cases,
with median localization error 0. The same mechanism costs 19.76 marks on
average when left uncorrected and 4.14 marks after the gated detector’s decisions.

A deferred question answered later is genuinely non-monotone and cannot be
represented exactly. The approximate monotone method fires in 0.686 of 14 cases,
with median localization error 1; it still withholds 4.30 marks on average. This
is not exact recovery and remains a limitation.

## A6. The configured minimum segment length determines the detection floor

It does not determine the observed floor. In the profile study, the internal
minimum is five items, but the smallest accepted displaced block was 11 at the
Conservative level, 9 at Balanced, and 8 at Sensitive. At the Balanced level,
the Monte Carlo gate was the sole failing gate in 49 single-gate rejection cases.

The calibration arm found that the reported p-value was below nominal 0.5 in
25/300 clean sheets, below 0.25 in 8/300, below 0.1 in 2/300, and below 0.05 in
1/300. The binding null was rotation in 185 cases, block bootstrap in 79, and
key-marginal resampling in 36.

The minimum segment length is therefore an internal safety condition, not a
policy knob. The acceptance profile is the live policy choice, and the measured
floor is a capability of the complete search-and-gate procedure.

## Conclusions supported by these measurements

- Permissive alignment is exploitable: corpus 1 reports 4.21 raw unearned marks
  per sheet for LCS, versus 0.19 for both no correction and the gated HMM.
- Contiguity is more discriminating than total score gain in the positive control
  (`p = 0.0003` versus `p = 0.143`).
- The Monte Carlo gate is less sensitive to asserted ability than the likelihood
  gates in the stress test.
- Monotonicity and injectivity are enforced by construction and covered by the
  invariant tests.
- Detection depends on candidate ability and shift size. The committed validation
  output reports one-row power of 0.333, 0.767, and 0.933 at abilities 0.55, 0.70,
  and 0.85, respectively; two-row power is 0.067, 0.233, and 0.450.
- An isolated misplaced answer is a negative control: the gated detector fires
  0.000 in the mechanism benchmark, avoiding a correction that would be worse
  than leaving the one-mark error alone.

## Assumptions carried forward

- The 1.8% registration-error rate is imported from Skiena and Sumazin (2004), not
  measured in this repository.
- The default maximum displacement is three rows and is not calibrated against a
  confirmed historical corpus.
- The frequency of individual mechanisms is unknown; results are reported by
  mechanism rather than weighted as a deployment mixture.
- The response sequence is assumed to have been digitized correctly. Scanner
  artefacts are simulated separately in the large corpus, not validated from real
  images.
- Cohort screening is implemented through `CohortScreen` and exercised in a
  synthetic 4,000-sheet simulation, but it has no operational calibration.
