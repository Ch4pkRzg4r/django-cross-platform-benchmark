# Reproducibility

## Current controlling computational release

The current thesis computational release is **v360**. It preserves the byte-exact validated **v330 calibrated end-to-end pipeline** as the computational base and adds a small, transparent release layer for the independently adjudicated post-v359 corrections.

The byte-exact v330 source SHA-256 remains:

`d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574`

Reconstruct that validated base source with:

```bash
python analysis/materialize_v330_pipeline.py
```

The controlling v360 repository entry point is:

```bash
python analysis/run_v360_from_repo.py
```

By default this validates the frozen canonical design and writes the v360 release carriers. To execute the full validated v330 base first and then the v360 release layer, use:

```bash
python analysis/run_v360_from_repo.py --run-v330 \
  --docker-stats /path/to/docker_stats.zip \
  --figure-reference-dir /path/to/reference/thesis_figures
```

The release-layer implementation is `analysis/v360_release_corrections.py`. Its release files are staged and validated before publication; the manifest hashes an explicit output list and does not hash itself or unrelated stale files.

## Why v360 exists

Independent second adjudication identified one reproducibility-layer estimand mismatch in the historical v330 appendix carrier writer. The thesis defines p99/p50 tail inflation as the **median of run-level ratios**:

`median_r(latency_p99_r / latency_p50_r)`

The historical v330 appendix carrier writer instead emitted the **ratio of cell medians**:

`median_r(latency_p99_r) / median_r(latency_p50_r)`

Those are not the same operator. The printed thesis Table E.3 already used the intended median-of-run-ratios estimand; v360 therefore does **not** alter the frozen canonical dataset or the printed primary inference. It generates a corrected 28-cell tail-ratio carrier directly from run-level data and records the historical operator as superseded for that carrier only.

v360 also emits transparent carriers for:

- Figure 4.1 median-p95 coordinates, regenerated directly from the 28 canonical cells;
- completed-iteration shortfall relative to scenario-specific planned starts, explicitly separated from `dropped_iterations` and from an actual-start census;
- Figure 4.13 within-scenario rank profiles with exact stored-precision tie handling.

## Frozen dataset and main inference

The thesis-frozen canonical dataset remains 280 × 39 with SHA-256:

`710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7`

The validated v330 base reproduces the controlling statistical analysis:

- 28 balanced platform-scenario cells, 10 retained replications each;
- 20 scenario-stratified Kruskal-Wallis tests;
- 84 p95 Dunn comparisons with Holm adjustment within each scenario's 21-pair family;
- 23 significant p95 pairwise contrasts in the frozen data;
- Cliff's delta and rank-based eta-squared;
- 140 percentile-bootstrap intervals using 10,000 resamples and base seed 20260603;
- Chapter-4 Tables 4.1-4.16 under the full controlled evidence inputs.

The superseded cross-scenario Friedman/Wilcoxon H4 analysis is **not part of the current controlling analysis**.

## v360 release carriers

A normal v360 release check writes into `.v360-run/release/`:

- `v360_tail_ratio_cells.csv`
- `v360_figure4_1_p95_cells.csv`
- `v360_completed_iteration_shortfall.csv`
- `v360_figure4_13_rank_carrier.csv`
- `v360_release_manifest.json`

The release manifest records the canonical hash, design cardinality, estimand definitions, shortfall counts, explicit output hashes and the repository commit when Git metadata are available. Repeated successful runs must leave every listed output hash verifiable; the manifest itself is deliberately excluded from its own output-hash list.

## Scenario-D phase carrier

`data/supplementary/timeseries_burst_recovery.csv` is the retained replication-median per-second burst carrier. The thesis phase definition is baseline `60 <= tau <= 300`, peak `360 <= tau < 960`, and post-ramp `tau >= 1020`. The published peak-window achieved-rate value is a data-derived median of the retained per-second RPS curve in the half-open peak window; the frozen carrier yields 40 RPS for all seven paths. A literal `40` in the byte-exact historical v330 writer is provenance, not the current definition of the estimand.

## Full exact thesis-mirror prerequisites

GitHub intentionally does not duplicate the complete 120-run Docker telemetry archive as ordinary Git content. Exact Table 4.11 reproduction therefore still requires the controlled `docker_stats.zip` evidence archive.

The exact frozen-thesis regression additionally uses the controlled final-thesis publication-reference assets. These are maintained in the evidence package and are not silently substituted when input data change.

## Data-driven safeguard

The validated v330 pipeline was tested on a disposable altered-data copy. Changing compatible source values changed the corresponding table value, Kruskal-Wallis result and dynamic figure output. Exact frozen-thesis publication assets were not emitted on altered input. The analysis is therefore not a hard-coded output replay.

The v360 release layer also derives its carriers from run-level canonical values; it does not read printed thesis values as calculation inputs.

## Historical campaign boundary

Computational rerunning from retained analytical evidence is supported. Re-execution of the historical managed-cloud campaign is not claimed as bit-for-bit reproducible: provider-internal state, historical managed-platform state and some external transients are not observable or controllable after the experiment.

No benchmark-time, continuity-bridged executable identity manifest is retained for the load generator; a **later current-only capture** is available in `verification/k6_binary_identity.txt`. It must not be promoted to campaign-time binary proof.

## Raw archive integrity

The repository includes per-file integrity manifests for the retained raw k6 streams, run logs, Docker telemetry and archive parts under `data/raw-archive-manifests/`. The heavy raw evidence itself is retained in a controlled external archive because of size. No public raw-data URL is claimed until upload, verification and release approval are complete.
