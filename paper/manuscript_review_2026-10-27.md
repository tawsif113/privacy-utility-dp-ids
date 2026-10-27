# Manuscript methods and evidence review

**Decision:** proceed with manuscript revision; pause submission until the open items below are resolved.

**Review basis:** `ROADMAP_REVISED_V2.md` supplied with the research project, the accepted repository
snapshot `669d4bf4ec4c167ad94e5c04f8e3f7518c5cb7bc`, and accepted Experiments 06, 08, and 09.
The older roadmap's not-started statuses are superseded by the accepted experiment records;
its scope controls and claim boundaries still apply.

## Confirmed corrections

| Finding | Revision | Evidence |
|---|---|---|
| Abstract/RQ2 grouped label-aware access under black-box wording | Distinguish score-only black-box MIA from the true-label-aware audit | Experiment 05/06/09 threat-model configurations |
| Fixed attackers were not explained fully | State condition-specific attackers are reused across five target seeds, without retraining shadows | `results/repeated_runs/config.json`; Experiment 06 `build_selected_attack` |
| Calibration could be mistaken for record-disjoint data | State that shadow 505 is held out by model; all shadows reuse the same shadow pool | Experiment 05/09 `create_shadow_split` |
| Utility differences could be attributed solely to noise | Disclose shuffled non-private versus Poisson private sampling and clipping | Experiment 06 `create_train_loader` and `train_target_run` |
| `pr_auc` could be mistaken for trapezoidal area | Name the measure average precision and identify `average_precision_score` | Experiment 05/06/09 `calculate_ids_metrics` |
| UNSW preprocessing lacked reproducible detail | Add imputation rules, three categorical fields, exclusions, and 192 transformed inputs | `unsw_nb15_config.json`; `unsw_nb15_preprocessing_manifest.json` |
| Threshold search and ties were underspecified | Add 0.01–0.99 grid, F2/Recall sorting, and explicit UNSW lower-threshold tie-break | Experiment 06/09 `select_f2_threshold` |
| Sampling/accounting reporting was incomplete | Add actual target sample rates, nominal batch meaning, update schedule, noise, and per-model scope | `privacy_accounting_per_seed.csv`; `unsw_nb15_target_configs.csv` |
| Advantage/low-FPR metrics could imply target calibration | Distinguish retrospective target ROC summaries from shadow-calibrated balanced accuracy | Experiment 05/06/09 MIA metric functions |
| Main paper omitted some required attack metrics | Include AUC/advantage intervals, balanced accuracy, and low-FPR rates; add UNSW appendix | Final primary table and UNSW MIA table |
| Uncertainty descriptions mixed possible sources of variation | Separate five-seed t intervals, ordinary single-seed NSL bootstrap, and membership-stratified UNSW bootstrap | Experiment 05/06/09 statistical functions |
| Null differences could be read as equivalence | State no equivalence margin and no established equivalence/non-inferiority | Accepted paired intervals and Experiment 08 acceptance |
| Per-model epsilon could be read as a release-wide guarantee | Exclude joint model releases, data-dependent preprocessing, and the complete selection workflow | Accepted Experiment 08 claim boundaries |

## Confirmed decisions and rejected additions

- Retain binary MLP IDS, five-seed NSL-KDD primary evidence, and single-seed UNSW-NB15 supplement.
- Preserve the accepted CSV/JSON outputs and all reported experiment outcomes.
- Retain the negative overall MIA comparison and false-positive/AP costs; do not claim leakage
  elimination, an optimal epsilon, equivalence, end-to-end raw-data DP, or deployment readiness.
- Do not add models, datasets, budget sweeps, LiRA/RMIA, or a new privacy mechanism merely to
  obtain a stronger-looking result. Reopen experiments only for a specific justified blocker.
- Use the user's established full name as sole author. Affiliation and declarations remain
  unconfirmed; no supervisor, coauthor, or institutional affiliation is invented.
- Markdown is the editable manuscript source; generate LaTeX from it to prevent version drift.

## Verification performed and its limits

- `scripts/validate_evidence.py` passed for the committed evidence through Experiment 05.
- `scripts/validate_manuscript_evidence.py` independently recomputed 107 aggregate/paired summary
  rows from the committed per-seed tables and checked six manuscript tables against source CSVs.
- This review inspected notebook source, saved configurations, acceptance records, and aggregates.
  It did not rerun training, re-query original models, access the external full evidence bundles,
  or independently repeat the record bootstrap from raw predictions.
- The six delimited tables are checked automatically. Scientific prose and literature claims still
  require human review; the validator is not a proof of the complete paper's correctness.
- All 15 manuscript citation keys resolve to the existing bibliography. Markdown/LaTeX synchronization
  passed; the 13-page PDF compiled without LaTeX warnings or overfull boxes and was visually inspected.

## Open problems, assumptions, and risks

1. **Formal privacy wording:** before submission, explicitly reconcile the neighbor relation and
   numerical accountant assumptions with the pinned Opacus/PRV implementation. Preserve the
   fixed-preprocessing scope and justify the recorded delta choices of 1/N rather than silently
   changing them. This review verified recorded accounting inputs, not a new privacy proof.
2. **Literature and novelty:** the existing full-text evidence ledger remains the starting point.
   This pass did not repeat the full literature search or final publisher-metadata verification.
   Review the research gap against the chosen venue before claiming novelty.
3. **Author information:** confirm affiliation, correspondence details, funding, competing interests,
   acknowledgements, contribution statement, and any venue-required AI assistance disclosure.
4. **Reproducibility access:** compact evidence is public; model states and per-record outputs are
   referenced in external bundles. Decide on an accessible archival/data-availability statement.
5. **Operational and attack limitations:** there is no prespecified acceptable alert budget; the
   UNSW FPR is approximately 42%. Calibration shadows reuse records, train on fewer members,
   and the score-only primary attacker is limited. These limit claims, not automatically demand
   another experiment.
6. **Publication readiness:** venue, formatting limits, and final independent scientific review are
   outstanding. The paper remains an author-review draft.

## Next milestones

1. Review the revised contribution and Discussion against these claim boundaries.
2. Complete the formal-privacy wording check and the focused literature/metadata pass.
3. Confirm author declarations and select a suitable venue, then adapt the template and obtain
   independent research feedback where possible. A supervisor/coauthor is not a prerequisite.
4. Submit only after the scientific, evidence, metadata, and venue checks are complete.
