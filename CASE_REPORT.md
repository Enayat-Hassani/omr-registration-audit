# Case report: the sheet that prompted this work

This is an analysis of one disputed examination sheet. It motivated the detector
but is not validation data. The detector design and synthetic evaluation are in
[REPORT.md](REPORT.md); the answer files are described in [data/README.md](data/README.md).

## 1. Background and data

The case was raised through BANFES, an assessment system built by Education Bridge
for Afghanistan. A candidate reportedly performed well in other subjects but
scored 7/46 in mathematics. The proposed explanation was a skipped bubble row
that shifted every later answer.

The mathematics section has 46 questions and four options. It occupies questions
1–46 of a 150-question sheet. The answer key for the other 104 questions was not
provided, so the claim about performance elsewhere cannot be checked.

The public data contain the mathematics key and the candidate’s 46 marks. Rows
1–46 agree exactly with the marking record. Rows 47–150 were transcribed from an
image without independent verification and are not stored as verified data.

## 2. Finding

**No re-registration is supported. The original score stands at 7/46.**

The current default output is `results/case_default_prior.txt`:

| Criterion | Observed value | Requirement |
|---|---:|---:|
| log₁₀ Bayes factor | 0.1159 | ≥ 2.0 |
| Posterior shift probability | 0.023378 | ≥ 0.95 |
| Worst-null Monte Carlo p-value | 0.9010 | ≤ 0.010 |
| Segment coherence | no displaced segment | required |
| Non-trivial MAP registration | identity | required to differ |

The posterior uses the configured 1.8% sheet-level prior. The strongest coherent
non-zero-offset block is Q31–Q35 at offset +3, with 4/5 correct and binomial
tail p = 0.0156. The reported Monte Carlo p-value is 0.901 because the block
bootstrap null is the least favourable of the three nulls.

The default evidence break-even for this sheet is 2.55 questions. This is a
diagnostic quantity, not a claim that correcting two or three questions would
automatically justify re-registration: all gates still have to pass.

## 3. Supporting analyses

### Displacement search

The best raw displacement result is offset +12 with 15 correct matches out of 34.
Its uncorrected p-value is 0.012; after accounting for the 77 tested offsets it
is 0.59. This is a broad search diagnostic, not the detector’s acceptance test.

### Answer counts

Reordering marks cannot change the number of each option. The observed counts are
incompatible with the expected counts for a competent candidate at abilities of
0.75 or above (`p ≤ 0.014`):

| Option | Key count | Candidate count |
|---|---:|---:|
| A | 16 | 7 |
| B | 10 | 12 |
| C | 11 | 13 |
| D | 9 | 14 |

This position-invariant check argues against a simple reordering of a competent
candidate’s answers. It does not identify why the observed sequence has this
composition.

### Other structure tests

The strongest mutual-information result has p = 0.78. Four change-point methods
disagree: CUSUM selects Q11, binary segmentation Q12, the coherence scan Q31,
and the pair HMM finds no non-identity change. The spread is 20 questions, so no
single change-point result is persuasive.

The mathematics sequence has Lempel–Ziv complexity 13, compared with a random
baseline of 17.3 (`p = 0.0004`). Equal-length windows elsewhere on the transcribed
sheet have complexity 16–18. This analysis depends on unverified rows 47–150 and
should be rerun against the board’s own digitization.

## 4. Other registration hypotheses

The case scripts test each family with its own search-space correction:

| Family | Best result | Corrected p |
|---|---|---:|
| Displacement | offset +12, 15/34 | 0.5948 |
| Symbol + displacement | 12/19 | 0.5721 |
| Reversal | 9/46 | 0.8471 |
| Rotation | 17/46 | 0.8928 |
| Option relabelling | 16/46 | 0.8950 |
| Block/column swap | 17/46 | 0.9983 |

These are case-specific search results, not population estimates.

## 5. Ability robustness

The default case verdict is not accepted. If the external ability assertion is
raised, the case can look more favourable to a shift under the likelihood model:
at an operating ability of 0.85 the posterior is 0.1431 and the evidence gate
still fails. The Monte Carlo p-value remains 0.9010 because it uses no ability
model. At the highest stress-test prior concentration, the Bayes-factor and
posterior gates can pass for some settings, but the Monte Carlo gate still fails.

The result is therefore not “the candidate could not have been able”; it is that
the available mathematics response pattern does not provide enough safe evidence
for a correction under the configured decision rule.

## 6. Recommendation and missing evidence

The board’s stated framework calls for a re-examination rather than a statistical
correction. A rescan of the physical sheet should come first, because faint marks,
erasures, and double marks can create apparent registration errors more directly
than a response-sequence model can resolve.

The most valuable missing evidence is the answer key and marking record for the
other 104 questions. A verified digitization of rows 47–150 would also allow the
provenance and sequence-structure analyses to be rerun.
