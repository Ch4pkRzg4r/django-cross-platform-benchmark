#!/usr/bin/env python3
"""
analyze_coldstart.py  --  Turn coldstart_raw.csv (from measure_coldstart.ps1)
into a Chapter-4-ready summary table + a figure.

USAGE:
    python analyze_coldstart.py coldstart_raw.csv

OUTPUTS:
    coldstart_summary.csv     (per-platform cold p50/p95/p99, warm p50, penalty)
    fig_coldstart_measured.png (cold vs warm bar chart with penalty labels)
"""
import sys, os
import pandas as pd, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

csv = sys.argv[1] if len(sys.argv) > 1 else "coldstart_raw.csv"
if not os.path.exists(csv): sys.exit(f"not found: {csv}")
df = pd.read_csv(csv)
df = df[(df.cold_ms > 0) & (df.warm_ms > 0)]          # drop failed probes

rows = []
for p, g in df.groupby("platform"):
    rows.append({
        "platform": p, "n": len(g),
        "cold_p50": g.cold_ms.median(), "cold_p95": g.cold_ms.quantile(0.95),
        "cold_p99": g.cold_ms.quantile(0.99), "cold_max": g.cold_ms.max(),
        "warm_p50": g.warm_ms.median(),
        "penalty_p50": g.cold_ms.median() / max(1.0, g.warm_ms.median()),
    })
S = pd.DataFrame(rows).round(1)
S.to_csv("coldstart_summary.csv", index=False)
print(S.to_string(index=False))

# figure: cold p50/p95 vs warm p50
plats = S.platform.tolist(); x = np.arange(len(plats)); w = 0.27
plt.figure(figsize=(8.6, 4.8))
plt.bar(x - w, S.warm_p50, w, label="warm p50", color="#54a24b")
plt.bar(x,     S.cold_p50, w, label="cold p50", color="#f58518")
plt.bar(x + w, S.cold_p95, w, label="cold p95", color="#d62728")
for i, r in S.iterrows():
    plt.text(i, r.cold_p95 * 1.02, f"{r.penalty_p50:.0f}x", ha="center", fontsize=10, fontweight="bold")
plt.yscale("log"); plt.xticks(x, plats); plt.ylabel("Latency (ms, log scale)")
plt.title("Measured cold-start vs warm latency (penalty = cold p50 / warm p50)")
plt.legend(); plt.grid(True, axis="y", ls=":", alpha=.5); plt.tight_layout()
plt.savefig("fig_coldstart_measured.png", dpi=130)
print("\nWrote coldstart_summary.csv and fig_coldstart_measured.png")
print("Send both back to splice into Chapter 4 as the quantified cold-start result.")
