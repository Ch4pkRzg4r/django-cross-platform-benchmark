#!/usr/bin/env python3
"""Verify the Git-tracked v330 analytical update without controlled heavy evidence.

This check is intentionally repository-local. It verifies byte integrity of the
v330 source payload/materialized source, canonical data hash, the v330 delta
manifest, the complete 16-table current namespace, and publication-asset hash
registry metadata. It does NOT claim to replace the full controlled-evidence
pipeline run that requires Docker telemetry and exact publication references.
"""
from __future__ import annotations
import base64, csv, gzip, hashlib, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_MASTER = "710b3a7a79d794425ac04254caba892419ad78f56cf4c174843e3c417c5ebde7"
EXPECTED_PIPELINE = "d4c5febbd8c778c7089f59228a696e9eb63c5aa733090e080f41a0496335b574"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def fail(msg: str) -> None:
    print(f"FAIL {msg}")
    raise SystemExit(2)


def ok(msg: str) -> None:
    print(f"PASS {msg}")


def main() -> None:
    master = ROOT / "data" / "canonical" / "master_runs.csv"
    if sha256_file(master) != EXPECTED_MASTER:
        fail("canonical master_runs.csv SHA-256")
    ok("canonical master_runs.csv SHA-256")

    parts = [ROOT / "analysis" / "v330-payload" / f"payload_{i:02d}.b64" for i in range(1, 6)]
    if not all(p.is_file() for p in parts):
        fail("all five v330 source payload parts exist")
    encoded = "".join(p.read_text(encoding="ascii").strip() for p in parts)
    raw = gzip.decompress(base64.b64decode(encoded))
    if sha256_bytes(raw) != EXPECTED_PIPELINE:
        fail("reconstructed v330 controlling source SHA-256")
    ok("reconstructed v330 controlling source SHA-256")

    manifest = ROOT / "MANIFEST_V330_UPDATE_SHA256.csv"
    with manifest.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    checked = 0
    for row in rows:
        rel = row["path"]
        expected = row["sha256"].lower()
        if rel.startswith("MATERIALIZED:"):
            if expected != EXPECTED_PIPELINE:
                fail("materialized-target manifest hash")
            continue
        path = ROOT / rel
        if not path.is_file():
            fail(f"manifested file missing: {rel}")
        got = sha256_file(path)
        if got != expected:
            fail(f"SHA-256 mismatch: {rel}; expected {expected}, got {got}")
        checked += 1
    ok(f"v330 delta manifest verified for {checked} Git-tracked files plus materialized target")

    tables = sorted((ROOT / "results" / "current-thesis" / "tables").glob("Table_4_*.csv"))
    expected_names = [f"Table_4_{i:02d}.csv" for i in range(1, 17)]
    if [p.name for p in tables] != expected_names:
        fail("current-thesis Table 4.1-4.16 namespace")
    ok("current-thesis Table 4.1-4.16 namespace complete (16/16)")

    fig_manifest = ROOT / "results" / "current-thesis" / "verification" / "PUBLISHED_FIGURE_SHA256_MANIFEST.csv"
    with fig_manifest.open("r", encoding="utf-8-sig", newline="") as f:
        fig_rows = list(csv.DictReader(f))
    if len(fig_rows) != 18 or not all(str(r.get("byte_identical", "")).lower() == "true" for r in fig_rows):
        fail("published-figure hash registry has 18 byte-identical PASS rows")
    ok("published-figure hash registry has 18 byte-identical PASS rows")

    required = [
        ROOT / "README.md",
        ROOT / "REPRODUCIBILITY.md",
        ROOT / "DATA_AVAILABILITY.md",
        ROOT / "FILE_INDEX_v330.csv",
        ROOT / "analysis" / "materialize_v330_pipeline.py",
        ROOT / "analysis" / "run_v330_from_repo.py",
        ROOT / "results" / "current-thesis" / "verification" / "EXACT_TABLE_MIRROR_CHECK.txt",
        ROOT / "results" / "current-thesis" / "verification" / "NUMERIC_REGRESSION_CHECK_v329.txt",
        ROOT / "results" / "current-thesis" / "verification" / "DATA_DRIVEN_MUTATION_TEST.txt",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.is_file()]
    if missing:
        fail("required current-v330 files missing: " + ", ".join(missing))
    ok("required current-v330 documentation and verification records present")

    print("\nOVERALL V330 REPOSITORY STATE: PASS")


if __name__ == "__main__":
    main()
