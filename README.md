# Django Cross-Platform Benchmark — MSc Thesis Research Artefacts

Research artefacts supporting the MSc thesis **“Benchmarking and Evaluation of Traditional Web Servers and Serverless Architectures for an E-Commerce System”** by **Chapk Rzgar Mohammed Abdalla**, College of Science, **University of Sulaimani** (2026).

**Canonical repository:** `Ch4pkRzg4r/django-cross-platform-benchmark`

> Repository status: **private thesis/examination artefact repository**. Public release is intentionally deferred pending supervisor/college approval.

> Thesis-document alignment: the submission document reviewed for final QA is **v344**, while the controlling numerical/statistical analysis remains the validated **v330** pipeline. The v344 changes after the v330 analytical freeze are editorial/notation/labelling/redaction/document-QA corrections and do not change the frozen canonical data or numerical Chapter 4 results. See `THESIS_V344_ALIGNMENT.md`.

> Completeness boundary: this repository is complete for the declared canonical-data/analytical audit scope, but it is **not** represented as containing every historical raw byte or the entire runnable historical Django application tree. See `REPOSITORY_COMPLETENESS_AUDIT_V344.md`.

## Study scope

One Django 5.1.2 e-commerce application was evaluated across seven deployment configurations — Apache + mod_wsgi, Nginx + uWSGI, Gunicorn, IIS + Waitress, Azure Container Apps, Koyeb and Fly.io — under four open-arrival k6 workload scenarios. Ten retained replications were analysed per platform–scenario cell: **7 × 4 × 10 = 280 retained runs**. The application used PostgreSQL 17 with PgBouncer.

The frozen canonical analytical dataset is:

`data/canonical/master_runs.csv` — **280 rows × 39 source fields**  
SHA-256: `710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7`

## Current controlling analysis — v330

The current controlling numerical/statistical thesis analysis is the validated **v330 calibrated end-to-end pipeline**. It is data-driven: compatible changes to analytical input values propagate to the statistical results, tables and dynamically generated figures.

Validated v330 source SHA-256:

`d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574`

The byte-exact source is carried in `analysis/v330-payload/` and reconstructed with an integrity check by:

```bash
python analysis/materialize_v330_pipeline.py
```

Analysis dependencies are recorded in:

`environment/requirements-analysis-v330.txt`

## Running v330

Create/activate a Python environment, then:

```bash
pip install -r environment/requirements-analysis-v330.txt
```

### A. Frozen exact-thesis run

A full frozen-thesis mirror requires two controlled evidence inputs that are intentionally **not duplicated as ordinary Git content**:

1. the complete 120-run `docker_stats.zip` resource-telemetry archive, required for exact Table 4.11; and
2. the directory containing the 18 exact final-thesis publication reference figures, used only as a byte-identity regression oracle.

Run:

```bash
python analysis/run_v330_from_repo.py \
  --docker-stats /path/to/docker_stats.zip \
  --figure-reference-dir /path/to/reference/thesis_figures \
  --verify-against-v329
```

The runner constructs a disposable `.v330-run/` directory, copies the Git-tracked canonical/supplementary analytical carriers, copies the v330 analytical Table 4.1–4.16 reference CSVs strictly as regression oracles, materialises the byte-exact v330 source, and runs the complete verification chain.

### B. Changed-data/data-driven test

To test a compatible changed analytical dataset, supply it explicitly:

```bash
python analysis/run_v330_from_repo.py --master /path/to/changed_master_runs.csv
```

When the supplied master hash differs from the frozen thesis hash, v330 recalculates analyses/tables/dynamic figures and deliberately does **not** emit frozen publication rasters or require exact-thesis reference figures. This is the intended safeguard against hard-coded thesis output.

## Current analytical contract

For the frozen controlled input set, v330 was validated to reproduce:

