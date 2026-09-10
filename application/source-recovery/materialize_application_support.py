#!/usr/bin/env python3
"""Materialize the reviewed v365 application-support payload.

The payload contains support modules, migrations, templates and template tags
recovered from the retained 2026-06-24 public-release archive.

Existing files are handled safely:
- if an existing file is byte-identical to the payload copy, it is skipped;
- if an existing file differs, materialisation fails unless --overwrite is used.
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


def payload_path_for(member: tarfile.TarInfo) -> Path | None:
    p = Path(member.name)
    parts = [x for x in p.parts if x not in (".", "")]
    if not parts or parts[0] != "application" or len(parts) == 1:
        return None
    return Path(*parts[1:])


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
        help="Allow replacement of an existing non-identical file.",
    )
    args = ap.parse_args()

    here = Path(__file__).resolve().parent
    payload_file = here / PAYLOAD_NAME
    raw = base64.b64decode(payload_file.read_text(encoding="utf-8"))
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_PAYLOAD_SHA256:
        raise RuntimeError(
            f"Payload SHA-256 mismatch: expected {EXPECTED_PAYLOAD_SHA256}, got {digest}"
        )

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)

    written = 0
    identical = 0

    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tf:
        members = list(safe_members(tf))

        # Preflight the full payload before writing anything.
        planned = []
        for member in members:
            if not member.isfile():
                continue
            rel = payload_path_for(member)
            if rel is None:
                continue
            src = tf.extractfile(member)
            if src is None:
                raise RuntimeError(f"Could not read {member.name}")
            data = src.read()
            out = target / rel

            if out.exists():
                if out.read_bytes() == data:
                    planned.append((out, data, "identical"))
                    continue
                if not args.overwrite:
                    raise FileExistsError(
                        f"Refusing to overwrite non-identical file: {out}. "
                        "Use --overwrite only after reviewing the provenance boundary."
                    )
                planned.append((out, data, "overwrite"))
            else:
                planned.append((out, data, "create"))

        for out, data, action in planned:
            if action == "identical":
                identical += 1
                print(f"identical   {out.relative_to(target).as_posix()}")
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
            written += 1
            print(f"{action:10s} {out.relative_to(target).as_posix()}")

    print(f"PASS: payload SHA-256 {digest}")
    print(f"PASS: written={written}, identical-skipped={identical}")


if __name__ == "__main__":
    main()
