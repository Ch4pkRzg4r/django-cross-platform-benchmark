# Thesis analytical artefacts and document crosswalk

The current document-facing map is `figure_map_2026-10-01.csv`:

- 4.1: relative p95 latency gap.
- 4.2: callback-qualified goodput attainment.
- 4.3: relative callback-qualified goodput gap (unchanged v367 renderer).
- 4.4: completed-iteration delivery across 280 retained runs.
- 4.5: temporal diagnostics (warm-up and post-idle).
- 4.6: Scenario D burst-phase p95 relative to baseline.
- 4.7: median p95 with percentile-bootstrap intervals.
- 4.8: conditional warm-cost versus scenario-specific median p95.
- 4.9(a–f): 336-cell scenario-specific metric profile.

`release-2026-10-01/` holds the reviewed descriptive CSV regression references and manifest. The current entry point regenerates these data from `data/canonical/master_runs.csv`; reference CSVs are read only by verification, never by the calculators.

The `tables/`, `figure_map.csv`, versioned maps and `verification/` retain historical computational/publication namespaces. Their numbering must not be substituted for the current document numbering. Historical table filenames remain unchanged for the frozen v330 regression. `v367/` retains the Figure 4.3/H4 outputs.

```bash
python analysis/run_current_thesis.py
python verification/verify_current_thesis.py
```

Default outputs go to `.current-thesis-run/release/`; see `../../REPRODUCIBILITY.md` for scope, fonts and optional controlled-input execution.
