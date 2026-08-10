#!/usr/bin/env python3
"""Prepare repository inputs and run the validated v330 pipeline.

GitHub contains the canonical analytical dataset and the small supplementary
carriers. The full 120-run Docker resource telemetry is intentionally kept in the
controlled evidence archive because it is large. Supply it with --docker-stats
when an exact Table 4.11 / full thesis-mirror run is required.
"""
from __future__ import annotations
import argparse, shutil, subprocess, sys, tempfile
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docker-stats", type=Path, default=None,
                    help="optional full docker_stats.zip from the controlled evidence package")
    ap.add_argument("--verify-against-v329", action="store_true",
                    help="request exact v329 table/numeric regression; requires controlled reference assets and full telemetry")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    materializer = root / "analysis" / "materialize_v330_pipeline.py"
    subprocess.check_call([sys.executable, str(materializer)], cwd=root)
    pipeline = root / "analysis" / "thesis_analysis_pipeline_v330_calibrated.py"

    run_root = root / ".v330-run"
    data = run_root / "data"
    out = run_root / "outputs"
    if run_root.exists():
        shutil.rmtree(run_root)
    data.mkdir(parents=True)

    shutil.copy2(root / "data" / "canonical" / "master_runs.csv", data / "master_runs.csv")
    for name in ("warmup_transient.csv", "timeseries_burst_recovery.csv", "coldstart_raw.csv"):
        shutil.copy2(root / "data" / "supplementary" / name, data / name)
    if args.docker_stats:
        shutil.copy2(args.docker_stats.resolve(), data / "docker_stats.zip")

    cmd = [sys.executable, str(pipeline), "--data-dir", str(data), "--output-dir", str(out)]
    if args.verify_against_v329:
        cmd.append("--verify-against-v329")
    raise SystemExit(subprocess.call(cmd, cwd=root))


if __name__ == "__main__":
    main()
