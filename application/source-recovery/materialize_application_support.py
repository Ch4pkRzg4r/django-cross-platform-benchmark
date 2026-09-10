#!/usr/bin/env python3
"""Materialize the reviewed v365 application-support payload.

The payload contains only support modules, migrations, templates and template tags
recovered from the retained 2026-06-24 public-release archive. Existing core files
are never overwritten by default.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import tarfile
from pathlib import Path

EXPECTED_PAYLOAD_SHA256 = "7a4dacc5a01390c4b9d887d5ee5c4fb22c884d0054ab966ece5dc00a76b3ed7c"
PAYLOAD_NAME = "application_support_v365.b64"


def safe_members(tf: tarfile.TarFile):
    for member in tf.getmembers():
        p = Path(member.name)
        if p.is_absolute() or ".." in p.parts:
            raise RuntimeError(f"Unsafe payload path: {member.name}")
        yield member


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--target",
        default=str(Path(__file__).resolve().parents[1]),
        help="Application directory to populate (default: repository application/)",
    )
    ap.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow replacement of an already-existing file. Default is fail closed.",
    )
    args = ap.parse_args()

    here = Path(__file__).resolve().parent
    payload_path = here / PAYLOAD_NAME
    raw = base64.b64decode(payload_path.read_text(encoding="utf-8"))
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_PAYLOAD_SHA256:
        raise RuntimeError(
            f"Payload SHA-256 mismatch: expected {EXPECTED_PAYLOAD_SHA256}, got {digest}"
        )

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)

    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tf:
        members = list(safe_members(tf))
        for member in members:
            if not member.isfile():
                continue
            # Payload layout is ./application/<relative path> plus ./README.txt.
            p = Path(member.name)
            parts = [x for x in p.parts if x not in (".", "")]
            if not parts or parts[0] != "application":
                continue
            rel = Path(*parts[1:])
            out = target / rel
            if out.exists() and not args.overwrite:
                raise FileExistsError(
                    f"Refusing to overwrite existing file: {out}. "
                    "Use --overwrite only after reviewing the provenance boundary."
                )

        for member in members:
            if not member.isfile():
                continue
            p = Path(member.name)
            parts = [x for x in p.parts if x not in (".", "")]
            if not parts or parts[0] != "application":
                continue
            rel = Path(*parts[1:])
            out = target / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            src = tf.extractfile(member)
            if src is None:
                raise RuntimeError(f"Could not extract {member.name}")
            out.write_bytes(src.read())
            print(f"materialized {rel.as_posix()}")

    print(f"PASS: payload SHA-256 {digest}")


if __name__ == "__main__":
    main()
