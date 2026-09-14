# Notebooks

## Canonical execution order

| Experiment | Notebook | Status |
| --- | --- | --- |
| 01 | `01_baseline_nsl_kdd_ids.ipynb` | Complete; compact canonical rerunnable version |
| 02–03 | `02_03_mia_ready_baseline_and_audit.ipynb` | Complete and accepted |
| 04 | `04_dp_sgd_feasibility_smoke_test.ipynb` | Complete and accepted; executed outputs and result tables are committed |
| 05 | `05_dp_sgd_privacy_utility_sweep.ipynb` | Complete and accepted as single-run evidence; outputs and result tables committed |
| 06 | `06_repeated_runs_stability.ipynb` | Complete and accepted; five-seed selected-condition evidence |
| 08 | `08_privacy_utility_frontier.ipynb` | Complete and accepted; executed final analysis |
| 09 | `09_unsw_nb15_external_validation.ipynb` | Protocol frozen; ready to run; evidence pending |

## Archived Experiment 01 record

`01_Baseline_IDS_+_validation_threshold_tuning.ipynb` is retained as the original executed, output-bearing record of Experiment 01. The lowercase `01_baseline_nsl_kdd_ids.ipynb` is the canonical rerunnable notebook linked from the root README.

Results in the archived notebook provide baseline IDS context only; they are not formal differential-privacy or membership-inference evidence.

Future notebooks should be added only when the corresponding experiment is actually created.

Do not use filename suffixes such as `clean`, `v2`, `(1)`, or `final_final` in the repository. Version history belongs in Git commits.


## Current next step: run Experiment 09

Experiment 08 is accepted; see `report/experiment08_acceptance.md`. Experiment 09 is now
created under the frozen compact UNSW-NB15 design: non-private, epsilon about 4, and epsilon
about 2 only. Put the two official UNSW-NB15 training/testing CSV files in the Drive path stated
in the notebook, run all cells, and preserve the completed evidence ZIP and executed notebook.
The optional Experiment 07 comparator remains skipped under the scope decision.
