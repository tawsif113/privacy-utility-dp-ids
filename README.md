# Privacy–Utility Auditing of DP-SGD for ML-Based Network Intrusion Detection

A reproducible empirical study of how formally accounted DP-SGD affects intrusion-detection utility and measurable training-membership leakage in an MLP trained on NSL-KDD.

## Quick review

- [Accepted experiment summary](report/experiment_summary.md) — methods, results, and claim boundaries in one place
- [Evidence index](results/README.md) — maps every reported result to its committed CSV or JSON source
- [Research roadmap](ROADMAP.md) — completed work, current gate, and next experiments
- `python scripts/validate_evidence.py` — checks that the committed manifests and result tables agree

**Current boundary:** Experiments 01–05 are complete and accepted as single-run evidence. Experiment 06 repeated-run stability is the current gate; ε≈4 is only a candidate balance point until repeated runs confirm it.

## Research question

How does formally accounted DP-SGD affect IDS utility—particularly Recall and False Negative Rate (FNR)—and membership-inference risk under score-only and label-aware attacks?

## Current stage

Experiments 01–05 are complete. Experiment 05 compared a non-private PyTorch MLP with formally accounted DP-SGD conditions at actual ε values 7.9936, 3.9983, and 1.9990 using the locked split and condition-matched shadow protocol. Overall MIA estimates remained near chance, and paired 95% confidence intervals did not support an overall leakage-reduction claim. Experiment 06 repeated-run stability is now the current gate.

| Phase | Artifact | Status |
|---|---|---|
| Baseline IDS comparison | Experiment 01 | Complete and archived |
| Locked MIA-ready MLP and baseline audit | Experiments 02–03 | Complete and accepted |
| PyTorch parity and DP-SGD feasibility | Experiment 04 | Complete and accepted |
| Privacy-budget sweep and per-model MIA | Experiment 05 | Complete and accepted as single-run evidence |
| Repeated-run stability analysis | Experiment 06 | Pending |
| Optional heuristic-noise comparator | Experiment 07 | Optional; not part of the core claim |
| Final privacy–utility analysis | Experiment 08 | Pending |

## Verified evidence

| Condition | Actual ε | Recall | FNR | F1 | PR-AUC | Shadow-selected overall MIA AUC |
|---|---:|---:|---:|---:|---:|---:|
| Non-private | — | 0.7080 | 0.2920 | 0.8146 | 0.9357 | 0.5018 |
| DP-SGD ε≈8 | 7.9936 | 0.7128 | 0.2872 | 0.8033 | 0.8967 | 0.5028 |
| DP-SGD ε≈4 | 3.9983 | 0.7267 | 0.2733 | 0.8106 | 0.8978 | 0.5031 |
| DP-SGD ε≈2 | 1.9990 | 0.6850 | 0.3150 | 0.7842 | 0.8960 | 0.5029 |

These are validation-threshold-selected, single-seed KDDTest+ utility results. The ε≈4 condition is the candidate balance point for repeated-run validation, not a confirmed optimum. Its higher Recall comes with a higher FPR and lower PR-AUC than the non-private model.

All shadow-selected overall MIA AUC confidence intervals include 0.5. The paired overall comparisons do not support measured leakage reduction for any DP condition. Formal privacy accounting and empirical MIA resistance therefore remain separate conclusions.

Experiment 04 remains the accepted implementation-feasibility checkpoint; Experiment 05 supplies the first multi-epsilon comparison.

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

### 4. Validate the committed evidence

~~~bash
python scripts/validate_evidence.py
~~~

This check does not rerun model training. It verifies dataset identity, privacy accounting, utility tables, MIA tables, confidence intervals, shadow budgets, paired comparisons, and manifest agreement across Experiments 01–05.


## Claim boundary

The supported project description is:

> We evaluate formally accounted DP-SGD for tabular intrusion detection at multiple privacy budgets using IDS-specific utility metrics and shadow-calibrated membership-inference auditing.

Do not infer that:

- DP-SGD reduced overall measurable membership leakage
- epsilon 4 is a confirmed optimal setting
- membership leakage has been eliminated
- the final privacy–utility tradeoff is known
- the study outperforms prior work

The reported DP guarantee is conditional on fixed preprocessing. The current study is limited to NSL-KDD, binary classification, one MLP family, and the stated black-box MIA threat models.

## Researcher

**Kazi Md. Tawsif Rahman**

- [Academic portfolio](https://research.tawsifrahman.flaro-tech.com)
- [GitHub profile](https://github.com/tawsif113)
- [Email](mailto:tawsifcse113@gmail.com)
