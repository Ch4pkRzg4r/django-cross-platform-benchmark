#!/usr/bin/env python3
"""v360 release-layer corrections and reproducibility carriers.

This module deliberately leaves the byte-exact validated v330 analytical source
unchanged. It applies the independently adjudicated post-v359 release-layer
corrections defined from the frozen canonical run-level dataset:

1. p99/p50 tail inflation is computed per run first, then summarised by the
   median within each platform-scenario cell. This supersedes the historical
   ratio-of-cell-medians appendix carrier emitted by the v330 table writer.
2. The completed-iteration shortfall diagnostic is explicitly separated from
   k6 dropped_iterations and is computed relative to scenario-specific planned
   iteration starts.
3. Figure 4.1 and Figure 4.13 data carriers are regenerated directly from the
   frozen canonical run-level data.

The script fails closed on the frozen 280-run / 28-cell / 10-replication design.
All release CSVs are staged and validated before publication. The manifest hashes
an explicit CSV list, never hashes itself, and is published last.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

FROZEN_CANONICAL_SHA256 = "710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7"

PLATFORM_LABEL = {
    "01_apache_modwsgi": "Apache + mod_wsgi",
    "02_nginx_uwsgi": "Nginx + uWSGI",
    "03_django_gunicorn": "Django + Gunicorn",
    "04_aca": "Azure Container Apps",
    "05_koyeb": "Koyeb",
    "06_flyio": "Fly.io",
    "07_iis_waitress": "IIS + Waitress",
}
SCENARIO_LABEL = {
    "A_browse": "A",
    "B_mixed": "B",
    "C_checkout": "C",
    "D_burst": "D",
}
PLANNED_ITERATION_STARTS = {
    "A_browse": 36000,
    "B_mixed": 27000,
    "C_checkout": 18000,
    "D_burst": 32100,
}
RANK_METRICS = [
    "latency_p50", "latency_p95", "latency_p99", "latency_p999",
    "latency_cv", "tail_ratio", "goodput_rps", "error_pct",
    "apdex_t500_f2000", "waiting_p50", "waiting_p95", "bandwidth_rx_bps",
]
PUBLISHED_CSVS = [
    "v360_tail_ratio_cells.csv",
    "v360_figure4_1_p95_cells.csv",
    "v360_completed_iteration_shortfall.csv",
    "v360_figure4_13_rank_carrier.csv",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def git_commit(repo: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repo, text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return None


def validate_design(df: pd.DataFrame) -> None:
    required = {
        "run_id", "platform", "scenario", "replication", "latency_p50",
        "latency_p95", "latency_p99", "latency_p999", "latency_cv",
        "goodput_rps", "error_rate", "apdex_t500_f2000", "waiting_p50",
        "waiting_p95", "bandwidth_rx_bps", "k6_iterations",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise SystemExit(f"missing required canonical fields: {missing}")
    if len(df) != 280 or df.run_id.nunique() != 280:
        raise SystemExit("v360 release correction requires exactly 280 unique retained runs")
    counts = df.groupby(["platform", "scenario"]).size()
    if len(counts) != 28 or not (counts == 10).all():
        raise SystemExit("v360 release correction requires 28 balanced cells with 10 runs each")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--master", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, default=None)
    ap.add_argument("--burst-carrier", type=Path, default=None,
                    help="replication-median per-second Scenario-D carrier; defaults to data/supplementary/timeseries_burst_recovery.csv")
    ap.add_argument("--allow-nonfrozen", action="store_true",
                    help="allow a changed canonical file for exploratory testing")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parent.parent
    master = (args.master or (repo / "data" / "canonical" / "master_runs.csv")).resolve()
    out = (args.out_dir or (repo / ".v360-run" / "release")).resolve()
    burst_carrier = (args.burst_carrier or (repo / "data" / "supplementary" / "timeseries_burst_recovery.csv")).resolve()

    got_sha = sha256(master)
    if got_sha != FROZEN_CANONICAL_SHA256 and not args.allow_nonfrozen:
        raise SystemExit(
            f"canonical hash mismatch: expected {FROZEN_CANONICAL_SHA256}, got {got_sha}; "
            "use --allow-nonfrozen only for exploratory testing"
        )

    df = pd.read_csv(master)
    validate_design(df)
    df = df.copy()
    df["tail_ratio"] = df["latency_p99"] / df["latency_p50"]
    df["error_pct"] = 100.0 * df["error_rate"]

    keys = ["platform", "scenario"]
    med = df.groupby(keys, sort=False).median(numeric_only=True).reset_index()

    ratio_cells = (
        df.groupby(keys, sort=False)["tail_ratio"].median().rename("p99_over_p50")
        .reset_index()
    )
    wrong = (
        df.groupby(keys, sort=False)
        .agg(p99_median=("latency_p99", "median"), p50_median=("latency_p50", "median"))
        .reset_index()
    )
    wrong["historical_ratio_of_cell_medians"] = wrong.p99_median / wrong.p50_median
    ratio_cells = ratio_cells.merge(
        wrong[keys + ["historical_ratio_of_cell_medians"]], on=keys, validate="one_to_one"
    )
    ratio_cells["difference_vs_historical_operator"] = (
        ratio_cells.p99_over_p50 - ratio_cells.historical_ratio_of_cell_medians
    )
    ratio_cells["platform_label"] = ratio_cells.platform.map(PLATFORM_LABEL)
    ratio_cells["scenario_label"] = ratio_cells.scenario.map(SCENARIO_LABEL)
    if len(ratio_cells) != 28 or ratio_cells[keys].duplicated().any():
        raise SystemExit("tail-ratio carrier must contain exactly 28 unique cells")

    fig41 = med[keys + ["latency_p95"]].copy()
    fig41["platform_label"] = fig41.platform.map(PLATFORM_LABEL)
    fig41["scenario_label"] = fig41.scenario.map(SCENARIO_LABEL)
    fig41 = fig41.rename(columns={"latency_p95": "median_p95_ms"})
    if len(fig41) != 28 or fig41[keys].duplicated().any():
        raise SystemExit("Figure 4.1 carrier must contain exactly 28 unique cells")

    short = df[["run_id", "platform", "scenario", "replication", "k6_iterations"]].copy()
    short["planned_iteration_starts"] = short.scenario.map(PLANNED_ITERATION_STARTS)
    short["completed_iteration_shortfall_count"] = np.maximum(
        short.planned_iteration_starts - short.k6_iterations, 0
    )
    short["completed_iteration_shortfall_pct"] = (
        100.0 * short.completed_iteration_shortfall_count / short.planned_iteration_starts
    )
    if len(short) != 280 or short.run_id.nunique() != 280:
        raise SystemExit("shortfall carrier must contain exactly 280 unique retained runs")

    # Scenario-D achieved rate is derived from the retained replication-median
    # per-second curve, not copied from a literal constant in the frozen v330
    # writer. The current estimand is median(rps_tau) for 360 <= tau < 960.
    if not burst_carrier.exists():
        raise SystemExit(f"missing Scenario-D burst carrier: {burst_carrier}")
    burst = pd.read_csv(burst_carrier)
    burst_required = {"platform", "second", "rps"}
    burst_missing = sorted(burst_required - set(burst.columns))
    if burst_missing:
        raise SystemExit(f"burst carrier missing required fields: {burst_missing}")
    peak = burst[(burst["second"] >= 360) & (burst["second"] < 960)].copy()
    if peak.empty:
        raise SystemExit("burst carrier contains no rows in 360 <= tau < 960")
    peak_rps = peak.groupby("platform", sort=True)["rps"].median()
    if len(peak_rps) != 7 or peak_rps.isna().any():
        raise SystemExit("burst peak-window validation requires seven non-missing platform medians")

    # `med` already contains the median of the run-level tail_ratio because
    # tail_ratio was added before groupby(). Reuse it directly. The previous
    # implementation merged a second tail_ratio column and caused pandas to
    # return a Series for row["tail_ratio"], which made the official entry fail.
    cell = med.copy()
    rank_rows: list[dict] = []
    for scenario, g in cell.groupby("scenario", sort=False):
        for metric in RANK_METRICS:
            vals = g[metric]
            ranks = vals.rank(method="average", ascending=True)
            norm = (ranks - 1.0) / 6.0
            lo = vals.min()
            hi = vals.max()
            for idx, row in g.iterrows():
                value = float(row[metric])
                rank_rows.append({
                    "scenario": scenario,
                    "scenario_label": SCENARIO_LABEL.get(scenario, scenario),
                    "platform": row.platform,
                    "platform_label": PLATFORM_LABEL.get(row.platform, row.platform),
                    "metric": metric,
                    "value": value,
                    "average_rank_1_to_7": float(ranks.loc[idx]),
                    "rank_scale_0_to_1": float(norm.loc[idx]),
                    "L": bool(value == lo),
                    "H": bool(value == hi),
                })
    rank_df = pd.DataFrame(rank_rows)
    if rank_df.columns.duplicated().any():
        raise SystemExit("rank carrier contains duplicate column names")
    if len(rank_df) != 336:
        raise SystemExit(f"rank carrier must contain 336 rows, got {len(rank_df)}")
    if rank_df[["scenario", "platform", "metric"]].duplicated().any():
        raise SystemExit("rank carrier contains duplicate scenario/platform/metric rows")

    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="v360-stage-", dir=str(out.parent)) as tmp:
        stage = Path(tmp)
        ratio_cells.to_csv(stage / PUBLISHED_CSVS[0], index=False)
        fig41.to_csv(stage / PUBLISHED_CSVS[1], index=False)
        short.to_csv(stage / PUBLISHED_CSVS[2], index=False)
        rank_df.to_csv(stage / PUBLISHED_CSVS[3], index=False)

        manifest = {
            "release": "v360",
            "purpose": "release-layer correction over byte-exact validated v330 base",
            "repository_commit_if_available": git_commit(repo),
            "canonical_path": str(master),
            "canonical_sha256": got_sha,
            "canonical_rows": int(len(df)),
            "canonical_cells": int(df.groupby(keys).ngroups),
            "tail_ratio_estimand": "median_r(latency_p99_r / latency_p50_r)",
            "historical_operator_superseded": "median_r(latency_p99_r) / median_r(latency_p50_r)",
            "tail_ratio_cells": 28,
            "historical_operator_differs_at_3dp_cells": int(
                (ratio_cells.p99_over_p50.round(3) != ratio_cells.historical_ratio_of_cell_medians.round(3)).sum()
            ),
            "shortfall_definition": "100*max(P-I,0)/P where I is retained completed iterations; not an actual-start census and not k6 dropped_iterations",
            "shortfall_gt_1pct_runs": int((short.completed_iteration_shortfall_pct > 1.0).sum()),
            "shortfall_ge_5pct_runs": int((short.completed_iteration_shortfall_pct >= 5.0).sum()),
            "shortfall_max_pct": float(short.completed_iteration_shortfall_pct.max()),
            "rank_rows": int(len(rank_df)),
            "burst_carrier_path": str(burst_carrier),
            "burst_carrier_sha256": sha256(burst_carrier),
            "burst_peak_window": "360 <= tau < 960",
            "burst_peak_rps_estimand": "median_tau(rps_tau) on the retained replication-median per-second curve",
            "burst_peak_rps_by_platform": {str(k): float(v) for k, v in peak_rps.items()},
            "outputs": {},
        }
        # Hash only the explicit release CSVs. Never include the manifest itself
        # or stale v360_* files from a previous run.
        for name in PUBLISHED_CSVS:
            path = stage / name
            manifest["outputs"][name] = {"sha256": sha256(path), "bytes": path.stat().st_size}

        manifest_path = stage / "v360_release_manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

        out.mkdir(parents=True, exist_ok=True)
        # Publish only after all data/rank/manifest validation has succeeded.
        for name in PUBLISHED_CSVS:
            os.replace(stage / name, out / name)
        os.replace(manifest_path, out / "v360_release_manifest.json")

    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
