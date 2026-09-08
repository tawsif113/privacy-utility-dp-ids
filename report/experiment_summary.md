# Experiment Summary

This file records only accepted results and the current experimental gate under ROADMAP_REVISED_V2.

## Experiment 01 — Baseline IDS comparison

**Status:** Complete and archived.

RF, XGBoost, and MLP utility comparisons are retained as IDS context. They are not privacy evidence.

## Experiments 02–03 — MIA-ready MLP and baseline MIA audit

**Status:** Complete and accepted.

- Locked 70/10/20 KDDTrain+ split
- KDDTest+ reserved for final IDS utility
- Target MLP seed 42
- Shadow seeds 101, 202, 303, 404, and 505
- Shadow 505 used only for attacker calibration
- Score-only and label-aware attacks
- 1,000 bootstrap repetitions

At the validation-selected threshold 0.24, the accepted scikit-learn target MLP reached Recall 0.7092, FNR 0.2908, F1 0.8020, and PR-AUC 0.9171 on KDDTest+.

The strongest evaluated baseline attack reached MIA ROC-AUC 0.5029 with a 95% interval containing 0.5. Accepted interpretation:

> Under the specified shadow-calibrated score-only and label-aware threat models, measurable overall membership leakage from the non-private MLP was weak.

This does not establish that the model is private.

## Experiment 04 — PyTorch parity and DP-SGD feasibility

**Status:** Complete and accepted as a feasibility gate.

PyTorch parity passed. The five-epoch Opacus smoke run reached actual ε=7.9986285 at δ=1.1340311×10^-5 with maximum gradient norm 1.0 and PRV accounting. At its validation-selected threshold it reached Recall 0.6620, FNR 0.3380, F1 0.7680, and PR-AUC 0.9193.

Accepted interpretation:

> Formal DP-SGD training and explicit privacy accounting are feasible for the locked MLP pipeline.

## Experiment 05 — Privacy-budget sweep and condition-matched MIA

**Status:** Complete and accepted as a single-seed sweep.

### Protocol

- Non-private PyTorch target plus DP-SGD targets ε≈8, 4, and 2
- Actual ε recorded at fixed δ=1/88,181
- Thirty epochs, batch size 256, maximum gradient norm 1.0, PRV accountant
- Five condition-matched shadows per target condition
- Shadows 101–404 used for attacker training; shadow 505 used for calibration
- Identical target MIA records across conditions
- Score-only and label-aware attacks
- 1,000 bootstrap repetitions and paired DP-minus-non-private comparisons

### IDS utility on KDDTest+

| Condition | Actual ε | Threshold | Recall | FNR | F1 | FPR | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|---:|
| Non-private | — | 0.29 | 0.7080 | 0.2920 | 0.8146 | 0.0401 | 0.9357 |
| DP-SGD ε≈8 | 7.9936 | 0.03 | 0.7128 | 0.2872 | 0.8033 | 0.0818 | 0.8967 |
| DP-SGD ε≈4 | 3.9983 | 0.02 | 0.7267 | 0.2733 | 0.8106 | 0.0877 | 0.8978 |
| DP-SGD ε≈2 | 1.9990 | 0.03 | 0.6850 | 0.3150 | 0.7842 | 0.0821 | 0.8960 |

The ε≈4 condition is the provisional balance candidate. Its higher Recall and lower FNR occur at a higher FPR and lower PR-AUC than the non-private model; this is an operating-point tradeoff, not evidence that DP improved the underlying classifier.

### Membership-inference result

The shadow-selected overall MIA AUCs are approximately 0.5018 for non-private, 0.5028 for ε≈8, 0.5031 for ε≈4, and 0.5029 for ε≈2. Every corresponding 95% interval includes 0.5. Every paired overall AUC and advantage comparison has an interval crossing zero.

Accepted interpretation:

> Under the evaluated attacks, overall membership leakage remained weak for both non-private and DP-SGD models. The experiment does not support a claim that DP-SGD reduced measurable overall leakage.

Some Rare-group paired reductions are statistically separated from zero, but the subgroup contains only 208 records and was examined alongside multiple groups and attacks. These findings remain exploratory.

### Limitations

- Single target-training seed
- Formal guarantee conditional on fixed preprocessing
- `secure_mode: false` recorded
- Opacus warnings preserved
- NSL-KDD binary task and one MLP architecture only
- Baseline MIA floor limits empirical leakage-reduction claims

## Experiment 06 — Repeated-run stability

**Status:** Accepted for bounded final analysis. [Full acceptance review](experiment06_acceptance.md).

All 15 condition/seed runs and both attacker policies are complete. Artifact checksums and
recomputed summaries agree. Mean Recall/F1/FPR are 0.70934/0.80975/0.05610 non-private,
0.71338/0.80166/0.08755 at epsilon about 4, and 0.70108/0.79461/0.08382 at epsilon about 2.
The epsilon-4 Recall gain is uncertain; FPR rises and average precision falls. Do not declare
an optimum. Paired AUC intervals cross zero. Disclose the small exploratory increase in
epsilon-2 label-aware advantage. Some conditional across-seed AUC intervals exclude 0.5.

## Next gate — Experiment 08

The final-analysis notebook is ready. It produces tables and figures from accepted evidence,
without training. Review its output ZIP before final paper claims or scope expansion.
