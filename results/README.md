# Evidence Index

This directory contains concise evidence exported from accepted runs. It is an audit layer, not a claim that every planned experiment is complete.

## Current evidence boundary

- Experiments 01–06 and 08 are accepted within the evidence limits described in [`report/experiment_summary.md`](../report/experiment_summary.md).
- Experiment 05 is accepted as a single-seed sweep; Experiment 06 has now tested stability; its acceptance review does not establish a final optimal point.
- Formal privacy accounting and empirical membership-inference resistance are reported separately. A near-chance attack does not prove privacy, and an epsilon value does not show that measured leakage decreased.

## Experiments 02–03: baseline IDS and membership-inference audit

| Evidence file | What it supports |
|---|---|
| [`target_ids_results.csv`](baseline_mia/target_ids_results.csv) | Locked target-model utility at default and validation-selected thresholds |
| [`mia_summary.csv`](baseline_mia/mia_summary.csv) | Overall MIA metrics, low-FPR TPR, and bootstrap intervals |
| [`shadow_model_runs.csv`](baseline_mia/shadow_model_runs.csv) | Five shadow seeds and training diagnostics |
| [`target_training_diagnostics.csv`](baseline_mia/target_training_diagnostics.csv) | Target MLP training diagnostics |
| [`baseline_mia_combined_manifest.json`](../manifests/baseline_mia_combined_manifest.json) | Dataset identity, partitions, seeds, calibration policy, and provenance |

The strongest evaluated baseline attack reached MIA ROC-AUC 0.502893 with a 95% interval containing 0.5. This is weak measured leakage under the evaluated attacks, not evidence that the model is private.

## Experiment 04: DP-SGD feasibility

| Evidence file | What it supports |
|---|---|
| [`non_private_pytorch_parity.csv`](dp_sgd_smoke_test/non_private_pytorch_parity.csv) | Predeclared PyTorch parity checks |
| [`non_private_pytorch_ids_results.csv`](dp_sgd_smoke_test/non_private_pytorch_ids_results.csv) | Non-private PyTorch utility |
| [`private_smoke_test.csv`](dp_sgd_smoke_test/private_smoke_test.csv) | Single-run DP-SGD feasibility utility |
| [`dp_sgd_training_history.csv`](dp_sgd_smoke_test/dp_sgd_training_history.csv) | Per-epoch loss and privacy accounting |
| [`dp_sgd_smoke_utility_comparison.csv`](dp_sgd_smoke_test/dp_sgd_smoke_utility_comparison.csv) | Matched smoke-test utility differences |
| [`dp_sgd_smoke_manifest.json`](dp_sgd_smoke_test/dp_sgd_smoke_manifest.json) | Architecture, DP configuration, software, and provenance |

The smoke run reached ε=7.9986285 at δ=1.1340311×10^-5 after five epochs. It establishes feasibility only.

## Experiment 05: privacy-budget sweep and condition-matched MIA

