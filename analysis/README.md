# Analysis directory

## Current computational authority

The repository deliberately separates the **document version** from the **computational release layers**.

- Current thesis document candidate: **v366** (minor-revision closure of the independently audited v365 candidate).
- Current repository computational entry point: **v360**.
- Frozen validated computational base: **v330**.

The byte-exact v330 calibrated end-to-end pipeline remains the frozen numerical base. Its validated source SHA-256 is:

`d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574`

Materialise and verify that frozen source with:

```bash
python materialize_v330_pipeline.py
```

The current repository-aware entry point is:

```bash
python run_v360_from_repo.py
```

To execute the full frozen base before the v360 release layer, follow `REPRODUCIBILITY.md`; exact resource-table reproduction additionally requires the controlled 120-run Docker telemetry archive.

## What each layer controls

### v330 — frozen validated base

The byte-exact v330 pipeline prepares/validates the analytical frame, performs the scenario-stratified inferential analysis and produces the frozen analytical/table carriers. For the frozen 280×39 input it reproduces the controlling primary inference, including:

- 20 scenario-stratified Kruskal–Wallis tests;
- 84 p95 Dunn comparisons with Holm adjustment within each scenario’s 21-pair family;
- 23 significant p95 contrasts;
- Cliff’s delta and rank-based eta-squared;
- 140 percentile-bootstrap intervals using 10,000 resamples under the controlling deterministic seed schedule;
- the validated numerical components underlying Tables 4.1–4.16 in the historical wrapper namespace.

### v360 — current computational release layer

`run_v360_from_repo.py` invokes `v360_release_corrections.py` over the frozen canonical data. It corrects/re-expresses a small set of independently adjudicated release carriers without rewriting the v330 base or the 280×39 dataset. These include the run-level tail-ratio carrier, completed-iteration shortfall, the p95 cell-coordinate carrier and the historical rank/tie carrier.

### v366 — document/evidence alignment, not a new statistical model

The v366 minor-revision closure updates document/repository provenance wording, current-figure mapping, raw-availability disclosure, the complete data dictionary and a prospective Nginx/uWSGI reproduction recipe. It does **not** introduce a new inferential pipeline and does not change the frozen primary numerical results.

## Historical and focused utilities

`run_analysis.py`, `phase1_validation.py`, `phase2_eda.py`, `ch4_evidence_pipeline.py`, `analyze_coldstart.py` and `analyze_timeseries.py` are retained because they document analytical development/provenance and some remain useful focused utilities. They must not be mistaken for the current repository entry point.

`historical-provenance/` contains explicitly superseded analytical code. Historical BCa/bootstrap, ranking and other exploratory outputs remain provenance records where retained; they do not replace the final percentile-bootstrap convention or the controlling scenario-stratified analysis.

See `../REPRODUCIBILITY.md` and `../THESIS_V366_ALIGNMENT.md` for the complete hierarchy and evidence boundaries.
