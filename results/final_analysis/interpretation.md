# Experiment 08 interpretation boundaries

- The accepted five-seed results support final analysis, not a confirmed epsilon optimum.
- At epsilon about 4, mean Recall is 0.71338 versus 0.70934 non-private. The paired Recall
  interval crosses zero. Do not claim a confirmed detection improvement or equivalence.
- Mean FPR is 0.08755 versus 0.05610; mean average precision is 0.89068 versus 0.93750.
  The corresponding unadjusted paired intervals indicate higher FPR and lower average precision.
- MIA AUCs are close to 0.5, but several conditional across-seed intervals exclude 0.5.
  Do not repeat the Experiment 05 statement that every AUC interval contains 0.5.
- Neither primary nor secondary paired AUC comparisons establish reduced leakage.
- Epsilon about 2 has a small positive label-aware advantage difference (about 0.00345;
  unadjusted 95% interval about [0.00068, 0.00621]). Disclose it as an exploratory result.
  Advantage maximizes TPR-FPR over target thresholds; it is not the shadow-fixed operating score.
- All inference is conditional on one fixed dataset split and frozen attackers. Seed intervals
  do not include evaluation-record sampling uncertainty, shadow retraining or dataset variation.
- Unadjusted intervals span many metrics. Small positive advantage or zero-width TPR intervals
  do not establish population leakage or its absence. Raw t interval bounds are preserved,
  even when they extend outside [0,1].
- Formal DP accounting is conditional on fixed non-private preprocessing, with secure_mode=False.
  Individual-run epsilon is not a composition bound for jointly releasing every trained model.
- Epsilon 4 was identified after inspecting the sweep; this is not independent held-out
  confirmation of configuration selection. No operational acceptability threshold is established.
- Experiment 05 subgroup findings are single-seed and exploratory, especially the Rare group
  of 208 records. No new subgroup significance claims are made here.
- Keep Experiment 07, additional datasets, new privacy mechanisms and stronger attack suites
  outside this notebook. Consider external validation only after reviewing these outputs.
