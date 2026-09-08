# Django Cross-Platform Benchmark — MSc Thesis Research Artefacts

Research artefacts supporting the MSc thesis **“Benchmarking and Evaluation of Traditional Web Servers and Serverless Architectures for an E-Commerce System”** by **Chapk Rzgar Mohammed Abdalla**, College of Science, University of Sulaimani (2026).

> Repository status: **private thesis/examination artefact repository**. Public release is deferred pending supervisor/college approval.

## Current thesis / analysis alignment

The current document release is **v360**. The computational authority is intentionally layered:

1. frozen canonical dataset: `data/canonical/master_runs.csv` — **280 × 39**;
2. byte-exact validated **v330 calibrated end-to-end pipeline** as the computational base;
3. **v360 release layer** for the independently adjudicated post-v359 reproducibility/document corrections.

Use:

```bash
python analysis/run_v360_from_repo.py
```

The v360 release layer is implemented in `analysis/v360_release_corrections.py`. It does **not** rewrite the frozen canonical data or the validated v330 statistical base. See `REPRODUCIBILITY.md` and `THESIS_V360_ALIGNMENT.md`.

Canonical dataset SHA-256:

`710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7`

Validated v330 source SHA-256:

`d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574`

## Why v360 was added

Independent second adjudication confirmed that the printed thesis tail-inflation values use the intended estimand — **median of run-level p99/p50 ratios** — but the historical v330 appendix carrier writer emitted a **ratio of cell medians**. v360 preserves v330 as historical validated code and supersedes only that release carrier with a transparent run-level correction.

v360 also emits data-derived carriers for:

- Figure 4.1 median-p95 coordinates;
- completed-iteration shortfall relative to scenario-specific planned starts, explicitly separate from `dropped_iterations` and from an actual-start census;
- Figure 4.13 within-scenario ranks with exact stored-precision tie handling.

## Main frozen analytical results

The current release preserves the principal frozen results:

- **7 × 4 × 10 = 280 retained runs**;
- **28** platform-scenario cells, 10 retained replications each;
- **20** scenario-stratified Kruskal-Wallis tests;
- **84** p95 Dunn comparisons, Holm-adjusted within four 21-pair scenario families;
- **23** significant p95 contrasts;
- Cliff’s delta and rank-based eta-squared;
- **140** percentile-bootstrap intervals using 10,000 resamples and base seed `20260603`.

The targeted 279-run sensitivity excluding only `05_koyeb__C_checkout__rep08` retains the same 20 omnibus decisions and the same 23 significant p95 pair set. It is a post-campaign diagnostic, not a replacement for the 280-run primary analysis.

## Repository structure

- `THESIS_V360_ALIGNMENT.md` — current thesis/repository authority and evidence boundaries.
- `REPRODUCIBILITY.md` — controlling v360 entry point, v330 base, inputs and release carriers.
- `benchmark/` — orchestrator, k6 workload scripts and parser.
- `application/` — selected sanitised benchmark-relevant Django source/runtime capture.
- `configuration/` — retained deployment/configuration evidence; current/as-built captures are not silently treated as per-run historical proof.
- `analysis/` — v330 materialiser/base runner, v360 release layer and historical analytical provenance.
- `data/canonical/` — frozen 280×39 dataset and data dictionary.
- `data/supplementary/` — warm-up, burst-recovery and post-idle analytical carriers.
- `data/raw-archive-manifests/` — integrity manifests for heavy raw evidence retained outside ordinary Git history.
- `results/current-thesis/` — Chapter-4 analytical mirrors and verification artefacts.
- `verification/` — retained integrity/configuration records.
- `environment/` — runtime/dependency records.

## Evidence boundary

The repository supports inspection and selected computational rerunning of the retained analysis. It does **not** claim bit-for-bit re-execution of the historical managed-cloud campaign: provider-internal state, historical provider state, complete per-run deployment identity and some external transients are not reconstructible after the experiment.

The full original k6 JSON/CSV archive and the complete Docker telemetry archive remain controlled external evidence because of size. Their integrity manifests are retained in the repository. Historical scripts remain available for provenance but are labelled historical where they are not the current executable authority.

## Citation and licensing

Please cite the thesis and repository. Machine-readable citation metadata is in `CITATION.cff`; licensing and third-party boundaries are documented in `LICENSING.md`.
