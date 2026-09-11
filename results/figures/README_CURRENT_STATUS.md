# Figure asset status

The PNG assets and `figure_map.csv` already present in this directory are retained as **historical analytical/thesis provenance**. They must not be interpreted as the authoritative current v366 Chapter-4 figure numbering.

The historical validated wrapper map is retained at:

`results/current-thesis/figure_map.csv`

The current v366 document-facing crosswalk is:

`results/current-thesis/figure_map_v366.csv`

The current thesis Chapter 4 ends at Figure 4.8, with Figure 4.8 continued across six panels. Historical wrapper labels such as Figure 4.13 remain visible only to preserve provenance and are not current thesis references.

The frozen computational base and v360 release layer regenerate/check analytical carriers from the frozen canonical dataset. The exact v366 embedded publication rasters are document-finalisation artefacts and are not silently substituted into the historical wrapper’s publication-raster gate.

`results/current-thesis/verification/PUBLISHED_FIGURE_SHA256_MANIFEST.csv` therefore remains the manifest for its **historical wrapper dependency**. The fact that those historical target rasters are not all present in the current submission evidence does not convert newer v366 rasters into byte-identical replacements.

This separation is intentional:

- changed analytical data must regenerate changed analytical carriers;
- historical bytes remain labelled historical;
- current document numbering is recorded in the v366 crosswalk;
- current embedded figure appearance is verified against the actual v366 DOCX/PDF, not inferred from a stale filename namespace.
