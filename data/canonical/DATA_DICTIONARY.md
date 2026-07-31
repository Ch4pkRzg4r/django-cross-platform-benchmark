# Data Dictionary — master_runs.csv (280 rows × 39 columns)

| column | description |
|---|---|
| `run_id` | unique run identifier platform__scenario__repNN |
| `platform` | deployment configuration (01–07) |
| `scenario` | workload scenario (A_browse, B_mixed, C_checkout GET-only, D_burst) |
| `replication` | see thesis §3.12 (author to confirm exact wording) |
| `start_time` | see thesis §3.12 (author to confirm exact wording) |
| `end_time` | see thesis §3.12 (author to confirm exact wording) |
| `test_duration_s` | see thesis §3.12 (author to confirm exact wording) |
| `target_rps` | configured arrival rate (iterations/s) |
| `rps_actual` | achieved request rate |
| `goodput_rps` | callback-passing requests/s |
| `total_requests` | see thesis §3.12 (author to confirm exact wording) |
| `total_errors` | see thesis §3.12 (author to confirm exact wording) |
| `error_rate` | callback-defined failure fraction |
| `latency_p50` | run-level p50 (ms) |
| `latency_p90` | see thesis §3.12 (author to confirm exact wording) |
| `latency_p95` | run-level p95 (ms) |
| `latency_p99` | run-level p99 (ms) |
| `latency_p999` | see thesis §3.12 (author to confirm exact wording) |
| `latency_mean` | see thesis §3.12 (author to confirm exact wording) |
| `latency_min` | see thesis §3.12 (author to confirm exact wording) |
| `latency_max` | see thesis §3.12 (author to confirm exact wording) |
| `latency_stddev` | see thesis §3.12 (author to confirm exact wording) |
| `latency_cv` | coefficient of variation of latency |
| `dns_p50` | see thesis §3.12 (author to confirm exact wording) |
| `dns_p95` | see thesis §3.12 (author to confirm exact wording) |
| `tcp_p50` | see thesis §3.12 (author to confirm exact wording) |
| `tcp_p95` | see thesis §3.12 (author to confirm exact wording) |
| `tls_p50` | see thesis §3.12 (author to confirm exact wording) |
| `tls_p95` | see thesis §3.12 (author to confirm exact wording) |
| `waiting_p50` | see thesis §3.12 (author to confirm exact wording) |
| `waiting_p95` | see thesis §3.12 (author to confirm exact wording) |
| `waiting_p99` | see thesis §3.12 (author to confirm exact wording) |
| `apdex_t500_f2000` | Apdex, T=500 ms, F=2000 ms |
| `bytes_received` | see thesis §3.12 (author to confirm exact wording) |
| `bytes_sent` | see thesis §3.12 (author to confirm exact wording) |
| `bandwidth_rx_bps` | see thesis §3.12 (author to confirm exact wording) |
| `k6_iterations` | see thesis §3.12 (author to confirm exact wording) |
| `first_ts` | see thesis §3.12 (author to confirm exact wording) |
| `last_ts` | see thesis §3.12 (author to confirm exact wording) |
