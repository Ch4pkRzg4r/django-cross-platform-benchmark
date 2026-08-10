# v330 calibrated analysis candidate

This branch stages the final calibrated end-to-end analysis pipeline validated against the current thesis Chapter 4.

## Frozen analytical input

- `master_runs.csv`: 280 rows × 39 source fields
- 7 configurations × 4 scenarios × 10 retained replications = 280 runs
- SHA-256: `710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7`

## Calibrated pipeline candidate

- Local validated filename: `thesis_analysis_pipeline_v330_calibrated.py`
- SHA-256: `d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574`
- Purpose: data → validation/EDA → current Chapter-3 inferential workflow → Tables 4.1–4.16 → Figures 4.1–4.12 + Figure 4.13a–f → manifests/checks.

## Independent run status

The candidate was rerun on the author's Windows machine and the returned output bundle was independently rechecked before staging this branch.

PASS items:

- exact frozen input hash
- 28 balanced platform–scenario cells, 10 replications each
- 20 scenario-stratified Kruskal–Wallis tests
- 84 Dunn comparisons with Holm correction within each 21-pair scenario family
- 23 Holm-significant p95 contrasts
- 140 bootstrap cell-outcome intervals (28 × 5; 10,000 resamples)
- Tables 4.1–4.16 exact cell text/order/rounding mirror for the frozen thesis input
- current Chapter-4 numerical carriers reproduce the thesis
- 18 expected current visual outputs exist
- 18 exact published thesis figure assets passed byte-identity checking in the validated package
- changed-data mutation test confirmed that compatible input changes propagate to tables, inference and dynamic figures

## Important evidence boundary

The exact published thesis raster figures are archival publication assets. Dynamic figures are regenerated from the supplied analytical data. Exact frozen publication assets must not be emitted as if they were newly generated results when the analytical input differs from the frozen thesis dataset.

## Update policy

The existing `main` branch is not modified until this staging branch has the controlling v330 script, documentation/index updates, integrity manifest updates and final branch-level verification. Historical code remains recoverable through Git history and explicit historical-provenance notes.
