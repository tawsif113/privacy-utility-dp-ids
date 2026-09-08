# Experiment 06 acceptance review

**Decision: proceed to Experiment 08 final analysis.** Accept the evidence as a five-target-seed
stability study conditional on the fixed dataset split and frozen attackers. This decision does
not confirm epsilon 4 as optimal or establish a reduction in measured leakage.

## Evidence identity and verification

- Accepted Experiment 06 manifest SHA-256: `f1d93ba4362ebe9308fd7e47bcf111f90a9c8d2e8ebd7e3691e5f1686a16b570`.
- All 15 artifact checksums match; 15 distinct condition/seed results are present.
- Three accepted seed-42 targets were reused and 12 additional targets were trained.
- Non-private, epsilon about 4, and epsilon about 2 each have seeds 42/52/62/72/82.
- Training configuration, CPU runtime, package versions, accounting fields and source manifests agree.
- Confusion-matrix utility metrics, means, sample SDs, t intervals and matched-seed differences
  were independently recomputed from the submitted per-run tables for both attacker policies.
- Seed-42 utility agrees with Experiment 05. The documented 9.45e-9 AUC discrepancy is within
  the explicit 1e-8 numerical reproduction tolerance; advantage remains checked at 1e-10.
- Experiment 05 prerequisite hashes agree after accounting for trailing-newline normalization
  in the repository copies. Scientific settings and reused values agree.
- Source neural models and full per-sample scores are external: this audit checks the submitted
  evidence, not an independent rerun of training, predictions or privacy accounting.

## Five-seed utility

Values are means; rates below are percentages.

| Condition | Actual epsilon | Recall | FNR | F1 | FPR | Average precision |
|---|---:|---:|---:|---:|---:|---:|
| Non-private | — | 70.9343 | 29.0657 | 80.9750 | 5.6101 | 0.937504 |
| DP epsilon about 4 | 3.998267 | 71.3380 | 28.6620 | 80.1657 | 8.7550 | 0.890681 |
| DP epsilon about 2 | 1.999038 | 70.1083 | 29.8917 | 79.4605 | 8.3822 | 0.890575 |

For epsilon about 4 versus non-private, Recall changes by +0.404 percentage points
(95% matched-seed t interval: -1.334 to +2.142 points). This does not establish an improvement
or equivalence. FPR changes by +3.145 points (interval +0.460 to +5.830); average precision
changes by -0.046824 (interval -0.054617 to -0.039030). These intervals are unadjusted.

The original recall-based rationale for a confirmed epsilon-4 balance point is not established.
Retain both private budgets as comparative tradeoffs; do not select a universal winner.

## Membership inference

Primary score-only mean AUC: non-private 0.502297, epsilon about 4 0.503009, epsilon about 2
0.503268. Primary label-aware mean AUC: 0.500882, 0.501594, 0.501463 respectively.
The magnitudes remain close to chance. Several conditional across-seed intervals exclude 0.5,
so the old single-seed statement that every AUC interval contains 0.5 must not be reused here.
All paired AUC intervals cross zero under both primary and secondary policies: no demonstrated
AUC reduction. No overall advantage reduction is supported either.

Epsilon about 2 has a small positive label-aware advantage difference: +0.003445, unadjusted
interval [+0.000682, +0.006208]. Disclose this exploratory increase rather than hiding it.
Maximum-threshold advantage is an evaluation diagnostic, not performance at the shadow-fixed
operating threshold; it is upward-biased by maximization in finite samples.

## Required interpretation limits

- Five-seed t intervals describe target-training variability on fixed records and frozen attackers.
  They do not include record-sampling uncertainty, retrained shadow variability, or dataset variation.
- Intervals are unadjusted across multiple metrics. Preserve raw bounds even when a t interval
  extends outside [0,1]. An all-zero low-FPR TPR series does not prove zero population leakage.
- PR-AUC in the code is `average_precision_score`, not trapezoidal integration.
- Formal privacy is conditional on fixed, non-private preprocessing; `secure_mode=False` remains
  disclosed. Per-model epsilon is not the privacy budget of jointly releasing all models.
- Epsilon 4 was shortlisted after inspecting the sweep. No fresh test set validates selection.
- No deployment-specific utility threshold or equivalence margin has been established.
- Experiment 05 Rare-group results (208 records) remain single-seed and exploratory.

## Next milestone

Run `notebooks/08_privacy_utility_frontier.ipynb`. It checks this accepted evidence and creates
final tables, figures, raw plot data, an interpretation file and a checksummed ZIP. It trains no
models and tunes no thresholds. Epsilon about 8 stays explicitly single-seed context.

The three seed-42 score caches are needed for distribution plots. Missing caches produce a
clearly marked partial export with recovery paths; they are not grounds to retrain the models.
Review the Experiment 08 ZIP before paper-result finalization or compact external validation.
Skip the optional Experiment 07 feature-noise comparator unless a documented question requires it.
