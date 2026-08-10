# v330 calibrated analysis staging status

This branch stages the validated final-thesis analytical update while leaving `main` unchanged until the branch audit is complete.

## Frozen analytical input

- `master_runs.csv`: 280 rows × 39 source fields
- 7 configurations × 4 scenarios × 10 retained replications = 280 runs
- SHA-256: `710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7`

## Current controlling pipeline candidate

- Validated filename: `thesis_analysis_pipeline_v330_calibrated.py`
- SHA-256: `d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574`
- Byte-exact Git transport: `analysis/v330-payload/payload_01.b64` … `payload_05.b64`
- Integrity materializer: `analysis/materialize_v330_pipeline.py`
- Repository-aware runner: `analysis/run_v330_from_repo.py`

The materializer reconstructs the controlling source and refuses to write it if the SHA-256 differs from the validated value.

## Validated analytical result

The candidate was rerun on the author's Windows machine and the returned output bundle was independently checked before repository staging.

PASS:

- frozen input hash and balanced 28-cell design;
- 20 scenario-stratified Kruskal–Wallis tests;
- 84 p95 Dunn comparisons with Holm correction within each scenario's 21-pair family;
- 23 Holm-significant p95 contrasts;
- 140 percentile-bootstrap cell/outcome intervals;
- Tables 4.1–4.16 exact current-thesis cell text/order/rounding mirror;
- current Chapter-4 numerical figure carriers;
- 18 expected dynamic visual outputs;
- 18/18 exact final-thesis publication assets byte-identical in the controlled calibration package;
- changed-data mutation safeguard: altered input changed tables, inference and dynamic figures and did not emit frozen publication assets.

## Git-tracked current-thesis namespace now staged

`results/current-thesis/` now contains the authoritative current Table 4.1–4.16 CSV set, current figure map and the frozen-input verification/hash records. Earlier `results/tables/` and `results/figures/` paths are explicitly labelled as pre-v330 provenance instead of being silently overwritten.

A separate `MANIFEST_V330_UPDATE_SHA256.csv` records the validated analytical-update hashes while the earlier `MANIFEST_SHA256.csv` remains the immutable pre-v330 baseline snapshot.

## Controlled-evidence boundary

The frozen exact-thesis run still requires two controlled assets not duplicated as ordinary Git content:

1. the full 120-run Docker telemetry ZIP, needed for exact Table 4.11 regeneration; and
2. the 18 exact final-thesis reference figures, used only for byte-identity regression.

The multi-GB original per-run k6 JSON/CSV archive also remains outside ordinary Git history. GitHub contains its integrity/provenance manifests. No public raw-data URL is claimed until controlled upload, completeness checking and release approval are complete.

## Repository verification

`verification/verify_v330_repository_state.py` checks the Git-tracked v330 source payload/materialized hash, canonical dataset hash, v330 delta manifest, complete 16-table namespace and publication-figure hash registry. `.github/workflows/verify-v330.yml` stages the same repository-local check for GitHub Actions.

No CI PASS is claimed until GitHub records an actual workflow result.

## Merge policy

`main` remains untouched. Merge only after final branch-level verification and review of the PR diff. The heavy raw-evidence/Drive staging is a separate controlled-evidence step and must not be falsely represented as already uploaded.
