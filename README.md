# Django Cross-Platform Benchmark — MSc Thesis Research Artefacts

Research artefacts supporting the MSc thesis **“Benchmarking and Evaluation of Traditional Web Servers and Serverless Architectures for an E-Commerce System”** by **Chapk Rzgar Mohammed Abdalla**, College of Science, **University of Sulaimani** (2026).

**Canonical repository:** `Ch4pkRzg4r/django-cross-platform-benchmark`

> Repository status: **private thesis/examination artefact repository**. Public release is intentionally deferred pending supervisor/college approval.

## Study scope

One Django 5.1.2 e-commerce application was evaluated across seven deployment configurations — Apache + mod_wsgi, Nginx + uWSGI, Gunicorn, IIS + Waitress, Azure Container Apps, Koyeb and Fly.io — under four open-arrival k6 workload scenarios. Ten retained replications were analysed per platform–scenario cell: **7 × 4 × 10 = 280 retained runs**. The application used PostgreSQL 17 with PgBouncer.

The frozen canonical analytical dataset is:

`data/canonical/master_runs.csv` — **280 rows × 39 source fields**  
SHA-256: `710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7`

## Current controlling analysis — v330

The current thesis-matched end-to-end analysis is **v330**. It is data-driven: compatible changes to the analytical input propagate to the statistical results, tables and dynamically generated figures.

Validated v330 source SHA-256:

`d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574`

The byte-exact source is carried in `analysis/v330-payload/` and reconstructed with an integrity check by:

```bash
python analysis/materialize_v330_pipeline.py
```

For a normal repository rerun using the canonical dataset plus the small supplementary carriers:

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows:     .venv\Scripts\activate
pip install -r environment/requirements.txt
python analysis/run_v330_from_repo.py
```

The runner assembles the repository layout into a disposable `.v330-run/` data directory, materialises the byte-exact controlling source, and executes the current pipeline.

### Full exact thesis-mirror run

The exact Table 4.11 resource summary requires the retained **120-run Docker telemetry archive**, which is deliberately not duplicated as ordinary Git content. For a full controlled run, supply the telemetry ZIP from the evidence archive:

```bash
python analysis/run_v330_from_repo.py --docker-stats /path/to/docker_stats.zip
```

Exact regression against the final thesis also uses the controlled v329 reference assets. Those reference assets and the heavy raw campaign archive are maintained in the controlled evidence package rather than claimed as standalone GitHub-only evidence.

## Current analytical contract

For the frozen thesis input, the validated v330 pipeline reproduces:

- **28** platform–scenario cells with exactly **10** retained runs per cell;
- **20** scenario-stratified Kruskal–Wallis tests: 5 declared outcomes × 4 scenarios;
- **84** p95 Dunn pairwise comparisons: 21 per scenario, with Holm adjustment within each scenario family;
- **23** Holm-significant p95 contrasts in the frozen thesis data;
- Cliff’s delta effect sizes and rank-based eta-squared;
- **140** percentile-bootstrap intervals: 28 cells × 5 outcomes, 10,000 resamples with fixed base seed `20260603`;
- exact current-thesis **Tables 4.1–4.16** for the frozen controlled input;
- dynamic current Chapter-4 figure carriers for Figures 4.1–4.12 and 4.13a–f.

The current controlling analysis **does not use the superseded cross-scenario Friedman/Wilcoxon H4 test**. Earlier analytical scripts are retained only for provenance and historical auditability.

## Repository contents

- `benchmark/` — benchmark-time orchestrator, four k6 workload scripts and parser.
- `application/` — as-built Django application capture, with credential-templated public derivatives where required.
- `configuration/` — retained platform/scenario/deployment configuration evidence.
- `analysis/` — current v330 materialiser/runner plus retained earlier analytical components and historical provenance.
- `data/canonical/` — frozen 280×39 dataset and dictionary.
- `data/supplementary/` — warm-up, burst-recovery and post-idle inputs that are small enough for Git.
- `data/raw-archive-manifests/` — per-file integrity manifests for the retained raw campaign and resource evidence.
- `results/tables/` — Chapter-4 machine-readable table sources.
- `results/figures/` — thesis figure assets / figure mapping; current v330 figure-map synchronization is tracked with the final analysis update.
- `verification/` — integrity, configuration-truth and v330 validation records.
- `environment/` — dependency/runtime records.

## Evidence and reproducibility boundary

This repository supports inspection of the benchmark implementation, canonical data, analytical logic, integrity records and deterministic computational rerunning of the retained analysis. It does **not** claim that a historical managed-cloud campaign can be recreated bit-for-bit today: provider-internal state, historical platform state and some external transients are not controllable or observable after the fact.

The full original per-run raw k6 JSON/CSV evidence and the complete resource-telemetry archive are retained as controlled evidence outside ordinary Git history because of their size. GitHub stores their integrity/provenance manifests. No public raw-data URL is claimed until the controlled archive has been uploaded, checked and approved for release.

## Data-driven behaviour

v330 was also tested on a disposable changed-data copy. Altering retained source values changed the corresponding Chapter-4 table values, Kruskal–Wallis result and dynamic Figure 4.1. Exact frozen-thesis publication assets were not emitted for the changed dataset. This guards against a hard-coded thesis-output pipeline.

## Citation and licensing

Please cite the thesis and repository; machine-readable citation metadata is in `CITATION.cff`.

Original author code/scripts are under the repository code licence; author-owned data/documentation/table/figure artefacts are under the stated data licence. Third-party software, provider names and trademarks are not relicensed. See `LICENSING.md`.
