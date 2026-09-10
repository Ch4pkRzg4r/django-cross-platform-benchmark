# Privacy-safe fixture provenance (v365)

Historical source fixture SHA-256: `dbe1b8628aadf3832774dfe224930ddf40f06892a1453757dc61f830376b0d42`.

The raw historical `datadump.json` is deliberately **not** committed because it contains real-looking account/contact data and Django password hashes. The repository file `datadump.PUBLIC.json` is a deterministic privacy-safe derivative for reproduction/demo use only; it is not represented as the frozen historical database dump.

Independent validation of the v2 derivative established:

- 71 objects across 15 models, matching the source fixture cardinality;
- 17 `auth.user` records mapped one-to-one to unique synthetic usernames;
- all 17 passwords replaced by Django's unusable-password marker `!`;
- 22 natural-key User relations rewritten and resolved consistently;
- model/PK ordering preserved;
- zero original username values remaining;
- zero Django password-hash patterns remaining;
- zero private-key or token-assignment patterns remaining;
- all email values restricted to the reserved `example.invalid` domain.

The repository JSON is a compact serialization of the validated v2 derivative. Formatting therefore differs from the transfer-package copy, while the record content is equivalent.

Use `python load_public_fixture.py` after migrations. Set `RESET_BEFORE_FIXTURE_LOAD=true` only for a disposable reproduction database if a flush is intended. The historical `load_data.py` is retained as provenance and is not the recommended public-fixture loader.
