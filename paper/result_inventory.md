# Frozen result, method, and figure inventory

**Freeze point:** accepted Experiment 08 (primary NSL-KDD analysis) and accepted Experiment 09
(supplementary UNSW-NB15 check). No value below should be replaced by an exploratory notebook
output without reopening the acceptance review.

## 1. Study design

| Item | Frozen specification |
|---|---|
| Primary dataset | NSL-KDD: `KDDTrain+.txt` development source; `KDDTest+.txt` utility test |
| Supplementary dataset | Official UNSW-NB15 training/testing CSV partitions |
| Task | Binary Normal versus Attack classification |
| Primary model | MLP, 122 encoded NSL-KDD inputs, hidden layers 64 and 32, ReLU, one logit |
| Training | Adam, 30 epochs, batch 256, learning rate 0.001, weight decay 0.0001 |
| NSL-KDD split | 88,181 target-train; 12,597 target-validation; 25,195 shadow-pool |
| NSL-KDD test | 22,544 untouched `KDDTest+` records |
| Target seeds | 42, 52, 62, 72, 82 for non-private, epsilon-about-4, epsilon-about-2 |
| DP mechanism | Opacus DP-SGD, max gradient norm 1.0, Poisson sampling, PRV accountant |
| NSL delta | 1.134031140495118e-05 (= 1 / 88,181) |
| Actual NSL epsilons | 3.9982670409 and 1.9990375327 |
| Threshold policy | Maximise F2 on target-validation; evaluate once on external test |
| MIA members/non-members | Balanced samples from target-train / target-validation |
| Shadows | Five per condition; 101–404 attacker training, 505 calibration |
| Primary attacks | Score-only logistic regression on attack probability; label-aware loss threshold |
| Secondary attacks | Best shadow-calibration AUC among predeclared threshold/logistic/RF families |
| MIA metrics | ROC-AUC, advantage, balanced accuracy, TPR at 1% and 5% FPR |
| Uncertainty | Five-seed two-sided t intervals; 1,000 paired bootstrap replicates where declared |
| Privacy scope | DP-SGD optimisation conditional on fixed, non-private preprocessing |

## 2. Primary NSL-KDD utility table

Five-seed means at validation-selected F2 thresholds. Parentheses show standard deviations.

| Condition | Actual epsilon | Recall | FNR | F1 | FPR | Average precision |
|---|---:|---:|---:|---:|---:|---:|
| Non-private | — | 0.7093 (0.0222) | 0.2907 (0.0222) | 0.8097 (0.0161) | 0.0561 (0.0227) | 0.9375 (0.0079) |
| DP-SGD epsilon about 4 | 3.9983 | 0.7134 (0.0138) | 0.2866 (0.0138) | 0.8017 (0.0082) | 0.0876 (0.0042) | 0.8907 (0.0063) |
| DP-SGD epsilon about 2 | 1.9990 | 0.7011 (0.0116) | 0.2989 (0.0116) | 0.7946 (0.0074) | 0.0838 (0.0015) | 0.8906 (0.0063) |

Source: `results/final_analysis/tables/five_seed_summary.csv`.

## 3. Paired NSL-KDD utility differences

DP minus non-private, paired by target-training seed; 95% t intervals.

| Comparison | Metric | Mean difference | 95% interval | Interpretation |
|---|---|---:|---:|---|
| epsilon about 4 | Recall | +0.00404 | [-0.01334, 0.02142] | Uncertain |
| epsilon about 4 | F1 | -0.00809 | [-0.02241, 0.00622] | Uncertain |
| epsilon about 4 | FPR | +0.03145 | [0.00460, 0.05830] | Higher false-positive burden |
| epsilon about 4 | Average precision | -0.04682 | [-0.05462, -0.03903] | Lower ranking quality |
| epsilon about 2 | Recall | -0.00826 | [-0.03135, 0.01483] | Uncertain |
| epsilon about 2 | F1 | -0.01514 | [-0.03364, 0.00335] | Uncertain |
| epsilon about 2 | FPR | +0.02772 | [0.00038, 0.05507] | Higher false-positive burden |
| epsilon about 2 | Average precision | -0.04693 | [-0.05312, -0.04074] | Lower ranking quality |

Source: `results/final_analysis/tables/primary_paired_differences_summary.csv`.

## 4. Primary NSL-KDD membership results

Five-seed conditional means. These values are close to chance in magnitude. Some across-seed
conditional AUC intervals exclude 0.5; the stronger paper-level comparison is the paired
DP-minus-non-private result, for which every primary and secondary AUC interval crosses zero.

