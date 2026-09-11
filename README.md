# Django Cross-Platform Benchmark — MSc Thesis Research Artefacts

Research artefacts supporting the MSc thesis **“Benchmarking and Evaluation of Traditional Web Servers and Serverless Architectures for an E-Commerce System”** by **Chapk Rzgar Mohammed Abdalla**, College of Science, University of Sulaimani (2026).

> Repository status: **public source/computational research repository**. Sensitive credentials, private histories, original identifying account data, provider-private material and unrecovered heavy raw evidence are not published. See `SECURITY_AND_REDACTION.md`, `DATA_AVAILABILITY.md` and `data/raw-archive-manifests/AVAILABILITY_AND_RECONSTRUCTION.md`.

## Current thesis / analysis alignment

The current document candidate is **v368**, with the four frozen Chapter Two corrections applied. The computational release remains **v367** and all scientific results are unchanged. Native Word finalisation and the final PDF regression review remain pending. No final submission verdict is implied. See `THESIS_V368_ALIGNMENT.md` for the targeted correction record.

1. Frozen canonical dataset: `data/canonical/master_runs.csv` — **280 × 39**.
2. Byte-exact validated **v330 calibrated end-to-end pipeline** — the statistical base.
3. Unchanged **v360 carrier layer** — corrected tail-ratio, shortfall, p95-cell and rank carriers.
4. Current **v367 release layer** — the thesis-defined strict H4 predicate and legible Figure 4.3.

```bash
python analysis/run_v367_from_repo.py
```

This entry point runs v360 and then the v367 corrections. To regenerate only the affected outputs, use `python analysis/v367_release_corrections.py`. See `REPRODUCIBILITY.md` and `THESIS_V367_ALIGNMENT.md`.

Canonical dataset SHA-256:

`710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7`

Validated v330 source SHA-256:

`d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574`

## Authority versus historical provenance

The repository intentionally retains historical files and namespaces. A historical filename, figure number, Dockerfile label or script is **not** silently upgraded to current authority.

- `analysis/run_v367_from_repo.py` is the current computational repository entry point.
- the byte-exact v330 pipeline remains the frozen computational base;
- `analysis/ch4_evidence_pipeline.py` and `analysis/historical-provenance/` are retained for historical analytical provenance;
- `results/current-thesis/figure_map.csv` is the historical v330/current-thesis figure namespace used by the validated wrapper;
- `results/current-thesis/figure_map_v367.csv` is the document-facing crosswalk for Chapter 4 (unchanged in v368), whose numbering ends at Figure 4.8 (six continued panels);
- the historical computational pin `5cfb18adb04da928bd07517a4f76261fe74246a1` remains a historical pin where cited; it is not the identity of the current public branch head.

## Main frozen analytical results

The current document preserves the principal frozen results:

- **7 × 4 × 10 = 280 retained runs**;
- **28** platform-scenario cells, 10 retained replications each;
- **20** scenario-stratified Kruskal-Wallis tests;
- **84** p95 Dunn comparisons, Holm-adjusted within four 21-pair scenario families;
- **23** significant p95 contrasts;
- Cliff’s delta and rank-based eta-squared;
- **140** percentile-bootstrap intervals using 10,000 resamples and base seed `20260603` under the controlling deterministic seed schedule.

The targeted 279-run sensitivity excluding only `05_koyeb__C_checkout__rep08` retains the same 20 omnibus decisions and the same 23 significant p95 pair set. It is a post-campaign diagnostic, not a replacement for the 280-run primary analysis.

## Repository structure

- `THESIS_V367_ALIGNMENT.md` — current document/repository authority, figure crosswalk and evidence boundaries.
- `REPRODUCIBILITY.md` — controlling v367 computational entry point, v330 base, inputs and release carriers.
- `benchmark/` — orchestrator, k6 workload scripts and parser.
- `application/` — reviewed/sanitised benchmark-relevant Django source/runtime material.
- `configuration/` — retained deployment/configuration evidence plus explicitly prospective reproduction derivatives.
- `configuration/reproduction/nginx-uwsgi-v366/` — **prospective public reproduction recipe only**; it resolves the retained Nginx/uWSGI file mismatch without pretending to be benchmark-time proof.
- `configuration/SCENARIO_AUTHORITY_V366.md` — final workload-script authority and scenario-rate semantics.
- `analysis/` — v330 materialiser/base runner, v360 carriers, v367 correction layer and historical analytical provenance.
- `data/canonical/` — frozen 280×39 dataset and complete data dictionary.
- `data/supplementary/` — warm-up, burst-recovery and post-idle analytical carriers.
- `data/raw-archive-manifests/` — expected raw-evidence integrity manifests and current availability statement.
- `results/current-thesis/` — analytical mirrors, historical wrapper namespace and v367 document-facing crosswalk.
- `verification/` — retained integrity/configuration records.
- `environment/` — runtime/dependency records.

## Evidence boundary

The repository supports inspection and computational rerunning from the frozen analytical evidence. It does **not** claim bit-for-bit re-execution of the historical managed-cloud campaign: provider-internal state, historical provider state, complete per-run deployment identity and some external transients are not reconstructible after the experiment.

The current submission evidence also does **not** contain a complete intact 280-run raw-request archive. Independent recovery of the supplied damaged raw archives established **73 complete canonical JSON/CSV run pairs; 207 canonical run pairs were unavailable** in the supplied submission evidence. The repository retains expected per-file and archive-part integrity manifests, but a manifest is not evidence that the corresponding bytes are presently accessible. See `data/raw-archive-manifests/AVAILABILITY_AND_RECONSTRUCTION.md`.

Full 120-run Linux Docker telemetry remains controlled external evidence because of size; the repository contains its integrity manifests and representative/sample material. Historical scripts remain available for provenance but are labelled historical where they are not the current executable authority.

## Citation and licensing

Please cite the thesis and repository. Machine-readable citation metadata is in `CITATION.cff`; licensing and third-party boundaries are documented in `LICENSING.md`.

