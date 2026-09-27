# Data Availability

**Raw-data access:** the complete retained k6 JSON/CSV collection is stored in the author's [raw-data archive on Google Drive](https://drive.google.com/drive/folders/1jAqu_W0vK0bgscBe5DE6t67NCMf2Sfhd). GitHub hosts the code, canonical analytical dataset, supplementary inputs and integrity manifests. Google Drive permissions govern download access; if prompted, request access from the author through Google Drive.

| Asset | Status |
|---|---|
| Canonical 280×39 dataset (`data/canonical/master_runs.csv`) | **Public in this repository**; SHA-256 `710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7` |
| Small supplementary inputs (post-idle, burst-recovery, warm-up) | **Public in this repository** under `data/supplementary/`; provenance/correction notes retained where applicable |
| Per-file SHA-256 manifests for the raw campaign, run logs, Docker telemetry and historical archive parts | **Public in this repository** under `data/raw-archive-manifests/`; manifests record expected identities but do not prove present possession of all corresponding bytes |
| Full retained per-run k6 JSON/CSV archive | **Stored separately on Google Drive:** [raw-data archive on Google Drive](https://drive.google.com/drive/folders/1jAqu_W0vK0bgscBe5DE6t67NCMf2Sfhd). Complete 280 JSON/CSV run pairs (560 files), in five JSON and three CSV RAR volumes; all eight volumes and all 560 files were checked against the retained size and SHA-256 manifests. These archives are not distributed as ordinary Git content. See `data/raw-archive-manifests/AVAILABILITY_AND_RECONSTRUCTION.md`. |
| Historical run-log layer | Integrity-manifested/controlled evidence. The public repository does not claim that every historical log byte is present as ordinary Git content. |
| Full 120-run Linux Docker resource telemetry | **Controlled external evidence** because of size; required for exact reproduction of the scoped Linux resource summary. GitHub contains representative/sample material plus integrity manifests. |
| Current thesis embedded figure assets | Document-finalisation artefacts in the controlling DOCX/PDF/evidence package; current document mapping is in `results/current-thesis/figure_map_v366.csv`. |
| Historical 18-raster wrapper publication targets | Historical regression dependency; the exact target raster set was not fully recovered in the audited submission evidence and is not silently replaced by newer v366 rasters. |
| Sensitive items (credentials, private histories, invoices, original identifying account data, provider-private material) | **Not published**. Public-safe derivatives/redactions are documented in `SECURITY_AND_REDACTION.md`. |

## Release boundary

The source/computational repository is public. The complete retained raw-request archive is stored separately on Google Drive under the access conditions stated above. Public repository access does not imply unrestricted access to sensitive historical data or preservation of all provider-internal state.

The current evidence state is:

- complete frozen analytical dataset available and hash-identified;
- computational base/release code available;
- small supplementary carriers available;
- complete retained raw-request collection (280/280 canonical JSON/CSV pairs) stored on Google Drive;
- all eight archive volumes and all 560 per-run file sizes/hashes verified against the retained integrity manifests;
- full Linux Docker telemetry controlled externally;
- provider-internal historical state and some exact deployment continuity unreconstructible after the campaign.

## Using the raw archive

Download all parts of the required RAR set from the linked Google Drive folder and verify them against the repository manifests before extraction and analysis. See `data/raw-archive-manifests/AVAILABILITY_AND_RECONSTRUCTION.md` for the file groups and verification steps.

This file describes current retained-data availability. Version-specific audit and alignment records describe their historical evidence packages and do not supersede this statement. Complete retained-run availability is distinct from a complete immutable history of every attempted, replaced or excluded run.
