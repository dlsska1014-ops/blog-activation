#!/usr/bin/env python3
"""Prepare a user-owned photo for privacy-safe blog transfer."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_region(raw: str) -> tuple[int, int, int, int]:
    try:
        x, y, width, height = (int(part.strip()) for part in raw.split(","))
    except (TypeError, ValueError) as exc:
        raise argparse.ArgumentTypeError("blur region must be x,y,width,height") from exc
    if min(x, y, width, height) < 0 or width == 0 or height == 0:
        raise argparse.ArgumentTypeError("blur region values must be non-negative with positive size")
    return x, y, width, height


def prepare_photo(
    source: Path,
    output: Path,
    blur_regions: list[tuple[int, int, int, int]],
    max_long_edge: int,
    quality: int,
    manual_review_confirmed: bool,
) -> Path:
    source = source.resolve()
    output = output.resolve()
    if source == output:
        raise ValueError("source and output paths must differ")
    if not source.is_file():
        raise FileNotFoundError(source)
    if max_long_edge < 600:
        raise ValueError("max_long_edge must be at least 600")
    if not 60 <= quality <= 100:
        raise ValueError("quality must be between 60 and 100")

    output.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGB")

    applied_regions: list[list[int]] = []
    for x, y, width, height in blur_regions:
        right = min(x + width, image.width)
        bottom = min(y + height, image.height)
        if x >= image.width or y >= image.height or right <= x or bottom <= y:
            raise ValueError(f"blur region is outside the image: {x},{y},{width},{height}")
        box = (x, y, right, bottom)
        region = image.crop(box).filter(ImageFilter.GaussianBlur(radius=max(12, min(width, height) // 8)))
        image.paste(region, box)
        applied_regions.append([x, y, right - x, bottom - y])

    if max(image.size) > max_long_edge:
        scale = max_long_edge / max(image.size)
        size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
        image = image.resize(size, Image.Resampling.LANCZOS)

    suffix = output.suffix.casefold()
    if suffix in {".jpg", ".jpeg"}:
        image.save(output, format="JPEG", quality=quality, optimize=True)
    elif suffix == ".png":
        image.save(output, format="PNG", optimize=True)
    elif suffix == ".webp":
        image.save(output, format="WEBP", quality=quality, method=6)
    else:
        raise ValueError("output must use .jpg, .jpeg, .png, or .webp")

    with Image.open(output) as checked:
        metadata_removed = len(checked.getexif()) == 0 and not bool(checked.info.get("exif"))
        dimensions = list(checked.size)

    sidecar = output.with_suffix(output.suffix + ".privacy.json")
    record = {
        "schema_version": 1,
        "source_filename": source.name,
        "source_sha256": sha256(source),
        "output_filename": output.name,
        "output_sha256": sha256(output),
        "dimensions": dimensions,
        "metadata_removed": metadata_removed,
        "blur_regions": applied_regions,
        "manual_privacy_review_confirmed": manual_review_confirmed,
        "manual_review_reminder": "Check faces, plates, addresses, receipts, screens, QR codes, signs, and reflections.",
    }
    sidecar.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return sidecar


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    parser.add_argument("--blur", action="append", default=[], type=parse_region, metavar="X,Y,W,H")
    parser.add_argument("--max-long-edge", type=int, default=2000)
    parser.add_argument("--quality", type=int, default=90)
    parser.add_argument(
        "--confirm-manual-review",
        action="store_true",
        help="Set only after inspecting the prepared image at full resolution.",
    )
    args = parser.parse_args()

    try:
        sidecar = prepare_photo(
            Path(args.source),
            Path(args.output),
            args.blur,
            args.max_long_edge,
            args.quality,
            args.confirm_manual_review,
        )
    except Exception as exc:
        print(f"BLOCKED: {exc}")
        return 1
    if args.confirm_manual_review:
        print(f"PASS: prepared photo and confirmed privacy record: {sidecar}")
    else:
        print(f"PREPARED: inspect the output at full resolution before confirming review: {sidecar}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
