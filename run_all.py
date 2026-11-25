import json
import os

from src.simulate_samples import simulate_samples
from src.qc_checks import run_qc, validate_flagging
from src.pooling_optimization import run_pooling_optimization


def main():
    samples, true_defects = simulate_samples(n_samples=820)
    flagged = run_qc(samples)
    qc_validation = validate_flagging(flagged, true_defects)
    pooling_results, mean_cost_reduction_pct = run_pooling_optimization(samples, n_batches=5)

    os.makedirs("results", exist_ok=True)
    summary = {"n_samples": len(samples), "qc_validation": qc_validation,
               "pooling_batches": pooling_results, "mean_cost_reduction_pct": mean_cost_reduction_pct}
    with open("results/summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
