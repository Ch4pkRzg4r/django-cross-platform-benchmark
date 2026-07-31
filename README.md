# Django Cross-Platform Benchmark — Research Artefact Repository

Research artefacts supporting the MSc thesis **“Benchmarking and Evaluation of Traditional Web Servers and Serverless Architectures for an E-Commerce System”** by **Chapk Rzgar Mohammed Abdalla**, College of Science, **University of Sulaimani** (2026).

## Scope
A controlled cross-platform benchmark of one Django 5.1.2 e-commerce application deployed on **seven configurations** — Apache + mod_wsgi, Nginx + uWSGI, Gunicorn, Azure Container Apps, Koyeb, Fly.io, and IIS + Waitress (Windows) — under **four open-model k6 workload scenarios** (steady browse, mixed browse/admin GET traffic, a GET-only cart sequence, and a burst profile), with **ten retained replications per platform–scenario cell: 7 × 4 × 10 = 280 measured runs**, backed by PostgreSQL 17 with PgBouncer.

## Contents
`benchmark/` — the final orchestrator and the four campaign k6 scenario scripts plus the output parser (byte-identical to the campaign-time integrity manifests) · `application/` — the as-built Django application capture with credential-templated `.PUBLIC` derivatives · `configuration/` — deployment and platform/scenario configuration (secrets templated) · `analysis/` — the corrected unified analysis wrapper, validation/EDA phases, both analyzers and the controlling Chapter-4 exhibit pipeline, each at its thesis-recorded SHA-256 (`analysis/historical-provenance/` holds a superseded phase retained for provenance) · `data/canonical/` — the frozen 280 × 39 analytical dataset with a data dictionary · `data/supplementary/` — cold-start, burst-recovery and warm-up inputs · `data/raw-archive-manifests/` — complete per-file SHA-256 manifests for the retained raw campaign (560 streams, 280 run logs, 120 resource-usage files, archive parts) · `results/tables/` — full-precision machine-readable sources of the printed Chapter-4 tables · `results/figures/` — the exact thesis figures with `results/figures/figure_map.csv` · `environment/` — dependency and runtime records · `verification/` — integrity and configuration truth summaries · `documentation/` — evidence-state notes.

## Quick start (analysis)
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r environment/requirements.txt
python analysis/run_analysis.py --data data/canonical/master_runs.csv
sha256sum -c <(tail -n +2 MANIFEST_SHA256.csv | awk -F, '{print $3"  "$1}')   # integrity check
```

## Evidence and reproducibility boundaries
These artefacts support inspection and **limited computational rerunning** of the statistical analysis from the retained canonical data (fixed bootstrap base seed 20260603; scenario-stratified Kruskal–Wallis, Dunn–Holm, Cliff’s delta). They do **not** enable re-execution of the historical cloud campaign: provider-internal behaviour, historical managed-platform state and some benchmark-time transients are unobservable or were not recorded, exactly as bounded in the thesis (Chapter 3). The load generator is identified by version and a continuity-bridged SHA-256 (`verification/k6_binary_identity.txt`). Full statements: `REPRODUCIBILITY.md`, `ARTEFACT_PROVENANCE.md`.

## Data availability
The canonical dataset, supplementary inputs, full-precision table sources and all integrity manifests are in this repository. The multi-gigabyte raw event archives are **not hosted here**; they are identified file-by-file by SHA-256 in `data/raw-archive-manifests/` and retained as described in `DATA_AVAILABILITY.md`.

## Citation
Please cite the thesis and this repository; machine-readable metadata is in `CITATION.cff`.

## Licences
Original code and scripts: MIT. Author-owned datasets, documentation, tables and figures: CC BY 4.0. Third-party software, provider names and trademarks are not relicensed. Scope details: `LICENSING.md`.
