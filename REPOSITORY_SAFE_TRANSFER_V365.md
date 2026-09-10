# Repository Safe Transfer v365

This note records the content-level review of `REPO_SAFE_SOURCE_EXPORT_V365.zip` supplied on 2026-09-10 and the safe repository additions made from it. It does not change the frozen analytical dataset or validated thesis results.

## Transfer package integrity

The transfer contained 20 files and the public application archive matched its prior inventory hash:

`ecommerce_migrated_public_clean.tar.gz`  
SHA-256 `3b4d15c1f9e200e9cc93fe13cb344f18dffa2ffb1893fb1e0929d6e2dbe0393f`

The retained environment manifest records capture time `2026-06-24T00:57:40+03:00`, Git commit `9555ac78b174175a2d213533f59700e71fb11cab`, modified `commerce/views.py` and `ecommerce/urls.py`, and several untracked deployment files. The archive is therefore a retained post-campaign source snapshot, not a byte-exact whole-tree benchmark-time attestation.

## Whole-archive publication decision

The nominally `public_clean` tar archive is **not safe for wholesale promotion**. Content review found hard-coded credential-shaped values in `docker-compose-phase65.yml` and password examples in documentation. The raw tar archive remains controlled evidence and is not committed to ordinary Git.

A reviewed 43-file application-support subset was created from the source archive. It contains support modules, migrations, templates and template tags and passed content-level secret scanning and Python byte-compilation. Existing controlling core source files are not silently replaced by this recovered subset. The reviewed subset is stored through a hash-verified materializer under `application/source-recovery/`.

The recovered `ecommerce/gunicorn_conf.py` was also promoted directly because the repository Docker configuration references that module and it contains no secret-bearing content.

## Safe runnable settings derivative

`application/ecommerce/settings.py` and `settings.PUBLIC.py` are explicit public repository derivatives. Runtime secret and database password values are required from the environment rather than embedded. `.env.example` provides placeholders only. These files are for safe rerunning and are not claimed as byte-exact benchmark-time settings files.

## Fly.io

Raw source SHA-256:

`7760d48f66c207e73d9a2e41fe6df0dbe80968b736cd148119719517bd18f300`

The raw `fly.toml` was not promoted because it carried sensitive assignments. A reviewed `configuration/platforms/06_flyio/fly.PUBLIC.toml` derivative preserves the recorded deployment semantics while redacting the app name, database endpoint and credentials. Its provenance file records the source hash and derivative boundary.

## IIS + Waitress

Safe IIS/Waitress evidence from the retained 2026-06-22 alignment capture was reviewed and selected. Repository additions include a redacted `web.config.PUBLIC.xml`, the retained memory-limit configuration script, the Waitress/Python dependency capture, runtime versions, active Waitress process command, IIS module list, safe site-state capture and process-memory snapshot.

These files strengthen configuration auditability but do **not** prove that a hard 2-GiB Job Object limit was effectively enforced for every historical benchmark run. The thesis boundary remains controlling: intended policy/configuration is recorded; complete benchmark-time continuity and effective-cap verification are not asserted.

## Remaining gaps before repository-completeness closure

1. `load_data.py` is retained, but the referenced `datadump.json` fixture is not yet in the repository. The local inventory records a candidate fixture with SHA-256 `dbe1b8628aadf3832774dfe224930ddf40f06892a1453757dc61f830376b0d42`; it requires a dedicated PII/credential review before any promotion.
2. Static/media source assets were not bulk-promoted. They are not part of the k6 browserless request census, but a complete visual-site source release requires either reviewed assets in Git or a separately hashed/linked asset archive.
3. No exact benchmark-time Azure Container Apps deployment export/Bicep/YAML has been recovered. Current/later configuration facts may be documented as such but must not be promoted to benchmark-time immutable truth.
4. No exact immutable benchmark-time Koyeb service export/digest has been recovered. Retained deployment event/configuration facts remain bounded evidence.
5. `application/Dockerfile.v2` contains an internal Python-version inconsistency: its `FROM` line is `python:3.12-slim` while a comment/label says 3.13. This historical/configuration file must be adjudicated with provenance rather than silently rewritten.
6. `FILE_INDEX.csv` and `MANIFEST_SHA256.csv` must be regenerated after the final branch tree is settled.
7. Current-release CI for the v360 entry point should be added after source/config staging stabilises.

## Preservation rule

No repository-completeness edit is authorised to alter `data/canonical/master_runs.csv`, the byte-exact validated v330 analytical base, or validated inferential results. Historical and current-state evidence must remain explicitly distinguished.