- **28** platform–scenario cells with exactly **10** retained runs per cell;
- **20** scenario-stratified Kruskal–Wallis tests: 5 declared outcomes × 4 scenarios;
- **84** p95 Dunn pairwise comparisons: 21 per scenario, with Holm adjustment within each scenario family;
- **23** Holm-significant p95 contrasts in the frozen thesis data;
- Cliff’s delta effect sizes and rank-based eta-squared;
- **140** percentile-bootstrap intervals: 28 cells × 5 outcomes, 10,000 resamples with fixed base seed `20260603`;
- the current-thesis numerical results underlying **Tables 4.1–4.16**;
- current dynamic figure carriers for Figures 4.1–4.12 and 4.13a–f;
- 18/18 exact final-thesis publication-asset hashes in the controlled calibration package.

The current controlling analysis **does not use the superseded cross-scenario Friedman/Wilcoxon H4 test**. Earlier analytical scripts are retained only for provenance/auditability.

## Current Chapter-4 artefacts

The authoritative current namespace is:

`results/current-thesis/`

It contains:

- Table 4.1–4.16 numerical/analytical CSV mirrors from the validated v330 pipeline; v344 thesis-only editorial heading clarifications are documented in `THESIS_V344_ALIGNMENT.md`;
- the current Figure 4.1–4.12 + 4.13a–f map;
- frozen-input verification records;
- the SHA-256 manifest of the 18 exact publication figure assets.

Earlier files under `results/tables/` and `results/figures/` are retained as pre-v330 provenance and are explicitly labelled as such rather than silently overwritten.

The validated v330 analytical-update integrity manifest is:

`MANIFEST_V330_UPDATE_SHA256.csv`

The earlier `MANIFEST_SHA256.csv` remains the integrity snapshot of the pre-v330 repository baseline. The two manifests are intentionally distinct so historical hashes are not rewritten retroactively.

## Repository contents

- `THESIS_V344_ALIGNMENT.md` — current thesis-document/repository alignment and evidence boundary.
- `REPOSITORY_COMPLETENESS_AUDIT_V344.md` — explicit present/missing-material audit and approved thesis wording.
- `benchmark/` — benchmark-time orchestrator, four k6 workload scripts and parser.
- `application/` — selected sanitised benchmark-relevant Django source/runtime capture; this is not claimed as the entire historical runnable application tree.
- `configuration/` — retained platform/scenario/deployment configuration evidence, using safe/redacted derivatives where required.
- `analysis/` — v330 source payload/materialiser/repository runner plus earlier analytical provenance.
- `data/canonical/` — frozen 280×39 dataset and dictionary.
- `data/supplementary/` — warm-up, burst-recovery and post-idle analytical carriers small enough for Git.
- `data/raw-archive-manifests/` — integrity manifests for the retained raw campaign and resource evidence.
- `results/current-thesis/` — current Chapter-4 analytical carriers and verification artefacts.
- `verification/` — retained baseline integrity/configuration-truth records.
- `environment/` — runtime/dependency records.

## Evidence and reproducibility boundary

This repository supports inspection of the benchmark implementation, canonical data, analytical logic, integrity records and controlled computational rerunning of the retained analysis. It does **not** claim that the historical managed-cloud campaign can be recreated bit-for-bit today: provider-internal state, historical managed-platform state and some external transients are not controllable or observable after the experiment.

The full original per-run k6 JSON/CSV evidence and other heavy raw evidence are retained as controlled evidence outside ordinary Git history because of size. GitHub stores integrity/provenance manifests. The complete runnable historical Django application tree is likewise not claimed to be fully duplicated in ordinary Git; the repository contains selected sanitised source captures suitable for evidence inspection. No public raw-data URL is claimed until the controlled archive has been uploaded, checked and approved for release.

## Data-driven safeguard

A controlled mutation test doubled only the ten IIS + Waitress / Scenario-A p95 source values. The regenerated Table 4.2 p95 changed from **116.9 ms to 233.7 ms**, the corresponding Kruskal–Wallis result changed, and the dynamic Figure 4.1 hash changed. Frozen publication assets were not emitted. See `results/current-thesis/verification/DATA_DRIVEN_MUTATION_TEST.txt`.

## Citation and licensing

Please cite the thesis and repository; machine-readable citation metadata is in `CITATION.cff`.

Original author code/scripts are under the repository code licence; author-owned data/documentation/table/figure artefacts are under the stated data licence. Third-party software, provider names and trademarks are not relicensed. See `LICENSING.md`.
