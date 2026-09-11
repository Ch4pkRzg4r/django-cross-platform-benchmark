# Data Dictionary — `master_runs.csv` (280 rows × 39 columns)

This dictionary documents the frozen canonical run-level dataset used by the controlling analysis. The canonical file SHA-256 is:

`710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7`

Each row is one retained benchmark **run summary / analytical observation**, not one HTTP request. Request-level k6 Point records are reduced into run-level counts, distributions and rates by the historical parser. The frozen file contains 7 platforms × 4 scenarios × 10 retained replications = 280 rows.

## Field definitions

| column | unit / type | definition |
|---|---|---|
| `run_id` | string | Deterministic retained-run identifier: `platform__scenario__repNN`. Unique across the frozen 280-row dataset. |
| `platform` | categorical string | Deployment-path identifier: `01_apache_modwsgi`, `02_nginx_uwsgi`, `03_django_gunicorn`, `04_aca`, `05_koyeb`, `06_flyio`, or `07_iis_waitress`. |
| `scenario` | categorical string | Final retained workload scenario: `A_browse`, `B_mixed`, `C_checkout`, or `D_burst`. `C_checkout` is the final GET-only three-request cart-path scenario despite its historical name. |
| `replication` | integer | Retained replication number within a platform-scenario cell; final design uses 1–10 in every cell. |
| `start_time` | ISO-8601 timestamp | Controller/orchestrator-supplied run-start timestamp. This is provenance metadata and is distinct from the first k6 Point timestamp used to derive the measured Point-stream duration. |
| `end_time` | ISO-8601 timestamp | Controller/orchestrator-supplied run-end timestamp. Distinct from `last_ts`. |
| `test_duration_s` | seconds | Measured retained Point-stream span: `last_ts − first_ts`, rounded to 2 decimal places by the historical parser. It is the denominator for `rps_actual`, `goodput_rps` and `bandwidth_rx_bps`. |
| `target_rps` | historical scalar metadata | Orchestrator-supplied target/rate metadata retained with the run. For A/B/C it represents the configured constant **iteration arrival rate** (20/15/10 iterations/s). In Scenario C each iteration issues three GET requests, so 10 iterations/s is nominally about 30 requests/s before delivery effects. For Scenario D the frozen scalar (`10`) is historical metadata and is **not** the staged schedule authority; the final retained burst script/evidence uses a ramping schedule with baseline 5 and peak 40 iterations/s. |
| `rps_actual` | requests/s | `total_requests / test_duration_s`, rounded to 3 decimals. Because `total_requests` counts request-duration Points, this is achieved **request** rate, not necessarily iteration rate. |
| `goodput_rps` | callback-qualified requests/s | `(total_requests − total_errors) / test_duration_s`, rounded to 3 decimals. “Goodput” here is tied to the configured k6 expected-status callback / `http_req_failed` semantics; it is not independent business-transaction correctness. |
| `total_requests` | count | Number of retained `http_req_duration` Point records in the JSON stream. Used as the run request denominator. |
| `total_errors` | count | Count of retained `http_req_failed` Point records whose value equals 1 under the configured expected-status callback semantics. |
| `error_rate` | fraction 0–1 | `total_errors / total_requests`, rounded to 6 decimals; historical zero-request fallback is 0. Error percentage displayed elsewhere is this fraction × 100. |
| `latency_p50` | ms | 50th percentile of retained `http_req_duration` values using the historical parser’s sorted linear interpolation; rounded to 3 decimals. |
| `latency_p90` | ms | 90th percentile of retained `http_req_duration`; linear interpolation; rounded to 3 decimals. |
| `latency_p95` | ms | 95th percentile of retained `http_req_duration`; primary latency endpoint; rounded to 3 decimals. |
| `latency_p99` | ms | 99th percentile of retained `http_req_duration`; secondary tail endpoint; rounded to 3 decimals. Values at the ~60 s timeout boundary require censoring-aware interpretation. |
| `latency_p999` | ms | 99.9th percentile of retained `http_req_duration`; appendix/diagnostic tail field; rounded to 3 decimals. |
| `latency_mean` | ms | Arithmetic mean of retained `http_req_duration`; rounded to 3 decimals. |
| `latency_min` | ms | Minimum retained `http_req_duration`; rounded to 3 decimals. |
| `latency_max` | ms | Maximum retained `http_req_duration`; rounded to 3 decimals. |
| `latency_stddev` | ms | Sample standard deviation of retained `http_req_duration` values (denominator `n−1`), rounded to 3 decimals when at least two values exist. |
| `latency_cv` | ratio | `latency_stddev / latency_mean` from the unrounded parser calculations, rounded to 6 decimals. Used as a variability diagnostic. |
| `dns_p50` | ms / missing | 50th percentile of retained `http_req_dns` values when present. In the frozen canonical dataset this field is blank/NaN for all 280 rows because no discriminating DNS Point vector was retained. Blank is **not zero**. |
| `dns_p95` | ms / missing | 95th percentile of retained `http_req_dns` values when present. Blank/NaN in all 280 frozen rows; blank is **not zero**. |
| `tcp_p50` | ms | 50th percentile of retained `http_req_connecting` values (TCP connection timing) when present; rounded to 3 decimals. Zero can be a legitimate retained timing value and is not a missing-value code. |
| `tcp_p95` | ms | 95th percentile of retained `http_req_connecting`; rounded to 3 decimals. |
| `tls_p50` | ms | 50th percentile of retained `http_req_tls_handshaking` values when present; rounded to 3 decimals. On non-TLS/reused-connection paths the retained values may be zero/non-discriminating and should be interpreted as diagnostics, not primary outcomes. |
| `tls_p95` | ms | 95th percentile of retained `http_req_tls_handshaking`; rounded to 3 decimals. |
| `waiting_p50` | ms | 50th percentile of retained `http_req_waiting` values (k6 waiting/TTFB component); rounded to 3 decimals. |
| `waiting_p95` | ms | 95th percentile of retained `http_req_waiting`; rounded to 3 decimals. |
| `waiting_p99` | ms | 99th percentile of retained `http_req_waiting`; rounded to 3 decimals. |
| `apdex_t500_f2000` | score 0–1 | Request-level **latency-only Apdex-style** score with T=500 ms and F=2000 ms: `(satisfied + tolerated/2) / total_request_durations`, rounded to 4 decimals. Callback-defined failures are not independently inserted into the Apdex formula, so this field is not a success/transaction metric. |
| `bytes_received` | bytes | Sum of retained `data_received` Point values for the run. |
| `bytes_sent` | bytes | Sum of retained `data_sent` Point values for the run. |
| `bandwidth_rx_bps` | **bytes/s** | Historical field name. The parser stores `bytes_received / test_duration_s`, rounded to 1 decimal; despite the suffix `_bps`, the quantity is **bytes per second, not bits per second**. Chapter 4 displays decimal kB/s only after division by 1,000. |
| `k6_iterations` | count | Sum of retained k6 `iterations` Point values. In A/B/D, one iteration issues one request; in final Scenario C, one iteration issues three GET requests, so `total_requests` is approximately 3× `k6_iterations` before delivery/failure effects. |
| `first_ts` | ISO-8601 timestamp | First timestamp encountered by the historical parser across retained k6 `Point` records, before metric-specific routing. Together with `last_ts` it defines `test_duration_s`. |
| `last_ts` | ISO-8601 timestamp | Last timestamp encountered by the historical parser across retained k6 `Point` records. |

