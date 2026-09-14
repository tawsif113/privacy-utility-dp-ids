# Experiment 09 frozen protocol — compact UNSW-NB15 external validation

## Purpose and status

Experiment 09 is a supplementary, single-target-seed external validation of the accepted
NSL-KDD findings. The protocol remains frozen. The completed evidence ZIP and executed notebook
have passed review; see [the acceptance decision](experiment09_acceptance.md).

## Dataset and split

- Dataset: official `UNSW_NB15_training-set.csv` and `UNSW_NB15_testing-set.csv` partitions.
- Frozen training file identity: 32,293,018 bytes; SHA-256
  `bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa`.
- Frozen testing file identity: 15,380,800 bytes; SHA-256
  `734fe6642edf758f7c94d7d9149426b49d202fe8e7bf0bef47392489c3c0a559`.
- If absent, the notebook retrieves these exact bytes from mirror revision
  `6f5f54594dfc80c84264aec4c7cc3d9b162f1e2f` and verifies them before loading data.
- Task: binary Normal versus Attack.
- Excluded from model features: `id`, `attack_cat`, and `label`.
- Categorical model features: `proto`, `service`, and `state`; all other model features are
  numeric.
- Development split of the official training partition, with target seed 42 and stratification
  by binary label plus attack family:
  - 70% target train;
  - 10% target validation;
  - 20% shadow pool.
- The official test partition is used only for final IDS utility.
- The F2 operating threshold is selected only on target validation.
- Target preprocessing is fitted only on target train. Each shadow preprocessor is fitted only
  on that shadow model's member half.

The notebook records raw-file SHA-256 hashes, split indices, split counts, feature names, and
the fitted target preprocessor in the evidence bundle.

## Fixed model and training procedure

| Item | Frozen value |
| --- | --- |
| Target seed | 42 |
| Conditions | non-private, DP-SGD ε≈4, DP-SGD ε≈2 |
| Architecture | 64–32 ReLU MLP, one output logit |
| Optimizer | Adam |
| Epochs | 30 |
| Batch size | 256 |
| Learning rate | 0.001 |
| Weight decay | 0.0001 |
| DP clipping | flat, max norm 1.0 |
| Accountant | Opacus PRV |
| Sampling | Poisson for DP-SGD |
| Delta | `1 / target_train_rows` |

Noise multipliers are recomputed for UNSW-NB15. ε≈4 is the utility-favoured tested DP
setting from the NSL-KDD study, not an optimum. ε≈2 is the strongest tested privacy setting.
ε≈8 and new privacy values are excluded.

## Fixed membership-inference protocol

- Shadow seeds: 101, 202, 303, 404, and 505 for each of the three conditions.
- Total training runs: 3 target models plus 15 condition-matched shadows = 18.
- Seeds 101–404 train the score-only attacker.
- Seed 505 calibrates attack operating thresholds.
- Fixed attacks only:
  - score-only black-box logistic regression using `prob_attack`;
  - label-aware loss-threshold attack using true-label loss.
- Target members: family-balanced records from target train.
- Target non-members: matching family-balanced records from target validation.
- No target output is used to train or calibrate an attacker.
- Overall MIA AUC and advantage receive 1,000-repetition stratified bootstrap intervals.
- DP-minus-non-private MIA differences use paired stratified bootstrap resampling on identical
  target records.
- Attack-family results are descriptive diagnostics without bootstrap intervals.

The bootstrap intervals quantify record-sampling uncertainty conditional on one trained target
model. They do not quantify target-training-seed uncertainty.

## Required reporting boundary

- Call this supplementary single-seed external evidence.
- Do not call ε≈4 optimal.
- Do not claim cross-dataset generalisation before comparing the accepted UNSW-NB15 evidence
  with the accepted NSL-KDD evidence.
- Do not claim DP reduced measured leakage unless the paired interval for the stated attack and
  metric lies entirely below zero.
- Keep formal DP guarantees distinct from empirical MIA performance.
- State that the DP guarantee covers optimisation conditional on fixed preprocessing.
- Do not introduce architecture tuning, privacy-budget tuning, extra datasets, or new attack
  selection after seeing UNSW-NB15 results.

## Completion gate

The run is reviewable only if the final cell prints `EXPERIMENT 09: COMPLETE` and creates
`experiment09_evidence.zip`. The executed notebook and that ZIP must both be preserved and
reviewed before paper drafting begins.
