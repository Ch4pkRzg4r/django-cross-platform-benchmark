# v330 validated source payload

The byte-exact validated `thesis_analysis_pipeline_v330_calibrated.py` source is stored in five gzip/base64 payload parts in this directory. Reconstruct it with:

```bash
python analysis/materialize_v330_pipeline.py
```

Expected reconstructed source SHA-256:

`d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574`

This payload representation is an integrity-preserving transport form. It is not analytical input, and the materializer verifies the reconstructed bytes before writing the Python source.
