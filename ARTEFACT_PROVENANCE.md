# Artefact Provenance

- **Renames from integrity-prefixed evidence copies.** Campaign artefacts were preserved under content-hash-prefixed filenames (e.g. `3CE761554598_scenario_C_checkout.js`). Public copies use their natural names; byte-identity to the campaign-time hashes is verified in `verification/` and the private register.
- **`Dockerfile.v2`, `docker-compose-phase65.yml`.** Exact captured filenames retained: changing them would break provenance against the recorded configuration manifests. `phase65`/`v2` are file-identity tokens, not narrative labels.
- **Application-revision markers.** Verification CSVs quote the literal recorded revision markers (REV5 for the Windows-specific IIS+Waitress deployment; REV6 for the Linux/container family) exactly as returned by the runtime identity endpoint — these are recorded values, not workflow vocabulary.
- **`application/commerce/views.py` does not byte-compile.** The as-built source capture was redaction-processed at collection time; the redactor replaced a password *variable reference* with `[REDACTED]` (lines 341–342), producing a syntax artefact. The file is retained verbatim (no synthetic repair). Deployed behaviour is anchored by the recorded image digests, not by this capture.
- **`k6_binary_identity.txt`** is a header-neutralised copy of the author's capture; every value (path, size, SHA-256, timestamps, version output) is verbatim.

- **`analysis/ch4_evidence_pipeline.py` internal comments** contain the historical package tokens `v154`/`thesis-mirror`. The file is hash-anchored source evidence (SHA-256 a1c2583d…, the exact thesis-recorded value); editing its bytes would break provenance, so it is retained verbatim. These tokens are file-internal history, not repository vocabulary.
- **`analysis/historical-provenance/`** holds `phase3_inferential.py` strictly as historical analytical provenance; the controlling path is `run_analysis.py` + `ch4_evidence_pipeline.py` (author-designated controlling copy).

- **Historical local paths.** `verification/RUN_MANIFEST.json` (and, where present, other verbatim evidence artefacts) contain local filesystem paths from the original execution machine. These are historical execution metadata, not live credentials, and do not imply the paths exist for any other user; the files are labelled historical evidence artefacts and retained byte-exact.
