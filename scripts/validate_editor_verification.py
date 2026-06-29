#!/usr/bin/env python3
"""Validate post-transfer editor evidence before save or publish."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_IMAGE_FIELDS = {
    "index",
    "role",
    "rendered",
    "caption_present",
    "anchor_found",
    "text_position",
    "text_artifact_found",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verification", required=True, type=Path)
    return parser.parse_args()


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = int(data.get("expected_image_count", -1))
    actual = int(data.get("actual_image_count", -2))
    images = data.get("images", [])
    body_chars = int(data.get("body_chars", 0))
    if expected < 1 or actual != expected or len(images) != expected:
        errors.append("editor image count does not match the manifest")
    if data.get("title_exact") is not True:
        errors.append("editor title does not exactly match")
    if data.get("body_text_clean") is not True or data.get("raw_marker_found") is True:
        errors.append("editor body contains missing or raw internal text")
    if int(data.get("tags_count", 0)) < 3:
        errors.append("fewer than three relevant tags are present")
    if data.get("disclosure_required") and not data.get("disclosure_present"):
        errors.append("required disclosure is not visible")
    if data.get("representative_image_index") != 1:
        errors.append("the scene-first image is not the representative image")
    if data.get("final_state_verified") is not True:
        errors.append("draft or publication state is not verified")

    positions = []
    roles = set()
    for image in images:
        missing = REQUIRED_IMAGE_FIELDS - image.keys()
        if missing:
            errors.append(f"image {image.get('index')} missing fields: {', '.join(sorted(missing))}")
            continue
        roles.add(image["role"])
        positions.append(int(image["text_position"]))
        if image["rendered"] is not True:
            errors.append(f"image {image['index']} did not render")
        if image["caption_present"] is not True:
            errors.append(f"image {image['index']} has no caption")
        if image["anchor_found"] is not True:
            errors.append(f"image {image['index']} is not near its intended section")
        if image["text_artifact_found"] is True:
            errors.append(f"image {image['index']} contains broken text artifacts")

    if body_chars >= 1800 and len(roles) < 3:
        errors.append("long post uses fewer than three visual roles")
    if positions and body_chars > 0:
        ordered = sorted(positions)
        if ordered[0] > body_chars * 0.2:
            errors.append("the first image appears too late")
        if body_chars >= 1800 and not any(body_chars * 0.25 <= value <= body_chars * 0.75 for value in ordered):
            errors.append("no image supports the middle of the article")
        if len(ordered) >= 3 and ordered[-1] - ordered[0] < body_chars * 0.35:
            errors.append("images are clustered instead of distributed through the article")
        if len(set(ordered)) != len(ordered):
            errors.append("multiple images share the same text position")
    return errors


def main() -> int:
    args = parse_args()
    try:
        data = json.loads(args.verification.read_text(encoding="utf-8"))
        errors = validate(data)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "blocked", "errors": [str(exc)]}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": "blocked" if errors else "pass", "errors": errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

