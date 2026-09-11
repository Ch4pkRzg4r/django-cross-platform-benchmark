# v366 final QA summary

Date: 11 September 2026

This record accompanies the v366 minor-revision closure and summarizes the final QA performed before returning the package for independent re-audit.

## Thesis document QA

The v366 DOCX was produced from the exact independently audited v365 candidate and edited only for the bounded M01–M08 correction set. No frozen dataset or controlling statistical carrier was rewritten.

Final structural checks on the v366 DOCX:

- ZIP/OOXML CRC: clean;
- all XML and relationship parts parsed;
- tracked-change/comment markers: 0;
- complex fields: 565 balanced `begin/separate/end` triplets across all Word parts;
- live EndNote citation fields: 226;
- live EndNote bibliography field: 1;
- TOC/LOT/LOF fields: 3;
- PAGEREF fields: 216;
- PAGE fields: 119;
- bookmarks: 901 starts / 901 ends, 901 unique names and balanced IDs;
- missing internal relationship targets: 0;
- rendered QA pagination: 189 physical pages.

Visual regression used the independently audited v365 render as the baseline. 142 physical pages were pixel-identical; all 47 changed pages were reviewed as a targeted visual set, including the corrected methods tables/text, access/reproducibility diagrams, Chapter-4 figures, Chapter-6 limitation/conclusion wording and Appendix-D configuration table. No new clipping/overlap/cropping or continuation defect was identified in the changed-page review.

Figure 4.6 was inspected at full-page size after regeneration; platform labels and axes are materially larger than the audited ~8–9 pt raster labels and use the Times-compatible serif finalisation convention. The other affected regenerated Roman-letter figures use the same serif finalisation rule. Numerical coordinates/statistical intervals were not intentionally altered by typography work.

## Repository QA

The v366 branch contains executable closure verification and current-state bookkeeping:

- `verification/verify_v366_repository_closure.py`;
- `tools/finalize_v366_repository.py`;
- `FILE_INDEX_V366.csv`;
- `MANIFEST_V366_SHA256.csv` (manifest self excluded);
- `.github/workflows/finalize-v366-closure.yml`.

GitHub Actions independently regenerated the current index/manifest and returned **success** for the v366 closure checks before the generated files were committed by `github-actions[bot]`. The final generated-file commit contains only the verified current index/manifest refresh.

The branch also keeps the v365 `FILE_INDEX.csv`/`MANIFEST_SHA256.csv` as historical closure snapshots instead of rewriting their history.

## Scientific invariants

The v366 closure intentionally preserves:

- frozen canonical 280×39 design and SHA-256;
- 28 balanced cells × 10 retained replications;
- 20 controlling scenario-stratified Kruskal–Wallis results;
- 84 p95 Dunn/Holm comparisons and 23 significant p95 contrasts;
- Cliff’s delta/rank eta-squared conventions;
- final 10,000-resample percentile-bootstrap convention;
- disclosed limitations and evidence boundaries that were not correction findings.

## Remaining procedural boundary

The PDF rendered in the automated QA environment is a QA counterpart, not a claim of a fresh native Microsoft Word export. For official submission or a native-PDF re-audit, open the final v366 DOCX in Microsoft Word, update fields through the normal Word workflow, repaginate, save, and export the native PDF. A Windows Word finalisation helper is supplied with the final handoff package.
