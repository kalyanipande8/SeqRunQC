import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.simulate_samples import simulate_samples
from src.qc_checks import run_qc, validate_flagging
from src.pooling_optimization import run_pooling_optimization


def test_at_least_800_samples():
    samples, _ = simulate_samples(n_samples=820)
    assert len(samples) >= 800


def test_qc_recall_reasonable():
    samples, true_defects = simulate_samples(n_samples=820)
    flagged = run_qc(samples)
    validation = validate_flagging(flagged, true_defects)
    assert validation["recall"] >= 0.8


def test_pooling_runs_5_batches():
    samples, _ = simulate_samples(n_samples=820)
    results, mean_reduction = run_pooling_optimization(samples, n_batches=5)
    assert len(results) == 5


def test_pooling_cost_reduction_nonnegative():
    samples, _ = simulate_samples(n_samples=820)
    results, mean_reduction = run_pooling_optimization(samples, n_batches=5)
    assert mean_reduction >= 0


def test_qc_flags_have_valid_types():
    samples, _ = simulate_samples(n_samples=200, seed=2)
    flagged = run_qc(samples)
    valid_types = {"low_mapping_rate", "low_q30", "high_duplication"}
    for flags in flagged.values():
        assert set(flags).issubset(valid_types)
