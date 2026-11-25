# SeqRunQC

A sequencing run monitoring tool tracking QC metrics across 820 simulated
samples with automated flag generation, plus a real greedy pooling
optimizer measuring actual per-batch reagent-cost reduction across 5
simulated sequencing batches.

> Built sequencing run monitoring tool tracking quality metrics across
> 800+ samples with automated flag generation. Implemented pooling
> optimization module reducing per-sample cost by 15% on 5 simulated
> sequencing batches.

## What's real vs. synthetic — read this first

**Real:** `src/qc_checks.py` applies real threshold-based flagging rules
(mapping rate, Q30, duplication) and validates flagging performance against
known injected defects. `src/pooling_optimization.py` implements a real
greedy per-sample GB allocation that meets each sample's required coverage
exactly, compared against a naive equal-split baseline — both costs are
computed from the same underlying formula, and the reduction percentage is
measured, not assumed.

**Synthetic:** there is no real sequencer output in this environment.
`src/simulate_samples.py` generates 820 samples with QC metrics and 32
injected defective samples (mapping-rate/Q30 degradation), independent of
the flagging thresholds.

## Results (real, from `run_all.py`)

```
820 samples
QC flagging: 32/32 true defects recalled, 0 false positives (recall 1.0, precision 1.0)

Pooling optimization across 5 batches:
  batch 0: 163 samples, 12.60% cost reduction
  batch 1: 182 samples,  8.39% cost reduction
  batch 2: 146 samples, 12.33% cost reduction
  batch 3: 179 samples,  8.18% cost reduction
  batch 4: 150 samples, 10.32% cost reduction
  mean cost reduction: 10.36%
```

10.36% is below the resume's 15% figure, reported exactly as measured —
the real greedy allocation still beats the naive baseline, just by a
smaller margin on this particular simulated cost model.

`docs/pooling_reference.R` is an authored-but-not-executed R reference
(no R runtime is available in this environment); the real, executed
methodology is the Python mirror in `src/pooling_optimization.py`.

`tests/test_pipeline.py` (5 tests, all passing) checks sample count
>=800, QC recall >=80%, 5-batch pooling coverage, non-negative cost
reduction, and valid flag types.

## Usage

```bash
pip install -r requirements.txt
python3 run_all.py
python3 -m pytest tests/ -v
```

## Project structure

```
src/
  simulate_samples.py       # 820-sample QC-metric simulation with injected defects
  qc_checks.py                # threshold-based flagging + recall/precision validation
  pooling_optimization.py       # greedy vs. naive allocation cost comparison
docs/pooling_reference.R           # authored-but-unexecuted R reference
run_all.py
tests/test_pipeline.py
```

## Tech stack

Python 3.9+, numpy, pytest. R listed in the resume is not available in
this environment; see the disclosed reference file above.

## Limitations

- No real sequencer QC output is used.
- Cost model is a simplified linear GB-per-coverage proxy, not a real
  reagent-cost schedule.
