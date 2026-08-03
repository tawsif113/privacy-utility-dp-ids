# Research Roadmap

## Working title

**Privacy–Utility Auditing of DP-SGD for ML-Based Network Intrusion Detection**

The title is justified only after formal DP-SGD is implemented with valid privacy accounting.

## Core research question

Can formal DP-SGD reduce measurable training-membership leakage in a tabular IDS model while retaining acceptable detection utility, especially Recall and False Negative Rate?

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

1. **Experiment 01 — Baseline IDS comparison:** trained the baseline models and tuned the IDS decision threshold using validation data only.
2. **Experiments 02–03 — MIA-ready baseline and audit:** locked the 70/10/20 split, trained the target MLP, and completed a five-shadow, shadow-disjoint membership-inference audit with manifests, confidence intervals, and low-FPR metrics.
3. **Experiment 04 — DP-SGD feasibility:** established non-private PyTorch parity, verified Opacus compatibility, and completed a single formal DP-SGD smoke test. The accepted run reports actual $\epsilon \approx 7.9986$ at $\delta = 1.134 \times 10^{-5}$. This is feasibility evidence, not a privacy–utility sweep.

## Current accepted conclusion

Under the specified score-only and label-aware shadow-calibrated attacks, measurable overall membership leakage from the non-private MLP was weak and its uncertainty interval included chance-level performance. This does not prove that the model is private. Formal differential-privacy accounting and empirical attack resistance are treated as separate forms of evidence.

## Current gate

### Experiment 05 — DP-SGD privacy–utility sweep

The implementation is ready, but the experiment is not complete until the sweep has been executed and its evidence has been reviewed.

For every privacy target:

1. Calibrate and record the requested and actual privacy budget at a fixed delta.
2. Train the target model and condition-matched shadow models with the same DP mechanism.
3. Measure IDS utility and membership-inference outcomes under the locked protocol.
4. Save manifests, accounting parameters, result tables, diagnostics, and paired uncertainty estimates.

### Acceptance gate

Do not mark Experiment 05 complete until:

- every DP target has a reproducible actual epsilon at the fixed delta;
- every target and shadow condition uses the documented matching procedure;
- the committed CSVs and manifests agree with the notebook outputs;
- utility, MIA, and uncertainty results have passed the repository's review checks.

## Next phases

1. Review and accept Experiment 05.
2. Run **Experiment 06 — repeated-run stability analysis**.
3. Complete **Experiment 08 — privacy–utility frontier and final analysis**.
4. Add stronger attacks or a compact external comparator only if the accepted results justify them.

## Scope restrictions

Do not add federated learning, extra datasets, transformers, adversarial evasion, new privacy mechanisms, or broad model comparisons to the current study unless a documented research question requires them.
