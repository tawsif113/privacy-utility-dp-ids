# Research Roadmap — Revised v2

## Working title

**Privacy–Utility Tradeoff in Differentially Private Machine Learning for Network Intrusion Detection**

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

## Completed

1. Archived baseline IDS comparison.
2. Locked the final 70/10/20 split.
3. Trained the MIA-ready target MLP.
4. Tuned IDS threshold using target validation only.
5. Completed a five-shadow, shadow-disjoint MIA audit.
6. Recorded manifests, model diagnostics, confidence intervals, and low-FPR metrics.

## Current accepted conclusion

Under the specified score-only and label-aware shadow-calibrated attacks, measurable overall membership leakage from the non-private MLP was weak. This does not prove the model is private.

## Next phase

### Experiment 04 — DP-SGD feasibility smoke test

1. Rebuild the target MLP in PyTorch.
2. Establish non-private PyTorch utility parity.
3. Ensure the architecture is Opacus-compatible.
4. Run one DP-SGD configuration.
5. Record delta, epsilon, noise multiplier, clipping norm, sample rate, batch size, epochs, optimizer, learning rate, and accountant.

### Gate before the full sweep

Do not start the full DP-SGD sweep until:

- the PyTorch non-private MLP has acceptable utility parity;
- Opacus reports a reproducible actual epsilon at a fixed delta;
- no privacy-accounting or incompatible-layer issue remains.

## Later phases

- Formal DP-SGD privacy–utility sweep
- Repeated-run stability analysis
- Stronger MIA only if justified by weak baseline leakage
- Compact external validation only after the NSL-KDD study is complete

## Scope restrictions

Do not add federated learning, extra datasets, transformers, adversarial evasion, new privacy mechanisms, or broad model comparisons unless a documented research question requires them.
