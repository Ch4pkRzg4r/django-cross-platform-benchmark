# Analysis directory

## Current script-of-record

The final-thesis controlling analysis is **v330**.

Validated source SHA-256:

`d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574`

Because this update was transferred through an integrity-preserving text transport, the byte-exact source is stored in `v330-payload/`. Materialise and verify it with:

```bash
python materialize_v330_pipeline.py
```

Then use the repository-aware runner:

```bash
python run_v330_from_repo.py
```

For the full scoped resource summary, provide the controlled 120-run telemetry archive:

```bash
python run_v330_from_repo.py --docker-stats /path/to/docker_stats.zip
```

## What v330 controls

The pipeline prepares/validates the analytical frame, emits EDA diagnostics, performs the current scenario-stratified inferential analysis, produces the current Chapter-4 table carriers and dynamically regenerates the current figure carriers. Compatible changes to the source analytical data propagate through these outputs.

For the frozen thesis input it was validated against the current thesis: 20 Kruskal–Wallis tests, 84 Dunn/Holm p95 comparisons, 23 significant p95 contrasts, 140 bootstrap intervals and Tables 4.1–4.16.

## Earlier files

`run_analysis.py`, `phase1_validation.py`, `phase2_eda.py`, `ch4_evidence_pipeline.py`, `analyze_coldstart.py` and `analyze_timeseries.py` are retained because they document the analytical development/provenance and some remain useful as focused utilities. They must not be mistaken for the current final-thesis controlling pipeline.

`historical-provenance/` contains explicitly superseded analytical code.
