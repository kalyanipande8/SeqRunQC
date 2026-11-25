"""Simulate 800+ sequencing samples with QC metrics and known injected
flaggable defects, independent of the flagging/pooling-optimization logic."""
import numpy as np


def simulate_samples(n_samples: int = 820, seed: int = 13):
    rng = np.random.default_rng(seed)
    mapped_pct = np.clip(rng.normal(96, 2, n_samples), 60, 100)
    q30_pct = np.clip(rng.normal(93, 3, n_samples), 50, 100)
    duplication_pct = np.clip(rng.normal(12, 4, n_samples), 0, 80)
    required_coverage = rng.choice([10, 20, 30], size=n_samples)
    true_available_yield_gb = np.clip(rng.normal(5.0, 1.2, n_samples), 0.5, 12)

    n_defects = max(1, n_samples // 25)
    defect_idx = rng.choice(n_samples, size=n_defects, replace=False)
    mapped_pct[defect_idx] -= rng.uniform(20, 40, size=n_defects)
    q30_pct[defect_idx] -= rng.uniform(15, 30, size=n_defects)

    samples = []
    for i in range(n_samples):
        samples.append({"sample_id": i, "mapped_pct": round(float(mapped_pct[i]), 2),
                         "q30_pct": round(float(q30_pct[i]), 2),
                         "duplication_pct": round(float(duplication_pct[i]), 2),
                         "required_coverage": int(required_coverage[i]),
                         "available_yield_gb": round(float(true_available_yield_gb[i]), 3)})
    return samples, set(defect_idx.tolist())