| Condition | Score-only AUC | Label-aware AUC | Score-only advantage | Label-aware advantage |
|---|---:|---:|---:|---:|
| Non-private | 0.50230 | 0.50088 | 0.00941 | 0.00786 |
| DP-SGD epsilon about 4 | 0.50301 | 0.50159 | 0.01107 | 0.01097 |
| DP-SGD epsilon about 2 | 0.50327 | 0.50146 | 0.01145 | 0.01130 |

Paired primary AUC differences:

| Comparison | Threat model | Mean AUC difference | 95% interval |
|---|---|---:|---:|
| epsilon about 4 minus non-private | Score-only | +0.00071 | [-0.00111, 0.00254] |
| epsilon about 4 minus non-private | Label-aware | +0.00071 | [-0.00094, 0.00236] |
| epsilon about 2 minus non-private | Score-only | +0.00097 | [-0.00076, 0.00270] |
| epsilon about 2 minus non-private | Label-aware | +0.00058 | [-0.00126, 0.00242] |

The secondary epsilon-about-2 label-aware advantage difference is +0.00345 with interval
[0.00068, 0.00621]. It is exploratory, small, and points toward increased—not reduced—measured
advantage. It must be disclosed if secondary results are discussed.

Sources: `results/final_analysis/tables/final_primary_privacy_utility.csv`,
`primary_paired_differences_summary.csv`, and `secondary_paired_differences_summary.csv`.

## 5. Supplementary UNSW-NB15 utility

Single target seed; official testing partition; validation-selected F2 threshold.

| Condition | Actual epsilon | Threshold | Recall | FNR | F1 | FPR | Average precision |
|---|---:|---:|---:|---:|---:|---:|---:|
| Non-private | — | 0.24 | 0.998831 | 0.001169 | 0.853572 | 0.418432 | 0.981609 |
| DP-SGD epsilon about 4 | 3.995481 | 0.02 | 0.999846 | 0.000154 | 0.852478 | 0.423784 | 0.968490 |
| DP-SGD epsilon about 2 | 1.995670 | 0.02 | 0.999890 | 0.000110 | 0.852436 | 0.424000 | 0.967663 |

The very high Recall is coupled to an approximately 42% FPR. At the default threshold 0.5,
FPR is 0.272865 non-private and 0.407189 for both private conditions. This operational burden
must be visible wherever UNSW-NB15 results are discussed.

## 6. Supplementary UNSW-NB15 membership results

| Condition | Score-only AUC (95% bootstrap interval) | Label-aware AUC (95% bootstrap interval) |
|---|---:|---:|
| Non-private | 0.499363 [0.493715, 0.505200] | 0.504553 [0.498349, 0.510101] |
| DP-SGD epsilon about 4 | 0.500772 [0.494636, 0.506606] | 0.504064 [0.498273, 0.509983] |
| DP-SGD epsilon about 2 | 0.500000 [0.500000, 0.500000] | 0.504033 [0.497777, 0.509767] |

The epsilon-about-2 score-only attacker is degenerate and emits constant chance scores. Its
isolated advantage difference (-0.006559, interval [-0.018478, -0.001995]) is not evidence of a
general leakage reduction.

Sources: `results/unsw_nb15_external_validation/unsw_nb15_ids_results.csv`,
`unsw_nb15_mia_results.csv`, and `unsw_nb15_paired_mia_differences.csv`.

## 7. Frozen figure set

### Main paper

1. `results/final_analysis/figures/10_false_alarms_and_average_precision.pdf` — primary
   operational utility result.
2. `results/final_analysis/figures/04_mia_auc_vs_epsilon.pdf` — primary MIA magnitude and
   uncertainty.
3. `results/final_analysis/figures/06_f1_vs_mia_auc.pdf` — joint utility/leakage view; state that
   marginal error bars are not a joint confidence region.
4. `results/unsw_nb15_external_validation/figures/01_unsw_ids_utility.pdf` — supplementary
   external utility.
5. `results/unsw_nb15_external_validation/figures/02_unsw_mia_auc.pdf` — supplementary MIA.

### Supplement or repository only

- All other accepted Experiment 08 figures.
- UNSW-NB15 privacy–utility scatter, whose narrow F1 axis can visually magnify tiny differences.
- Seed-42 member/non-member distributions.

## 8. Frozen interpretation

Supported: formally accounted DP-SGD retained broadly similar selected-threshold F1 and Recall
under the tested pipeline, while increasing false positives and reducing average precision. The
evaluated overall MIAs were close to chance and paired comparisons did not show DP-induced AUC
reduction. The UNSW-NB15 check showed the same broad utility pattern but is single-seed evidence.

Unsupported: optimal epsilon, improved underlying classifier quality, eliminated membership
leakage, immunity to stronger/adaptive attacks, production-grade cryptographic randomness,
end-to-end raw-data DP, or universal cross-dataset generalisation.
