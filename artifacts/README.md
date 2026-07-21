# External artifacts

Large model and preprocessing artifacts are stored outside Git, currently in Google Drive.

Canonical Experiment 02–03 artifacts:

```text
artifacts/models/target_mlp.joblib
artifacts/preprocessor/target_mlp_preprocessor.joblib
```

Their originating paths and protocol metadata are recorded in `manifests/baseline_mia_combined_manifest.json`.

Do not commit `.joblib`, `.pkl`, `.pt`, `.pth`, `.npy`, or large per-sample score files to this repository.
