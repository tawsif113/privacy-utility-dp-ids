"""Read-only audit of an Experiment 08 evidence ZIP.

Usage:
    python scripts/audit_experiment08.py experiment08_evidence.zip \
        [experiment06_evidence.zip]

The optional Experiment 06 bundle enables source-table and source-manifest verification.
This script does not rerun neural training, prediction, or privacy accounting.
"""

import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import sys
import zipfile

import numpy as np
import pandas as pd


SEEDS = [42, 52, 62, 72, 82]
CONDITIONS = ["non_private", "dp_eps_4", "dp_eps_2"]
THREATS = ["score_only_black_box", "label_aware_audit"]
IDS_METRICS = ["recall", "fnr", "f1", "fpr", "precision", "pr_auc", "threshold"]
MIA_METRICS = [
    "mia_auc",
    "mia_advantage",
    "mia_balanced_accuracy",
    "tpr_at_1pct_fpr",
    "tpr_at_5pct_fpr",
]
T_CRITICAL = 2.7764451051977987


def require(test, message):
    if not bool(test):
        raise ValueError(message)


def close(actual, expected, message, atol=2e-12):
    require(
        np.allclose(
            np.asarray(actual, dtype=float),
            np.asarray(expected, dtype=float),
            rtol=0,
            atol=atol,
            equal_nan=True,
        ),
        message,
    )


def stats(values):
    values = np.asarray(values, dtype=float)
    require(len(values) == 5 and np.isfinite(values).all(), "Expected five finite seeds")
    mean = values.mean()
    sd = values.std(ddof=1)
    half = T_CRITICAL * sd / np.sqrt(5)
    return [mean, sd, mean - half, mean + half]


def read_zip(path):
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        names = [item.filename for item in infos]
        require(len(names) == len(set(names)), "Duplicate ZIP entries")
        for name in names:
            parsed = PurePosixPath(name)
            require(not parsed.is_absolute() and ".." not in parsed.parts, "Unsafe ZIP path")
        require(archive.testzip() is None, "ZIP CRC failure")
        return {name: archive.read(name) for name in names}


def csv(blobs, name):
    return pd.read_csv(io.BytesIO(blobs[name]))


def find_row(frame, **keys):
    selected = frame
    for key, value in keys.items():
        selected = selected[selected[key].isna()] if pd.isna(value) else selected[selected[key] == value]
    require(len(selected) == 1, f"Expected one summary row: {keys}")
    return selected.iloc[0]


def check_summary(row, values, label):
    expected = stats(values)
    require(int(row.n_seeds) == 5, f"Incomplete summary: {label}")
    require(row.ci_method == "two-sided t interval, df=4", f"Wrong interval method: {label}")
    close(
        [row["mean"], row.standard_deviation, row.ci_low, row.ci_high],
        expected,
        f"Summary mismatch: {label}",
    )


