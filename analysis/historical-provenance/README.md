# Historical analytical provenance

This directory contains superseded analytical material retained for auditability only.

`phase3_inferential.py` records an earlier inferential phase. Earlier root-level components such as `run_analysis.py` and `ch4_evidence_pipeline.py` also document the development history of the analysis, but they are **not the current script-of-record** for the final thesis.

The current controlling analysis is the validated **v330 calibrated end-to-end pipeline**, reconstructed and integrity-checked with:

```bash
python ../materialize_v330_pipeline.py
```

Expected controlling-source SHA-256:

`d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574`

Do not use historical copies to regenerate the current final-thesis Chapter-4 results.
