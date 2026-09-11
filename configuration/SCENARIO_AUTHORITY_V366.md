# Scenario execution authority — v366 document closure

This note resolves a provenance/interpretation issue in which older planning/configuration metadata does not fully match the final retained workload scripts. **Historical files are preserved; conflicts are documented rather than silently rewritten.**

## Authority rule

For interpretation of the frozen campaign and `master_runs.csv`:

1. the final retained k6 workload scripts under `benchmark/k6-scenarios/` control request/iteration semantics;
2. the frozen canonical rows and retained temporal carriers control observed run evidence;
3. `configuration/scenarios.json` is retained as historical planning/configuration metadata and must not override a conflicting final script;
4. `target_rps` in the canonical dataset is historical scalar metadata, not a universal definition of the complete offered-load schedule.

## Final scenario semantics

| Scenario | Final script authority | Arrival schedule | Requests per iteration / endpoint pattern | Canonical-rate interpretation |
|---|---|---|---|---|
| A — `A_browse` | `benchmark/k6-scenarios/scenario_A_browse.js` | constant 20 iterations/s | one GET request per iteration selected from the browse mix | `target_rps=20` is iteration rate; achieved `rps_actual` is request rate and is approximately comparable because each iteration issues one request. |
| B — `B_mixed` | `benchmark/k6-scenarios/scenario_B_mixed.js` | constant 15 iterations/s | retained final mixed/session path defined by the script | `target_rps=15` is iteration-rate metadata; `rps_actual`/`goodput_rps` remain request rates. |
| C — `C_checkout` | `benchmark/k6-scenarios/scenario_C_checkout.js` | constant 10 iterations/s | **three GETs per iteration**: `/shop/`, `/cart/`, `/about/`; no retained final write/POST transaction | `target_rps=10` is iteration rate; nominal request offer is ~30 requests/s. Therefore `rps_actual` and `goodput_rps` must not be compared to 10 as if they were iteration rates. |
| D — `D_burst` | `benchmark/k6-scenarios/scenario_D_burst.js` | ramping arrival rate: 5 baseline → ramp to 40 → 40 peak → ramp to 5 → 5 recovery (30-min proportions 5/1/10/1/13 min) | one GET `/shop/` request per iteration | the frozen scalar `target_rps=10` is historical metadata and **does not encode the staged D schedule**. Use the script and retained per-second carrier for burst-rate interpretation. |

## Known stale planning metadata

`configuration/scenarios.json` contains historical descriptions that predate the final workload freeze, including older Scenario-C write/POST language and older Scenario-D descriptive targets. It is preserved for provenance and must not be cited as the final execution authority where it conflicts with the scripts above.

## Why this matters

- Scenario C explains why approximately 10 iterations/s can produce approximately 30 requests/s before delivery effects.
- Scenario D cannot be reduced to one scalar target rate; phase-level analysis uses the retained staged schedule and per-second carrier.
- callback-qualified goodput/error and latency-only Apdex remain request-level outcomes, while k6 iteration counts describe iteration delivery.

This note changes no frozen data and no reported benchmark result; it makes the final workload semantics explicit for reproduction and audit.
