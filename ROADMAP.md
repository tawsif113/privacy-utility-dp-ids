# Research Roadmap

## Working title

**Privacy–Utility Auditing of DP-SGD for ML-Based Network Intrusion Detection**

Formal DP-SGD has been implemented with explicit accounting. The reported guarantee remains conditional on fixed preprocessing.

## Core research question

How does formally accounted DP-SGD affect IDS utility—especially Recall and False Negative Rate—and measurable membership leakage under the stated score-only and label-aware attacks?

## Fixed scope

- Dataset: NSL-KDD
- Main task: Binary Normal vs Attack
- Baseline models: RF, XGBoost, MLP
- Full privacy target: MLP only
- Formal private method: DP-SGD with Opacus
- MIA threat models: score-only black-box and label-aware audit
- Utility metrics: Recall, FNR, F1, PR-AUC
- Privacy metrics: MIA AUC, advantage, balanced accuracy, TPR at 1% and 5% FPR, bootstrap confidence intervals

## Locked split

```text
KDDTrain+
├── target_train       70%
├── target_validation  10%
└── shadow_pool        20%

KDDTest+
└── final IDS utility only
```

## Completed and accepted

1. **Experiment 01 — Baseline IDS comparison:** archived RF, XGBoost, and MLP utility results with validation-only threshold selection.
2. **Experiments 02–03 — MIA-ready baseline and audit:** locked the 70/10/20 split and completed the five-shadow baseline MIA audit.
3. **Experiment 04 — DP-SGD feasibility:** established PyTorch parity and a formally accounted Opacus run.
4. **Experiment 05 — DP-SGD privacy–utility sweep:** completed non-private and ε≈8, 4, and 2 target conditions with condition-matched shadows, IDS utility, MIA estimates, bootstrap intervals, group diagnostics, and paired comparisons.

## Accepted Experiment 05 result

| Condition | Actual ε | Recall | FNR | F1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| Non-private | — | 0.7080 | 0.2920 | 0.8146 | 0.9357 |
| DP-SGD ε≈8 | 7.9936 | 0.7128 | 0.2872 | 0.8033 | 0.8967 |
| DP-SGD ε≈4 | 3.9983 | 0.7267 | 0.2733 | 0.8106 | 0.8978 |
| DP-SGD ε≈2 | 1.9990 | 0.6850 | 0.3150 | 0.7842 | 0.8960 |

The ε≈4 condition is the provisional balance candidate. Its higher Recall is accompanied by higher FPR and lower PR-AUC than the non-private model, so it is not yet an established improvement or optimum.

Overall membership leakage remained near chance for every condition. All shadow-selected overall MIA AUC confidence intervals include 0.5, and no paired overall comparison supports measured leakage reduction. Rare-group reductions are exploratory only because the group has 208 evaluated records and multiple comparisons were made.

## Current gate

### Experiment 06 — Repeated-run stability

Repeat only:

```text
Non-private MLP
DP-SGD ε≈4 — provisional balanced condition
DP-SGD ε≈2 — strongest tested privacy condition with usable single-run utility
```

Use seeds `[42, 52, 62, 72, 82]`. Keep the split, preprocessing definition, architecture, epoch schedule, threshold rule, MIA protocol, delta, and accountant fixed.

### Acceptance gate

Do not select a final balance point until:

- mean, standard deviation, and uncertainty are reported for IDS F1, Recall, FNR, MIA AUC, MIA advantage, and actual epsilon;
- the ε≈4 utility pattern persists across seeds;
- conclusions are weakened if the apparent balance disappears;
- every repeated condition has CSV evidence and a manifest.

## Later phases

1. Review and accept Experiment 06.
2. Complete Experiment 08 — final privacy–utility frontier and interpretation.
3. Consider a compact UNSW-NB15 check only after the NSL-KDD conclusion is stable.
4. Retain the optional feature-perturbation comparator only if it answers a documented question.

## Scope restrictions

Do not add federated learning, extra primary datasets, transformers, adversarial evasion, new privacy mechanisms, or broad model comparisons to the current study.
