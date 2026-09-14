# Experiment 09 acceptance review

**Decision: accept Experiment 09 as supplementary single-seed external evidence and proceed
to paper drafting.** The run satisfies the frozen UNSW-NB15 protocol. It supports a bounded
cross-dataset consistency claim about the observed privacy–utility tradeoff; it does not establish
universal generalisation, an optimal privacy budget, or a general reduction in measured leakage.

## Evidence verification

- Executed notebook commit: `8e2922364427865f5cb863e86a6b455fa848dabb`.
- All 16 code cells executed and the saved notebook contains no error output.
- The final cell reports `EXPERIMENT 09: COMPLETE`; all ten declared gates are true.
- Canonical Drive bundle: `experiment09_evidence.zip`, 12,693,915 bytes.
- Bundle SHA-256 reported by the completed notebook:
  `9b40cd2decfe2ecb03feae64d9c37d99bcdc5fe88f2f82e6d84d7e9ed7783511`.
- The evidence manifest declares 27 files excluding itself, with per-file byte counts and hashes.
- The compact repository snapshot preserves the manifests, configurations, aggregate tables,
  warnings, interpretation, and all six PNG/PDF figures. Large per-record feature exports, split
  indices, the fitted preprocessor, and the duplicate ZIP remain in Drive.
- Dataset identity matches the frozen protocol:
  - training: 175,341 rows; SHA-256
    `bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa`;
  - testing: 82,332 rows; SHA-256
    `734fe6642edf758f7c94d7d9149426b49d202fe8e7bf0bef47392489c3c0a559`.
- The development split is complete and disjoint: 122,738 target-train, 17,534
  target-validation, and 35,069 shadow-pool records.
- Three target models and 15 condition-matched shadow models completed. The private targets
  reached epsilon 3.995481 and 1.995670 at delta 8.147436e-06.
- Target-score use was excluded from attacker training and calibration. The official testing
  partition was excluded from threshold selection and MIA.
- The three publication figures are readable and agree with their source tables.

This review checks the executed notebook, Drive manifests, compact result tables, and figures.
It does not independently retrain the 18 neural models or regenerate their predictions.

## Final IDS utility

Official UNSW-NB15 testing results at the F2 threshold selected on target-validation:

| Condition | Actual epsilon | Threshold | Recall | FNR | F1 | FPR | Average precision |
|---|---:|---:|---:|---:|---:|---:|---:|
| Non-private | — | 0.24 | 0.998831 | 0.001169 | 0.853572 | 0.418432 | 0.981609 |
| DP epsilon about 4 | 3.995481 | 0.02 | 0.999846 | 0.000154 | 0.852478 | 0.423784 | 0.968490 |
| DP epsilon about 2 | 1.995670 | 0.02 | 0.999890 | 0.000110 | 0.852436 | 0.424000 | 0.967663 |

Relative to non-private, epsilon about 4 changes Recall by +0.001015, F1 by -0.001093,
FPR by +0.005351, and average precision by -0.013119. Epsilon about 2 changes Recall by
+0.001059, F1 by -0.001136, FPR by +0.005568, and average precision by -0.013946.

The DP conditions therefore preserve F1 closely at the frozen F2 operating policy while moving
to slightly higher Recall and lower FNR at the cost of higher false-positive rates and lower
ranking quality. This is an operating-point tradeoff, not evidence that DP improved the
underlying classifier. No target-training-seed interval is available for these UNSW-NB15
differences.

The absolute tuned FPR is about 42% for every condition. At the default 0.5 threshold, FPR is
0.272865 non-private and 0.407189 for both private models, while F1 is 0.886653, 0.855643,
and 0.855394. These values must be visible in any operational discussion: the very high Recall
does not imply a deployable false-alarm burden.

## Membership-inference results

| Condition | Score-only MIA AUC (95% bootstrap interval) | Label-aware MIA AUC (95% bootstrap interval) |
|---|---:|---:|
| Non-private | 0.499363 [0.493715, 0.505200] | 0.504553 [0.498349, 0.510101] |
| DP epsilon about 4 | 0.500772 [0.494636, 0.506606] | 0.504064 [0.498273, 0.509983] |
| DP epsilon about 2 | 0.500000 [0.500000, 0.500000] | 0.504033 [0.497777, 0.509767] |

Every overall MIA AUC interval contains chance. The epsilon-about-2 score-only logistic attacker
produced constant chance-level scores, giving AUC 0.5 and advantage 0. This is a valid recorded
attack outcome but a degenerate empirical measurement, not proof that membership leakage is
absent.

Seven of eight paired DP-minus-non-private AUC or advantage intervals cross zero. The only
separated comparison is epsilon-about-2 score-only advantage: -0.006559 with interval
[-0.018478, -0.001995]. Because the corresponding score-only attacker is constant, AUC does
not show a reduction, the label-aware comparisons are inconclusive, and all observed effects are
near chance, this isolated advantage result is not sufficient for a general leakage-reduction
claim.

Attack-family rows are descriptive only. The largest recorded family AUC is 0.5235 for Analysis
under the non-private model on 400 balanced records; it has no multiplicity-adjusted interval and
must not be elevated to a primary result.

## Cross-dataset interpretation

Experiment 09 is qualitatively consistent with the accepted NSL-KDD analysis:

- DP-SGD can retain useful IDS utility under the frozen architecture and evaluation procedure.
- The apparent Recall/FNR benefit is inseparable from the selected threshold and a higher
  false-positive burden.
- Average precision is lower for the private conditions.
- Overall MIA remains close to chance for non-private and private models, leaving little empirical
  room to demonstrate a leakage reduction.
- Neither dataset confirms epsilon about 4 as optimal. On UNSW-NB15, epsilon about 2 and epsilon
  about 4 have almost identical selected-threshold utility.

The result supports saying that the same broad tradeoff was observed in a compact external check.
It does not support a universal cross-dataset performance or privacy claim because Experiment 09
uses one target-training seed and one architecture.

## Warnings and limitations

- `secure_mode=False` is recorded. This is acceptable for the experiment but not a
  production-strength randomness claim.
- Opacus accounting-tightness, PyTorch hook, and deprecation warnings are preserved. They did not
  cause non-finite evidence or a failed privacy-budget gate.
- The formal DP statement covers optimisation conditional on fixed, non-private preprocessing.
- Bootstrap intervals measure record-sampling uncertainty conditional on one trained target;
  they do not measure target-training-seed variation.
- The privacy–utility scatter plot uses a narrow F1 axis. It is numerically correct but can
  visually magnify negligible absolute F1 differences; the table must accompany it.

## Accepted claim boundary

The supported conclusion is:

> In a supplementary single-seed UNSW-NB15 evaluation, formally accounted DP-SGD at epsilon
> about 4 and epsilon about 2 preserved selected-threshold F1 and Recall closely, while increasing
> the false-positive burden and reducing average precision. Evaluated membership-inference AUCs
> remained near chance for every condition, and the evidence does not establish a general
> DP-induced reduction in measured leakage.

Do not claim that epsilon about 4 is optimal, that DP improved classifier quality, that membership
leakage was eliminated, or that one UNSW-NB15 seed establishes universal generalisation.

## Next milestone

No additional experiment is required by the frozen roadmap. Complete full-text related-work
verification, then draft the paper from the accepted NSL-KDD and supplementary UNSW-NB15
evidence with the limitations above explicit.
