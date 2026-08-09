# Evidence Index

This directory contains concise evidence exported from accepted runs. It is an audit layer, not a claim that every planned experiment is complete.

## Current evidence boundary

- Experiments 01–04 are complete under the protocol described in [`report/experiment_summary.md`](../report/experiment_summary.md).
- Experiment 05 code exists, but no Experiment 05 result tables or manifests are committed. The privacy-budget sweep therefore remains **in progress**.
- Formal privacy accounting and empirical membership-inference resistance are reported separately. A near-chance attack does not prove privacy, and an epsilon value does not show that measured leakage decreased.

## Experiments 02–03: baseline IDS and membership-inference audit

| Evidence file | What it supports |
|---|---|
| [`target_ids_results.csv`](baseline_mia/target_ids_results.csv) | Locked target-model utility at the default and validation-selected thresholds |
| [`mia_summary.csv`](baseline_mia/mia_summary.csv) | Overall score-only and label-aware MIA metrics, bootstrap confidence intervals, advantage, and low-FPR TPR |
| [`shadow_model_runs.csv`](baseline_mia/shadow_model_runs.csv) | Five shadow-model seeds and training diagnostics |
| [`target_training_diagnostics.csv`](baseline_mia/target_training_diagnostics.csv) | Target MLP seed, iteration limit, and final loss |
| [`baseline_mia_combined_manifest.json`](../manifests/baseline_mia_combined_manifest.json) | Dataset hashes, locked split sizes, seeds, calibration policy, and artifact provenance |

The strongest evaluated overall baseline attack has ROC-AUC 0.502893, with a 95% bootstrap interval that includes 0.5. This is evidence of weak measured leakage under the evaluated attacks, not evidence that the model is private.

## Experiment 04: DP-SGD feasibility

| Evidence file | What it supports |
|---|---|
| [`non_private_pytorch_parity.csv`](dp_sgd_smoke_test/non_private_pytorch_parity.csv) | Predeclared parity checks between the accepted scikit-learn baseline and the PyTorch MLP |
| [`non_private_pytorch_ids_results.csv`](dp_sgd_smoke_test/non_private_pytorch_ids_results.csv) | Non-private PyTorch utility under the locked evaluation policy |
| [`private_smoke_test.csv`](dp_sgd_smoke_test/private_smoke_test.csv) | Single-run DP-SGD feasibility utility |
| [`dp_sgd_training_history.csv`](dp_sgd_smoke_test/dp_sgd_training_history.csv) | Per-epoch loss and accumulated privacy accounting |
| [`dp_sgd_smoke_utility_comparison.csv`](dp_sgd_smoke_test/dp_sgd_smoke_utility_comparison.csv) | Matched non-private versus DP smoke-test metric differences |
| [`dp_sgd_smoke_manifest.json`](dp_sgd_smoke_test/dp_sgd_smoke_manifest.json) | Architecture, training configuration, epsilon, delta, clipping, sampling, accountant, software versions, and artifact provenance |

The accepted smoke run reached epsilon 7.9986285 at delta 1.1340311 × 10^-5 after five epochs. It establishes implementation and accounting feasibility only; it does not establish a privacy–utility frontier or reduced membership leakage.

The manifest records `secure_mode: false`. This matches Opacus's faster experimental setting and is disclosed as a limitation of the feasibility run. Any final result intended to support a production-strength implementation claim should use secure randomness or provide a documented justification.

## Intentionally excluded artifacts

Raw NSL-KDD data, fitted models, preprocessing objects, split-index arrays, transformed feature arrays, and per-sample attack scores are excluded to keep the repository lightweight and avoid redistributing raw or per-sample data. Dataset hashes, split sizes, seeds, and originating paths are retained in the manifests where available.

## Validate internal consistency

Run:

```bash
python scripts/validate_evidence.py
```

The validator uses only Python's standard library. It checks cross-file agreement; it does not retrain models or independently reproduce the experiments.
