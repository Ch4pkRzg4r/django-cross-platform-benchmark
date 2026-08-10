# Reproducibility

## Current controlling computational analysis

The current controlling thesis analysis is the validated **v330 calibrated end-to-end pipeline**.

Byte-exact validated source SHA-256:

`d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574`

Reconstruct the validated source from the integrity-preserving repository payload with:

```bash
python analysis/materialize_v330_pipeline.py
```

A normal repository rerun is:

```bash
python analysis/run_v330_from_repo.py
```

This uses `data/canonical/master_runs.csv` plus the small supplementary carriers in `data/supplementary/`.

## What the frozen analysis reproduces

For the thesis-frozen canonical dataset (280 × 39; SHA-256 `710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7`), v330 reproduces the current controlling statistical analysis:

- 28 balanced platform–scenario cells, 10 retained replications each;
- 20 scenario-stratified Kruskal–Wallis tests;
- 84 p95 Dunn comparisons with Holm adjustment within each scenario's 21-pair family;
- 23 significant p95 pairwise contrasts in the frozen data;
- Cliff's delta and rank-based eta-squared;
- 140 percentile-bootstrap intervals using 10,000 resamples and base seed 20260603;
- current Chapter-4 Tables 4.1–4.16 under the full controlled evidence inputs;
- data-driven current Chapter-4 figure carriers.

The superseded cross-scenario Friedman/Wilcoxon H4 analysis is **not part of the current controlling v330 analysis**.

## Full exact thesis-mirror prerequisites

GitHub intentionally does not duplicate the complete 120-run Docker telemetry archive as ordinary Git content. Exact Table 4.11 reproduction therefore requires the controlled `docker_stats.zip` evidence archive:

```bash
python analysis/run_v330_from_repo.py --docker-stats /path/to/docker_stats.zip
```

The exact frozen-thesis regression additionally uses the controlled final-thesis reference assets. These are maintained in the evidence package and are not silently substituted when input data change.

## Data-driven safeguard

The validated pipeline was tested on a disposable altered-data copy. Changing compatible source values changed the corresponding table value, Kruskal–Wallis result and dynamic figure output. Exact frozen-thesis publication assets were not emitted on altered input. The analysis is therefore not a hard-coded output replay.

## Historical campaign boundary

Computational rerunning from retained analytical evidence is supported. Re-execution of the historical managed-cloud campaign is not claimed as bit-for-bit reproducible: provider-internal state, historical managed-platform state and some external transients are not observable or controllable after the experiment. The load generator identity record remains in `verification/k6_binary_identity.txt`.

## Raw archive integrity

The repository includes per-file integrity manifests for the retained raw k6 streams, run logs, Docker telemetry and archive parts under `data/raw-archive-manifests/`. The heavy raw evidence itself is retained in a controlled external archive because of size. No public raw-data URL is claimed until upload, verification and release approval are complete.
