# Artefact Provenance

- **Renames from integrity-prefixed evidence copies.** Campaign artefacts were preserved under content-hash-prefixed filenames (e.g. `3CE761554598_scenario_C_checkout.js`). Public copies use their natural names; byte-identity to the campaign-time hashes is verified in `verification/` and the private register.
- **`Dockerfile.v2`, `docker-compose-phase65.yml`.** Exact captured filenames retained: changing them would break provenance against the recorded configuration manifests. `phase65`/`v2` are file-identity tokens, not narrative labels.
- **Application-revision markers.** Verification CSVs quote the literal recorded revision markers (REV5 for the Windows-specific IIS+Waitress deployment; REV6 for the Linux/container family) exactly as returned by the runtime identity endpoint — these are recorded values, not workflow vocabulary.
- **`application/commerce/views.py` does not byte-compile.** The as-built source capture was redaction-processed at collection time; the redactor replaced a password *variable reference* with `[REDACTED]` (lines 341–342), producing a syntax artefact. The file is retained verbatim (no synthetic repair). Deployed behaviour is anchored by the recorded image digests, not by this capture.
- **`verification/k6_binary_identity.txt`.** This is a later, current-only capture of the load-generator executable identity (path, size, SHA-256, timestamps and version output). It is useful current evidence but is **not** a benchmark-time, continuity-bridged identity proof for the historical campaign.

## Analytical authority map

Three analytical roles are intentionally separated:

1. **Historical evidence wrapper — not current executable authority.** `analysis/ch4_evidence_pipeline.py` is retained verbatim because its bytes and SHA-256 are historically anchored. Internal tokens such as `v154`/`thesis-mirror` are file-internal history, not current repository vocabulary.
2. **Frozen validated computational base.** The byte-exact v330 calibrated end-to-end pipeline is materialised by `analysis/materialize_v330_pipeline.py` and executed through `analysis/run_v330_from_repo.py`. Its source SHA-256 is documented in `REPRODUCIBILITY.md` and must remain byte-exact.
3. **Current v360 release authority.** `analysis/run_v360_from_repo.py` is the current repository entry point. It invokes `analysis/v360_release_corrections.py` for the adjudicated release-layer carriers over the frozen canonical dataset. These release-layer corrections do not rewrite the v330 base or the historical campaign evidence.

`analysis/run_analysis.py`, `analysis/ch4_evidence_pipeline.py` and files under `analysis/historical-provenance/` remain available for historical provenance or earlier workflow context; they are not promoted to the current v360 executable authority.

- **Historical local paths.** `verification/RUN_MANIFEST.json` (and, where present, other verbatim evidence artefacts) contain local filesystem paths from the original execution machine. These are historical execution metadata, not live credentials, and do not imply the paths exist for any other user; the files are labelled historical evidence artefacts and retained byte-exact.
