#!/usr/bin/env python3
"""Prepare a disposable run directory and execute the validated v330 pipeline.

The final frozen-thesis mirror intentionally depends on two controlled assets that
are not duplicated as ordinary Git content: the full 120-run Docker telemetry ZIP
and the exact final-thesis publication figure-reference directory. Supply both for
a frozen exact-mirror run. A changed-master exploratory rerun does not emit frozen
publication assets and therefore does not require the figure-reference directory.
"""
from __future__ import annotations
import argparse, hashlib, shutil, subprocess, sys
from pathlib import Path

FROZEN_MASTER_SHA256 = "710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--master", type=Path, default=None,
                    help="optional master_runs.csv override; defaults to the frozen repository dataset")
    ap.add_argument("--docker-stats", type=Path, default=None,
                    help="full docker_stats.zip from the controlled evidence package")
    ap.add_argument("--figure-reference-dir", type=Path, default=None,
                    help="directory containing the 18 exact final-thesis reference figure assets")
    ap.add_argument("--verify-against-v329", action="store_true",
                    help="run the full numerical v329 regression in addition to the always-on frozen table check")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parent.parent
    source_master = args.master.resolve() if args.master else repo / "data" / "canonical" / "master_runs.csv"
    if not source_master.exists():
        raise SystemExit(f"master dataset not found: {source_master}")
    frozen = sha256(source_master) == FROZEN_MASTER_SHA256

    if frozen:
        missing = []
        if not args.docker_stats:
            missing.append("--docker-stats /path/to/docker_stats.zip")
        if not args.figure_reference_dir:
            missing.append("--figure-reference-dir /path/to/reference/thesis_figures")
        if missing:
            raise SystemExit(
                "Frozen exact-thesis run requires controlled evidence not duplicated in ordinary Git history:\n  "
                + "\n  ".join(missing)
                + "\nUse a changed --master for a data-driven exploratory rerun, or supply the controlled assets."
            )

    # Reconstruct the validated byte-exact source and then execute a COPY inside
    # the disposable run root so the pipeline's root-relative reference paths do
    # not modify or depend on the Git working tree.
    materializer = repo / "analysis" / "materialize_v330_pipeline.py"
    subprocess.check_call([sys.executable, str(materializer)], cwd=repo)
    materialized = repo / "analysis" / "thesis_analysis_pipeline_v330_calibrated.py"

    run_root = repo / ".v330-run"
    if run_root.exists():
        shutil.rmtree(run_root)
    data = run_root / "data"
    scripts = run_root / "scripts"
    refs_tables = run_root / "reference" / "thesis_tables"
    refs_figs = run_root / "reference" / "thesis_figures"
    out = run_root / "outputs"
    for d in (data, scripts, refs_tables):
        d.mkdir(parents=True, exist_ok=True)

    pipeline = scripts / "thesis_analysis_pipeline_v330_calibrated.py"
    shutil.copy2(materialized, pipeline)
    shutil.copy2(source_master, data / "master_runs.csv")
    for name in ("warmup_transient.csv", "timeseries_burst_recovery.csv", "coldstart_raw.csv"):
        shutil.copy2(repo / "data" / "supplementary" / name, data / name)

    # Current exact table references live in Git and are safe to use only as a
    # regression oracle; the pipeline never reads them to calculate results.
    for p in (repo / "results" / "current-thesis" / "tables").glob("Table_4_*.csv"):
        shutil.copy2(p, refs_tables / p.name)

    if args.docker_stats:
        ds = args.docker_stats.resolve()
        if not ds.exists():
            raise SystemExit(f"Docker telemetry ZIP not found: {ds}")
        shutil.copy2(ds, data / "docker_stats.zip")

    if args.figure_reference_dir:
        src = args.figure_reference_dir.resolve()
        if not src.is_dir():
            raise SystemExit(f"figure reference directory not found: {src}")
        refs_figs.mkdir(parents=True, exist_ok=True)
        for p in src.iterdir():
            if p.is_file():
                shutil.copy2(p, refs_figs / p.name)

    cmd = [
        sys.executable, str(pipeline),
        "--data-dir", str(data),
        "--output-dir", str(out),
        "--reference-dir", str(refs_tables),
    ]
    if args.verify_against_v329:
        cmd.append("--verify-against-v329")
    if frozen:
        cmd.append("--require-frozen-hash")

    print(f"Run mode: {'FROZEN EXACT-THESIS' if frozen else 'CHANGED-DATA'}")
    print(f"Disposable run root: {run_root}")
    raise SystemExit(subprocess.call(cmd, cwd=run_root))


if __name__ == "__main__":
    main()
