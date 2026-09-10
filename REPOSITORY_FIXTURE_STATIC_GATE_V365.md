# Repository Fixture and Static Gate v365

This note records the metadata-only fixture/static gate performed on 2026-09-10. It does **not** publish the raw historical fixture or static binaries.

## Fixture identity

- Source: retained `ecommerce_migrated/datadump.json`
- Size: 18,445 bytes
- SHA-256: `dbe1b8628aadf3832774dfe224930ddf40f06892a1453757dc61f830376b0d42`
- Identity check against the prior local inventory: **PASS**
- Objects: **71**
- Models: **15**

The raw fixture is **not suitable for direct publication**. The structure-only privacy scan found 138 field/pattern rows requiring review, including:

- 17 `auth.user` records containing password hashes, usernames, names and email fields;
- 10 profile records with biography, birth-date and location fields;
- contact information/messages/person records containing email/phone/address/message fields;
- order/payment records linked to users.

Actual pattern hits include 17 Django password hashes and 23 email-like values. No raw values were transferred during this gate.

The benchmark workload itself does not require real personal credentials: the retained k6 scenarios are GET-only; the mixed scenario fetches the admin login page without submitting credentials, and the checkout-path scenario accepts the unauthenticated cart redirect. Therefore a **sanitised fixture derivative** can support application reconstruction without exposing the historical personal fields, provided primary/foreign-key structure and non-sensitive benchmark-relevant content are preserved.

## Static tree

- Files: **73**
- Total size: **17,063,611 bytes**
- Text files flagged for possible secrets: **0**

The static tree includes CSS/JS, images, a video and third-party-looking font assets. The secret-scan result is favourable, but **zero secret flags is not a redistribution/licensing clearance**. Static binaries should therefore be staged only after a transfer review, with a licensing/provenance boundary recorded for any third-party assets before a public release.

## Decision

1. Do **not** commit raw `datadump.json`.
2. Produce a deterministic `datadump.PUBLIC.json` derivative from the verified source hash, replacing/removing personal identifiers and password material while preserving model cardinality, PK/FK relationships and benchmark-relevant non-sensitive fields.
3. Package the 73 static files for inspection on the private completeness branch; do not yet describe them as cleared for public redistribution.
4. Record derivative provenance and source hash.
5. After content review, stage the sanitised fixture and approved static assets, then regenerate `FILE_INDEX.csv` and `MANIFEST_SHA256.csv`.

This gate does not alter the frozen 280×39 canonical benchmark dataset or the validated statistical analysis.