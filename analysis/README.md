# Analysis directory

The current entry point is `python analysis/run_current_thesis.py`. It stages the unchanged v360/v367 layers, the reviewed Chapter 4 descriptive supplement and the current Figure 4.4 and Figure 4.9 renderers. Validate with `python verification/verify_current_thesis.py` (use the same `--out-dir` for an explicit destination).

The default run does not rerun all primary inference or every figure. The byte-exact v330 source, historical runners and previous release scripts remain unchanged. `--run-v330` requires the controlled telemetry and historical reference rasters documented in `../REPRODUCIBILITY.md`.

`current-thesis/` contains portable command-line copies of the reviewed 27 September plotting/calculation scripts. Explicit input/output paths replace the historical local-folder assumptions; the mathematical operations and plotting geometry are preserved. Current figure numbering ends at Figure 4.9(a–f), and all 336 profile cells are descriptive within-scenario ranks, not an overall ranking.

See `../THESIS_2026-10-02_ALIGNMENT.md` and `../results/current-thesis/figure_map_2026-10-01.csv`. Earlier manifests and namespaces remain historical provenance.
