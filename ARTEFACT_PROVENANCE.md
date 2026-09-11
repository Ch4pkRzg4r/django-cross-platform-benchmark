# Artefact Provenance

- **Renames from integrity-prefixed evidence copies.** Campaign artefacts were preserved under content-hash-prefixed filenames (for example `3CE761554598_scenario_C_checkout.js`). Public copies use their natural names; byte-identity to the retained campaign hashes is recorded in `verification/` and the historical/private evidence register where available.
- **`Dockerfile.v2`, `docker-compose-phase65.yml`.** Historical filenames are retained because renaming/re-writing them would blur provenance against recorded configuration manifests. `phase65`/`v2` are file-identity tokens, not claims that each file is current authority.
- **Application-revision markers.** Verification CSVs quote literal recorded revision markers (REV5 for the Windows-specific IIS+Waitress deployment; REV6 for the Linux/container family) exactly as captured by the runtime identity evidence. They are recorded values, not workflow vocabulary.
- **Historical `application/commerce/views.py` capture artefact versus current recovered source.** An earlier retained source capture was redaction-processed and replaced a password-variable reference with `[REDACTED]`, producing a syntax artefact in that historical capture. The **current public `application/commerce/views.py` is a separately reviewed/recovered source materialisation**: it byte-compiles and was exercised by the independent v365 audit. The historical syntax artefact therefore belongs to the earlier capture only and must not be described as a defect in the current public file. See `application/source-recovery/` and `REPOSITORY_CLOSURE_V365.md`.
- **`verification/k6_binary_identity.txt`.** This is a later current-only capture of the load-generator executable identity (path, size, SHA-256, timestamps and version output). It is useful current evidence but is **not** a benchmark-time, continuity-bridged executable identity proof for the historical campaign.

## Analytical authority map

Four roles are intentionally separated:

1. **Historical analytical/exhibit wrappers — not current executable authority.** `analysis/ch4_evidence_pipeline.py` and `analysis/historical-provenance/` are retained because their bytes and outputs document analytical development. Internal tokens such as `v154`, historical BCa references or older figure numbers are provenance, not current thesis vocabulary.
2. **Frozen validated computational base.** The byte-exact v330 calibrated end-to-end pipeline is materialised by `analysis/materialize_v330_pipeline.py` and can be executed through `analysis/run_v330_from_repo.py`. Its source SHA-256 is documented in `REPRODUCIBILITY.md` and remains byte-exact.
3. **Current computational release layer.** `analysis/run_v360_from_repo.py` is the current repository computational entry point and invokes `analysis/v360_release_corrections.py` for adjudicated release-layer carriers over the frozen canonical dataset. These corrections do not rewrite the v330 base or the historical campaign evidence.
4. **Current document/evidence alignment.** The v366 document-facing alignment (`THESIS_V366_ALIGNMENT.md`, the complete data dictionary, current figure crosswalk and prospective Nginx/uWSGI reproduction recipe) corrects provenance/interpretation documentation without creating a new statistical pipeline or rewriting historical files.

`analysis/run_analysis.py`, `analysis/ch4_evidence_pipeline.py` and files under `analysis/historical-provenance/` remain available for historical provenance or earlier workflow context; they are not promoted to current v360 executable authority.

## Configuration provenance rule

A retained configuration file is not automatically benchmark-time authority merely because it is executable or plausible. This rule is particularly important for Nginx/uWSGI: the retained `configuration/uwsgi.ini` uses TCP `127.0.0.1:3031` with 4 processes × 2 threads, while `configuration/nginx-uwsgi.conf` expects a UNIX socket and the thesis/current nominal target is 2 processes × 4 threads. Those historical/current files are preserved as found. `configuration/reproduction/nginx-uwsgi-v366/` is an explicitly **prospective public reproduction derivative** that makes the target topology internally consistent; it is not retroactive proof of the campaign-time Nginx/uWSGI variant.

## Historical local paths

`verification/RUN_MANIFEST.json` (and, where present, other verbatim evidence artefacts) contain local filesystem paths from the original execution machine. These are historical execution metadata, not live credentials, and do not imply the paths exist for another user. Such files remain labelled historical evidence artefacts and are retained byte-exact where provenance requires it.
