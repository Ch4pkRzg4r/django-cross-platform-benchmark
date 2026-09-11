# Thesis v366 alignment

This file maps the **v366 minor-revision thesis candidate** to the repository after the independent full-evidence audit of the exact v365 candidate. v366 is a bounded document/provenance/formatting closure. It does not create a new experimental campaign, change the frozen canonical dataset, or replace the validated statistical base.

## Controlling hierarchy

1. **Current thesis document candidate:** v366
   - direct minor-revision successor to the independently audited v365 candidate;
   - incorporates the bounded M01–M08 correction set (provenance, route interpretation, access/fixture wording, Nginx reproduction boundary, repository documentation, raw availability, stale references and figure typography).
2. **Frozen canonical run-level dataset:** `data/canonical/master_runs.csv`
   - 280 rows × 39 fields;
   - SHA-256 `710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7`.
3. **Validated computational base:** byte-exact v330 calibrated pipeline
   - materialiser: `analysis/materialize_v330_pipeline.py`;
   - source SHA-256 `d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574`.
4. **Current computational repository entry point:** `analysis/run_v360_from_repo.py`.
5. **v360 release corrections/carriers:** `analysis/v360_release_corrections.py`.
6. **Historical scripts/namespaces** such as `analysis/ch4_evidence_pipeline.py`, historical figure numbering and exploratory outputs remain provenance records and are not silently promoted to current authority.

The historical computational pin `5cfb18adb04da928bd07517a4f76261fe74246a1` remains a historical pin where cited. The current public branch head is a later repository-closure identity and should be recorded separately from the historical computational pin.

## Frozen primary results retained

The v366 closure does not alter the frozen primary inference:

- 7 platforms × 4 scenarios × 10 retained replications = 280 run-level observations;
- 28 balanced platform-scenario cells;
- 20/20 declared scenario-stratified Kruskal–Wallis tests significant;
- 84 p95 Dunn pairwise comparisons with Holm adjustment within four 21-pair scenario families;
- 23 significant p95 contrasts (A=3, B=5, C=8, D=7);
- Cliff’s delta and rank-based eta-squared retained;
- 140 final percentile-bootstrap intervals use 10,000 resamples under the deterministic seed schedule rooted at 20260603;
- the targeted 279-run sensitivity excluding only `05_koyeb__C_checkout__rep08` retains the same 20 omnibus decisions and the same 23 significant p95 pair set.

## Current Chapter 4 figure crosswalk

The current v366 document ends at **Figure 4.8**, with Figure 4.8 continued across six panels. The historical `results/current-thesis/figure_map.csv` remains a provenance map for the validated wrapper and includes historical numbers through Figure 4.13. It is not the current document numbering.

Use `results/current-thesis/figure_map_v366.csv` for the current document-facing crosswalk:

| v366 figure | current thesis role | retained analytical/source relationship |
|---|---|---|
| 4.1 | Relative p95 latency gap between provider-managed and self-managed paths | descriptive family contrast from current cell-level p95 evidence. |
| 4.2 | Callback-qualified goodput attainment versus nominal offered rate | request/iteration-aware delivery carrier; interpret Scenario C and D with `configuration/SCENARIO_AUTHORITY_V366.md`. |
| 4.3 | Relative callback-qualified goodput gap | descriptive family contrast from callback-qualified goodput cell summaries. |
| 4.4 | Temporal diagnostics: warm-up and post-idle panels | `data/supplementary/warmup_transient*.csv` and `coldstart_raw.csv`; descriptive/supplementary evidence. |
| 4.5 | Scenario-D burst-phase p95 relative to baseline | `data/supplementary/timeseries_burst_recovery.csv`; phase-level descriptive carrier. |
| 4.6 | Median p95 with 95% percentile-bootstrap intervals | final 28-cell p95 interval carrier; 10,000-resample percentile bootstrap. |
| 4.7 | Conditional warm-cost versus scenario-specific median p95 | conditional cost model + scenario-specific p95 medians; one platform-level cost repeated across scenarios is one modelled quantity, not four observations. |
| 4.8(a–f) | Six-panel scenario-specific metric profile | descriptive 28-cell metric/rank carrier; no composite overall ranking. |

