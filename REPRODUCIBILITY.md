# Reproducibility

Supported today: integrity verification of every listed artefact (`sha256sum -c` against `MANIFEST_SHA256.csv`), inspection of benchmark and configuration sources, and deterministic re-derivation of the Chapter-4 exhibits from `data/canonical/master_runs.csv` using the retained analysis scripts (fixed bootstrap base seed 20260603; scenario-stratified Kruskal–Wallis, Dunn with Holm adjustment, and Cliff’s delta).

Not supported, by design and disclosed: re-execution of the historical cloud campaign (provider-internal state, historical managed-platform digests and some benchmark-time transients are unobservable or unrecorded). The load generator is identified by version and a continuity-bridged SHA-256 (`verification/k6_binary_identity.txt`).

Raw-archive integrity: `7z t "raw data excel.part001.rar"` (volumes must sit together) and per-file verification against `data/raw-archive-manifests/raw_files_sha256_manifest.csv`.
