#!/usr/bin/env python3
"""
analyze_timeseries.py  --  Extract WITHIN-RUN time-series from the raw k6 output
that already exists for all 280 runs (data/raw/<run_id>.csv). The aggregated
master_runs.csv hides time; this recovers it, enabling two analyses the thesis
does not yet have:

  (1) BURST RECOVERY (D_burst): how p95 latency and request rate evolve second
      by second, and how long each platform takes to recover after the burst.
  (2) WARM-UP TRANSIENT: first-30s p95 vs steady-state p95, per platform/scenario
      (a within-run warm-up proxy, complementary to the dedicated cold-start probe).

It reads k6 CSV output (k6 run --out csv=...), whose rows are individual metric
points with columns: metric_name, timestamp, metric_value, ... . We use the
'http_req_duration' rows (one per request, value in ms, timestamp in unix sec).

USAGE:
    python analyze_timeseries.py  path/to/data/raw
    # default: data/raw

OUTPUTS:
    timeseries_burst_recovery.csv     (per platform: second, p95_ms, rps  for D_burst)
    fig_burst_recovery_p95.png        (p95 latency vs time, all platforms)
    fig_burst_recovery_rps.png        (achieved RPS vs time, all platforms)
    warmup_transient.csv              (first-30s vs steady p95 per platform/scenario)

NOTE ON FORMAT: k6's CSV column names are auto-detected. If your files differ,
run it once; if it errors, send ONE raw D_burst CSV and the column names will be
confirmed. The script is deliberately defensive.
"""
import sys, os, glob, re
import pandas as pd, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

RAW = sys.argv[1] if len(sys.argv) > 1 else "data/raw"
LAB = {"01_apache_modwsgi":"Apache","02_nginx_uwsgi":"Nginx","03_django_gunicorn":"Django",
       "04_aca":"ACA","05_koyeb":"Koyeb","06_flyio":"Fly.io","07_iis_waitress":"IIS"}
COL = {"Apache":"#d62728","Nginx":"#2ca02c","Django":"#9467bd","IIS":"#1f77b4",
       "ACA":"#ff7f0e","Koyeb":"#8c564b","Fly.io":"#e377c2"}

def load_points(path):
    """Return DataFrame with columns [t_rel(int sec), dur_ms] from a k6 CSV."""
    df = pd.read_csv(path, low_memory=False)
    cols = {c.lower(): c for c in df.columns}
    mname = cols.get("metric_name"); tname = cols.get("timestamp"); vname = cols.get("metric_value")
    if not (mname and tname and vname):
        raise ValueError(f"unexpected columns in {os.path.basename(path)}: {list(df.columns)[:8]}")
    d = df[df[mname] == "http_req_duration"][[tname, vname]].copy()
    d.columns = ["ts", "dur_ms"]
    d["ts"] = pd.to_numeric(d["ts"], errors="coerce")
    d["dur_ms"] = pd.to_numeric(d["dur_ms"], errors="coerce")
    d = d.dropna()
    if d.empty: return d
    d["t_rel"] = (d["ts"] - d["ts"].min()).astype(int)
    return d[["t_rel", "dur_ms"]]

def per_second(d):
    g = d.groupby("t_rel")["dur_ms"]
    out = pd.DataFrame({"p95": g.quantile(0.95), "rps": g.count()})
    return out

# ---- gather files ----
files = glob.glob(os.path.join(RAW, "*.csv"))
if not files: sys.exit(f"no CSVs in {RAW}")
pat = re.compile(r"(\d\d_[a-z_]+?)__([A-D]_[a-z]+)__rep(\d+)")

# ---------- (1) BURST RECOVERY (D_burst) ----------
burst = {}   # platform -> list of per-second frames
warm_rows = []
for f in files:
    m = pat.search(os.path.basename(f))
    if not m: continue
    plat, scen = LAB.get(m.group(1)), m.group(2)
    if not plat: continue
    try:
        d = load_points(f)
    except Exception as e:
        print("WARN", e); continue
    if d.empty: continue
    ps = per_second(d)
    # warm-up transient (all scenarios): first 30s vs steady (60s..end)
    early = d[d.t_rel < 30]["dur_ms"]; steady = d[d.t_rel >= 60]["dur_ms"]
    if len(early) and len(steady):
        warm_rows.append({"platform":plat,"scenario":scen,
                          "p95_first30s":early.quantile(0.95),"p95_steady":steady.quantile(0.95)})
    if scen == "D_burst":
        burst.setdefault(plat, []).append(ps)

# average burst curves across reps (align by second, cap to 1800s)
def avg_curve(frames, col):
    alls = pd.concat([fr[col].rename(i) for i,fr in enumerate(frames)], axis=1)
    return alls.median(axis=1)

if burst:
    plt.figure(figsize=(10,5))
    rec_rows=[]
    for plat, frames in burst.items():
        c = avg_curve(frames,"p95").rolling(5,min_periods=1).median()
        plt.plot(c.index, c.values, label=plat, color=COL.get(plat), lw=1.6)
    plt.yscale("log"); plt.xlabel("Time within run (s)"); plt.ylabel("p95 latency (ms, log)")
    plt.title("D_burst: within-run p95 latency over time (burst & recovery)")
    plt.legend(ncol=4,fontsize=8); plt.grid(True,which="both",ls=":",alpha=.4); plt.tight_layout()
    plt.savefig("fig_burst_recovery_p95.png",dpi=130); plt.close()

    plt.figure(figsize=(10,5))
    for plat, frames in burst.items():
        c = avg_curve(frames,"rps").rolling(5,min_periods=1).median()
        plt.plot(c.index, c.values, label=plat, color=COL.get(plat), lw=1.4)
    plt.xlabel("Time within run (s)"); plt.ylabel("Achieved requests/s")
    plt.title("D_burst: within-run achieved request rate over time")
    plt.legend(ncol=4,fontsize=8); plt.grid(True,ls=":",alpha=.4); plt.tight_layout()
    plt.savefig("fig_burst_recovery_rps.png",dpi=130); plt.close()

    # export averaged curves
    exp=[]
    for plat,frames in burst.items():
        p95=avg_curve(frames,"p95"); rps=avg_curve(frames,"rps")
        for s in p95.index:
            exp.append({"platform":plat,"second":int(s),"p95_ms":round(float(p95[s]),1),
                        "rps":round(float(rps.get(s,np.nan)),1)})
    pd.DataFrame(exp).to_csv("timeseries_burst_recovery.csv",index=False)
    print("Wrote fig_burst_recovery_p95.png, fig_burst_recovery_rps.png, timeseries_burst_recovery.csv")
else:
    print("No D_burst raw files found — check the folder path.")

# ---------- (2) WARM-UP TRANSIENT ----------
if warm_rows:
    W=pd.DataFrame(warm_rows).groupby(["platform","scenario"]).median(numeric_only=True).reset_index()
    W["warmup_ratio"]=(W.p95_first30s/W.p95_steady).round(2)
    W.round(1).to_csv("warmup_transient.csv",index=False)
    print("\nWarm-up transient (first-30s p95 / steady p95), median per cell:")
    print(W.pivot_table("warmup_ratio","platform","scenario").round(2).to_string())
    print("\nWrote warmup_transient.csv")
