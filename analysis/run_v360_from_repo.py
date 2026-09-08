#!/usr/bin/env python3
"""Controlling v360 repository entry point.

v360 preserves the byte-exact validated v330 analytical base and adds a small,
transparent release layer for the independently adjudicated post-v359 issues.
The release layer does not rewrite the frozen canonical dataset or historical
campaign evidence.

Default mode validates and writes the v360 release carriers from the frozen
canonical dataset. Use --run-v330 to also execute the validated v330 base first;
that full exact-thesis run still requires the controlled Docker telemetry and
publication-reference assets documented by run_v330_from_repo.py.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--master", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, default=None)
    ap.add_argument("--allow-nonfrozen", action="store_true")
    ap.add_argument("--run-v330", action="store_true",
                    help="execute the validated v330 base before generating v360 release carriers")
    ap.add_argument("--docker-stats", type=Path, default=None)
    ap.add_argument("--figure-reference-dir", type=Path, default=None)
    ap.add_argument("--verify-against-v329", action="store_true")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parent.parent
    master = args.master.resolve() if args.master else repo / "data" / "canonical" / "master_runs.csv"

    if args.run_v330:
        cmd = [sys.executable, str(repo / "analysis" / "run_v330_from_repo.py")]
        if args.master:
            cmd += ["--master", str(master)]
        if args.docker_stats:
            cmd += ["--docker-stats", str(args.docker_stats.resolve())]
        if args.figure_reference_dir:
            cmd += ["--figure-reference-dir", str(args.figure_reference_dir.resolve())]
        if args.verify_against_v329:
            cmd.append("--verify-against-v329")
        subprocess.check_call(cmd, cwd=repo)

    corr = [
        sys.executable,
        str(repo / "analysis" / "v360_release_corrections.py"),
        "--master", str(master),
    ]
    if args.out_dir:
        corr += ["--out-dir", str(args.out_dir.resolve())]
    if args.allow_nonfrozen:
        corr.append("--allow-nonfrozen")
    subprocess.check_call(corr, cwd=repo)

    print("PASS v360 release-layer checks and carriers generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
