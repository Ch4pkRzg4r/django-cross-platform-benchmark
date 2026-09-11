# Reproducibility

## Current controlling computational release

The **document candidate is v366**, while the current controlling **computational repository release remains v360**. v360 preserves the byte-exact validated **v330 calibrated end-to-end pipeline** as the computational base and adds a small, transparent release layer for independently adjudicated release-carrier corrections. The v366 document/repository closure does not renumber or replace that computational stack.

The byte-exact v330 source SHA-256 remains:

`d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574`

Reconstruct that validated base source with:

```bash
python analysis/materialize_v330_pipeline.py
```

The controlling repository entry point is:

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

Those are not the same operator. The printed thesis used the intended median-of-run-ratios estimand; v360 therefore does **not** alter the frozen canonical dataset or the printed primary inference. It generates a corrected 28-cell tail-ratio carrier directly from run-level data and records the historical operator as superseded for that carrier only.

v360 also emits transparent **historical-namespace** carriers for:

- a 28-cell median-p95 coordinate carrier;
- completed-iteration shortfall relative to scenario-specific planned starts, explicitly separated from `dropped_iterations` and from an actual-start census;
- the historical within-scenario rank/tie carrier formerly labelled Figure 4.13 in the wrapper namespace.

These carrier filenames/numbers are computational provenance; they are **not the current v366 thesis figure numbering**. The current document crosswalk is `results/current-thesis/figure_map_v366.csv` and ends at Figure 4.8 (six continued panels).

## Frozen dataset and main inference

The thesis-frozen canonical dataset remains 280 × 39 with SHA-256:

`710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7`

The validated v330 base reproduces the controlling statistical analysis:

- 28 balanced platform-scenario cells, 10 retained replications each;
- 20 scenario-stratified Kruskal-Wallis tests;
- 84 p95 Dunn comparisons with Holm adjustment within each scenario's 21-pair family;
- 23 significant p95 pairwise contrasts in the frozen data;
- Cliff's delta and rank-based eta-squared;
- 140 percentile-bootstrap intervals using 10,000 resamples under the controlling deterministic seed schedule rooted at 20260603;
- validated Chapter-4 numerical/table carriers under the full controlled analytical inputs.

The superseded cross-scenario Friedman/Wilcoxon H4 analysis is **not part of the current controlling analysis**.

## v360 release carriers

A normal v360 release check writes into `.v360-run/release/`:

- `v360_tail_ratio_cells.csv`
- `v360_figure4_1_p95_cells.csv`
- `v360_completed_iteration_shortfall.csv`
- `v360_figure4_13_rank_carrier.csv`
- `v360_release_manifest.json`

The historical filenames are retained for provenance. The release manifest records the canonical hash, design cardinality, estimand definitions, shortfall counts, explicit output hashes and the repository commit when Git metadata are available. Repeated successful runs must leave every listed output hash verifiable; the manifest itself is deliberately excluded from its own output-hash list.

## Scenario and rate semantics

Final workload-script semantics are documented in `configuration/SCENARIO_AUTHORITY_V366.md`.

- Scenario C uses 10 iterations/s with three GET requests per iteration, so request-rate fields are not iteration-rate fields.
- Scenario D is staged/ramping (5→40→5 iterations/s); the canonical scalar `target_rps=10` is historical metadata and is not the burst schedule authority.

`data/supplementary/timeseries_burst_recovery.csv` is the retained replication-median per-second burst carrier. The thesis phase definition is baseline `60 <= tau <= 300`, peak `360 <= tau < 960`, and post-ramp `tau >= 1020`. The published peak-window achieved-rate value is data-derived from the retained per-second curve; the frozen carrier yields 40 requests/s for all seven paths. A literal `40` in byte-exact historical code is provenance, not the definition of the estimand.

## Full exact thesis-mirror prerequisites

GitHub intentionally does not duplicate the complete 120-run Docker telemetry archive as ordinary Git content. Exact reproduction of the scoped Linux resource summary therefore still requires the controlled `docker_stats.zip` evidence archive.

The historical v330 wrapper also contains an 18-raster publication-copy regression dependency. Those exact historical target rasters were not all recovered in the independently audited submission evidence. Current v366 embedded figures are verified against the actual v366 document and are **not** silently substituted as byte-identical historical targets.

## Data-driven safeguard

The validated v330 pipeline was tested on a disposable altered-data copy. Changing compatible source values changed the corresponding table value, Kruskal-Wallis result and dynamic figure output. Exact frozen publication assets were not emitted on altered input. The analysis is therefore not a hard-coded output replay.

The v360 release layer also derives its carriers from run-level canonical values; it does not read printed thesis values as calculation inputs.

## Historical campaign boundary

Computational rerunning from retained analytical evidence is supported. Re-execution of the historical managed-cloud campaign is not claimed as bit-for-bit reproducible: provider-internal state, historical managed-platform state and some external transients are not observable or controllable after the experiment.

No benchmark-time, continuity-bridged executable identity manifest is retained for the load generator; a **later current-only capture** is available in `verification/k6_binary_identity.txt`. It must not be promoted to campaign-time binary proof.

The Nginx/uWSGI retained configuration files also contain a concrete historical/current conflict (TCP 4×2 INI versus UNIX-socket/nominal 2×4 descriptions). The prospective consistent rerun recipe is under `configuration/reproduction/nginx-uwsgi-v366/`; it is not retroactive proof of the campaign-time variant.

## Raw archive integrity and current availability

The repository includes expected per-file integrity manifests for raw k6 streams, run logs, Docker telemetry and historical archive parts under `data/raw-archive-manifests/`. **A manifest is an identity/checking record, not proof that the corresponding bytes are currently available.**

Independent recovery of the raw archives supplied with the v365 audit established **73 complete canonical JSON/CSV run pairs; 207 canonical run pairs were unavailable** in the supplied submission evidence. The four supplied raw ZIPs were truncated; complete-prefix members that passed structural/hash checks reconciled with their corresponding canonical rows. Full raw-to-canonical reconstruction of all 280 retained runs therefore cannot be certified from the currently supplied raw bytes.

See `data/raw-archive-manifests/AVAILABILITY_AND_RECONSTRUCTION.md` for the precise current state and recovery protocol.

## Current document/repository closure

`THESIS_V366_ALIGNMENT.md` records the document-facing v366 authority, current figure crosswalk, PERMDISP provenance qualification, public/private fixture boundary, raw-availability boundary and Nginx prospective reproduction rule. These are provenance/reproduction corrections; they do not change the frozen primary numerical results.
