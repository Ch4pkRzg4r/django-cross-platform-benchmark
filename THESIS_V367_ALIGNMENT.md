# v367 correction candidate and computational authority

The v367 DOCX corrects eight independently evidenced minor issues in v366 and resolves the two remaining source decisions. Native Microsoft Word finalisation and review of every resulting PDF page remain pending. This repository update is not a thesis submission verdict.

The current entry point is `python analysis/run_v367_from_repo.py`. It runs the unchanged v360 carrier layer, then `analysis/v367_release_corrections.py`. Use the latter directly when only the affected H4 and Figure 4.3 outputs need regeneration. The byte-exact v330 statistical source and canonical 280×39 dataset remain unchanged.

## H4: preserve the thesis's stated rule

For each platform, the Scenario-D median callback-defined request-failure rate must strictly exceed the median in **each** of A, B and C. Overall descriptive support requires all seven platforms to satisfy that rule. No cross-scenario significance test is introduced.

The frozen v330 helper instead compared D with the median of the three A/B/C cell medians. That helper is superseded for H4 by `_consistent_h4_supported` in `v367_release_corrections.py`. Frozen historical source bytes remain intact for provenance; its H4 helper must not be used as the current predicate.

Azure Container Apps changes from true under the old helper to false under the thesis rule: D = 0.0002025 is less than B = 0.0002035. Gunicorn and IIS satisfy the strict rule; the other five platforms do not. The overall conclusion remains **not supported** under both rules. `results/current-thesis/v367/v367_h4_descriptive.csv` exposes all four medians and three strict comparisons for each platform.

## Figure 4.3

The figure retains the same balanced family contrast: first take each platform's run-level median goodput, then each family's median across platforms, and calculate `100*(provider-managed - self-managed)/self-managed`. The four displayed values remain −0.5%, 0.0%, −0.5% and +0.6%.

The replacement is generated at its final 450×270 point placement size. All labels are at least 10.5 points; a text-boundary check prevents clipping. The PNG, vector PDF/SVG, data carrier and font/output manifest are under `results/current-thesis/v367/`. The current figure crosswalk is `results/current-thesis/figure_map_v367.csv`. Other current thesis figure numbers and data remain unchanged.

## Reference authority and document corrections

The corrected source package has **115 references and 256 source-use links**. Stable IDs are retained; R051 is removed, not reused. Its sole Appendix A collective sentence remains supported by eleven other verified sources. R110 now explicitly cites the actually inspected Wohlin et al. **2024 second edition**, DOI `10.1007/978-3-662-69306-3`; all four affected uses are supported.

Other document corrections preserve scientific results: a nonbreaking hyphen in “re-estimated”; Gonzalez as the third author of Hellerstein et al. (2019); `PLATFORM_ID` in Table 3.10; pages 24–30 for Zuhairnawan et al.; an explicit Table D.1 continuation caption; and precise identification of the preliminary study's inferential methods in Table 2.1. Correct official documentation captures supplement R029/R042/R080/R086 in the controlled source package. Full third-party source texts are not republished in this public repository.

## Unchanged statistical and evidence boundaries

The 280×39 canonical design, 20 Kruskal–Wallis tests, 84 p95 Dunn/Holm comparisons, 23 significant p95 contrasts, Cliff's delta, rank-based eta-squared and 140 controlling percentile-bootstrap intervals are unchanged. The completed independent v366 recomputations are carried forward; the v367 correction does not repeat the primary analysis.

The 73 recoverable raw-run pairs and 207 unavailable pairs remain the disclosed raw-data boundary. Historical executable identity, provider state, Nginx configuration conflicts and controlled Docker telemetry prerequisites are unchanged. `REPRODUCIBILITY.md` retains their precise scope. A source-package correction does not supply missing historical campaign evidence.

`MANIFEST_V367_SHA256.csv` and `FILE_INDEX_V367.csv` identify this release. Earlier version-named manifests and alignment documents are retained as historical records. The commit actually reviewed and final Word-produced file hashes belong in the final audit packet after native finalisation.
