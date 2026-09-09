# Privacy–Utility Auditing of DP-SGD for ML-Based Network Intrusion Detection

A reproducible empirical study of how formally accounted DP-SGD affects intrusion-detection utility and measurable training-membership leakage in an MLP trained on NSL-KDD.

## Quick review

- [Accepted experiment summary](report/experiment_summary.md) — methods, results, and claim boundaries in one place
- [Evidence index](results/README.md) — maps every reported result to its committed CSV or JSON source
- [Research roadmap](ROADMAP.md) — completed work, current gate, and next experiments
- `python scripts/validate_evidence.py` — checks that the committed manifests and result tables agree

**Current boundary:** Experiment 08 is accepted and the NSL-KDD final analysis is complete. The tested results do not establish ε≈4 as optimal or demonstrate reduced measured leakage. See the [final-analysis review](report/experiment08_acceptance.md) and [evidence snapshot](results/final_analysis/README.md).

## Research question

How does formally accounted DP-SGD affect IDS utility—particularly Recall and False Negative Rate (FNR)—and membership-inference risk under score-only and label-aware attacks?

## Current stage

Experiments 01–06 and 08 are complete. Experiment 06 tested non-private, ε≈4, and ε≈2 conditions over five target-training seeds using the locked split and frozen attackers. Experiment 08 verified the accepted evidence and produced the final tables and figures without new training. A compact UNSW-NB15 protocol is the next gate; it must remain external validation rather than a new sweep.

| Phase | Artifact | Status |
|---|---|---|
| Baseline IDS comparison | Experiment 01 | Complete and archived |
| Locked MIA-ready MLP and baseline audit | Experiments 02–03 | Complete and accepted |
| PyTorch parity and DP-SGD feasibility | Experiment 04 | Complete and accepted |
| Privacy-budget sweep and per-model MIA | Experiment 05 | Complete and accepted as single-run evidence |
| Repeated-run stability analysis | Experiment 06 | Complete; evidence independently checked |
| Optional heuristic-noise comparator | Experiment 07 | Optional; not part of the core claim |
| Final privacy–utility analysis | Experiment 08 | Complete; evidence independently checked |
| Compact external validity | Experiment 09 | Protocol freeze pending |

## Verified evidence

| Condition | Actual ε | Recall | FNR | F1 | FPR | Average precision | Score-only MIA AUC |
|---|---:|---:|---:|---:|---:|---:|---:|
| Non-private | — | 0.7093 | 0.2907 | 0.8097 | 0.0561 | 0.9375 | 0.5023 |
| DP-SGD ε≈4 | 3.9983 | 0.7134 | 0.2866 | 0.8017 | 0.0876 | 0.8907 | 0.5030 |
| DP-SGD ε≈2 | 1.9990 | 0.7011 | 0.2989 | 0.7946 | 0.0838 | 0.8906 | 0.5033 |

These are five-seed means at validation-selected thresholds. The ε≈4 Recall difference is
uncertain, while its FPR is higher and average precision lower than non-private. All primary
and secondary paired MIA AUC intervals cross zero, so the study does not support a measured
leakage-reduction claim. Some conditional across-seed MIA AUC intervals exclude 0.5; do not
reuse the earlier single-seed statement that every interval contains chance.

The ε≈8 result is retained only as single-seed sweep context and is not pooled with the
five-seed conditions.

## Experimental protocol

- **Dataset:** NSL-KDD
- **Task:** Binary classification, Normal vs Attack
- **Target model:** MLP
- **Locked development split:** 70% target-train, 10% target-validation, 20% shadow-pool
- **External IDS evaluation:** KDDTest+ only
- **Threshold policy:** Select the F2 operating threshold on target-validation only
- **MIA protocol:** Five shadow models with score-only and label-aware attacks
- **Attack calibration:** Shadow outputs only; no target-score tuning
- **Uncertainty:** 1,000 bootstrap repetitions for MIA estimates and paired DP-minus-non-private comparisons
- **Formal private training:** Opacus DP-SGD with explicit epsilon, delta, clipping, sampling, noise, epoch, and accountant records
- **Core IDS metrics:** Recall, FNR, F1, PR-AUC
- **Core MIA metrics:** ROC-AUC, advantage, balanced accuracy, TPR at 1% and 5% FPR, and bootstrap confidence intervals

