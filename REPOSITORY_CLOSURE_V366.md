# Repository closure — v366 minor-revision evidence alignment

Date: 11 September 2026

This closure record documents the bounded repository changes made in response to the independent full-evidence audit of the exact v365 thesis candidate. The audit verdict was **MINOR REVISIONS** and identified eight correction groups (M01–M08). No audited finding required a new benchmark campaign, a change to the frozen 280×39 dataset, or a change to the controlling univariate statistical results.

## What v366 changes

### M01 — PERMDISP provenance

Repository/document wording now distinguishes the recovered historical PERMANOVA implementation/carriers from PERMDISP. No original historical PERMDISP implementation/configuration/output was recovered. Any later dispersion calculation remains post-hoc audit sensitivity and is not promoted to campaign-time provenance.

### M02 — home-route authentication boundary

The thesis now describes the home view as authentication-gated and distinguishes authenticated ORM activity from the unauthenticated k6 redirect path. Repository source was not rewritten to manufacture a different route.

### M03 — public repository and privacy-safe fixture

Current documentation states that the source/computational repository is public while sensitive historical material remains restricted/unavailable. The public fixture is correctly described as a 71-object, 15-model privacy-safe derivative with 17 synthetic user/account objects; it is not the frozen historical database.

### M04 — Nginx/uWSGI configuration conflict

The conflicting retained files are preserved unchanged:

- historical/current `configuration/uwsgi.ini`: TCP `127.0.0.1:3031`, 4 processes × 2 threads;
- retained `configuration/nginx-uwsgi.conf`: UNIX socket `/run/uwsgi/django.sock`;
- thesis/current nominal target: 2 processes × 4 threads.

No exact benchmark-time 2×4 UNIX-socket uWSGI capture was recovered. `configuration/reproduction/nginx-uwsgi-v366/` therefore supplies a **prospective public reproduction derivative** (UNIX socket, 2×4, explicit repository-root build context) and is explicitly not retroactive campaign proof.

### M05 — current documentation and data dictionary

- README distinguishes v366 document, v360 current computational entry point and v330 frozen base.
- `analysis/README.md`, `REPRODUCIBILITY.md`, `ARTEFACT_PROVENANCE.md`, `SECURITY_AND_REDACTION.md` and figure-status documentation are aligned.
- `data/canonical/DATA_DICTIONARY.md` now defines all 39 fields, units, missing-value rules, timestamp/reduction semantics, historical parser rounding, latency-only Apdex, Scenario-C request/iteration semantics and Scenario-D staged-rate authority.
- current v366 document figure numbering is separated from the historical wrapper namespace by `results/current-thesis/figure_map_v366.csv`.

### M06 — raw archive availability

The current evidence statement records the audited state: four supplied raw ZIPs are truncated; 73 complete canonical JSON/CSV run pairs were recoverable and hash/reconciliation-verified; 207 canonical run pairs were unavailable in the supplied submission evidence. Integrity manifests are treated as expected-identity records, not proof of present byte availability.

### M07 — stale document references

These are thesis-document corrections (stale Figure 4.9 reference, old Figure 4.4 left/right wording, old Figure 4.7 coordinate wording and repeated script-table rows). No repository numerical carrier was rewritten to create new values.

### M08 — figure typography

The v366 document-finalisation pass regenerates the affected current thesis figures with Times-compatible Roman/serif typography and a ≥10 pt target at final placement, including Figure 4.6. This is a document-finalisation change; numerical coordinates and the controlling statistical convention are preserved. Current document rasters do not replace the historical 18-raster wrapper gate.

## Computational state preserved

The frozen canonical dataset remains:

`data/canonical/master_runs.csv`

SHA-256:

`710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7`

The byte-exact v330 computational base remains:

`d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574`

The current repository computational entry point remains:

```bash
python analysis/run_v360_from_repo.py
```

The independently audited principal results remain unchanged: 20 controlling scenario-stratified Kruskal–Wallis tests, 84 p95 Dunn/Holm comparisons with 23 significant contrasts, Cliff’s delta/rank eta-squared and the final 10,000-resample percentile-bootstrap convention.

## Current integrity bookkeeping

The v365 `FILE_INDEX.csv` and `MANIFEST_SHA256.csv` are retained as historical closure snapshots tied to the previous repository state; they are **not silently rewritten** as if their hashes had always described v366.

The v366 branch adds:

- `tools/finalize_v366_repository.py`;
- `FILE_INDEX_V366.csv` (generated current file index);
- `MANIFEST_V366_SHA256.csv` (generated SHA-256 manifest; the manifest excludes its own hash);
- `verification/verify_v366_repository_closure.py`;
- `.github/workflows/finalize-v366-closure.yml`.

The finalisation workflow regenerates the current index/manifest from the actual tracked tree and verifies the v366 authority, data dictionary, raw-availability boundary, scenario semantics, Nginx prospective recipe, current figure crosswalk and current-source provenance.

## Evidence boundary retained

This closure does not claim:

- full 280-run raw-to-canonical reconstruction from currently supplied raw bytes;
- exact historical Nginx/uWSGI socket/worker variant where the retained files conflict;
- historical PERMDISP provenance that was not recovered;
- complete historical 18-raster wrapper target availability;
- bit-for-bit reconstruction of managed-provider internal state;
- invoice/current-price validation of the conditional cost model;
- provider lifecycle-state proof from the small post-idle probe.

Those boundaries are explicit so that reproducibility is strengthened by accurate provenance rather than by fabricated completeness.
