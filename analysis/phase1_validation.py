"""
PHASE 1 — DATA VALIDATION
Thesis: Benchmarking Traditional Web Servers vs Serverless (E-Commerce)
Author: Chapk Rzgar Mohammed Abdalla, University of Sulaimani

This script performs comprehensive validation of the 280-row master_runs.csv:
1. Row count and cell completeness
2. Null audit
3. Quality flag audit (6 flags)
4. Configuration consistency
5. SHA-256 file integrity
"""

import hashlib
import pandas as pd
import numpy as np
import json
from pathlib import Path

# ===================================================================
# 0. SHA-256 INTEGRITY HASH
# ===================================================================
def sha256_of(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()

DATA = "master_runs_FINAL_280.csv"
digest = sha256_of(DATA)
print("=" * 70)
print("PHASE 1 — DATA VALIDATION")
print("=" * 70)
print(f"\n[0] SHA-256 of {DATA}:")
print(f"    {digest}")

# Save digest to manifest
with open("checksums.sha256", "w") as f:
    f.write(f"{digest}  {DATA}\n")
print(f"    Saved to checksums.sha256")

# ===================================================================
# 1. LOAD AND STRUCTURAL VALIDATION
# ===================================================================
df = pd.read_csv(DATA)

print("\n" + "=" * 70)
print("[1] STRUCTURAL VALIDATION")
print("=" * 70)
print(f"Total rows:      {len(df)} (expected 280)")
print(f"Total columns:   {len(df.columns)}")
print(f"Distinct platforms: {df.platform.nunique()} (expected 7)")
print(f"Distinct scenarios: {df.scenario.nunique()} (expected 4)")
print(f"Duplicate run_id:   {df.run_id.duplicated().sum()} (expected 0)")

# Cell completeness (10 per platform × scenario)
counts = df.groupby(['platform', 'scenario']).size().unstack(fill_value=0)
print(f"\nCell counts (rows per platform × scenario, expected 10 everywhere):")
print(counts)
all_ten = (counts == 10).all().all()
print(f"\n✓ All 28 cells = 10 reps: {all_ten}")

# Replication completeness (1..10 in every cell)
expected_reps = set(range(1, 11))
gaps_found = []
for (p, s), g in df.groupby(['platform', 'scenario']):
    gaps = expected_reps - set(g['replication'])
    if gaps:
        gaps_found.append((p, s, gaps))
if gaps_found:
    print("\n⚠️ Replication gaps:")
    for p, s, g in gaps_found:
        print(f"  {p} × {s}: missing reps {sorted(g)}")
else:
    print("✓ All cells have replications 1..10")

# ===================================================================
# 2. NULL AUDIT
# ===================================================================
print("\n" + "=" * 70)
print("[2] NULL AUDIT — Critical columns")
print("=" * 70)
critical_cols = ['latency_p50', 'latency_p95', 'latency_p99', 'rps_actual',
                 'goodput_rps', 'total_requests', 'total_errors', 'error_rate',
                 'apdex_t500_f2000', 'test_duration_s']
null_counts = df[critical_cols].isna().sum()
print(null_counts.to_string())
print(f"\n✓ All critical columns null-free: {(null_counts == 0).all()}")

# ===================================================================
# 3. QUALITY FLAG AUDIT (6 FLAGS)
# ===================================================================
print("\n" + "=" * 70)
print("[3] QUALITY FLAG AUDIT")
print("=" * 70)

# Target RPS map
TARGET = {"A_browse": 20, "B_mixed": 15, "C_checkout": 10, "D_burst": 10}
df['target_rps_expected'] = df['scenario'].map(TARGET)

# Per-cell median request count
cell_med_req = df.groupby(['platform', 'scenario'])['total_requests'].transform('median')

# Flag 1: Zero/near-zero requests
df['flag_low_requests'] = df['total_requests'] < 0.5 * cell_med_req

# Flag 2: Short duration (target is 1800s = 30 min)
df['flag_short_duration'] = (df['test_duration_s'] - 1800).abs() > 30

# Flag 3: Saturated latencies (timeout ~60000ms)
df['flag_saturated_latency'] = df['latency_max'] >= 59000

# Flag 4: Anomalous error rate (outside burst)
df['flag_high_error'] = (df['error_rate'] > 0.05) & (df['scenario'] != 'D_burst')

# Flag 5: Coordinated omission (under-issued RPS)
df['flag_coord_omission'] = (df['rps_actual'] / df['target_rps_expected']) < 0.95

# Flag 6: RPS overshoot (scenario-overshoot indicator)
df['flag_rps_overshoot'] = (df['rps_actual'] / df['target_rps_expected']) > 1.10

flag_cols = [c for c in df.columns if c.startswith('flag_')]
print(f"Flag definitions:")
print(f"  flag_low_requests        : total_requests < 0.5 × cell-median")
print(f"  flag_short_duration      : |duration − 1800s| > 30s")
print(f"  flag_saturated_latency   : latency_max ≥ 59000ms (timeout signature)")
print(f"  flag_high_error          : error_rate > 5% (outside D_burst)")
print(f"  flag_coord_omission      : rps_actual/target < 0.95")
print(f"  flag_rps_overshoot       : rps_actual/target > 1.10")

print(f"\nTotal rows flagged on each criterion:")
for col in flag_cols:
    n = df[col].sum()
    print(f"  {col:30s}: {n:3d} rows")

# Per-cell flag summary
print(f"\nCells with any flag:")
cell_flags = df.groupby(['platform', 'scenario'])[flag_cols].sum()
cell_flagged = cell_flags[cell_flags.sum(axis=1) > 0]
print(cell_flagged.to_string())

# ===================================================================
# 4. RUNTIME CONFIGURATION CONSISTENCY
# ===================================================================
print("\n" + "=" * 70)
print("[4] CONFIGURATION CONSISTENCY (target_rps invariance per scenario)")
print("=" * 70)
# Check that target_rps is invariant within each scenario
scenario_target = df.groupby('scenario')['target_rps'].nunique()
print("Distinct target_rps values per scenario (expected 1 each):")
print(scenario_target.to_string())
print(f"\n✓ Target RPS consistent per scenario: {(scenario_target == 1).all()}")

# ===================================================================
# 5. SUMMARY REPORT
# ===================================================================
print("\n" + "=" * 70)
print("[5] VALIDATION SUMMARY")
print("=" * 70)

validation_passed = (
    len(df) == 280
    and all_ten
    and (null_counts == 0).all()
    and not gaps_found
    and (scenario_target == 1).all()
)
print(f"\n{'✓ PHASE 1 VALIDATION PASSED' if validation_passed else '✗ PHASE 1 VALIDATION FAILED'}")
print(f"  280 rows present:        {len(df) == 280}")
print(f"  10 reps per cell:        {all_ten}")
print(f"  No critical nulls:       {(null_counts == 0).all()}")
print(f"  No replication gaps:     {not gaps_found}")
print(f"  Scenario targets clean:  {(scenario_target == 1).all()}")

# Save validated dataset (with flags)
df.to_csv('master_runs_VALIDATED.csv', index=False)
print(f"\n✓ Saved: master_runs_VALIDATED.csv (with quality flags)")

# Save validation report as JSON
report = {
    'sha256': digest,
    'total_rows': int(len(df)),
    'total_columns': int(len(df.columns)),
    'platforms': df.platform.nunique(),
    'scenarios': df.scenario.nunique(),
    'all_cells_ten_reps': bool(all_ten),
    'null_critical_columns': bool((null_counts == 0).all()),
    'replication_gaps': bool(not gaps_found),
    'scenario_targets_invariant': bool((scenario_target == 1).all()),
    'validation_passed': bool(validation_passed),
    'flag_counts': {col: int(df[col].sum()) for col in flag_cols},
    'flagged_cells': {
        f"{idx[0]}__{idx[1]}": {col: int(row[col]) for col in flag_cols if row[col] > 0}
        for idx, row in cell_flagged.iterrows()
    }
}
with open('validation_report.json', 'w') as f:
    json.dump(report, f, indent=2)
print(f"✓ Saved: validation_report.json")
