#!/usr/bin/env python3
"""Self-test the photo-led visual storyboard gate."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate_visual_storyboard.py")
SPEC = importlib.util.spec_from_file_location("validate_visual_storyboard", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def checks(photo: bool = True) -> dict:
    values = {
        "semantic_match": True,
        "no_accidental_text": True,
        "no_fake_branding": True,
        "visual_polish": True,
    }
    if photo:
        values.update(
            {
                "geometry_coherent": True,
                "lighting_coherent": True,
                "natural_texture": True,
                "weather_coherent": True,
            }
        )
    return values


def visual(index: int, role: str, origin: str, ratio: float) -> dict:
    item = {
        "path": f"images/{index}.jpg",
        "role": role,
        "origin": origin,
        "purpose": f"purpose {index}",
        "section_anchor": f"section {index}",
        "placement_ratio": ratio,
        "opened_original_resolution": True,
        "quality_checks": checks(role in MODULE.PHOTO_ROLES),
        "caption": "독자가 이 장면에서 확인해야 할 실제 기준을 설명합니다.",
    }
    if origin in {"owned", "licensed"}:
        item["synthetic_weather_added"] = False
    if origin == "ai_generated":
        item["candidate_count"] = 2
    if role in MODULE.TEXT_CARDS:
        item["text_density"] = 0.18
        item["template_reuse"] = False
    return item


def main() -> int:
    good = {
        "body_chars": 2400,
        "visuals": [
            visual(1, "licensed_photo", "licensed", 0.08),
            visual(2, "official_screenshot", "official", 0.32),
            visual(3, "owned_context_photo", "owned", 0.55),
            visual(4, "checklist_card", "self_created", 0.78),
        ],
    }
    assert MODULE.validate_post(good, Path(".")) == []

    bad = {
        "body_chars": 2400,
        "visuals": [
            visual(1, "licensed_photo", "licensed", 0.7),
            visual(2, "comparison_table", "self_created", 0.72),
            visual(3, "diagram", "self_created", 0.74),
            visual(4, "checklist_card", "self_created", 0.76),
        ],
    }
    bad["visuals"][0]["synthetic_weather_added"] = True
    errors = MODULE.validate_post(bad, Path("."))
    assert any("text card" in error for error in errors), errors
    assert any("synthetic weather" in error for error in errors), errors
    assert any("photographic visuals" in error for error in errors), errors
    print("PASS: visual storyboard gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
