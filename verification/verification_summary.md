# Verification Summary (neutral)
- Canonical dataset: 280 rows × 39 columns; 28 platform-scenario cells × 10 replications; unique run identifiers; SHA-256 equals the thesis-recorded value.
- Benchmark scripts and parser: byte-identical to the campaign-time integrity manifest; Scenario C contains three GET requests and zero POST operations.
- Table reconciliation: the medians of Tables 4.2 and 4.3 re-derive exactly (28/28 rows each) from the canonical dataset in an independent environment.
- Load generator: version v2.0.0-rc1 with a continuity-bridged SHA-256 capture (`k6_binary_identity.txt`).
- Configuration truth tables quote the recorded runtime identity values verbatim.

- Table mirrors: full-precision sources of the printed tables; Tables 4.2 and 4.3 mirrors reconcile 28/28 each against the canonical dataset (printed thesis values are their roundings). Tables 4.10, 4.11 and 4.15 have no distinct CSV in the retained collection and are documented accordingly.
- Figure map: 26 body figures ↔ media files, 26/26 hash-matched, generated from the controlling DOCX relationships; three non-figure media items are inventoried separately under documentation/.

- Analysis set complete: five controlling artefacts installed at their exact thesis-recorded SHA-256 values; phase-3 retained strictly as historical provenance.
