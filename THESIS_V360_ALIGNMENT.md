# Thesis v360 alignment

This file maps the final v360 thesis release to the repository authority after the independent second adjudication.

## Controlling hierarchy

1. **Frozen canonical run-level dataset**: `data/canonical/master_runs.csv`
   - 280 rows × 39 fields
   - SHA-256 `710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7`
2. **Validated computational base**: byte-exact v330 calibrated pipeline
   - materialiser: `analysis/materialize_v330_pipeline.py`
   - source SHA-256 `d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574`
3. **Current release entry point**: `analysis/run_v360_from_repo.py`
4. **v360 release corrections/carriers**: `analysis/v360_release_corrections.py`
5. **Historical scripts** such as `analysis/ch4_evidence_pipeline.py` remain provenance records and are not the current executable authority.

## v360 release-layer corrections

- Tail inflation is `median_r(p99_r/p50_r)`. The historical v330 appendix carrier's `median(p99)/median(p50)` operator is superseded for that carrier only; the printed thesis Table E.3 already used the intended run-level-ratio estimand.
- Figure 4.1 coordinates are regenerated from the 28 canonical cell median p95 values.
- Delivery shortfall is named **completed-iteration shortfall relative to planned starts** and is not equated with `dropped_iterations` or with a reconstructed actual-start census.
- Figure 4.13 rank carriers use average within-scenario ranks and mark all exact stored-precision ties at the extrema.
- The targeted 279-run sensitivity excludes only `05_koyeb__C_checkout__rep08`; it is a post-campaign diagnostic and does not replace the 280-run primary analysis.

## Main inferential results retained

The v360 release does not alter the frozen primary inference:

- 20/20 declared scenario-stratified Kruskal-Wallis tests remain significant.
- 23 p95 Dunn/Holm contrasts remain significant across four separately adjusted 21-pair scenario families.
- The targeted 279-run sensitivity retains the same 20 omnibus decisions and the same 23-pair p95 set.

## Evidence boundaries

- Historical provider state, complete per-run deployment identity and a complete attempted-run census are not claimed.
- Heavy raw streams and full Docker telemetry remain controlled external evidence rather than ordinary Git content.
- Current/as-built configuration captures are not silently upgraded to benchmark-time per-run proof.
- Native Word/EndNote field refresh and final PDF pagination are document-finalisation steps, not computational analysis steps.
