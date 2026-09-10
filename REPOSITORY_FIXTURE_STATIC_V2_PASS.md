# Fixture/static transfer v2 — PASS

The supplied `REPO_PUBLIC_FIXTURE_STATIC_TRANSFER_V365_V2.zip` was independently unpacked and checked before repository promotion.

## Transfer integrity

- 78 ZIP entries total.
- Transfer manifest covers 77 non-manifest files.
- All 77 recorded SHA-256 values matched the extracted bytes.
- No missing transfer-manifest target was found.

## Privacy-safe fixture

Source historical fixture SHA-256: `dbe1b8628aadf3832774dfe224930ddf40f06892a1453757dc61f830376b0d42`.

Validated derivative properties:

- 71 objects / 15 models;
- 17 unique synthetic `auth.user` natural keys;
- 22 User natural-key relations resolve to those synthetic users;
- 17 password values replaced with Django's unusable-password marker `!`;
- zero Django password-hash patterns;
- zero private-key markers;
- zero token-assignment patterns;
- zero non-`example.invalid` email addresses;
- zero original username values reported by the deterministic sanitiser;
- model cardinality and model/PK sequence preserved.

The repository now contains a compact serialization at `application/datadump.PUBLIC.json`, plus `application/FIXTURE_PUBLIC_PROVENANCE_V365.md` and a dedicated safe loader `application/load_public_fixture.py`. The raw historical fixture remains excluded.

## Static tree

- 73 files;
- 17,063,611 bytes;
- all 73 files matched the earlier static identity manifest;
- 8 text assets were rescanned and passed the secret-pattern gate;
- 65 binary/non-text assets had prior identity hashes verified;
- zero static secret flags.

The static bytes are **not yet promoted through the GitHub connector**, because the connector writes UTF-8 files only and because public redistribution rights for the image/video/font bundle have not yet been fully documented. Their complete SHA-256 inventory is retained in `documentation/STATIC_ASSET_MANIFEST_V365.csv`.

## Related repository-only correction

V16 is closed by adding `data/supplementary/warmup_transient_v365_corrected.csv` and its provenance note while preserving the frozen historical `warmup_transient.csv`. The Fly.io / D_burst one-decimal ratio is 0.5 (`193.2 / 354.4 = 0.545146...`).

No frozen 280×39 canonical-data value or validated inferential result was changed by this gate.
