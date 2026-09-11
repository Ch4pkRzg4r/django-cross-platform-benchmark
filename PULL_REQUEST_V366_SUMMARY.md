# v366 minor-revision closure — pull-request summary

This branch closes the eight bounded correction groups (M01–M08) from the independent 11 September 2026 full-evidence thesis audit.

## Scope

- No new benchmark campaign.
- No change to frozen `master_runs.csv` (280 × 39).
- No change to the controlling 20 Kruskal–Wallis decisions, 84 p95 Dunn/Holm comparisons, 23 significant p95 contrasts, Cliff’s delta/rank eta-squared conventions, or final percentile-bootstrap convention.
- No fabrication of missing PERMDISP, raw-archive, Nginx historical runtime or provider-internal evidence.

## Main corrections

- public/private and privacy-safe fixture wording aligned with current repository;
- PERMDISP historical provenance qualified;
- final workload/rate authority documented for Scenario C and D;
- Nginx/uWSGI conflict preserved and a prospective self-consistent reproduction recipe added;
- complete 39-field canonical data dictionary;
- raw evidence availability corrected to 73 complete canonical pairs recoverable / 207 unavailable;
- historical versus v366 current figure namespaces separated;
- current/recovered `views.py` provenance corrected;
- current v366 file index/manifest and executable closure QA added.

## Automated QA

`finalize-v366-closure` regenerates `FILE_INDEX_V366.csv` and `MANIFEST_V366_SHA256.csv` from the actual tree and runs `verification/verify_v366_repository_closure.py`.

The existing `verify-current-release` pull-request workflow remains the independent computational regression gate for the frozen v330 state, current v360 release layer and public application compile checks.

See `V366_CORRECTION_REGISTER.md`, `REPOSITORY_CLOSURE_V366.md`, `V366_FINAL_QA_SUMMARY.md` and `THESIS_V366_ALIGNMENT.md`.
