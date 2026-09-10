# Warm-up transient correction (v365)

The historical carrier `warmup_transient.csv` is preserved unchanged for provenance.

A single derived-value defect was identified in its Fly.io / `D_burst` row:

- `p95_first30s = 193.2 ms`
- `p95_steady = 354.4 ms`
- exact ratio = `193.2 / 354.4 = 0.545146...`
- one-decimal value using the repository's displayed precision = **0.5**, not `0.6`.

The corrected derivative is `warmup_transient_v365_corrected.csv`. No other row is changed.

This repository-only correction does **not** alter the frozen 280×39 canonical dataset, the validated inferential results, or the thesis's reported A–C warm-up observations. The historical carrier remains available so the provenance trail is explicit rather than silently rewritten.
