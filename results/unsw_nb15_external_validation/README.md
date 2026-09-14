# Experiment 09 — accepted UNSW-NB15 external-validation evidence

This directory is the compact Git snapshot of the accepted Experiment 09 run. The experiment is
supplementary single-seed external evidence, not a new privacy-budget sweep or a generalisation
study.

## Canonical bundle

- Drive file: [`experiment09_evidence.zip`](https://drive.google.com/file/d/1ypTtwroESIy1R8quct0xvaJj1pUInnCL/view)
- Size: 12,693,915 bytes
- SHA-256 reported by the completed notebook:
  `9b40cd2decfe2ecb03feae64d9c37d99bcdc5fe88f2f82e6d84d7e9ed7783511`
- Protocol fingerprint:
  `a4908a4539a96761555845e400e8ad93cc2afa4650e93f88042d8ed15558196a`
- Executed notebook commit: `8e2922364427865f5cb863e86a6b455fa848dabb`

The complete bundle contains 27 files excluding `evidence_manifest.json`. All ten final gates are
true. See [`report/experiment09_acceptance.md`](../../report/experiment09_acceptance.md) for the
review decision, exact results, and claim boundaries.

## Key accepted results

| Condition | Actual epsilon | Recall | FNR | F1 | FPR | Average precision | Score-only MIA AUC | Label-aware MIA AUC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Non-private | — | 0.998831 | 0.001169 | 0.853572 | 0.418432 | 0.981609 | 0.499363 | 0.504553 |
| DP epsilon about 4 | 3.995481 | 0.999846 | 0.000154 | 0.852478 | 0.423784 | 0.968490 | 0.500772 | 0.504064 |
| DP epsilon about 2 | 1.995670 | 0.999890 | 0.000110 | 0.852436 | 0.424000 | 0.967663 | 0.500000 | 0.504033 |

IDS values use the F2 threshold selected on target-validation and then applied once to the official
UNSW-NB15 testing partition. The absolute FPR is high and must accompany the near-perfect Recall.
All overall MIA AUC intervals include chance.

## Included in Git

- dataset, split, preprocessing, protocol, run-status, and evidence manifests;
- target and shadow configurations;
- target training history and validation-threshold search;
- complete aggregate IDS, MIA, family-diagnostic, calibration, paired-difference, utility-
  difference, and warning tables;
- generated interpretation;
- all three figures in PNG and PDF.

## Retained only in the canonical Drive bundle

- `unsw_nb15_target_mia_features.csv`;
- `unsw_nb15_shadow_mia_features.csv`;
- `unsw_nb15_target_mia_sample_manifest.csv`;
- `provenance/unsw_nb15_split_indices.npz`;
- `provenance/target_preprocessor.joblib`;
- the duplicate evidence ZIP.

Their exact byte counts and SHA-256 hashes remain in `evidence_manifest.json`. Raw dataset files
and trained model states are excluded from both this snapshot and the evidence ZIP.
