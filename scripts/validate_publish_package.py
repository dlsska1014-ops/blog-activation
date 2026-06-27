#!/usr/bin/env python3
"""Validate a blog publication package before browser transfer."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from PIL import Image


RAW_MARKERS = {
    "markdown heading": re.compile(r"(?m)^#{1,6}\s"),
    "markdown table separator": re.compile(r"(?m)^\s*\|?\s*:?-{3,}"),
    "code fence": re.compile(r"```"),
    "image placeholder": re.compile(r"\[(?:이미지|image)\s*\d*\]", re.I),
}


def validate_post(post: dict, base: Path) -> list[str]:
    errors: list[str] = []
    name = post.get("title") or "untitled"
    body_path = base / str(post.get("body_path", ""))
    if not body_path.is_file():
        return [f"{name}: body file not found: {body_path}"]

    body = body_path.read_text(encoding="utf-8").strip()
    if len(body) < 800:
        errors.append(f"{name}: body is too short ({len(body)} characters)")
    for label, pattern in RAW_MARKERS.items():
        if pattern.search(body):
            errors.append(f"{name}: contains {label}")

    tags = [str(tag).strip() for tag in post.get("tags", []) if str(tag).strip()]
    if len(tags) < 3:
        errors.append(f"{name}: provide at least 3 tags")

    images = post.get("image_paths", [])
    expected = int(post.get("expected_image_count", 3))
    if len(images) < expected:
        errors.append(f"{name}: expected {expected} images, manifest has {len(images)}")
    for raw in images:
        path = base / str(raw)
        if not path.is_file():
            errors.append(f"{name}: image not found: {path}")
            continue
        try:
            with Image.open(path) as image:
                image.verify()
            with Image.open(path) as image:
                width, height = image.size
            if width < 600 or height < 338:
                errors.append(f"{name}: image is too small: {path} ({width}x{height})")
        except Exception as exc:
            errors.append(f"{name}: invalid image {path}: {exc}")

    if post.get("affiliate"):
        disclosure = str(post.get("disclosure_text", "")).strip()
        if not disclosure or disclosure not in body[:600]:
            errors.append(f"{name}: affiliate disclosure missing near the top")
        if not post.get("verified_links"):
            errors.append(f"{name}: affiliate links are not marked verified")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", help="JSON manifest path")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    posts = data.get("posts", [])
    errors = [] if posts else ["manifest contains no posts"]
    for post in posts:
        errors.extend(validate_post(post, manifest_path.parent))

    if errors:
        print("BLOCKED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: {len(posts)} post(s) ready for editor transfer")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