## Final scenario/rate authority

The final campaign semantics are defined by the retained k6 scripts and frozen evidence, not by stale planning text in older configuration metadata. See `../../configuration/SCENARIO_AUTHORITY_V366.md`.

| scenario | arrival semantics | request semantics relevant to rate interpretation |
|---|---|---|
| A_browse | constant 20 iterations/s | one GET request per iteration; achieved request rate is approximately the iteration rate subject to delivery effects. |
| B_mixed | constant 15 iterations/s | one request per iteration in the retained final script path; achieved request rate is approximately the iteration rate subject to delivery effects. |
| C_checkout | constant 10 iterations/s | **three GET requests per iteration** (`/shop/`, `/cart/`, `/about/`); therefore 10 iterations/s corresponds nominally to ~30 requests/s, and `rps_actual`/`goodput_rps` are request rates. |
| D_burst | ramping arrival rate | final retained script uses baseline 5 → ramp to 40 → peak 40 → ramp to 5 → recovery 5 iterations/s. The canonical scalar `target_rps=10` is historical metadata and must not be used to reconstruct the staged schedule. |

## Parser and rounding semantics

The historical parser (`benchmark/parse_k6_output.py`) scans line-delimited k6 JSON Point records. Malformed JSON lines are skipped without a retained skipped-line counter. It tracks `first_ts`/`last_ts` before metric-specific routing; therefore the Point-stream duration can differ from the controller `start_time`/`end_time` interval. The historical command interface also receives a CSV path, but the canonical master-row reduction is driven by the JSON Point stream plus orchestration metadata; CSV is retained for separate temporal/time-series work.

Historical rounding written into the frozen master row:

- `test_duration_s`: 2 decimal places;
- `rps_actual`, `goodput_rps`: 3 decimals;
- `error_rate`: 6 decimals;
- latency/connection/waiting percentiles and latency descriptive values: 3 decimals;
- `latency_cv`: 6 decimals;
- `apdex_t500_f2000`: 4 decimals;
- `bandwidth_rx_bps`: 1 decimal;
- counts remain integer-valued.

The parser appends rows and does not itself prevent duplicate run IDs. Final run-ID uniqueness, 28-cell completeness and 10-retained-replication balance are downstream structural validation properties of the frozen canonical dataset.

## Missing-value rule

Missing/blank canonical fields are not silently converted to zero. The 560 missing canonical entries are exactly `dns_p50` and `dns_p95` across the 280 rows. Primary outcome fields are populated for all retained rows.

## Scope

Supplementary warm-up/burst time series, post-idle probes, Linux Docker statistics, cost assumptions and audit reconstructions are **not additional columns in this 39-field canonical row**. They are separate evidence layers and must not be silently merged into the frozen dataset.
