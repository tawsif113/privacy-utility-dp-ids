# Experiment Summary

This file records only accepted results and the current experimental gate under ROADMAP_REVISED_V2.

## Experiment 01 — Baseline IDS comparison

**Status:** Complete and archived.

**Purpose:** Compare RF, XGBoost, and MLP utility and identify the model family carried into the privacy audit.

The archived baseline is retained for IDS context. It is not used as evidence of formal privacy or reduced membership leakage.

## Experiments 02–03 — MIA-ready MLP and baseline MIA audit

**Status:** Complete and accepted.

### Protocol

- Locked 70/10/20 split of KDDTrain+
- KDDTest+ reserved for final IDS utility
- Target MLP seed: 42
- Five shadow models: 101, 202, 303, 404, 505
- Shadow 505 reserved entirely for attacker calibration
- Score-only and label-aware attacks
- 1,000 bootstrap repetitions

### IDS result at the validation-selected threshold

| Metric | Result |
|---|---:|
| Threshold | 0.24 |
| Accuracy | 0.8007 |
| Precision | 0.9228 |
| Recall | 0.7092 |
| F1 | 0.8020 |
| FNR | 0.2908 |
| FPR | 0.0784 |
| ROC-AUC | 0.8981 |
| PR-AUC | 0.9171 |

### Privacy-audit result

The strongest evaluated overall attack reached approximately MIA ROC-AUC 0.5029, with a 95% confidence interval spanning chance. MIA advantage and low-FPR TPR were also negligible.

Accepted interpretation:

> Under the specified shadow-calibrated score-only and label-aware threat models, measurable overall membership leakage from the non-private MLP was weak.

This result does not establish that the model is private and does not support a leakage-reduction claim for DP-SGD. It creates a floor effect that must be reported in the final analysis.

## Experiment 04 — PyTorch parity and DP-SGD feasibility

**Status:** Complete and accepted as a feasibility gate.

### Protocol checkpoint

- PyTorch MLP parity check passed within the predeclared tolerances
- Opacus compatibility passed
- PRV accounting recorded
- Five DP training epochs
- Target epsilon: 8.0
- Actual epsilon: 7.9986285
- Delta: 1.1340311 × 10^-5
- Noise multiplier: 0.4698181
- Maximum gradient norm: 1.0
- Poisson sampling enabled
- Privacy scope conditional on fixed preprocessing

### DP smoke-test result at the validation-selected threshold

| Metric | Result |
|---|---:|
| Threshold | 0.07 |
| Accuracy | 0.7723 |
| Precision | 0.9142 |
| Recall | 0.6620 |
| F1 | 0.7680 |
| FNR | 0.3380 |
| FPR | 0.0821 |
| ROC-AUC | 0.8971 |
| PR-AUC | 0.9193 |

Accepted interpretation:

> Formal DP-SGD training and explicit privacy accounting are feasible for the locked MLP pipeline.

These are single-run feasibility results. They do not identify an optimal privacy budget, establish the final utility cost, or show that DP-SGD reduced membership leakage.

## Experiment 05 — Privacy-budget sweep and condition-matched MIA

**Status:** Current experimental gate; implementation is present, but execution evidence is pending.

The notebook now includes:

- Non-private and multiple target-epsilon conditions
- Explicit target privacy accounting
- Condition-matched shadow training
- DP shadow calibration to the same requested epsilon and fixed delta as each corresponding target condition
- Separate corrected shadow caches
- Score-only and label-aware MIA evaluation
- Low-FPR metrics
- Bootstrap confidence intervals
- Paired bootstrap differences against the non-private baseline
- Strict JSON output and protocol gates

Experiment 05 is **not complete** until the repository contains valid result CSVs and manifests for every configuration, with per-model MIA metrics, privacy accounting, paired comparisons, and uncertainty estimates.

## Next gate

Execute Experiment 05 from the accepted Experiment 04 prerequisites. Do not begin repeated-run stability analysis or final claims until the complete first-pass sweep has been reviewed for protocol validity, utility comparability, accounting, and MIA calibration.
