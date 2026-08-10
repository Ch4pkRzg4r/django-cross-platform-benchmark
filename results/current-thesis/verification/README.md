# v330 current-thesis verification records

These records come from the validated frozen-input calibration package and the author's independent Windows rerun that was subsequently rechecked before repository staging.

- `EXACT_TABLE_MIRROR_CHECK.txt` — Tables 4.1–4.16, exact cell text/order/rounding PASS.
- `NUMERIC_REGRESSION_CHECK_v329.txt` — current statistical and figure-carrier regression PASS.
- `EXACT_PUBLISHED_FIGURE_ASSET_CHECK.txt` — 18/18 controlled final-thesis publication assets byte-identical PASS.
- `PUBLISHED_FIGURE_SHA256_MANIFEST.csv` — SHA-256 registry for those 18 frozen publication assets.
- `PIPELINE_SUMMARY.json` — machine-readable frozen-run summary.
- `FINAL_CALIBRATION_REPORT.txt` — consolidated interpretation.
- `DATA_DRIVEN_MUTATION_TEST.txt` — controlled changed-input safeguard demonstrating that regenerated outputs change with the data.

The publication-asset PASS records refer to the controlled calibration package. The heavy/binary reference assets themselves are intentionally not duplicated here as ordinary Git content. They are regression oracles, not analytical inputs.
