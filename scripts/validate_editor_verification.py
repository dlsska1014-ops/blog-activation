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
    "source_fingerprint",
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
    platform = str(data.get("platform", "")).strip().casefold()
    if platform not in {"naver", "tistory"}:
        errors.append("platform must be naver or tistory")
    if data.get("topic_or_category_selected") is not True:
        errors.append("platform topic or category is not selected")
    if not str(data.get("topic_or_category_label", "")).strip():
        errors.append("platform topic or category label is missing")
    if data.get("non_affiliate_monetization_language_found") is True:
        errors.append("non-affiliate public copy exposes monetization workflow language")
    if platform == "tistory":
        if str(data.get("editor_mode", "")).strip().casefold() != "basic":
            errors.append("Tistory editor must remain in basic mode")
        if data.get("single_editor_tab") is not True:
            errors.append("Tistory requires exactly one editor tab")
        if data.get("mode_switch_used") is not False:
            errors.append("Tistory mode switching is not allowed during unattended transfer")
        if data.get("unsaved_recovery_present") is not False:
            errors.append("Tistory editor has an uncertain recovery state")
        if data.get("upload_in_progress") is not False:
            errors.append("Tistory still has an active image upload")
        if data.get("caption_contamination_found") is not False:
            errors.append("Tistory image caption contains body text")
        if int(data.get("long_caption_count", -1)) != 0:
            errors.append("Tistory contains an overlong image caption")
        if data.get("image_anchor_order_verified") is not True:
            errors.append("Tistory image anchor order is not verified")
        if data.get("body_replaced_after_image_insert") is not False:
            errors.append("Tistory body was replaced after image insertion")
        if str(data.get("mode", "")).strip().casefold() == "draft-only":
            try:
                before = int(data.get("draft_count_before"))
                after = int(data.get("draft_count_after"))
                if after != before + 1:
                    errors.append("Tistory draft count did not increase by exactly one")
            except (TypeError, ValueError):
                errors.append("Tistory draft counts are missing")
    if data.get("disclosure_required") and not data.get("disclosure_present"):
        errors.append("required disclosure is not visible")
    if data.get("representative_image_index") != 1:
        errors.append("the scene-first image is not the representative image")
    if int(data.get("editor_figure_count", -1)) != expected:
        errors.append("editor figure count does not match the manifest")
    if int(data.get("orphan_figure_count", -1)) != 0:
        errors.append("editor contains empty or orphan image figures")
    if int(data.get("duplicate_image_count", -1)) != 0:
        errors.append("editor contains duplicate images")
    if data.get("editor_image_sequence_unique") is not True:
        errors.append("editor image sequence is not unique")
    if int(data.get("duplicate_body_block_count", -1)) != 0:
        errors.append("editor body contains duplicated blocks")
    if data.get("final_state_verified") is not True:
        errors.append("draft or publication state is not verified")

    positions = []
    roles = set()
    source_fingerprints = []
    for image in images:
        missing = REQUIRED_IMAGE_FIELDS - image.keys()
        if missing:
            errors.append(f"image {image.get('index')} missing fields: {', '.join(sorted(missing))}")
            continue
        roles.add(image["role"])
        positions.append(int(image["text_position"]))
        fingerprint = str(image["source_fingerprint"]).strip()
        if not fingerprint:
            errors.append(f"image {image['index']} has no source fingerprint")
        source_fingerprints.append(fingerprint)
        if image["rendered"] is not True:
            errors.append(f"image {image['index']} did not render")
        if image["caption_present"] is not True:
            errors.append(f"image {image['index']} has no caption")
        if image["anchor_found"] is not True:
            errors.append(f"image {image['index']} is not near its intended section")
        if image["text_artifact_found"] is True:
            errors.append(f"image {image['index']} contains broken text artifacts")

    fingerprints = [item for item in source_fingerprints if item]
    if len(fingerprints) != len(set(fingerprints)):
        errors.append("editor image fingerprints are duplicated")

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
