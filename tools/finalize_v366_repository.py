#!/usr/bin/env python3
"""Generate the current v366 repository file index and SHA-256 manifest.

The older FILE_INDEX.csv / MANIFEST_SHA256.csv are retained as the v365 closure
snapshots tied to the historical closure commit.  This script writes new v366
files instead of rewriting those historical snapshots.
"""
from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "FILE_INDEX_V366.csv"
MANIFEST = ROOT / "MANIFEST_V366_SHA256.csv"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def tracked_paths() -> list[str]:
    out = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    paths = [p.decode("utf-8") for p in out.split(b"\0") if p]
    # Generated files may not yet be tracked on the first run.
    for generated in (INDEX.name, MANIFEST.name):
        if generated not in paths:
            paths.append(generated)
    return sorted(set(paths))


def role_for(path: str) -> str:
    if path == INDEX.name:
        return "current v366 tracked-file index"
    if path == MANIFEST.name:
        return "current v366 SHA-256 integrity manifest (self excluded from hash rows)"
    if path.startswith(".github/workflows/"):
        return "continuous-integration workflow"
    if path.startswith("analysis/historical-provenance/"):
        return "historical analytical provenance"
    if path.startswith("analysis/"):
        return "analysis / release-validation code"
    if path.startswith("application/source-recovery/"):
        return "reviewed application-source recovery carrier / provenance"
    if path.startswith("application/static/"):
        return "application static asset / documented redistribution boundary"
    if path.startswith("application/commerce/"):
        return "Django application source"
    if path.startswith("application/ecommerce/"):
        return "Django project/runtime source or safe configuration"
    if path.startswith("application/"):
        return "application source / runtime / reproduction configuration"
    if path.startswith("benchmark/k6-scenarios/"):
        return "campaign k6 workload scenario script"
    if path.startswith("benchmark/orchestrator/"):
        return "campaign orchestrator"
    if path.startswith("benchmark/"):
        return "benchmark tooling"
    if path.startswith("configuration/reproduction/"):
        return "prospective public reproduction derivative; not historical proof"
    if path.startswith("configuration/platforms/"):
        return "platform-specific deployment configuration / evidence"
    if path.startswith("configuration/"):
        return "deployment/workload configuration and authority documentation"
    if path.startswith("data/canonical/"):
        return "canonical analytical dataset / dictionary"
    if path.startswith("data/raw-archive-manifests/"):
        return "raw-evidence integrity/availability record"
    if path.startswith("data/supplementary/"):
        return "supplementary analytical data / correction record"
    if path.startswith("documentation/"):
        return "repository documentation / static-asset manifest"
    if path.startswith("environment/"):
        return "environment / dependency / runtime evidence"
    if path.startswith("results/current-thesis/tables/"):
        return "historical/current-thesis table mirror namespace"
    if path.startswith("results/current-thesis/verification/"):
        return "historical/current-thesis verification artefact"
    if path.startswith("results/current-thesis/"):
        return "current-thesis documentation / crosswalk / research artefact"
    if path.startswith("results/figures/"):
        return "historical figure source / thesis figure carrier"
    if path.startswith("results/tables/"):
        return "table source / full-precision result carrier"
    if path.startswith("results/"):
        return "repository research artefact"
    if path.startswith("verification/"):
        return "verification / integrity record or executable QA"
    if path.startswith("tools/"):
        return "repository finalisation / QA tool"
    if path.startswith("LICENSE") or path == "LICENSING.md":
        return "licence / redistribution statement"
    if path == "CITATION.cff":
        return "citation metadata"
    if path.startswith("THESIS_"):
        return "thesis/repository alignment record"
    if path.startswith("REPOSITORY_") or path in {
        "README.md", "REPRODUCIBILITY.md", "DATA_AVAILABILITY.md",
        "ARTEFACT_PROVENANCE.md", "SECURITY_AND_REDACTION.md",
    }:
        return "repository documentation / provenance / closure note"
    if path.startswith("MANIFEST"):
        return "historical integrity manifest"
    if path.startswith("FILE_INDEX"):
        return "historical file index"
    return "repository research artefact"


def main() -> None:
    paths = tracked_paths()

    # Index first so the manifest hashes the final index bytes.
    with INDEX.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["path", "role"])
        for rel in paths:
            w.writerow([rel, role_for(rel)])

    manifest_paths = sorted(set(paths) - {MANIFEST.name})
    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["path", "size_bytes", "sha256"])
        for rel in manifest_paths:
            p = ROOT / rel
            if not p.is_file():
                raise SystemExit(f"tracked/generated file missing: {rel}")
            w.writerow([rel, p.stat().st_size, sha256(p)])

    print(f"wrote {INDEX.relative_to(ROOT)}: {len(paths)} indexed paths")
    print(f"wrote {MANIFEST.relative_to(ROOT)}: {len(manifest_paths)} hashed files; manifest self excluded")


if __name__ == "__main__":
    main()