The exact v366 embedded publication rasters are document-finalisation artefacts. They do not retroactively satisfy the historical 18-raster wrapper copy gate.

## Workload/rate authority

Final workload-script semantics are documented in `configuration/SCENARIO_AUTHORITY_V366.md`.

- Scenario C uses 10 **iterations/s** and three GET requests per iteration; `rps_actual` and `goodput_rps` are request rates.
- Scenario D uses a staged 5→40→5 iteration/s ramp. The canonical scalar `target_rps=10` is historical metadata and is not the burst-schedule authority.

## Nginx/uWSGI evidence boundary

The retained Nginx/uWSGI files conflict if combined literally: the retained uWSGI INI uses TCP 127.0.0.1:3031 and 4×2, while the retained Nginx configuration expects a UNIX socket and the thesis/current nominal target is 2×4. No exact benchmark-time 2×4 UNIX-socket uWSGI capture was recovered.

Historical/current files remain unchanged. `configuration/reproduction/nginx-uwsgi-v366/` is an internally consistent **prospective public rerun recipe** (UNIX socket, 2 processes × 4 threads, repository-root build context). It resolves reproduction ambiguity without becoming retroactive campaign proof.

## PERMANOVA/PERMDISP boundary

The historical multivariate PERMANOVA implementation/carriers were recovered and independently reproduced. No original historical PERMDISP implementation/configuration/output was recovered. Any later centroid-dispersion calculation is explicitly post-hoc audit sensitivity and cannot be represented as the historical procedure. The current thesis therefore qualifies the affirmative historical PERMDISP wording rather than inventing provenance.

## Raw-evidence availability

The current submission evidence does **not** provide a complete intact raw-request archive. Independent recovery of the four supplied damaged raw ZIPs established 73 complete canonical JSON/CSV run pairs; 207 canonical run pairs were unavailable. Recovered complete members matched the expected canonical raw-file identities and their corresponding canonical rows.

The adjacent raw/archive manifests remain expected-identity records; they do not prove that missing bytes are currently accessible. See `data/raw-archive-manifests/AVAILABILITY_AND_RECONSTRUCTION.md`.

## Public/private and fixture boundary

The source/computational repository is public. Restricted historical credentials, private histories, original identifying database material, provider-private evidence and unrecovered heavy raw data remain separate.

The public fixture is a privacy-safe derivative containing 71 objects across the 15-model application schema, including 17 synthetic user/account objects with unusable passwords. It is **not** the frozen historical database.

## Application-source boundary

An earlier redacted source capture contained a syntax artefact after a variable reference was replaced. The current public `application/commerce/views.py` is a separately reviewed/recovered materialisation that byte-compiles and was exercised during the independent audit. See `ARTEFACT_PROVENANCE.md` and `application/source-recovery/`.

## Evidence boundaries retained

- Historical provider state, complete per-run deployment identity and provider-internal scaling trajectories are not claimed.
- Managed-provider mechanism explanations remain bounded by the observed external deployment outcomes and retained evidence.
- Linux Docker CPU/memory telemetry is scoped to the retained application-container evidence and does not represent the whole system/database/provider infrastructure.
- Cost values remain conditional historical-model assumptions, not invoices/current-price guarantees.
- The post-idle probe is small, managed-only and does not prove provider lifecycle state.
- Callback-qualified success/goodput and latency-only Apdex are not independent business-transaction correctness or user-satisfaction validation.
- The historical 18-raster publication-copy gate remains unverifiable where its exact target rasters are unavailable; current v366 figure QA is performed against the actual v366 document.

## Reproduction rule

Do not “repair” an unavailable historical fact by replacing it with a plausible current configuration. Reproduction derivatives must be explicitly labelled prospective/current; historical bytes and their uncertainties remain preserved. This principle is applied to Nginx/uWSGI, managed-provider configuration, raw archive availability and historical analytical diagnostics.
