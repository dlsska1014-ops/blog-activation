#!/usr/bin/env python3
"""Validate a photo-led, non-template blog visual storyboard."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


TEXT_CARDS = {"comparison_table", "checklist_card", "summary_card", "faq_card"}
PHOTO_ROLES = {
    "ai_scene_thumbnail",
    "ai_context_scene",
    "original_photo",
    "owned_context_photo",
    "licensed_photo",
    "product_image",
}
ALLOWED_ORIGINS = {"owned", "licensed", "official", "merchant", "ai_generated", "self_created"}
BASE_CHECKS = {"semantic_match", "no_accidental_text", "no_fake_branding", "visual_polish"}
PHOTO_CHECKS = {"geometry_coherent", "lighting_coherent", "natural_texture", "weather_coherent"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    return parser.parse_args()


def body_chars(post: dict[str, Any], root: Path) -> int:
    if post.get("body_chars") is not None:
        return int(post["body_chars"])
    body_path = post.get("body_path")
    if body_path and (root / body_path).exists():
        return len((root / body_path).read_text(encoding="utf-8"))
    return 0


def validate_visual(visual: dict[str, Any], index: int) -> list[str]:
    errors = []
    prefix = f"visual {index}"
    origin = visual.get("origin")
    if origin not in ALLOWED_ORIGINS:
        errors.append(f"{prefix}: origin is missing or unsupported")
    for field in ("purpose", "section_anchor", "placement_ratio", "opened_original_resolution", "quality_checks"):
        if field not in visual:
            errors.append(f"{prefix}: {field} is required")
    try:
        ratio = float(visual.get("placement_ratio", -1))
        if not 0 <= ratio <= 1:
            errors.append(f"{prefix}: placement_ratio must be between 0 and 1")
    except (TypeError, ValueError):
        errors.append(f"{prefix}: placement_ratio must be numeric")
    if visual.get("opened_original_resolution") is not True:
        errors.append(f"{prefix}: original-resolution review is not confirmed")

    checks = visual.get("quality_checks") or {}
    required = set(BASE_CHECKS)
    if visual.get("role") in PHOTO_ROLES:
        required |= PHOTO_CHECKS
    failed = sorted(name for name in required if checks.get(name) is not True)
    if failed:
        errors.append(f"{prefix}: failed quality checks: {', '.join(failed)}")

    if origin == "ai_generated" and int(visual.get("candidate_count", 0)) < 2:
        errors.append(f"{prefix}: AI scene requires at least two candidates")
    if origin in {"owned", "licensed"} and visual.get("synthetic_weather_added") is not False:
        errors.append(f"{prefix}: owned or licensed photos must not add synthetic weather")
    if visual.get("role") in TEXT_CARDS:
        try:
            if float(visual.get("text_density", 1)) > 0.25:
                errors.append(f"{prefix}: text card density exceeds 25 percent")
        except (TypeError, ValueError):
            errors.append(f"{prefix}: text_density must be numeric")
        if visual.get("template_reuse") is not False:
            errors.append(f"{prefix}: repeated card template is not allowed")
    if len(str(visual.get("caption", "")).strip()) < 10:
        errors.append(f"{prefix}: caption is missing or not useful")
    return errors


def validate_post(post: dict[str, Any], root: Path) -> list[str]:
    errors = []
    visuals = post.get("visuals") or []
    chars = body_chars(post, root)
    long_post = chars >= 1800
    minimum = 4 if long_post else 3
    if len(visuals) < minimum:
        errors.append(f"requires at least {minimum} visuals")
    if not visuals:
        return errors

    for index, visual in enumerate(visuals, 1):
        errors.extend(validate_visual(visual, index))

    roles = [visual.get("role") for visual in visuals]
    origins = [visual.get("origin") for visual in visuals]
    text_card_indexes = [index for index, role in enumerate(roles) if role in TEXT_CARDS]
    photo_count = sum(role in PHOTO_ROLES for role in roles)
    non_ai_count = sum(origin != "ai_generated" for origin in origins)
    ai_count = sum(origin == "ai_generated" for origin in origins)
    if long_post and len(set(roles)) < 3:
        errors.append("long post needs at least three visual roles")
    if long_post and photo_count < 2:
        errors.append("long post needs at least two photographic visuals")
    if long_post and non_ai_count < 2:
        errors.append("long post needs at least two non-AI visual origins")
    if ai_count > 1:
        errors.append("use no more than one AI-generated scene per post")
    if len(text_card_indexes) > 1:
        errors.append("use no more than one text card per post")
    if roles[0] not in PHOTO_ROLES:
        errors.append("first visual must be photographic and scene-first")
    if float(visuals[0].get("placement_ratio", 1)) > 0.2:
        errors.append("first visual appears too late")
    ratios = [float(visual.get("placement_ratio", -1)) for visual in visuals if isinstance(visual.get("placement_ratio"), (int, float))]
    if long_post and not any(0.25 <= ratio <= 0.6 for ratio in ratios):
        errors.append("no visual supports the middle section")
    if long_post and not any(ratio >= 0.6 for ratio in ratios):
        errors.append("no visual supports the later section")
    if len(set(origins)) < 2:
        errors.append("visual origins are not diverse")
    return errors


def main() -> int:
    args = parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        posts = manifest.get("posts") or []
        all_errors = []
        for index, post in enumerate(posts, 1):
            for error in validate_post(post, args.manifest.parent):
                all_errors.append(f"post {index}: {error}")
        if not posts:
            all_errors.append("manifest has no posts")
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "blocked", "errors": [str(exc)]}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": "blocked" if all_errors else "pass", "errors": all_errors}, ensure_ascii=False, indent=2))
    return 1 if all_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

