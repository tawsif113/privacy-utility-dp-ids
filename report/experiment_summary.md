# Experiment Summary

## Experiment 01 — Baseline IDS comparison

Status: complete and archived.

Purpose: compare RF, XGBoost, and MLP utility and identify the model family carried into the privacy audit.

## Experiment 02–03 — MIA-ready MLP and baseline MIA audit

Status: complete and accepted.

### Protocol

- Locked 70/10/20 split of KDDTrain+
- KDDTest+ reserved for final IDS utility
- Target MLP seed: 42
- Five shadow models: 101, 202, 303, 404, 505
- Shadow 505 reserved entirely for attacker calibration
- 1,000 bootstrap repetitions

### IDS result at validation-selected threshold

- Threshold: 0.24
- Accuracy: 0.8007
- Precision: 0.9228
- Recall: 0.7092
- F1: 0.8020
- FNR: 0.2908
- FPR: 0.0784
- ROC-AUC: 0.8981
- PR-AUC: 0.9171

### Privacy-audit result

The strongest evaluated overall attack reached approximately MIA AUC 0.5029, with a 95% confidence interval spanning chance. MIA advantage and low-FPR TPR were also negligible.

Accepted interpretation:

> Under the specified shadow-calibrated score-only and label-aware threat models, measurable overall membership leakage from the non-private MLP was weak.

This result does not establish that the model is private and does not yet support a leakage-reduction claim for DP-SGD.

## Next experiment

Experiment 04 must establish PyTorch utility parity and valid Opacus privacy accounting before a formal DP-SGD sweep.
