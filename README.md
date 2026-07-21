# Privacy–Utility Tradeoff in Differentially Private Machine Learning for Network Intrusion Detection

This repository contains a reproducible research pipeline for evaluating intrusion-detection utility and training-membership leakage before and after formal DP-SGD.

## Current scope

- Dataset: NSL-KDD
- Task: Binary classification, Normal vs Attack
- Main model: MLP
- Privacy audit: Shadow-calibrated membership inference
- Formal private training: DP-SGD with Opacus
- Core IDS metrics: Recall, FNR, F1, PR-AUC
- Core privacy metrics: MIA ROC-AUC, advantage, balanced accuracy, TPR at 1% and 5% FPR

## Current status

- Baseline IDS comparison: complete and archived
- Locked 70/10/20 MIA-ready split: complete
- Final five-shadow baseline MIA audit: complete
- Overall measurable baseline leakage under the evaluated attacks: weak
- Next experiment: PyTorch and Opacus DP-SGD feasibility smoke test

## Repository layout

```text
notebooks/   Colab notebooks in execution order
data/        Dataset instructions and split metadata only
results/     Concise final CSV evidence
manifests/   Reproducibility and protocol manifests
artifacts/   Documentation for external model artifacts
report/      Experiment interpretations and final tables
```

## Dataset

The NSL-KDD dataset is not included. Place the official `KDDTrain+.txt` and `KDDTest+.txt` files in Google Drive or another configured data directory.

## Execution order

1. `01_baseline_nsl_kdd_ids.ipynb`
2. `02_03_mia_ready_baseline_and_audit.ipynb`
3. `04_dp_sgd_feasibility_smoke_test.ipynb`
4. `05_dp_sgd_privacy_utility_sweep.ipynb`

## Claim boundary

This project should be described as differentially private only after DP-SGD is implemented with valid epsilon/delta accounting. Weak empirical MIA leakage does not by itself establish privacy.
