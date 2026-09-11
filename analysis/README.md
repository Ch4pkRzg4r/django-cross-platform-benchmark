# Analysis directory

The current repository entry point is `python analysis/run_v367_from_repo.py` from the repository root. It invokes the unchanged v360 carrier layer and then the v367 descriptive H4 and Figure 4.3 corrections. Native Word finalisation of the v367 thesis remains pending.

- **v330** is the byte-exact statistical base. `materialize_v330_pipeline.py` verifies source SHA-256 `d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574`.
- **v360** retains the corrected run-level tail-ratio, completed-iteration-shortfall, p95-cell and historical rank/tie carriers. Its implementation and outputs are unchanged.
- **v367** applies the thesis's strict H4 rule (D greater than each A/B/C median on every platform) and regenerates Figure 4.3 with labels at least 10.5 pt at final placement. It supersedes the frozen helper only for H4; the overall decision remains not supported.

To regenerate only the affected outputs, run `python analysis/v367_release_corrections.py`. To check them, run `python verification/verify_v367_release.py`. Both accept `--master` and `--out-dir`; the canonical input must match the frozen SHA-256. For full-base/controlled-input execution, see `../REPRODUCIBILITY.md`.

The 280×39 canonical data, 20 Kruskal–Wallis tests, 84 p95 Dunn/Holm comparisons, 23 significant contrasts, effect sizes and 140 bootstrap intervals remain unchanged. The v367 correction does not introduce a new statistical model or rerun requirement for the completed primary audit.

Historical utilities and `historical-provenance/` are retained for their documented roles. The frozen `_consistent_h4_supported` helper's median-of-A/B/C predicate is historical; the identically named function in `v367_release_corrections.py` is current. See `../THESIS_V367_ALIGNMENT.md` for the correction and evidence boundaries.
