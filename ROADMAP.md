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
5. **Experiment 06 — repeated-run stability:** accepted five target-training seeds for non-private, ε≈4, and ε≈2 under fixed attackers.
6. **Experiment 08 — final privacy–utility analysis:** accepted complete tables, figures, distributions, and bounded interpretation without new training.

## Accepted Experiment 05 result

| Condition | Actual ε | Recall | FNR | F1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| Non-private | — | 0.7080 | 0.2920 | 0.8146 | 0.9357 |
| DP-SGD ε≈8 | 7.9936 | 0.7128 | 0.2872 | 0.8033 | 0.8967 |
| DP-SGD ε≈4 | 3.9983 | 0.7267 | 0.2733 | 0.8106 | 0.8978 |
| DP-SGD ε≈2 | 1.9990 | 0.6850 | 0.3150 | 0.7842 | 0.8960 |

The ε≈4 condition is the provisional balance candidate. Its higher Recall is accompanied by higher FPR and lower PR-AUC than the non-private model, so it is not yet an established improvement or optimum.

Overall membership leakage remained near chance for every condition. All shadow-selected overall MIA AUC confidence intervals include 0.5, and no paired overall comparison supports measured leakage reduction. Rare-group reductions are exploratory only because the group has 208 evaluated records and multiple comparisons were made.

## Experiment 06 acceptance

The supplied five-seed bundle passed an independent evidence audit. See
[the acceptance review](report/experiment06_acceptance.md) for exact values and claim boundaries.
The small epsilon-4 Recall gain is uncertain; false alarms increase and average precision falls.
Paired MIA AUC comparisons do not support measured leakage reduction. Preserve the small
exploratory positive epsilon-2 label-aware advantage difference.

## Experiment 08 acceptance

The complete bundle passed checksum, table, interval, matched-seed, distribution, and figure
review. See [the final-analysis review](report/experiment08_acceptance.md). Experiment 08 is the
accepted endpoint for the NSL-KDD analysis. Epsilon about 8 remains single-seed context. The
optional Experiment 07 comparator is skipped.

## Current gate — compact external validity

Freeze a constrained UNSW-NB15 protocol before creating Experiment 09. Use only non-private,
epsilon about 4 as the utility-favoured tested DP setting, and epsilon about 2 as the strongest
tested privacy setting. Preserve the threat-model labels and reporting boundaries where the
dataset permits. Do not add a new privacy-budget sweep, architecture search, or broad
multi-dataset replication.

## Later phases

1. Write and approve the compact UNSW-NB15 protocol.
2. Run the constrained external-validity notebook and review its evidence.
3. Complete full-text related-work verification before novelty claims.
4. Draft the paper with conditional DP scope, frozen-attacker limitations and uncertainty explicit.

## Scope restrictions

Do not add federated learning, extra primary datasets, transformers, adversarial evasion, new privacy mechanisms, or broad model comparisons to the current study.