def audit(path08, path06=None):
    path08 = Path(path08)
    blobs = read_zip(path08)
    require("final_analysis_manifest.json" in blobs, "Final manifest missing")
    manifest = json.loads(blobs["final_analysis_manifest.json"])
    require(manifest["experiment"] == "08_privacy_utility_frontier", "Wrong experiment")
    require(manifest["protocol_version"] == "ROADMAP_REVISED_V2", "Wrong protocol")
    require(manifest["status"] == "COMPLETE", "Experiment 08 is not complete")
    require(all(manifest["gates"].values()), "A completion gate failed")
    require(not manifest["missing_distribution_inputs"], "Distribution inputs were missing")
    require(
        manifest["training_runs_started"] == 0
        and manifest["thresholds_tuned"] == 0
        and manifest["new_attacks_fitted"] == 0,
        "Experiment 08 changed the frozen analysis protocol",
    )
    outputs = manifest["output_sha256"]
    require(set(blobs) == set(outputs) | {"final_analysis_manifest.json"}, "Missing or extra output")
    for name, expected in outputs.items():
        require(hashlib.sha256(blobs[name]).hexdigest() == expected, f"Checksum failed: {name}")

    ids_all = csv(blobs, "tables/ids_default_and_tuned_per_seed.csv")
    ids = ids_all[
        (ids_all.split == "KDDTest+")
        & (ids_all.threshold_policy == "validation_selected_F2")
    ].copy()
    primary = csv(blobs, "tables/primary_mia_per_seed.csv")
    secondary = csv(blobs, "tables/secondary_mia_per_seed.csv")
    configs = csv(blobs, "tables/privacy_accounting_per_seed.csv")
    summary = csv(blobs, "tables/five_seed_summary.csv")
    require(len(ids_all) == 45 and len(ids) == 15, "Incomplete IDS rows")
    require(len(primary) == len(secondary) == 30, "Incomplete MIA rows")
    require(len(configs) == 15 and len(summary) == 53, "Incomplete config/summary rows")
    expected_keys = {(condition, seed) for condition in CONDITIONS for seed in SEEDS}
    require(set(zip(ids.condition, ids.seed)) == expected_keys, "IDS condition/seed keys changed")
    for table, role in [(primary, "primary"), (secondary, "secondary")]:
        require(table.analysis_role.eq(role).all(), f"Mixed {role} attacker role")
        require(
            set(zip(table.condition, table.seed, table.threat_model))
            == {(c, s, t) for c in CONDITIONS for s in SEEDS for t in THREATS},
            f"Incomplete {role} MIA keys",
        )

    for condition in CONDITIONS:
        for metric in IDS_METRICS:
            row = find_row(
                summary,
                condition=condition,
                domain="IDS",
                threat_model=np.nan,
                metric=metric,
            )
            check_summary(row, ids.loc[ids.condition == condition, metric], f"{condition}/IDS/{metric}")
        for threat in THREATS:
            for metric in MIA_METRICS:
                row = find_row(
                    summary,
                    condition=condition,
                    domain="MIA",
                    threat_model=threat,
                    metric=metric,
                )
                values = primary.loc[
                    (primary.condition == condition) & (primary.threat_model == threat), metric
                ]
                check_summary(row, values, f"{condition}/{threat}/{metric}")
    for condition in ["dp_eps_4", "dp_eps_2"]:
        row = find_row(
            summary,
            condition=condition,
            domain="privacy_accounting",
            threat_model=np.nan,
            metric="actual_epsilon",
        )
        check_summary(row, configs.loc[configs.condition == condition, "actual_epsilon"], condition)

    def check_paired(name, mia, include_ids):
        paired = csv(blobs, name)
        expected_rows = 34 if include_ids else 20
        require(len(paired) == expected_rows, f"Incomplete paired summary: {name}")
        for _, row in paired.iterrows():
            if include_ids and row.domain == "IDS":
                table = ids
            else:
                table = mia
            mask = table.condition.eq(row.comparison_condition)
            reference = table.condition.eq(row.reference_condition)
            if pd.notna(row.threat_model):
                mask &= table.threat_model.eq(row.threat_model)
                reference &= table.threat_model.eq(row.threat_model)
            comparison_values = table.loc[mask].set_index("seed")[row.metric]
            reference_values = table.loc[reference].set_index("seed")[row.metric]
            require(set(comparison_values.index) == set(reference_values.index) == set(SEEDS), "Unpaired seeds")
            close(
                [row["mean"], row.standard_deviation, row.ci_low, row.ci_high],
                stats(comparison_values - reference_values),
                f"Paired summary mismatch: {name}/{row.metric}",
            )

    check_paired("tables/primary_paired_differences_summary.csv", primary, True)
    check_paired("tables/secondary_paired_differences_summary.csv", secondary, False)

    cdf = csv(blobs, "plot_data/member_nonmember_distribution_cdf.csv")
    require(
        set(cdf.condition) == set(CONDITIONS)
        and set(cdf.seed) == {42}
        and set(cdf.membership) == {0, 1}
        and set(cdf.metric) == {"confidence", "loss"},
        "Distribution groups changed",
    )
    reconstructed = {}
    for keys, group in cdf.groupby(["condition", "metric", "membership"]):
        group = group.sort_values("value")
        values = group.value.to_numpy()
        cumulative = group.cdf.to_numpy()
        counts = np.rint(np.diff(np.r_[0, cumulative]) * 12597).astype(int)
        require(np.all(np.diff(values) > 0), f"Distribution values not unique/sorted: {keys}")
        require(np.all(np.diff(cumulative) > 0), f"CDF not increasing: {keys}")
        require(np.all(counts >= 1) and counts.sum() == 12597, f"CDF counts invalid: {keys}")
        close(np.cumsum(counts) / 12597, cumulative, f"CDF increments invalid: {keys}", 5e-12)
        reconstructed[keys] = (values, counts)
    require(len(reconstructed) == 12, "Incomplete distributions")

    max_auc_error = 0.0
    for condition in CONDITIONS:
        nonmember_values, nonmember_counts = reconstructed[(condition, "loss", 0)]
        member_values, member_counts = reconstructed[(condition, "loss", 1)]
        wins = sum(
            int(count)
            * (
                nonmember_counts[nonmember_values > value].sum()
                + 0.5 * nonmember_counts[nonmember_values == value].sum()
            )
            for value, count in zip(member_values, member_counts)
        )
        reconstructed_auc = wins / (12597**2)
        reported_auc = primary.loc[
            (primary.condition == condition)
            & (primary.seed == 42)
            & (primary.threat_model == "label_aware_audit"),
            "mia_auc",
        ].iloc[0]
        max_auc_error = max(max_auc_error, abs(reconstructed_auc - reported_auc))
    require(max_auc_error < 2e-15, "Loss distributions do not reproduce label-aware AUC")

    for number in range(1, 11):
        prefix = f"figures/{number:02d}_"
        pngs = [name for name in blobs if name.startswith(prefix) and name.endswith(".png")]
        require(len(pngs) == 1 and pngs[0][:-4] + ".pdf" in blobs, f"Figure {number:02d} missing")

    source_verified = False
    if path06 is not None:
        import audit_experiment06

        blobs06 = audit_experiment06.read_bundle(path06)
        _, source_tables, source_report = audit_experiment06.audit_bundle(blobs06)
        require(source_report["accepted_for_final_analysis"], "Experiment 06 source failed")
        require(
            source_report["manifest_sha256"] == manifest["source_experiment06_manifest_sha256"],
            "Experiment 06 source manifest changed",
        )
        pairs = {
            "tables/five_seed_summary.csv": "repeated_run_summary.csv",
            "tables/ids_default_and_tuned_per_seed.csv": "repeated_run_ids_results.csv",
            "tables/privacy_accounting_per_seed.csv": "repeated_run_configs.csv",
            "tables/primary_mia_per_seed.csv": "repeated_run_mia_results.csv",
            "tables/primary_paired_differences_summary.csv": "repeated_run_paired_summary.csv",
            "tables/secondary_mia_per_seed.csv": "secondary_mia_results.csv",
            "tables/secondary_paired_differences_summary.csv": "secondary_mia_paired_summary.csv",
        }
        for output_name, source_name in pairs.items():
            output = csv(blobs, output_name)
            source = source_tables[source_name]
            require(set(output.columns) == set(source.columns), f"Source columns changed: {output_name}")
            keys = [
                name
                for name in [
                    "condition", "seed", "split", "threshold_policy", "domain",
                    "threat_model", "metric", "analysis_role", "reference_condition",
                    "comparison_condition",
                ]
                if name in output.columns
            ]
            for key in keys:
                values = output[key].drop_duplicates()
                source = source[source[key].isin(values) | (source[key].isna() & output[key].isna().any())]
            output = output.sort_values(keys, na_position="first").reset_index(drop=True)
            source = source.sort_values(keys, na_position="first").reset_index(drop=True)
            require(output.shape == source.shape, f"Source row count changed: {output_name}")
            for column in output.columns:
                if pd.api.types.is_numeric_dtype(output[column]):
                    close(output[column], source[column], f"Source values changed: {output_name}/{column}")
                else:
                    require(
                        output[column].fillna("<NA>").astype(str).equals(
                            source[column].fillna("<NA>").astype(str)
                        ),
                        f"Source values changed: {output_name}/{column}",
                    )
        source_verified = True

    return {
        "accepted": True,
        "status": manifest["status"],
        "bundle_sha256": hashlib.sha256(path08.read_bytes()).hexdigest(),
        "verified_output_hashes": len(outputs),
        "summary_rows": len(summary),
        "distribution_rows": len(cdf),
        "distribution_groups": len(reconstructed),
        "maximum_seed42_loss_auc_reconstruction_error": max_auc_error,
        "figures_png_pdf": 10,
        "experiment06_source_verified": source_verified,
        "limitations": "No independent neural training, prediction, or privacy-accountant rerun.",
    }


if __name__ == "__main__":
    if len(sys.argv) not in {2, 3}:
        raise SystemExit(__doc__)
    print(json.dumps(audit(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else None), indent=2))