| Evidence file | What it supports |
|---|---|
| [`dp_sgd_ids_results.csv`](dp_sgd/dp_sgd_ids_results.csv) | Utility for all four target conditions at default and tuned thresholds |
| [`dp_sgd_configs.csv`](dp_sgd/dp_sgd_configs.csv) | Target privacy budgets, clipping, sampling, hyperparameters, and model identifiers |
| [`dp_sgd_mia_results.csv`](dp_sgd/dp_sgd_mia_results.csv) | Six overall attacks per condition with low-FPR metrics and intervals |
| [`dp_sgd_bootstrap_ci.csv`](dp_sgd/dp_sgd_bootstrap_ci.csv) | Long-form MIA AUC and advantage confidence intervals |
| [`dp_sgd_group_analysis.csv`](dp_sgd/dp_sgd_group_analysis.csv) | Normal, Attack, DoS, Probe, and Rare diagnostics |
| [`dp_sgd_paired_mia_differences.csv`](dp_sgd/dp_sgd_paired_mia_differences.csv) | Paired DP-minus-non-private differences on identical target records |
| [`dp_sgd_privacy_utility_summary.csv`](dp_sgd/dp_sgd_privacy_utility_summary.csv) | Joined utility and shadow-selected MIA results |
| [`mia_attack_calibration.csv`](dp_sgd/mia_attack_calibration.csv) | Attacker selection and thresholds from shadow calibration only |
| [`shadow_model_configs.csv`](dp_sgd/shadow_model_configs.csv) | Five condition-matched shadows per target condition |
| [`target_mia_sample_manifest.csv`](dp_sgd/target_mia_sample_manifest.csv) | Fixed balanced target evaluation membership and group identities |
| [`opacus_warning_summary.csv`](dp_sgd/opacus_warning_summary.csv) | Preserved runtime/accounting warnings |
| [`config.json`](dp_sgd/config.json) | Locked Experiment 05 protocol |
| [`dp_sgd_sweep_manifest.json`](dp_sgd/dp_sgd_sweep_manifest.json) | Dataset hashes, runtime, artifacts, configurations, and required outputs |

The actual DP budgets are ε=7.9936, 3.9983, and 1.9990 at the fixed δ. The ε≈4 condition is the single-run balance candidate, but repeated runs are required. All shadow-selected overall MIA AUC intervals contain 0.5, and no paired overall comparison supports measured leakage reduction.

## Limitations recorded with the evidence

- DP accounting is conditional on the fixed, non-private preprocessing artifact.
- `secure_mode` is false. This is disclosed as an experimental implementation limitation and is not a production-strength randomness claim.
- Opacus accounting warnings are preserved rather than suppressed.
- Experiment 05 is the single-seed sweep; Experiment 06 supplies selected-condition stability.
- Rare-group results use 208 records and remain exploratory.

## Intentionally excluded artifacts

Raw NSL-KDD data, fitted models, preprocessing objects, split-index arrays, transformed feature arrays, and intermediate attack-feature caches remain outside Git. Dataset hashes, split sizes, seeds, model hashes, and protocol metadata are retained in the committed evidence.

## Validate internal consistency

Run:

```bash
python scripts/validate_evidence.py
```

The validator uses only Python's standard library. It checks cross-file agreement; it does not retrain models or independently reproduce the experiments.


## Experiment 06: accepted repeated-run evidence

Concise CSV/JSON outputs are committed under `repeated_runs/`. The large target-sample manifest
remains in the original Experiment 06 ZIP and Drive project. Its hash is preserved in the manifest.

Run `python scripts/audit_experiment06.py /path/to/experiment06_evidence.zip` for the full
read-only audit. The directory copy in Git alone is intentionally insufficient for this check.
The audit recomputes utility and seed statistics; it does not independently retrain models.

See [the acceptance review](../report/experiment06_acceptance.md). Passing Experiment 06 does
not confirm a balance point or leakage reduction.

## Experiment 08: accepted final-analysis evidence

The publication-ready output is committed under [`final_analysis/`](final_analysis/). It includes
all final tables, captions, interpretation, and PNG/PDF figures. The canonical complete ZIP
remains in the project Drive with bundle SHA-256
`9eabc696aac5020598dc85cce2f445ad0decf97a8bf8bb10cff19d0d4bb6113d`.

The repository omits only the 66,138-row member/non-member ECDF plot-data file, the duplicate
ZIP, and upstream score caches. Their hashes remain in `final_analysis_manifest.json`. See the
[Experiment 08 acceptance review](../report/experiment08_acceptance.md).

Run `python scripts/audit_experiment08.py /path/to/experiment08_evidence.zip
/path/to/experiment06_evidence.zip` against the complete bundles. The audit verifies hashes,
source agreement, summary statistics, matched-seed intervals, and distribution consistency; it
does not rerun neural training or prediction.
