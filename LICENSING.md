# Licensing Scope

**MIT (`LICENSE-CODE-MIT.txt`)** covers original source code and scripts authored for this research: `benchmark/`, `analysis/` (including `analysis/historical-provenance/`), author-owned Python/HTML/template code under `application/`, and author-owned configuration templates in `configuration/`.

**CC BY 4.0 (`LICENSE-DATA-CC-BY-4.0.txt`)** covers author-owned research outputs: `data/canonical/`, `data/supplementary/`, `data/raw-archive-manifests/`, `results/tables/`, author-owned `results/figures/`, `documentation/`, `verification/` summaries, `environment/` records, and author-owned Markdown documentation at the repository root.

## Explicit exclusions / original licences

The repository licences above do **not** automatically relicense third-party material. In particular, the following remain under their original licences or require separate rights/provenance review:

- third-party software and packages named in requirements/environment captures;
- Docker base images, k6, provider platforms and their software;
- third-party fonts and icon-font files;
- image, video, theme/template or other static assets under `application/static/` whose authorship or redistribution rights have not been independently established;
- trademarks, logos and provider/product names.

The Material Design Iconic Font files identify their own upstream licensing (SIL OFL 1.1 for the font and MIT for its CSS). Other static assets must not be assumed to be MIT/CC BY merely because they are present in a private research repository.

The current v365 completeness work therefore treats `application/static/` as a **research/reproduction asset set with a separate licensing boundary** until provenance is resolved. A future public release may omit or replace assets whose redistribution rights cannot be established without affecting the frozen benchmark dataset or inferential results.
