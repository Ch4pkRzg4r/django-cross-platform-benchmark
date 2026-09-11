#!/usr/bin/env python3
"""Verify the v366 documentation/provenance/reproduction closure.

This check is intentionally repository-local. It does not rerun the historical
campaign and does not invent missing historical evidence.
"""
from __future__ import annotations

import csv
import hashlib
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def fail(msg: str) -> None:
    print(f"FAIL {msg}")
    raise SystemExit(2)


def ok(msg: str) -> None:
    print(f"PASS {msg}")


def text(rel: str) -> str:
    p = ROOT / rel
    if not p.is_file():
        fail(f"required file missing: {rel}")
    return p.read_text(encoding="utf-8-sig")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    readme = text("README.md")
    if "public source/computational research repository" not in readme:
        fail("README public-repository status")
    if "document candidate is **v366**" not in readme or "computational repository release remains v360" not in text("REPRODUCIBILITY.md"):
        fail("document v366 / computational v360 distinction")
    if "v330" not in readme:
        fail("v330 frozen-base authority documented")
    ok("document/repository authority hierarchy")

    dictionary = text("data/canonical/DATA_DICTIONARY.md")
    if "author to confirm" in dictionary.lower():
        fail("data dictionary still contains unresolved author-to-confirm text")
    expected_fields = [
        "run_id","platform","scenario","replication","start_time","end_time","test_duration_s","target_rps",
        "rps_actual","goodput_rps","total_requests","total_errors","error_rate","latency_p50","latency_p90",
        "latency_p95","latency_p99","latency_p999","latency_mean","latency_min","latency_max","latency_stddev",
        "latency_cv","dns_p50","dns_p95","tcp_p50","tcp_p95","tls_p50","tls_p95","waiting_p50","waiting_p95",
        "waiting_p99","apdex_t500_f2000","bytes_received","bytes_sent","bandwidth_rx_bps","k6_iterations",
        "first_ts","last_ts",
    ]
    found = re.findall(r"^\| `([^`]+)` \|", dictionary, flags=re.M)
    if found[:39] != expected_fields or len(found) < 39:
        fail(f"data dictionary field order/completeness: found {len(found)} field rows")
    for required in ["three GET requests per iteration", "5→40→5", "bytes per second, not bits per second", "Blank is **not zero**", "latency-only Apdex-style"]:
        if required not in dictionary:
            fail(f"data dictionary semantic note missing: {required}")
    ok("complete 39-field dictionary and scenario-specific rate semantics")

    avail = text("data/raw-archive-manifests/AVAILABILITY_AND_RECONSTRUCTION.md")
    if "73 complete canonical run pairs" not in avail or "207 of the 280 canonical run pairs unavailable" not in avail:
        fail("raw availability 73/207 disclosure")
    if "complete campaign raw data" in avail.lower() and "retained locally in verified multipart rar" in avail.lower():
        fail("obsolete complete-local-RAR claim still present")
    ok("raw evidence availability bounded to audited recoverable coverage")

    data_avail = text("DATA_AVAILABILITY.md")
    if "Public in this repository" not in data_avail or "73 complete canonical" not in data_avail:
        fail("top-level data availability alignment")
    ok("public/private data-availability alignment")

    # Prospective Nginx/uWSGI recipe must be internally consistent, while historical conflict remains documented.
    u = text("configuration/reproduction/nginx-uwsgi-v366/uwsgi.ini")
    n = text("configuration/reproduction/nginx-uwsgi-v366/nginx.conf")
    d = text("configuration/reproduction/nginx-uwsgi-v366/Dockerfile")
    recipe_readme = text("configuration/reproduction/nginx-uwsgi-v366/README.md")
    socket = "/run/uwsgi/django.sock"
    if socket not in u or socket not in n:
        fail("prospective Nginx/uWSGI socket agreement")
    if not re.search(r"(?m)^processes\s*=\s*2\s*$", u) or not re.search(r"(?m)^threads\s*=\s*4\s*$", u):
        fail("prospective Nginx/uWSGI 2x4 execution layout")
    if "COPY application/ /app/" not in d or "repository root" not in recipe_readme:
        fail("prospective Nginx/uWSGI build-context recipe")
    historical_u = text("configuration/uwsgi.ini")
    historical_n = text("configuration/nginx-uwsgi.conf")
    if "127.0.0.1:3031" not in historical_u or "processes        = 4" not in historical_u or "threads          = 2" not in historical_u:
        fail("historical conflicting uWSGI file was unexpectedly rewritten")
    if socket not in historical_n:
        fail("historical Nginx UNIX-socket evidence missing")
    if "prospective" not in text("configuration/platforms/README.md").lower():
        fail("Nginx prospective/historical boundary documentation")
    ok("Nginx/uWSGI historical conflict preserved and prospective recipe consistent")

    scenario_auth = text("configuration/SCENARIO_AUTHORITY_V366.md")
    for required in ["three GETs per iteration", "5 baseline", "40", "historical scalar metadata"]:
        if required not in scenario_auth:
            fail(f"scenario authority missing: {required}")
    ok("final workload-script/rate authority documented")

    figmap = text("results/current-thesis/figure_map_v366.csv")
    rows = list(csv.DictReader(figmap.splitlines()))
    expected = ["4.1","4.2","4.3","4.4","4.5","4.6","4.7","4.8a","4.8b","4.8c","4.8d","4.8e","4.8f"]
    if [r["Figure"] for r in rows] != expected:
        fail("v366 current-thesis figure crosswalk")
    if "Figure 4.13" not in text("results/current-thesis/README.md") or "historical" not in text("results/current-thesis/README.md").lower():
        fail("historical figure namespace not clearly bounded")
    ok("current v366 figure map separated from historical wrapper namespace")

    prov = text("ARTEFACT_PROVENANCE.md")
    sec = text("SECURITY_AND_REDACTION.md")
    if "current public `application/commerce/views.py`" not in prov or "byte-compiles" not in prov:
        fail("current recovered views.py provenance")
    if "does not apply to the current public" not in sec:
        fail("security document historical redaction scope")
    ok("historical source-redaction artefact scoped away from current recovered source")

    alignment = text("THESIS_V366_ALIGNMENT.md")
    for required in ["PERMANOVA/PERMDISP boundary", "73 complete canonical", "prospective public rerun recipe", "Figure 4.8"]:
        if required not in alignment:
            fail(f"v366 alignment missing: {required}")
    ok("v366 alignment record complete")

    # Current generated index/manifest.
    index = ROOT / "FILE_INDEX_V366.csv"
    manifest = ROOT / "MANIFEST_V366_SHA256.csv"
    if not index.is_file() or not manifest.is_file():
        fail("v366 index/manifest missing; run tools/finalize_v366_repository.py")

    tracked_raw = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    expected_paths = {p.decode("utf-8") for p in tracked_raw.split(b"\0") if p}
    expected_paths.update({index.name, manifest.name})
    with index.open("r", encoding="utf-8-sig", newline="") as f:
        idx_rows = list(csv.DictReader(f))
    indexed = {r["path"] for r in idx_rows}
    if indexed != expected_paths:
        fail(f"FILE_INDEX_V366 path set mismatch: indexed={len(indexed)} expected={len(expected_paths)}")

    with manifest.open("r", encoding="utf-8-sig", newline="") as f:
        man_rows = list(csv.DictReader(f))
    manifested = {r["path"] for r in man_rows}
    expected_manifested = expected_paths - {manifest.name}
    if manifested != expected_manifested:
        fail(f"MANIFEST_V366 path set mismatch: rows={len(manifested)} expected={len(expected_manifested)}")
    for row in man_rows:
        p = ROOT / row["path"]
        if not p.is_file() or p.stat().st_size != int(row["size_bytes"]) or sha256(p) != row["sha256"].lower():
            fail(f"v366 manifest mismatch: {row['path']}")
    ok(f"v366 tracked-file index and SHA-256 manifest ({len(man_rows)} hashed files; self excluded)")

    print("\nOVERALL V366 REPOSITORY CLOSURE: PASS")


if __name__ == "__main__":
    main()
