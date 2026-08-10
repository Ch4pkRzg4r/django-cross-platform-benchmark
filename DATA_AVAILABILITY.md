# Data Availability

| Asset | Status |
|---|---|
| Canonical 280×39 dataset (`data/canonical/master_runs.csv`) | **In this private repository**; SHA-256 `710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7` |
| Small supplementary inputs (post-idle, burst-recovery, warm-up) | **In this private repository** under `data/supplementary/`; thesis-recorded hashes retained |
| Per-file SHA-256 manifests for the raw campaign, run logs, Docker telemetry and archive parts | **In this private repository** under `data/raw-archive-manifests/` |
| Full original per-run k6 JSON/CSV archive | **Retained as controlled evidence outside ordinary Git history** because of size; no public URL is claimed until the archive is uploaded, completeness-checked and approved for release |
| 280 retained run logs | **Retained in the controlled evidence package** and indexed by repository manifests |
| Full 120-run Docker resource telemetry | **Retained in the controlled evidence package**; required for exact reproduction of the scoped Table 4.11 resource summary; GitHub contains a representative sample plus integrity manifests |
| Exact final-thesis reference assets used only for frozen-output regression | **Retained in the controlled thesis/evidence package**; not used as analytical inputs |
| Sensitive items (credentials, private histories, invoices, provider identifiers that should not be disclosed) | **Not published** |

## Release boundary

This repository is currently private and intended for thesis supervision/examination. The heavy raw archive is deliberately separated from normal Git history. A Google Drive evidence structure has been prepared for controlled transfer, but this repository does **not** claim that the full raw archive has already been uploaded or that a public raw-data URL exists.

When the complete raw archive is staged, the release audit should verify: 7 platforms × 4 scenarios × 10 retained replications, JSON/CSV pairing, run-ID uniqueness, naming/timestamp consistency, parser compatibility, raw-to-canonical reconciliation and the frozen `master_runs.csv` SHA-256.
