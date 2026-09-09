# Experiment 08 final-analysis evidence

This directory is the publication-ready repository snapshot of the accepted Experiment 08
output. The canonical complete bundle remains `experiment08_evidence.zip` in the project Drive.

## Evidence identity

- Bundle SHA-256: `9eabc696aac5020598dc85cce2f445ad0decf97a8bf8bb10cff19d0d4bb6113d`
- Status in `final_analysis_manifest.json`: `COMPLETE`
- Source Experiment 06 manifest SHA-256:
  `f1d93ba4362ebe9308fd7e47bcf111f90a9c8d2e8ebd7e3691e5f1686a16b570`
- The manifest declares zero new training runs, threshold searches, or fitted attacks.

The repository snapshot contains all final tables, captions, interpretation, and PNG/PDF
figures. It intentionally omits only:

```text
plot_data/member_nonmember_distribution_cdf.csv
```

That file contains 66,138 plotted ECDF points and remains in the complete Drive ZIP. Its
SHA-256 is `c0143fdbbda4d95d8e39984d1cb63b09e18082fc5f820385bc311e1ff638dda6`,
which is also recorded in the final manifest. Raw score caches, fitted models, and the duplicate
ZIP are not committed.

Run the bundle audit with:

```bash
python scripts/audit_experiment08.py /path/to/experiment08_evidence.zip \
  /path/to/experiment06_evidence.zip
```

See [`report/experiment08_acceptance.md`](../../report/experiment08_acceptance.md) for the
scientific decision and claim boundaries.
