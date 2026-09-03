#!/usr/bin/env python3
"""Validate internal consistency of the repository's committed evidence.

This script intentionally uses only the Python standard library. It does not
retrain any model; it checks that accepted CSV and JSON artifacts agree with
one another on the core reported results.
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CONDITIONS = {"non_private", "dp_eps_8", "dp_eps_4", "dp_eps_2"}
EXPECTED_DP_TARGETS = {"dp_eps_8": 8.0, "dp_eps_4": 4.0, "dp_eps_2": 2.0}
EXPECTED_SHADOW_SEEDS = {101, 202, 303, 404, 505}
EXPECTED_DELTA = 1.0 / 88181


def load_json(relative_path: str) -> dict[str, Any]:
    path = ROOT / relative_path
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_csv(relative_path: str) -> list[dict[str, str]]:
    path = ROOT / relative_path
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def close(left: float, right: float, *, tolerance: float = 1e-12) -> bool:
    return math.isclose(left, right, rel_tol=0.0, abs_tol=tolerance)


def select_one(
    rows: list[dict[str, str]],
    relative_path: str,
    **criteria: str,
) -> dict[str, str]:
    matches = [
        row
        for row in rows
        if all(row.get(column) == expected for column, expected in criteria.items())
    ]
    require(
        len(matches) == 1,
        f"Expected one matching row in {relative_path} for {criteria}; found {len(matches)}.",
    )
    return matches[0]


def validate_dataset_identity(*manifests: dict[str, Any]) -> None:
    reference = manifests[0]["dataset"]
    for manifest in manifests[1:]:
        for key in ("train_sha256", "test_sha256"):
            require(
                manifest["dataset"][key] == reference[key],
                f"Dataset hash mismatch for {key}.",
            )


def validate_baseline_mia() -> float:
    relative_path = "results/baseline_mia/mia_summary.csv"
    rows = load_csv(relative_path)
    overall_rows = [row for row in rows if row["subset"] == "overall"]
    require(overall_rows, f"No overall attack rows found in {relative_path}.")

    strongest = max(overall_rows, key=lambda row: float(row["mia_auc"]))
    auc = float(strongest["mia_auc"])
    ci_low = float(strongest["mia_auc_ci_low"])
    ci_high = float(strongest["mia_auc_ci_high"])

    require(close(auc, 0.502893104009985), "Unexpected strongest baseline MIA ROC-AUC.")
    require(ci_low <= 0.5 <= ci_high, "Strongest baseline MIA interval no longer spans chance.")
    return auc


def validate_pytorch_parity() -> None:
    rows = load_csv("results/dp_sgd_smoke_test/non_private_pytorch_parity.csv")
    require(rows, "The PyTorch parity table is empty.")
    require(
        all(row["passes"].strip().lower() == "true" for row in rows),
        "At least one predeclared PyTorch parity check failed.",
    )


def validate_dp_smoke(smoke_manifest: dict[str, Any]) -> tuple[float, float]:
    history_path = "results/dp_sgd_smoke_test/dp_sgd_training_history.csv"
    history = load_csv(history_path)
    require(history, f"No rows found in {history_path}.")
    final_epoch = history[-1]

    epsilon = float(smoke_manifest["dp"]["actual_epsilon"])
    delta = float(smoke_manifest["dp"]["delta"])
    require(close(float(final_epoch["epsilon"]), epsilon), "Final epsilon differs from the manifest.")
    require(close(float(final_epoch["delta"]), delta), "Final delta differs from the manifest.")
    require(
        epsilon <= float(smoke_manifest["dp"]["target_epsilon"]),
        "Actual epsilon exceeds the requested smoke-test target.",
    )

    private_path = "results/dp_sgd_smoke_test/private_smoke_test.csv"
    non_private_path = "results/dp_sgd_smoke_test/non_private_pytorch_ids_results.csv"
    comparison_path = "results/dp_sgd_smoke_test/dp_sgd_smoke_utility_comparison.csv"

    private_row = select_one(
        load_csv(private_path),
        private_path,
        model="pytorch_dp_sgd_smoke",
        split="KDDTest+",
        threshold_policy="validation_selected_F2",
    )
    non_private_row = select_one(
        load_csv(non_private_path),
        non_private_path,
        model="pytorch_non_private",
        split="KDDTest+",
        threshold_policy="validation_selected_F2",
    )
    comparison = {row["metric"]: row for row in load_csv(comparison_path)}

    for metric in (
        "accuracy",
        "precision",
        "recall",
        "f1",
        "fnr",
        "fpr",
        "roc_auc",
        "pr_auc",
    ):
        require(metric in comparison, f"Missing {metric} from {comparison_path}.")
        row = comparison[metric]
        non_private = float(non_private_row[metric])
        private = float(private_row[metric])
        require(close(float(row["non_private_pytorch"]), non_private), f"Non-private {metric} mismatch.")
        require(close(float(row["dp_sgd_smoke"]), private), f"DP smoke-test {metric} mismatch.")
        require(
            close(float(row["dp_minus_non_private"]), private - non_private),
            f"Reported {metric} difference is inconsistent.",
        )

    return epsilon, delta


def validate_dp_sweep(
    baseline_manifest: dict[str, Any],
    smoke_manifest: dict[str, Any],
) -> dict[str, dict[str, float | None]]:
    result_manifest = load_json("results/dp_sgd/dp_sgd_sweep_manifest.json")
    indexed_manifest = load_json("manifests/dp_sgd_sweep_manifest.json")
    config = load_json("results/dp_sgd/config.json")

    require(result_manifest == indexed_manifest, "Experiment 05 manifest copies differ.")
    require(result_manifest["experiment"] == "05_dp_sgd_privacy_utility_sweep", "Wrong sweep experiment.")
    require(result_manifest["protocol_version"] == "ROADMAP_REVISED_V2", "Wrong sweep protocol.")
    require(result_manifest["protocol_revision"] == "epsilon_delta_matched_v2", "Wrong sweep revision.")
    require(config["protocol_revision"] == "epsilon_delta_matched_v2", "Config revision mismatch.")
    require(close(float(result_manifest["target_delta"]), EXPECTED_DELTA), "Sweep delta mismatch.")
    require(close(float(config["target_delta"]), EXPECTED_DELTA), "Config delta mismatch.")
    validate_dataset_identity(baseline_manifest, smoke_manifest, result_manifest)

    configs_path = "results/dp_sgd/dp_sgd_configs.csv"
    configs = load_csv(configs_path)
    require(len(configs) == 4, "Expected four target configurations.")
    require({row["condition"] for row in configs} == EXPECTED_CONDITIONS, "Target conditions differ.")
    config_by_condition = {row["condition"]: row for row in configs}

    for condition, target in EXPECTED_DP_TARGETS.items():
        row = config_by_condition[condition]
        actual = float(row["actual_epsilon"])
        require(0.0 < actual <= target + 0.10, f"{condition} epsilon misses target.")
        require(close(float(row["target_epsilon"]), target), f"{condition} target epsilon mismatch.")
        require(close(float(row["delta"]), EXPECTED_DELTA), f"{condition} delta mismatch.")
        require(close(float(row["max_grad_norm"]), 1.0), f"{condition} clipping mismatch.")
        require(row["accountant"] == "prv", f"{condition} accountant mismatch.")
        require(int(row["epochs"]) == 30, f"{condition} epoch mismatch.")
        require(int(row["batch_size"]) == 256, f"{condition} batch-size mismatch.")

    ids_path = "results/dp_sgd/dp_sgd_ids_results.csv"
    ids = load_csv(ids_path)
    require(len(ids) == 12, "Expected twelve IDS result rows.")
    require(
        Counter(row["condition"] for row in ids)
        == Counter({condition: 3 for condition in EXPECTED_CONDITIONS}),
        "IDS rows are incomplete.",
    )
    for row in ids:
        for metric in (
            "threshold",
            "accuracy",
            "precision",
            "recall",
            "f1",
            "fnr",
            "fpr",
            "roc_auc",
            "pr_auc",
        ):
            value = float(row[metric])
            require(math.isfinite(value) and 0.0 <= value <= 1.0, f"Invalid IDS {metric}.")
        require(close(float(row["recall"]) + float(row["fnr"]), 1.0), "Recall/FNR mismatch.")
        observed_n = sum(int(row[key]) for key in ("tn", "fp", "fn", "tp"))
        expected_n = 12597 if row["split"] == "target_validation" else 22544
        require(observed_n == expected_n, "IDS confusion-matrix count mismatch.")

    tuned = {
        condition: select_one(
            ids,
            ids_path,
            condition=condition,
            split="KDDTest+",
            threshold_policy="validation_selected_F2",
        )
        for condition in EXPECTED_CONDITIONS
    }

    mia_path = "results/dp_sgd/dp_sgd_mia_results.csv"
    mia = load_csv(mia_path)
    require(len(mia) == 24, "Expected twenty-four overall MIA rows.")
    require(
        Counter(row["condition"] for row in mia)
        == Counter({condition: 6 for condition in EXPECTED_CONDITIONS}),
        "MIA rows are incomplete.",
    )
    for row in mia:
        require(int(row["n"]) == 25194, "Unexpected MIA evaluation size.")
        require(int(row["members"]) == int(row["nonmembers"]) == 12597, "MIA sample is unbalanced.")
        auc = float(row["mia_auc"])
        auc_low = float(row["mia_auc_ci_low"])
        auc_high = float(row["mia_auc_ci_high"])
        require(0.0 <= auc <= 1.0, "Invalid MIA AUC.")
        require(0.0 <= auc_low <= auc_high <= 1.0, "Invalid MIA AUC interval.")
        require(auc_low <= 0.5 <= auc_high, "An overall MIA AUC interval no longer contains chance.")

    summary_path = "results/dp_sgd/dp_sgd_privacy_utility_summary.csv"
    summary = load_csv(summary_path)
    require(len(summary) == 8, "Expected eight privacy-utility summary rows.")
    require(
        Counter(row["condition"] for row in summary)
        == Counter({condition: 2 for condition in EXPECTED_CONDITIONS}),
        "Privacy-utility summary is incomplete.",
    )
    for row in summary:
        ids_row = tuned[row["condition"]]
        for metric in ("recall", "fnr", "f1", "pr_auc"):
            require(row[metric] != "", f"Missing summary {metric}.")
            require(close(float(row[metric]), float(ids_row[metric])), f"Summary {metric} mismatch.")
        mia_row = select_one(
            mia,
            mia_path,
            condition=row["condition"],
            threat_model=row["threat_model"],
            attack_model=row["attack_model"],
        )
        require(close(float(row["mia_auc"]), float(mia_row["mia_auc"])), "Summary MIA AUC mismatch.")

    bootstrap = load_csv("results/dp_sgd/dp_sgd_bootstrap_ci.csv")
    groups = load_csv("results/dp_sgd/dp_sgd_group_analysis.csv")
    paired = load_csv("results/dp_sgd/dp_sgd_paired_mia_differences.csv")
    calibration = load_csv("results/dp_sgd/mia_attack_calibration.csv")
    shadows = load_csv("results/dp_sgd/shadow_model_configs.csv")
    sample = load_csv("results/dp_sgd/target_mia_sample_manifest.csv")

    require(len(bootstrap) == 48, "Bootstrap table is incomplete.")
    require(len(groups) == 48, "Group-analysis table is incomplete.")
    require(len(paired) == 84, "Paired-comparison table is incomplete.")
    require(len(calibration) == 24, "Attack-calibration table is incomplete.")
    require(len(shadows) == 20, "Shadow configuration table is incomplete.")
    require(len(sample) == 25194, "Target MIA sample manifest is incomplete.")
    require(
        Counter(int(row["membership"]) for row in sample) == Counter({0: 12597, 1: 12597}),
        "Target MIA manifest is not membership-balanced.",
    )

    for condition in EXPECTED_CONDITIONS:
        condition_shadows = [row for row in shadows if row["condition"] == condition]
        require(
            {int(row["shadow_seed"]) for row in condition_shadows} == EXPECTED_SHADOW_SEEDS,
            f"{condition} shadow seeds are incomplete.",
        )
    for row in shadows:
        if row["condition"] in EXPECTED_DP_TARGETS:
            require(
                abs(float(row["shadow_actual_epsilon"]) - float(row["requested_epsilon"])) <= 0.10,
                "A DP shadow misses its requested epsilon.",
            )
            require(close(float(row["shadow_delta"]), EXPECTED_DELTA), "A DP shadow delta differs.")

    overall_pairs = [row for row in paired if row["subset"] == "overall"]
    require(len(overall_pairs) == 12, "Overall paired comparisons are incomplete.")
    require(
        not any(row["supports_measured_reduction"].strip().lower() == "true" for row in overall_pairs),
        "The documented no-overall-reduction interpretation is stale.",
    )

    return {
        condition: {
            "epsilon": (
                None
                if condition == "non_private"
                else float(config_by_condition[condition]["actual_epsilon"])
            ),
            "recall": float(tuned[condition]["recall"]),
            "fnr": float(tuned[condition]["fnr"]),
            "f1": float(tuned[condition]["f1"]),
            "pr_auc": float(tuned[condition]["pr_auc"]),
        }
        for condition in sorted(EXPECTED_CONDITIONS)
    }


def main() -> None:
    baseline_manifest = load_json("manifests/baseline_mia_combined_manifest.json")
    smoke_manifest = load_json("results/dp_sgd_smoke_test/dp_sgd_smoke_manifest.json")

    validate_dataset_identity(baseline_manifest, smoke_manifest)
    baseline_auc = validate_baseline_mia()
    validate_pytorch_parity()
    smoke_epsilon, smoke_delta = validate_dp_smoke(smoke_manifest)
    sweep = validate_dp_sweep(baseline_manifest, smoke_manifest)

    print("Evidence validation passed.")
    print("- Dataset hashes agree across the accepted manifests.")
    print(f"- Strongest evaluated overall baseline MIA ROC-AUC: {baseline_auc:.6f}")
    print(f"- DP smoke-test accounting: epsilon={smoke_epsilon:.7f}, delta={smoke_delta:.10g}")
    print("- Experiment 05 target/shadow budgets, utility, MIA, uncertainty, and manifests agree.")
    print(
        "- Experiment 05 epsilon~4 candidate: "
        f"epsilon={sweep['dp_eps_4']['epsilon']:.6f}, "
        f"recall={sweep['dp_eps_4']['recall']:.6f}, "
        f"fnr={sweep['dp_eps_4']['fnr']:.6f}, "
        f"f1={sweep['dp_eps_4']['f1']:.6f}."
    )


if __name__ == "__main__":
    main()
