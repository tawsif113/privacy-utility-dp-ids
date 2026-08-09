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
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


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


def validate_dataset_identity(
    baseline_manifest: dict[str, Any],
    smoke_manifest: dict[str, Any],
) -> None:
    for key in ("train_sha256", "test_sha256"):
        require(
            baseline_manifest["dataset"][key] == smoke_manifest["dataset"][key],
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
    require(
        all(close(float(row["delta"]), delta) for row in history),
        "Delta changed during the DP smoke-test training history.",
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
    comparison = {
        row["metric"]: row for row in load_csv(comparison_path)
    }

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
        require(
            close(float(row["non_private_pytorch"]), non_private),
            f"Non-private {metric} differs between the result and comparison tables.",
        )
        require(
            close(float(row["dp_sgd_smoke"]), private),
            f"DP smoke-test {metric} differs between the result and comparison tables.",
        )
        require(
            close(float(row["dp_minus_non_private"]), private - non_private),
            f"Reported {metric} difference is inconsistent.",
        )

    return epsilon, delta


def main() -> None:
    baseline_manifest = load_json("manifests/baseline_mia_combined_manifest.json")
    smoke_manifest = load_json(
        "results/dp_sgd_smoke_test/dp_sgd_smoke_manifest.json"
    )

    validate_dataset_identity(baseline_manifest, smoke_manifest)
    baseline_auc = validate_baseline_mia()
    validate_pytorch_parity()
    epsilon, delta = validate_dp_smoke(smoke_manifest)

    print("Evidence validation passed.")
    print("- Dataset hashes agree across the accepted manifests.")
    print(f"- Strongest evaluated overall baseline MIA ROC-AUC: {baseline_auc:.6f}")
    print(f"- DP smoke-test accounting: epsilon={epsilon:.7f}, delta={delta:.10g}")
    print("- PyTorch parity checks and DP utility comparisons are internally consistent.")


if __name__ == "__main__":
    main()
