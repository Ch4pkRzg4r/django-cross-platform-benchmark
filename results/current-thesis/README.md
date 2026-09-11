# Current-thesis analytical artefacts and document crosswalk

This directory contains two deliberately different kinds of material:

1. the **historical v330/current-thesis wrapper namespace** retained for computational regression/provenance; and
2. the **current v366 document-facing crosswalk** that maps the final thesis numbering without pretending that historical wrapper filenames were renamed at campaign time.

## Historical computational namespace

- `tables/` contains the validated v330 Table 4.1–4.16 CSV mirror namespace used by the frozen computational wrapper.
- `figure_map.csv` is the historical wrapper figure map. It includes historical numbers through Figure 4.13 and must **not** be read as the current document’s figure numbering.
- `verification/` contains frozen-input calibration/publication-asset checks for that historical wrapper namespace.
- `analysis/v360_release_corrections.py` generates the v360 release carriers directly from the frozen canonical run-level dataset.

The v360 layer supersedes the historical ratio-of-cell-medians appendix-carrier operator only and provides corrected/explicit carriers for the run-level p99/p50 estimand, completed-iteration shortfall, p95 cell coordinates and the historical rank/tie representation. It does not renumber the current thesis figures.

## Current v366 document-facing map

The current thesis Chapter 4 ends at **Figure 4.8**, with Figure 4.8 continued across six panels. The authoritative document-facing crosswalk is:

`figure_map_v366.csv`

That crosswalk identifies the current thesis caption and the retained analytical/source carrier used to check it. It does **not** relabel the historical `figure_map.csv` assets as if they had always carried the current numbers.

The current document sequence is:

- Figure 4.1 — relative p95 latency gap;
- Figure 4.2 — callback-qualified goodput attainment;
- Figure 4.3 — relative callback-qualified goodput gap;
- Figure 4.4 — temporal diagnostics (warm-up and post-idle panels);
- Figure 4.5 — Scenario-D burst-phase p95 relative to baseline;
- Figure 4.6 — median p95 with final 95% percentile-bootstrap intervals;
- Figure 4.7 — conditional warm-cost versus scenario-specific median p95;
- Figure 4.8(a–f) — six-panel scenario-specific metric profile.

The exact v366 embedded publication rasters are document-finalisation artefacts. The historical 18-raster copy gate under `verification/PUBLISHED_FIGURE_SHA256_MANIFEST.csv` remains a historical wrapper dependency and was not silently redefined as the v366 figure set.

## Running the current computation

```bash
python analysis/run_v360_from_repo.py
```

Generated v360 release carriers are written to `.v360-run/release/` and include their own manifest. The byte-exact validated v330 source remains the computational base; historical scripts such as `analysis/ch4_evidence_pipeline.py` remain provenance records rather than the current release authority.

See `../../REPRODUCIBILITY.md` and `../../THESIS_V366_ALIGNMENT.md`.
