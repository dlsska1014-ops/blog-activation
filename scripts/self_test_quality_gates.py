#!/usr/bin/env python3
"""Run regression tests for the blog publication quality gates."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from PIL import Image, ImageDraw

from prepare_owned_photo import prepare_photo
from validate_publish_package import validate_post


def make_image(path: Path, kind: str, variant: int = 0) -> None:
    image = Image.new("RGB", (900, 600), (235, 240, 245))
    draw = ImageDraw.Draw(image)
    if kind == "scene":
        for index in range(12):
            draw.ellipse(
                (index * 60, 30 + index * 20, index * 60 + 220, 260 + index * 20),
                fill=(30 + index * 12, 110, 190 - index * 8),
            )
    elif kind == "stripes":
        for x in range(0, 900, 30):
            draw.rectangle((x, 0, x + 12, 599), fill=(20 + x % 180, 90, 150))
    elif kind == "flat":
        draw.rectangle((80, 80, 820, 520), fill=(40 + variant * 90, 100, 170 - variant * 50))
    if variant == 9:
        draw.rectangle((700, 500, 710, 510), fill=(0, 0, 0))
    image.save(path)


class QualityGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        body = "\n\n".join(
            f"Paragraph {index} gives a distinct reader decision, source boundary, caution, and practical next step so the publication package has enough useful editorial detail."
            for index in range(8)
        )
        (self.root / "body.txt").write_text(body, encoding="utf-8")
        make_image(self.root / "scene.png", "scene")
        make_image(self.root / "flat1.png", "flat", 0)
        make_image(self.root / "flat2.png", "flat", 1)

        self.post = {
            "title": "장마철 제습기 선택 기준",
            "body_path": "body.txt",
            "naturalness_qa_confirmed": True,
            "fact_freshness": {
                "level": "stable",
                "checked_date": date.today().isoformat(),
                "fact_qa_confirmed": True,
                "source_records": [],
                "fact_note": "Synthetic evergreen test package",
            },
            "intent_decision": {
                "action": "new_post",
                "reader_question": "장마철 제습기를 공간에 맞게 어떻게 골라야 할까",
                "duplicate_risk": "low",
                "difference_note": "공간과 생활 동선을 기준으로 비교",
                "cluster_key": "장마철 습기 관리",
                "cluster_role": "buying_guide",
            },
            "internal_links": [],
            "internal_link_note": "No relevant existing post in the synthetic fixture",
            "internal_link_qa_confirmed": True,
            "experience_basis": "research_only",
            "tags": ["제습기", "장마준비", "습도관리"],
            "expected_image_count": 3,
            "visual_qa_confirmed": True,
            "text_bearing_image_count": 0,
            "visuals": [
                {
                    "path": "scene.png",
                    "role": "ai_scene_thumbnail",
                    "caption": "",
                    "contains_text": False,
                    "visual_qa_confirmed": True,
                },
                {
                    "path": "flat1.png",
                    "role": "diagram",
                    "caption": "공간별 선택 기준",
                    "contains_text": False,
                    "visual_qa_confirmed": True,
                },
                {
                    "path": "flat2.png",
                    "role": "checklist_card",
                    "caption": "구매 전 확인 항목",
                    "contains_text": False,
                    "visual_qa_confirmed": True,
                },
            ],
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def prepare_owned(self, source_name: str, output_name: str, variant: int) -> dict:
        source = self.root / source_name
        make_image(source, "scene", variant)
        output = self.root / output_name
        prepare_photo(source, output, [], 1600, 90, True)
        return {
            "path": output.name,
            "role": "owned_context_photo",
            "caption": "",
            "contains_text": False,
            "visual_qa_confirmed": True,
            "ownership_basis": "user-owned neutral context photo",
            "privacy_qa_confirmed": True,
            "location_metadata_removed": True,
            "privacy_note": "Full-resolution synthetic review completed",
        }

    def test_distinct_flat_visuals_do_not_trigger_photo_duplicate_gate(self) -> None:
        self.assertEqual(validate_post(self.post, self.root), [])

    def test_owned_context_photo_is_allowed_in_research_only_post(self) -> None:
        post = copy.deepcopy(self.post)
        post["visuals"][0] = self.prepare_owned("owned-source.png", "owned.jpg", 0)
        self.assertEqual(validate_post(post, self.root), [])

    def test_near_duplicate_owned_photos_are_blocked(self) -> None:
        post = copy.deepcopy(self.post)
        first = self.prepare_owned("owned-a.png", "owned-a.jpg", 0)
        second = self.prepare_owned("owned-b.png", "owned-b.jpg", 9)
        second["caption"] = "비슷한 두 번째 장면"
        post["visuals"] = [first, second, post["visuals"][1]]
        errors = validate_post(post, self.root)
        self.assertTrue(any("near-duplicate owned photos" in error for error in errors), errors)

    def test_owned_photo_change_after_preparation_is_blocked(self) -> None:
        post = copy.deepcopy(self.post)
        owned = self.prepare_owned("owned-change-source.png", "owned-change.jpg", 0)
        post["visuals"][0] = owned
        path = self.root / "owned-change.jpg"
        with Image.open(path) as opened:
            changed = opened.convert("RGB")
        changed.putpixel((0, 0), (255, 0, 0))
        changed.save(path, quality=90)
        errors = validate_post(post, self.root)
        self.assertTrue(any("changed after privacy preparation" in error for error in errors), errors)

    def test_photo_preparation_strips_exif_and_records_blur(self) -> None:
        source = self.root / "exif-source.jpg"
        image = Image.new("RGB", (1200, 800), (120, 160, 200))
        exif = Image.Exif()
        exif[274] = 6
        exif[306] = "2026:06:27 10:00:00"
        image.save(source, exif=exif)
        output = self.root / "prepared.jpg"
        sidecar = prepare_photo(source, output, [(10, 10, 120, 100)], 1000, 88, True)
        record = json.loads(sidecar.read_text(encoding="utf-8"))
        with Image.open(output) as checked:
            self.assertEqual(len(checked.getexif()), 0)
            self.assertLessEqual(max(checked.size), 1000)
        self.assertTrue(record["metadata_removed"])
        self.assertTrue(record["manual_privacy_review_confirmed"])
        self.assertEqual(record["blur_regions"], [[10, 10, 120, 100]])

    def test_stale_current_facts_are_blocked(self) -> None:
        post = copy.deepcopy(self.post)
        stale = (date.today() - timedelta(days=8)).isoformat()
        post["fact_freshness"] = {
            "level": "current",
            "checked_date": stale,
            "fact_qa_confirmed": True,
            "source_records": [
                {
                    "source_name": "Official fixture",
                    "url": "https://example.com/official",
                    "source_type": "official",
                    "checked_date": stale,
                    "claim_summary": "Synthetic current condition",
                }
            ],
        }
        errors = validate_post(post, self.root)
        self.assertTrue(any("facts are stale" in error for error in errors), errors)

    def test_risky_title_claim_without_evidence_is_blocked(self) -> None:
        post = copy.deepcopy(self.post)
        post["title"] = "장마철 제습기 완벽 선택 기준"
        errors = validate_post(post, self.root)
        self.assertTrue(any("title_claim_evidence" in error for error in errors), errors)

    def test_risky_title_claim_needs_a_recorded_source(self) -> None:
        post = copy.deepcopy(self.post)
        post["title"] = "장마철 제습기 완벽 선택 기준"
        post["title_claim_evidence"] = "Synthetic claim note without a source"
        errors = validate_post(post, self.root)
        self.assertTrue(any("risky title claim needs a recorded source" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main(verbosity=2)
