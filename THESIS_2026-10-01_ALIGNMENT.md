# Thesis and repository alignment — 1 October 2026

This record supersedes v368 as the current document-facing alignment. Historical v330/v360/v367/v368 sources, manifests and records retain their historical roles. No old release is relabelled as the current thesis.

## Controlling Word documents

The current identity-restored Full / Part 1 / Part 2 document hashes and render counts are in `documentation/thesis_alignment_2026-10-01.json`. Full contains 191 rendered pages and equals the concatenated body text of the 102-page Part 1 and 89-page Part 2. The submitted document bytes are identified by SHA-256; Word files themselves are distributed separately.

The approved corrections cover Table B.5, Section 5.8, the abbreviation-list TOC entry, three Chapter 2 page references, the cgroup v2 reference and its Appendix A concordance, and four bounded literature-context paragraphs using five existing references. The reference count remains 115. Table B.5 recognises the retained 17 May inventory without inventing its timezone or claiming per-run runtime continuity.

Chapter 4 body text, scientific table values, image payloads, canonical data and primary statistical conclusions are unchanged. The Fly.io retained-run sensitivity and its four p95 pairwise decision changes remain disclosed; no new overall-winner claim is introduced.

## Word package and navigation checks

Each package passes ZIP CRC, XML parsing and internal relationship-target checks. Only `word/document.xml` changes inside the three packages; media and all other package payloads are byte-identical to their respective controlling inputs. Core/app metadata remain empty, and macros, comments, tracked changes, custom XML, embedded objects and live body fields remain absent. Existing static citations, restored identities, public evidence links and logos are preserved.

The Full copy's 177 unmatched U+202C controls are removed. The legitimate Kurdish U+200C joining character is preserved. All 222 static TOC/list page references match their target pages in the final local rendering. Page fields used for ordinary headers/footers are not replaced with live citation-manager fields.

Rendering uses LibreOffice, not native desktop Microsoft Word. The files were not submitted to Turnitin during this correction, and future server-side processing cannot be guaranteed from package checks. These documents include the restored student/supervisor/university information; they are not anonymous checker-service copies.

## Reproducibility release

`python analysis/run_current_thesis.py` stages the unchanged v360/v367 layers, the reviewed Chapter 4 descriptive supplement and the Figure 4.4 / 4.9 renderers. `python verification/verify_current_thesis.py` checks regenerated carriers against retained reviewed reference CSVs, protected inputs/source hashes, the current crosswalk and the release manifests.

Five descriptive CSV carriers reproduce the reviewed data: 280 runs, 28 cells, 28 runs with shortfall >1%, 10 runs with shortfall ≥5%, two configurations meeting the H4 descriptive rule, 28 scenario-specific conditional cost entries, and 336 profile cells with 104 H/L markers. These carriers add no independent experiment. Seven newly regenerated raster images (Figure 4.4 plus six Figure 4.9 panels) have decoded pixels identical to the current Word embeds in the recorded local environment.

The current figure map is `results/current-thesis/figure_map_2026-10-01.csv`. Its numbering ends at Figure 4.9(a–f). Default execution does not rerun the full v330 analysis or every thesis figure; the historical controlled-input prerequisites remain explicit in `REPRODUCIBILITY.md`.

`MANIFEST_2026-10-01_SHA256.csv` covers the current changed/added source, reference and alignment files. Earlier whole-repository manifests should be checked at their corresponding historical commits.
