# Experiment 09 interpretation boundary

This file is generated from a single target-training seed on UNSW-NB15.
It is supplementary external evidence, not a new optimisation study.

## Final IDS utility (validation-selected threshold)

```text
  condition  actual_epsilon  threshold   recall      fnr       f1      fpr   pr_auc
non_private             NaN       0.24 0.998831 0.001169 0.853572 0.418432 0.981609
   dp_eps_4        3.995481       0.02 0.999846 0.000154 0.852478 0.423784 0.968490
   dp_eps_2        1.995670       0.02 0.999890 0.000110 0.852436 0.424000 0.967663
```

## Overall membership-inference results

```text
  condition         threat_model        attack_model  mia_auc  mia_auc_ci_low  mia_auc_ci_high  mia_advantage
non_private score_only_black_box logistic_regression 0.499363        0.493715         0.505200       0.006559
non_private    label_aware_audit      loss_threshold 0.504553        0.498349         0.510101       0.013346
   dp_eps_4 score_only_black_box logistic_regression 0.500772        0.494636         0.506606       0.009182
   dp_eps_4    label_aware_audit      loss_threshold 0.504064        0.498273         0.509983       0.009353
   dp_eps_2 score_only_black_box logistic_regression 0.500000        0.500000         0.500000       0.000000
   dp_eps_2    label_aware_audit      loss_threshold 0.504033        0.497777         0.509767       0.009068
```

## Required claim boundaries

- Do not call epsilon 4 optimal.
- Do not generalise stability from one target-training seed.
- Do not claim measured leakage reduction unless a paired DP-minus-non-private interval is entirely below zero.
- Keep formal DP distinct from empirical MIA performance.
- State that DP applies to optimisation conditional on fixed preprocessing.