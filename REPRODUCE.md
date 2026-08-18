# Reproducing the results

Run these commands from the repository root. The committed files under
`results/` are the reference outputs. The commands that generate the long corpus
can take substantially longer than the control suite; use the quick modes first.

## Core reports and controls

```bash
python3 -m omr_registration_audit.core
python3 benchmark/omrbench.py --n 12
python3 benchmark/mechanisms.py --n 14
python3 benchmark/policy_profiles.py
python3 benchmark/cohort_screen.py
python3 benchmark/figures.py
python3 analysis/error_families.py
python3 analysis/latent_structure.py
python3 benchmark/verify_corpus.py
```

These commands regenerate the case outputs, positive control, model-comparison
tables, mechanism tables, profile results, cohort screen, figures, and control
checks. The control script exits non-zero on failure and does not replace the
committed result files.

## Large synthetic corpus

```bash
python3 benchmark/large_synthetic.py --quick
python3 benchmark/large_synthetic.py --full --jobs 8
```

The full run reproduces `results/large_synthetic/` at the shipped Balanced
profile. Use `--n` to reduce the number of sheets per condition while debugging.
Use `--level` only for a separate policy comparison; published headline metrics
are from the default run, while the profile study is the source for the named
operating points.

The conservative output in `results/large_synthetic_conservative/` is a separate
full run at level 0.001. Both runs use seed 20260804 and generate the same sheets;
they differ in the acceptance level used for the metrics arm.

## Auxiliary experiments

```bash
python3 extensions/irt_model.py --n 40
python3 extensions/weighted_scan.py --n 220 --perm 1200
```

These reproduce the negative-result experiments summarized in
[ASSUMPTIONS.md](ASSUMPTIONS.md).

`benchmark/policy_profiles.py` accepts `--clean`, `--shift`, and `--certify` to
change its three sample sizes. The committed profile output uses the defaults.
`benchmark/cohort_screen.py` accepts `--sheets`, `--q`, `--base-rate`, and
`--length`; the committed screen uses 4,000 sheets, `q = 0.05`, base rate 0.018,
and 46 questions.

## What the controls establish

`verify_corpus.py` checks that planted errors match their labels, a permissive
counterexample rule can produce false positives, a never-accept rule scores zero,
the known-answer cases behave as specified, and the CSV and JSON case data agree.
All of these controls are synthetic. They do not validate performance on real
examination papers.

The unit tests check monotonicity, injectivity, displacement bounds, relabelling
invariance, score bounds, mark immutability, profile nesting, and mutation probes:

```bash
python3 -m unittest discover -s tests -v
```

## Determinism and provenance

The detector and generators use fixed seeds. Per-generator benchmark seeds derive
from `zlib.crc32`; they do not depend on Python’s randomized `hash()`. Result files
include code fingerprints, parameters, and environment information. Re-running a
command from unchanged source should reproduce its output; compare with `git diff`.

## Data limitation in the case study

The case report’s analyses of the full 150-row sheet use rows 47–150 transcribed
from a published image without independent verification. Those rows are not in
the repository. Rows 1–46 agree with the marking record. Reproducing the full
provenance analysis therefore requires the board’s verified digitization.
