# Reproducibility

## Current document alignment: 2 October 2026

The current Word set and source identities are recorded in `THESIS_2026-10-02_ALIGNMENT.md` and `documentation/thesis_alignment_2026-10-02.json`. The canonical 280×39 data and byte-exact v330 statistical base are unchanged.

```bash
python -m pip install -r environment/requirements-analysis-v330.txt
python analysis/run_current_thesis.py
python verification/verify_current_thesis.py
```

Install Nimbus Roman (URW Base 35 fonts) to reproduce the typography of Figures 4.4 and 4.9. Font substitution changes rendered pixels without changing the data. The recorded local pixel comparison uses the installed Nimbus Roman font and the package versions in the release manifest; cross-environment byte-identical PDF/raster output is not promised.

The default output is `.current-thesis-run/release/`. `--out-dir PATH` selects a different output directory. Each run stages its files and writes its manifest only after successful calculation and rendering. The output manifest hashes every generated carrier/figure but not itself.

1. `base_layers/`: unchanged v360 estimands and v367 strict H4/Figure 4.3 correction.
2. `supplement/`: 280-run and 28-cell completed-iteration shortfall, seven H4 descriptive flags and 28 scenario-specific conditional warm-cost values.
3. `delivery_figure/`: Figure 4.4 from the 280-run carrier.
4. `profile_panels/`: the 336-cell carrier and six Figure 4.9 panels (104 high/low markers).

These are descriptive additions to the existing analysis, not new independent experiments or a composite winner. Fixed cost-model prices are the thesis's historical assumptions, not current quotations. The strict H4 decision remains supported by two configurations and not by all seven. `verification/verify_current_thesis.py` compares regenerated carriers with retained reviewed carriers, checks canonical/source identity and verifies the output manifest. It does not claim a complete historical deployment rerun.

To execute the frozen v330 base before these layers, the unchanged controlled-input prerequisites still apply:

```bash
python analysis/run_current_thesis.py --run-v330 \
  --docker-stats /path/to/docker_stats.zip \
  --figure-reference-dir /path/to/reference/thesis_figures
```

This optional exact-mirror mode is not the default and was not rerun for the 1 or 2 October document wording corrections. The historical 18-figure raster gate belongs to the v330 namespace, not to current Figure 4.1–4.9. Reconstruct the unchanged base alone with `python analysis/materialize_v330_pipeline.py`; expected source SHA-256 is `d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574`.

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

These carrier filenames/numbers are computational provenance; they are **not the current thesis figure numbering**. The current document crosswalk is `results/current-thesis/figure_map_2026-10-01.csv` and ends at Figure 4.9(a–f).

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

The historical v330 wrapper also contains an 18-raster publication-copy regression dependency. Those exact historical target rasters were not all recovered in the independently audited submission evidence. The current embedded figures are verified against the controlling corrected Word document and are **not** silently substituted as byte-identical historical targets.

## Data-driven safeguard

The validated v330 pipeline was tested on a disposable altered-data copy. Changing compatible source values changed the corresponding table value, Kruskal-Wallis result and dynamic figure output. Exact frozen publication assets were not emitted on altered input. The analysis is therefore not a hard-coded output replay.

The v360 release layer also derives its carriers from run-level canonical values; it does not read printed thesis values as calculation inputs.

## Historical campaign boundary

Computational rerunning from retained analytical evidence is supported. Re-execution of the historical managed-cloud campaign is not claimed as bit-for-bit reproducible: provider-internal state, historical managed-platform state and some external transients are not observable or controllable after the experiment.

No benchmark-time, continuity-bridged executable identity manifest is retained for the load generator; a **later current-only capture** is available in `verification/k6_binary_identity.txt`. It must not be promoted to campaign-time binary proof.

The Nginx/uWSGI retained configuration files also contain a concrete historical/current conflict (TCP 4×2 INI versus UNIX-socket/nominal 2×4 descriptions). The prospective consistent rerun recipe is under `configuration/reproduction/nginx-uwsgi-v366/`; it is not retroactive proof of the campaign-time variant.

## Raw archive integrity and current availability

The complete retained raw k6 collection is stored in the author's [raw-data archive on Google Drive](https://drive.google.com/drive/folders/1jAqu_W0vK0bgscBe5DE6t67NCMf2Sfhd): **280 canonical JSON/CSV run pairs (560 files)**, distributed across five JSON and three CSV RAR volumes. GitHub contains the canonical analytical dataset and the integrity manifests under `data/raw-archive-manifests/`; the heavy raw archives are downloaded separately from Google Drive.

The integrity review checked the actual bytes of all eight volumes and all 560 files against the retained sizes and SHA-256 values and reconciled the complete 7×4×10 retained design. The historical JSON parser reproduced all 32 JSON-derived fields for each retained run (8,960 comparisons); seven identity/metadata fields were retained from the canonical dataset and are not counted as independently re-derived JSON fields. Complete retained-run data do not establish a complete all-attempt ledger or reproduce unobserved historical provider state.

Google Drive permissions govern access. If the folder requires permission, request access from the author through Google Drive. See `data/raw-archive-manifests/AVAILABILITY_AND_RECONSTRUCTION.md` for the archive layout and verification procedure. This is the current raw-data statement; version-specific audit records retain their historical scope.

## Current document/repository alignment

`THESIS_2026-10-02_ALIGNMENT.md` is the current alignment record. The v366/v367/v368 alignment documents and SHA manifests are immutable historical snapshots; run their version-wide manifests at the corresponding historical commits, not against later edited README files. They do not supersede the current raw-data statement or establish the current Word file's field structure. The current Word body uses static citations and links, not the live EndNote fields recorded for v368.

## v367 outputs and targeted verification

The default v367 output directory is `.v367-run/release/`; the unchanged v360 files remain in `.v360-run/release/`. `--out-dir /path` places both layers' explicitly named files in the requested directory.

- `v367_h4_descriptive.csv`: seven platform rows, A/B/C/D medians, three strict comparisons, current flag and historical-helper flag.
- `v367_figure4_3_goodput_gap.csv`: four unchanged family-gap values derived from the canonical data.
- `Figure_4_3_v367.png`, `.pdf`, `.svg`: regenerated 450×270 pt figure.
- `v367_release_manifest.json`: input identity, H4 decision, figure font check and explicit output hashes.

Verify the affected outputs with `python verification/verify_v367_release.py`. For an explicit output directory, pass the same `--out-dir` to generation and verification. The strict-rule check covers the ACA counterexample and equal-zero rejection; it does not rerun primary inference or bootstrap calculations.
