# Experiment 08 acceptance review

**Decision: accept the final NSL-KDD analysis and proceed to a compact external-validity
protocol.** The evidence supports a formally accounted privacy–utility comparison among the
tested settings. It does not establish a universal optimal epsilon or reduced measured leakage.

## Evidence verification

- Canonical Drive bundle: `experiment08_evidence.zip`, 1,718,095 bytes.
- Bundle SHA-256: `9eabc696aac5020598dc85cce2f445ad0decf97a8bf8bb10cff19d0d4bb6113d`.
- The bundle is marked `COMPLETE`; all four analysis gates are true.
- All 40 declared output hashes match. The ZIP has 41 unique safe members, including the
  final manifest.
- The accepted Experiment 06 source bundle passed re-audit.
- Fifty-three summary rows, 15 tuned IDS rows, 30 primary MIA rows, 30 secondary MIA rows,
  and 15 accounting rows agree with the accepted source evidence.
- Means, sample standard deviations, df=4 t intervals, and primary/secondary matched-seed
  differences were independently recomputed.
- All ten figures are present in PNG and PDF and passed visual review.
- The 66,138-row distribution export has 12 valid monotone ECDF groups. Its three seed-42 loss
  distributions reproduce the label-aware MIA AUCs to floating-point precision.
- Experiment 08 started no training, tuned no thresholds, and fitted no attacks.

The original neural predictions, source models, and three score caches are not bundled. The
notebook verified the cache hashes before export, and the derived loss distributions reproduce
the recorded AUCs, but this review is not an independent rerun of training or prediction.

## Final five-seed result

| Condition | Actual epsilon | Recall | FNR | F1 | FPR | Average precision | Score-only MIA AUC | Label-aware MIA AUC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Non-private | — | 0.709343 | 0.290657 | 0.809750 | 0.056101 | 0.937504 | 0.502297 | 0.500882 |
| DP epsilon about 4 | 3.998267 | 0.713380 | 0.286620 | 0.801657 | 0.087550 | 0.890681 | 0.503009 | 0.501594 |
| DP epsilon about 2 | 1.999038 | 0.701083 | 0.298917 | 0.794605 | 0.083822 | 0.890575 | 0.503268 | 0.501463 |

At epsilon about 4, the paired Recall change is +0.00404 with an unadjusted 95% interval
[-0.01334, +0.02142]. A detection improvement or equivalence is not established. FPR increases
by +0.03145 [0.00460, 0.05830], and average precision decreases by -0.04682
[-0.05462, -0.03903].

All paired MIA AUC intervals cross zero under both attacker policies. MIA AUC remains close to
0.5, but that magnitude is not proof of zero leakage. Epsilon about 2 has a small exploratory
increase in label-aware advantage: +0.00345 [0.00068, 0.00621].

## Claim boundaries

- The t intervals measure target-training-seed variation on fixed records with frozen attackers.
  They omit record-sampling, shadow-retraining, and dataset variation.
- Intervals are unadjusted across multiple metrics.
- DP accounting is conditional on fixed non-private preprocessing and `secure_mode=False`.
- Per-model epsilon is not a composition bound for releasing every trained model.
- Epsilon about 8 and subgroup results remain single-seed context.
- Epsilon about 4 was selected after the sweep and is not independently confirmed as optimal.
- The final descriptive frontier covers only the tested NSL-KDD conditions and threat models.

## Next milestone

Freeze a compact UNSW-NB15 external-validity protocol before creating or running another
notebook. Compare only the non-private model, the epsilon-about-4 utility-favoured tested DP
condition, and the epsilon-about-2 strongest tested privacy condition. Do not introduce another
epsilon sweep, architecture search, or universal-best claim.
