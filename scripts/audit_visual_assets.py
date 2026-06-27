#!/usr/bin/env python3
"""Validate deterministic visual-card sidecars before manual pixel review."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from PIL import Image


HANGUL = re.compile(r"[가-힣]")
CORRUPTION = re.compile(r"\?{2,}|\ufffd")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("images", nargs="+")
    args = parser.parse_args()
    errors: list[str] = []

    for raw in args.images:
        path = Path(raw).resolve()
        sidecar = path.with_suffix(path.suffix + ".visual.json")
        if not path.is_file():
            errors.append(f"image not found: {path}")
            continue
        try:
            with Image.open(path) as image:
                image.verify()
        except Exception as exc:
            errors.append(f"invalid image {path}: {exc}")
            continue
        if not sidecar.is_file():
            errors.append(f"missing visual sidecar: {sidecar}")
            continue
        data = json.loads(sidecar.read_text(encoding="utf-8-sig"))
        rendered = " ".join(str(item) for item in data.get("rendered_text", []))
        if CORRUPTION.search(rendered):
            errors.append(f"corrupted source text: {path}")
        if data.get("language") == "ko" and not HANGUL.search(rendered):
            errors.append(f"Korean text expected but no Hangul found: {path}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if data.get("sha256") != digest:
            errors.append(f"image changed after sidecar creation: {path}")

    if errors:
        print("BLOCKED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: {len(args.images)} visual source record(s); manual pixel review still required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


