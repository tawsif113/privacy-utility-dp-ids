# Data

The raw NSL-KDD files are intentionally excluded from Git.

Expected external files:

```text
KDDTrain+.txt
KDDTest+.txt
```

The accepted final experiment used these SHA-256 hashes:

```text
KDDTrain+: 1b86d2f957b33082081bba410fe129b475efebcc13c9014c3f447c8271aadf95
KDDTest+:  fa46b0935342616aa83b7c2578db355b6a7aaabbc492248172c7a1e8b7ab8f84
```

Locked split sizes:

```text
target_train:      88,181
target_validation: 12,597
shadow_pool:       25,195
KDDTest+:          22,544
```

Split index arrays remain in Google Drive because `.npy` artifacts are excluded from Git. Their hashes and generation rules must be preserved in manifests.

## Experiment 09 — UNSW-NB15 external validation

Experiment 09 uses these frozen official predefined partitions:

```text
/content/drive/MyDrive/ML-DP-NID/data/unsw_nb15/UNSW_NB15_training-set.csv
/content/drive/MyDrive/ML-DP-NID/data/unsw_nb15/UNSW_NB15_testing-set.csv
```

```text
UNSW_NB15_training-set.csv
bytes:   32,293,018
SHA-256: bec7dd5ec88dc2a0ccc7a07879d338395ed7421750f675fd0339e07dfe0648fa

UNSW_NB15_testing-set.csv
bytes:   15,380,800
SHA-256: 734fe6642edf758f7c94d7d9149426b49d202fe8e7bf0bef47392489c3c0a559
```

The Experiment 09 notebook requires the standard 175,341-row training partition and 82,332-row
testing partition. If either file is absent, the notebook downloads it from the frozen mirror
revision `6f5f54594dfc80c84264aec4c7cc3d9b162f1e2f`; acquisition location does not change the
frozen file identity. It verifies the exact byte sizes and hashes before reading data or starting
training. Existing mismatched files are not overwritten. Raw UNSW-NB15 files are not placed in
Git or copied into the evidence ZIP.
