# Repository Fixture + Static Transfer Review v365

Review date: 2026-09-10  
Reviewed transfer: `REPO_PUBLIC_FIXTURE_STATIC_TRANSFER_V365.zip`

## Transfer integrity

The uploaded transfer ZIP was opened and checked independently. It contains 78 files: one proposed public fixture, one sanitisation report, 73 static assets, two manifests, and one transfer-boundary README.

- transfer manifest: PASS (all listed sizes and SHA-256 values matched the ZIP contents; no unlisted payload files)
- static manifest: PASS (73/73 files matched their manifest size and SHA-256)
- static aggregate: 73 files, 17,063,611 bytes
- static secret scan reported by the prior gate: 0 flags

## Fixture decision: REJECT CURRENT DERIVATIVE

`fixture/datadump.PUBLIC.json` must **not** be promoted in its current form.

The historical fixture was exported using Django natural keys for `auth.user`: the 17 user records have no numeric `pk`, and related objects refer to users by singleton natural-key values such as `["<username>"]`.

The first sanitiser incorrectly generated replacement usernames from `pk`. Because those 17 user records have no `pk`, every user became the same value `benchmark_user_`, while 22 `user` relation fields across cart/profile/order records retained 12 distinct historical natural-key usernames. Therefore the proposed derivative has two defects:

1. it is not relationally loadable as a faithful natural-key fixture because user natural keys no longer match the related records;
2. it still exposes historical usernames through natural-key foreign-key values.

The sanitisation report's statement that known relation fields were "preserved" is therefore insufficient: byte-preserving the original natural-key relation values preserved sensitive identifiers while breaking their link to the newly sanitised user records.

Required correction: construct a deterministic one-to-one mapping from every original `auth.user.fields.username` to a unique synthetic username, replace the username in each user record, and rewrite every matching Django natural-key relation consistently. Then verify that (a) all 17 synthetic usernames are unique, (b) every user natural-key relation resolves to one of those usernames, (c) no original username remains anywhere in the derivative, and (d) the 71-record / 15-model structure and all non-user PK/FK identities remain intact.

The raw historical `datadump.json` remains excluded from GitHub.

## Static decision

The static payload passed identity and secret checks, but it contains binary images/video and third-party-looking font/theme assets. No redistribution licence evidence was present in the transfer package. Therefore the binary static tree is **not promoted by this review**.

For repository reproducibility, a byte-level manifest is retained. The static assets can later be restored to the private repository from the verified local source if desired. Before any future public release, licence/provenance for the images, video, theme CSS/JS and bundled fonts must be adjudicated.

This static boundary does not affect the thesis numerical benchmark: the retained k6 campaign targets Django HTTP routes and the frozen 280 x 39 canonical dataset and validated inferential results remain unchanged.

## Next gate

1. Run the corrected natural-key-aware fixture builder against the exact historical fixture SHA-256 `dbe1b8628aadf3832774dfe224930ddf40f06892a1453757dc61f830376b0d42`.
2. Review the corrected `datadump.PUBLIC.json` for unique synthetic users, relation resolution and privacy regression.
3. Retain the static SHA-256 manifest in Git; do not claim public redistribution clearance for the binary static payload without licence evidence.
4. Continue with application materialisation/runnable QA, V16 repository-only correction, ACA/Koyeb evidence-boundary documentation, current-release CI, and regeneration of `FILE_INDEX.csv` / `MANIFEST_SHA256.csv`.

No change to the frozen 280 x 39 canonical dataset or scientific conclusions is authorised by this review.
