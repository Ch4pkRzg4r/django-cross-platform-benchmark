# Recovered application support source — v365

This directory records application files recovered from the retained `public_release_stage/ecommerce_migrated_public_clean.tar.gz` archive supplied for repository-completeness work.

Source archive SHA-256:

`3b4d15c1f9e200e9cc93fe13cb344f18dffa2ffb1893fb1e0929d6e2dbe0393f`

The archive was captured with the retained environment manifest on 2026-06-24. Its Git status recorded modified `commerce/views.py` and `ecommerce/urls.py` and several untracked deployment files. Therefore this material must **not** be described as a byte-exact benchmark-time repository snapshot.

A content-level review found that the nominally `public_clean` archive is **not safe for wholesale publication**: `docker-compose-phase65.yml` contains credential-shaped hard-coded values and some documentation contains password examples. The raw archive is therefore not committed to ordinary Git.

The safe recovery process only promotes independently reviewed support files that contain no credential-shaped values. These include project/app support modules, migrations, templates and template tags. Existing controlling benchmark-relevant source files in `application/` are not silently replaced by the recovery bundle.

Binary decorative static assets and the historical raw build logs are not required for the k6 benchmark request paths and are not promoted by this recovery step. The full retained source archive remains controlled evidence.

This recovery step does not change the frozen 280×39 canonical dataset or any validated thesis result.

## Carrier integrity repair — 10 September 2026

The earlier text carrier on `repo-completeness-v365` was rejected after its decoded SHA-256 failed the hash gate. The carrier was rebuilt from the retained source archive SHA-256 `3b4d15c1f9e200e9cc93fe13cb344f18dffa2ffb1893fb1e0929d6e2dbe0393f`. The current `PAYLOAD_MANIFEST.md` records the rebuilt payload SHA-256 and per-file identities. The rejected mismatching decoded hash was never accepted as provenance authority.