KDDTest+ is never used to tune the IDS threshold, train or calibrate the MIA attacker, or select a privacy configuration.

## Why the baseline floor effect matters

The strongest evaluated non-private baseline attack is already near chance. This leaves limited room for a large empirical leakage reduction after DP-SGD. Formal differential privacy and empirical MIA resistance are therefore reported as distinct forms of evidence: an epsilon/delta guarantee does not depend on the MIA result, and a weak MIA does not establish formal privacy.

## Repository layout

~~~text
notebooks/   Colab notebooks in execution order
data/        Dataset instructions, hashes, and split metadata
results/     Concise committed CSV and JSON evidence
manifests/   Reproducibility and protocol manifests
artifacts/   Documentation for external model/preprocessing artifacts
report/      Accepted experiment interpretations
scripts/     Repository-level evidence consistency checks
~~~

Large model files, transformed arrays, and per-sample scores remain outside Git. Their identifiers and originating paths are recorded in manifests where available.

## Reproduce the pipeline

### 1. Clone and create an environment

~~~bash
git clone https://github.com/tawsif113/privacy-utility-dp-ids.git
cd privacy-utility-dp-ids

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
~~~

The accepted Experiment 04 run used Python 3.12.13, PyTorch 2.11.0+cu128, Opacus 1.6.0, scikit-learn 1.6.1, NumPy 2.0.2, and pandas 2.2.2. The Experiment 05 manifest separately records its CPU runtime and package versions. Hardware changes runtime, not the locked protocol.

`requirements.txt` pins the versions verified by the accepted Experiment 04 manifest. Packages used only by earlier baseline notebooks remain explicitly unpinned where their exact run versions were not recorded.

### 2. Supply NSL-KDD externally

The raw dataset is intentionally excluded. Provide:

~~~text
KDDTrain+.txt
KDDTest+.txt
~~~

Expected SHA-256 hashes:

~~~text
KDDTrain+: 1b86d2f957b33082081bba410fe129b475efebcc13c9014c3f447c8271aadf95
KDDTest+:  fa46b0935342616aa83b7c2578db355b6a7aaabbc492248172c7a1e8b7ab8f84
~~~

See [data/README.md](data/README.md) for accepted split sizes and external-artifact notes.

### 3. Execute notebooks in order

1. [01_baseline_nsl_kdd_ids.ipynb](notebooks/01_baseline_nsl_kdd_ids.ipynb)
2. [02_03_mia_ready_baseline_and_audit.ipynb](notebooks/02_03_mia_ready_baseline_and_audit.ipynb)
3. [04_dp_sgd_feasibility_smoke_test.ipynb](notebooks/04_dp_sgd_feasibility_smoke_test.ipynb)
4. [05_dp_sgd_privacy_utility_sweep.ipynb](notebooks/05_dp_sgd_privacy_utility_sweep.ipynb)
5. [06_repeated_runs_stability.ipynb](notebooks/06_repeated_runs_stability.ipynb) — accepted; preserve outputs
6. [08_privacy_utility_frontier.ipynb](notebooks/08_privacy_utility_frontier.ipynb) — complete and accepted; no training

### 4. Validate the committed evidence

~~~bash
python scripts/validate_evidence.py
~~~

This check does not rerun model training. It verifies the committed evidence through Experiment
05. Use `scripts/audit_experiment06.py` and `scripts/audit_experiment08.py` for the corresponding
complete Drive bundles.


## Claim boundary

The supported project description is:

> We evaluate formally accounted DP-SGD for tabular intrusion detection at multiple privacy budgets using IDS-specific utility metrics and shadow-calibrated membership-inference auditing.

Do not infer that:

- DP-SGD reduced overall measurable membership leakage
- epsilon 4 is a confirmed optimal setting
- membership leakage has been eliminated
- one tested setting is universally optimal
- the study outperforms prior work

The reported DP guarantee is conditional on fixed preprocessing. The completed primary study is limited to NSL-KDD, binary classification, one MLP family, and the stated MIA threat models. External validation is pending.

## Researcher

**Kazi Md. Tawsif Rahman**

- [Academic portfolio](https://research.tawsifrahman.flaro-tech.com)
- [GitHub profile](https://github.com/tawsif113)
- [Email](mailto:tawsifcse113@gmail.com)
