#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize the byte-exact validated v330 analysis script from repository payload parts.

The five payload files are gzip-compressed/base64 chunks of the validated source.
The reconstructed UTF-8 source MUST hash to the thesis-recorded SHA-256 below.
This bootstrap does not modify analytical data and does not run the analysis unless
--run is supplied.
"""
from __future__ import annotations
import argparse, base64, gzip, hashlib, subprocess, sys
from pathlib import Path

EXPECTED_SHA256 = "d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574"
PARTS = [f"payload_{i:02d}.b64" for i in range(1, 6)]

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def materialize(repo_root: Path) -> Path:
    payload_dir = repo_root / "analysis" / "v330-payload"
    encoded = "".join((payload_dir / name).read_text(encoding="ascii").strip() for name in PARTS)
    raw = gzip.decompress(base64.b64decode(encoded))
    got = sha256_bytes(raw)
    if got != EXPECTED_SHA256:
        raise SystemExit(f"v330 payload integrity failure: expected {EXPECTED_SHA256}, got {got}")
    out = repo_root / "analysis" / "thesis_analysis_pipeline_v330_calibrated.py"
    out.write_bytes(raw)
    print(f"PASS materialized {out.relative_to(repo_root)}")
    print(f"SHA-256 {got}")
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true", help="run the reconstructed script after integrity verification")
    ap.add_argument("remainder", nargs=argparse.REMAINDER, help="arguments passed to the reconstructed script after --")
    args = ap.parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    script = materialize(repo_root)
    if args.run:
        rest = args.remainder
        if rest and rest[0] == "--":
            rest = rest[1:]
        raise SystemExit(subprocess.call([sys.executable, str(script), *rest], cwd=str(repo_root)))

if __name__ == "__main__":
    main()
