# Data Availability

| Asset | Status |
|---|---|
| Canonical 280×39 dataset (`data/canonical/master_runs.csv`) | **Public in this repository**; SHA-256 `710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7` |
| Small supplementary inputs (post-idle, burst-recovery, warm-up) | **Public in this repository** under `data/supplementary/`; provenance/correction notes retained where applicable |
| Per-file SHA-256 manifests for the raw campaign, run logs, Docker telemetry and historical archive parts | **Public in this repository** under `data/raw-archive-manifests/`; manifests record expected identities but do not prove present possession of all corresponding bytes |
| Full original per-run k6 JSON/CSV archive | **Not completely available in the supplied submission evidence.** Independent recovery of the four damaged supplied ZIPs established 73 complete canonical JSON/CSV run pairs; 207 canonical run pairs were unavailable. See `data/raw-archive-manifests/AVAILABILITY_AND_RECONSTRUCTION.md`. |
| Historical run-log layer | Integrity-manifested/controlled evidence. The public repository does not claim that every historical log byte is present as ordinary Git content. |
| Full 120-run Linux Docker resource telemetry | **Controlled external evidence** because of size; required for exact reproduction of the scoped Linux resource summary. GitHub contains representative/sample material plus integrity manifests. |
| Current thesis embedded figure assets | Document-finalisation artefacts in the controlling DOCX/PDF/evidence package; current document mapping is in `results/current-thesis/figure_map_v366.csv`. |
| Historical 18-raster wrapper publication targets | Historical regression dependency; the exact target raster set was not fully recovered in the audited submission evidence and is not silently replaced by newer v366 rasters. |
| Sensitive items (credentials, private histories, invoices, original identifying account data, provider-private material) | **Not published**. Public-safe derivatives/redactions are documented in `SECURITY_AND_REDACTION.md`. |

## Release boundary

The source/computational repository is public. Public availability of the repository does **not** mean that sensitive historical data, all provider-internal state, or a complete intact 280-run raw-request archive is public or currently recoverable.

The current evidence state is:

- complete frozen analytical dataset available and hash-identified;
- computational base/release code available;
- small supplementary carriers available;
- partial raw-request recovery (73/280 complete canonical run pairs);
- 207 canonical raw pairs unavailable in the supplied submission evidence;
- full Linux Docker telemetry controlled externally;
- provider-internal historical state and some exact deployment continuity unreconstructible after the campaign.

## If additional raw evidence is later recovered

Do not overwrite the damaged submission archives. Test the actual recovered archive/volumes, verify every member against the retained manifests, check 7×4×10 run pairing/uniqueness, and rerun raw-to-canonical reconciliation before claiming a complete raw release or publishing a raw-data URL.
