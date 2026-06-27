#!/usr/bin/env python3
"""Validate a blog publication package before browser transfer."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from PIL import Image


RAW_MARKERS = {
    "markdown heading": re.compile(r"(?m)^#{1,6}\s"),
    "markdown table separator": re.compile(r"(?m)^\s*\|?\s*:?-{3,}"),
    "code fence": re.compile(r"```"),
    "image placeholder": re.compile(r"\[(?:이미지|image)\s*\d*\]", re.I),
    "inline markdown code": re.compile(r"`[^`\n]+`"),
    "internal image note": re.compile(r"(?:이미지\s*메모|visual\s*prompt|thumbnail\s*prompt)\s*:", re.I),
}
VISUAL_CORRUPTION = re.compile(r"\?{2,}|\ufffd")
ALLOWED_VISUAL_ROLES = {
    "ai_scene_thumbnail",
    "original_photo",
    "licensed_photo",
    "official_screenshot",
    "source_evidence",
    "diagram",
    "comparison_table",
    "checklist_card",
    "summary_card",
    "faq_card",
    "product_image",
    "category_illustration",
}
SCENE_FIRST_ROLES = {"ai_scene_thumbnail", "original_photo", "licensed_photo"}
TEXT_CARD_ROLES = {"comparison_table", "checklist_card", "summary_card", "faq_card"}
EVIDENCE_ROLES = {"official_screenshot", "source_evidence", "diagram"}
DECISION_ROLES = {"comparison_table", "checklist_card", "diagram"}
SOURCE_REQUIRED_ROLES = {"licensed_photo", "official_screenshot", "source_evidence", "product_image"}
EXPERIENCE_BASES = {
    "research_only",
    "user_provided_experience",
    "user_owned_photo_report",
    "sponsored_product_review",
}
FIRSTHAND_CLAIM = re.compile(
    r"(?:직접\s*(?:다녀(?:왔|와)|방문(?:했|해)|써\s*봤|사용(?:했|해\s*봤)|구매(?:했|해)|먹어\s*봤|체험(?:했|해))"
    r"|(?:제가|저는|저도|저\s*역시|저희\s*아이|우리\s*아이).{0,40}(?:다녀왔|다니|즐기|써봤|사용해봤|구매했|먹어봤|체험했|좋아했|챙기는\s*편)"
    r"|작년에.{0,40}(?:샀|구매|다녀|사용))"
)


def validate_post(post: dict, base: Path) -> list[str]:
    errors: list[str] = []
    name = post.get("title") or "untitled"
    if not str(post.get("title", "")).strip():
        errors.append("untitled: title is required")
    elif len(str(post["title"]).strip()) > 60:
        errors.append(f"{name}: title is too long ({len(str(post['title']).strip())} characters)")
    body_path = base / str(post.get("body_path", ""))
    if not body_path.is_file():
        return [f"{name}: body file not found: {body_path}"]

    body = body_path.read_text(encoding="utf-8").strip()
    if len(body) < 800:
        errors.append(f"{name}: body is too short ({len(body)} characters)")
    for label, pattern in RAW_MARKERS.items():
        if pattern.search(body):
            errors.append(f"{name}: contains {label}")

    experience_basis = str(post.get("experience_basis", "")).strip()
    if experience_basis not in EXPERIENCE_BASES:
        errors.append(f"{name}: valid experience_basis is required")
    if experience_basis != "research_only" and not str(post.get("experience_note", "")).strip():
        errors.append(f"{name}: experience_note is required for {experience_basis}")
    if experience_basis == "research_only" and FIRSTHAND_CLAIM.search(body):
        errors.append(f"{name}: research_only body contains firsthand experience language")
    sponsored = post.get("sponsored") is True
    if experience_basis == "sponsored_product_review" and not sponsored:
        errors.append(f"{name}: sponsored_product_review must set sponsored to true")

    tags = [str(tag).strip() for tag in post.get("tags", []) if str(tag).strip()]
    if len(tags) < 3:
        errors.append(f"{name}: provide at least 3 tags")
    if len(tags) > 15:
        errors.append(f"{name}: too many tags ({len(tags)})")
    if len({tag.casefold() for tag in tags}) != len(tags):
        errors.append(f"{name}: duplicate tags found")

    visuals = post.get("visuals", [])
    if not isinstance(visuals, list) or not visuals:
        errors.append(f"{name}: visuals manifest is required; include path, role, caption, and QA fields")
        visuals = []
    visual_records = [item for item in visuals if isinstance(item, dict)]
    images = [str(item.get("path", "")) for item in visual_records]
    legacy_images = [str(item) for item in post.get("image_paths", [])]
    if visuals and legacy_images and images != legacy_images:
        errors.append(f"{name}: visuals paths and image_paths are not in the same editor order")
    expected = int(post.get("expected_image_count", 3))
    if len(images) < expected:
        errors.append(f"{name}: expected {expected} images, manifest has {len(images)}")
    if len(body) >= 1800 and len(images) < 4:
        errors.append(f"{name}: long posts require at least 4 visuals ({len(images)} provided)")
    if images and post.get("visual_qa_confirmed") is not True:
        errors.append(f"{name}: visual_qa_confirmed must be true after original-resolution review")

    roles: list[str] = []
    for index, visual in enumerate(visuals):
        if not isinstance(visual, dict):
            errors.append(f"{name}: visual #{index + 1} must be an object")
            continue
        role = str(visual.get("role", "")).strip()
        roles.append(role)
        if role not in ALLOWED_VISUAL_ROLES:
            errors.append(f"{name}: visual #{index + 1} has unsupported role: {role or 'missing'}")
        if index > 0 and not str(visual.get("caption", "")).strip():
            errors.append(f"{name}: visual #{index + 1} needs a useful body caption")
        if visual.get("visual_qa_confirmed") is not True:
            errors.append(f"{name}: visual #{index + 1} lacks original-resolution QA confirmation")
        if not isinstance(visual.get("contains_text"), bool):
            errors.append(f"{name}: visual #{index + 1} must declare contains_text as true or false")
        if role in SOURCE_REQUIRED_ROLES:
            for field in ("source_url", "checked_date", "reuse_basis"):
                if not str(visual.get(field, "")).strip():
                    errors.append(f"{name}: visual #{index + 1} ({role}) needs {field}")
        if role == "original_photo" and not str(visual.get("ownership_basis", "")).strip():
            errors.append(f"{name}: visual #{index + 1} original_photo needs ownership_basis")

    if roles:
        if roles[0] not in SCENE_FIRST_ROLES:
            errors.append(f"{name}: first visual must be a scene-first thumbnail or photo, not {roles[0]}")
        card_count = sum(role in TEXT_CARD_ROLES for role in roles)
        if card_count > 2:
            errors.append(f"{name}: use no more than 2 text-card visuals ({card_count} provided)")
        if any(a in TEXT_CARD_ROLES and b in TEXT_CARD_ROLES for a, b in zip(roles, roles[1:])):
            errors.append(f"{name}: consecutive text-card visuals are not allowed")
        if len(body) >= 1800:
            if len(set(roles)) < 3:
                errors.append(f"{name}: long posts require at least 3 distinct visual roles")
            if not any(role in EVIDENCE_ROLES for role in roles):
                errors.append(f"{name}: long posts require an evidence or explanation visual")
            if not any(role in DECISION_ROLES for role in roles):
                errors.append(f"{name}: long posts require a comparison, checklist, or decision diagram")
        if experience_basis in {"user_owned_photo_report", "sponsored_product_review"} and roles[0] != "original_photo":
            errors.append(f"{name}: evidence-backed package must lead with an original_photo")
        if experience_basis == "research_only" and "original_photo" in roles:
            errors.append(f"{name}: research_only package cannot claim original visit/use photos")

    text_bearing_count = int(post.get("text_bearing_image_count", 0))
    declared_text_bearing = sum(
        item.get("contains_text") is True for item in visuals if isinstance(item, dict)
    )
    if visuals and declared_text_bearing != text_bearing_count:
        errors.append(
            f"{name}: text_bearing_image_count is {text_bearing_count}, visual records declare {declared_text_bearing}"
        )
    visual_texts = [str(item) for item in post.get("visual_texts", [])]
    if text_bearing_count and not visual_texts:
        errors.append(f"{name}: expected text for text-bearing images is missing")
    for visual_text in visual_texts:
        if VISUAL_CORRUPTION.search(visual_text):
            errors.append(f"{name}: corrupted visual source text found")
    image_hashes: set[str] = set()
    for index, raw in enumerate(images):
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
            ratio = width / height
            if ratio < 0.75 or ratio > 2.2:
                errors.append(f"{name}: unusual image aspect ratio: {path} ({width}x{height})")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest in image_hashes:
                errors.append(f"{name}: duplicate image content found: {path}")
            image_hashes.add(digest)
            if visual_records[index].get("contains_text") is True:
                sidecar = path.with_suffix(path.suffix + ".visual.json")
                if not sidecar.is_file():
                    errors.append(f"{name}: text-bearing visual is missing its sidecar: {sidecar}")
        except Exception as exc:
            errors.append(f"{name}: invalid image {path}: {exc}")

    if post.get("affiliate") or sponsored:
        disclosure = str(post.get("disclosure_text", "")).strip()
        if not disclosure or disclosure not in body[:600]:
            errors.append(f"{name}: affiliate or sponsorship disclosure missing near the top")
    if post.get("affiliate"):
        if not post.get("verified_links"):
            errors.append(f"{name}: affiliate links are not marked verified")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", help="JSON manifest path")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    data = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    posts = data.get("posts", [])
    errors = [] if posts else ["manifest contains no posts"]
    titles = [str(post.get("title", "")).strip().casefold() for post in posts]
    if len(set(titles)) != len(titles):
        errors.append("manifest contains duplicate titles")
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
