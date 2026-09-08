# Current thesis Chapter 4 artefacts — v360 release

This directory retains the validated **v330/current-thesis** numerical mirror namespace while the repository-level **v360 release layer** supplies the independently adjudicated post-v359 corrections. Historical artefacts are not silently overwritten.

- `tables/` contains the current Table 4.1–4.16 CSV mirrors produced by the validated v330 base from the frozen controlled evidence inputs.
- `figure_map.csv` records the historical/current figure mapping retained for auditability.
- `verification/` records frozen-input calibration and publication-asset checks.
- `analysis/v360_release_corrections.py` generates the v360 release carriers directly from the frozen canonical run-level dataset.

The v360 release layer supersedes the historical ratio-of-cell-medians **appendix carrier operator only**. The printed thesis tail-inflation values use the intended median of run-level p99/p50 ratios. v360 also regenerates the Figure 4.1 p95 coordinate carrier, the completed-iteration-shortfall carrier and the Figure 4.13 rank/tie carrier.

Run:

```bash
python analysis/run_v360_from_repo.py
```

Generated release carriers are written to `.v360-run/release/` and include their own SHA-256 manifest. The byte-exact validated v330 source remains preserved as the computational base; historical scripts such as `analysis/ch4_evidence_pipeline.py` remain provenance records rather than the current release authority.

See `REPRODUCIBILITY.md` and `THESIS_V360_ALIGNMENT.md` for the controlling hierarchy and evidence boundaries.
