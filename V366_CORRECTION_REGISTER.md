# v366 independent-audit correction register

This register maps the eight bounded correction groups from the 11 September 2026 independent full-evidence audit to the v366 closure. It is a correction/provenance register, not a new scientific result.

| ID | Audit finding | v366 disposition | Repository evidence / document action | Status |
|---|---|---|---|---|
| M01 | Historical PERMDISP claim lacked recovered historical implementation/configuration/output. | Historical PERMANOVA remains identifiable; PERMDISP is qualified as unrecovered. Any new dispersion calculation is labelled post-hoc audit sensitivity only. | `THESIS_V366_ALIGNMENT.md`; thesis statistical-method/results wording revised. | CLOSED |
| M02 | Home-route ORM attribution omitted authentication boundary. | Home route described as authentication-gated; unauthenticated k6 path measures redirect rather than authenticated ORM view. | Current application source + thesis §3.4.2/Table 3.3 correction. | CLOSED |
| M03 | Private/public and fixture statements stale. | Repository documented as public source/computational repo; restricted material remains separate. Public fixture documented as 71 objects/15 models/17 synthetic user/account objects and not the historical database. | `README.md`, `DATA_AVAILABILITY.md`, `SECURITY_AND_REDACTION.md`, `application/FIXTURE_PUBLIC_PROVENANCE_V365.md`; thesis access/fixture wording and Figure 3.12 corrected. | CLOSED |
| M04 | Retained Nginx/uWSGI files conflict (TCP 4×2 vs UNIX/nominal 2×4). | Historical conflict preserved and bounded. Prospective self-consistent public rerun recipe added: UNIX `/run/uwsgi/django.sock`, 2 processes × 4 threads, explicit repository-root build context. No retroactive campaign proof claimed. | `configuration/platforms/README.md`, `application/DOCKERFILE_AUTHORITY_V365.md`, `configuration/reproduction/nginx-uwsgi-v366/`; thesis Table 3.6/Table D.1 evidence boundary corrected. | CLOSED |
| M05 | Repository docs/figure namespace/source provenance/data dictionary stale. | v366 document vs v360 computational release vs v330 frozen base distinguished; historical figure namespace separated; current source-redaction boundary corrected; all 39 canonical fields fully documented. | `README.md`, `analysis/README.md`, `REPRODUCIBILITY.md`, `ARTEFACT_PROVENANCE.md`, `SECURITY_AND_REDACTION.md`, `data/canonical/DATA_DICTIONARY.md`, `results/current-thesis/README.md`, `results/figures/README_CURRENT_STATUS.md`, `THESIS_V366_ALIGNMENT.md`, `figure_map_v366.csv`. | CLOSED |
| M06 | Submission raw archive incomplete; prior availability wording overclaimed completeness. | Current evidence explicitly records four truncated ZIPs, 73 complete verified canonical run pairs recovered and 207 unavailable. Manifests treated as identity records, not possession proof. | `DATA_AVAILABILITY.md`, `data/raw-archive-manifests/AVAILABILITY_AND_RECONSTRUCTION.md`; thesis §3.16/limits/conclusion wording corrected. | CLOSED |
| M07 | Stale figure references/panel wording and repeated script rows. | Figure 4.9 stale reference removed; Figure 4.4 panels named correctly; Figure 4.7 cost wording corrected; repeated Table 3.12 script rows consolidated. | v366 DOCX correction pass. | CLOSED |
| M08 | Regenerated figures used inconsistent sans type and Figure 4.6 labels were below guide minimum. | Affected current-thesis figures regenerated with Times-compatible serif typography and ≥10 pt target at final placement; Figure 4.6 rebuilt from controlling p95 percentile-bootstrap convention without changing values. | v366 DOCX figures; current figure crosswalk; QA render/page inspection. Historical wrapper raster gate remains separate. | CLOSED |

## Invariants preserved

- canonical `master_runs.csv`: 280 × 39, SHA-256 `710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7`;
- v330 frozen computational source SHA-256 `d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574`;
- 20 controlling scenario-stratified Kruskal–Wallis tests;
- 84 p95 Dunn/Holm comparisons and 23 significant p95 contrasts;
- Cliff’s delta and rank-based eta-squared convention;
- final 10,000-resample percentile-bootstrap convention;
- disclosed experimental/evidence boundaries not listed as correction groups remain disclosed rather than fabricated away.

## Verification

The v366 repository closure adds executable verification (`verification/verify_v366_repository_closure.py`) and generated current-state bookkeeping (`FILE_INDEX_V366.csv`, `MANIFEST_V366_SHA256.csv`) without overwriting the historical v365 closure manifests. GitHub Actions independently generated/verified those current-state files before committing them.
