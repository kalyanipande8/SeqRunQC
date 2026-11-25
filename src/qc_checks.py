"""Real automated flag generation rules for sequencing run monitoring."""

THRESHOLDS = {"mapped_pct_min": 85.0, "q30_pct_min": 80.0, "duplication_pct_max": 40.0}


def flag_sample(sample: dict) -> list:
    flags = []
    if sample["mapped_pct"] < THRESHOLDS["mapped_pct_min"]:
        flags.append("low_mapping_rate")
    if sample["q30_pct"] < THRESHOLDS["q30_pct_min"]:
        flags.append("low_q30")
    if sample["duplication_pct"] > THRESHOLDS["duplication_pct_max"]:
        flags.append("high_duplication")
    return flags


def run_qc(samples: list) -> dict:
    flagged = {}
    for s in samples:
        flags = flag_sample(s)
        if flags:
            flagged[s["sample_id"]] = flags
    return flagged


def validate_flagging(flagged: dict, true_defect_ids: set) -> dict:
    flagged_ids = set(flagged.keys())
    tp = len(flagged_ids & true_defect_ids)
    fp = len(flagged_ids - true_defect_ids)
    fn = len(true_defect_ids - flagged_ids)
    recall = tp / len(true_defect_ids) if true_defect_ids else 1.0
    precision = tp / len(flagged_ids) if flagged_ids else 1.0
    return {"true_positives": tp, "false_positives": fp, "false_negatives": fn,
            "recall": round(recall, 4), "precision": round(precision, 4)}
