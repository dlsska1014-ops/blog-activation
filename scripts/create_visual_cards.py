#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 675
FONT = "C:/Windows/Fonts/malgun.ttf"
FONT_BOLD = "C:/Windows/Fonts/malgunbd.ttf"
THEMES = {
    "blue": ("#f6f8f9", "#3f7188", "#1f3139", "#66777e", "#e8eef1"),
    "green": ("#f7f8f6", "#557b69", "#24352d", "#68766f", "#e9eeea"),
    "brown": ("#f8f7f4", "#8a6b48", "#3c3024", "#766b5d", "#eee9e1"),
    "gray": ("#f7f7f6", "#6c7779", "#2d3536", "#6b7475", "#e9ebea"),
}
HANGUL = re.compile(r"[가-힣]")
CORRUPTION = re.compile(r"\?{2,}|\ufffd")


def make_font(size: int, bold: bool = False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, size)


def card_text(card: dict) -> list[str]:
    values = [card.get("eyebrow", ""), card.get("title", ""), card.get("subtitle", ""), card.get("footer", "")]
    values.extend(str(item) for item in card.get("bullets", []))
    for row in card.get("table", []):
        values.extend(str(item) for item in row)
    return [str(value) for value in values if str(value).strip()]


def validate_card(card: dict) -> list[str]:
    errors = []
    texts = card_text(card)
    joined = " ".join(texts)
    if not card.get("filename"):
        errors.append("filename is required")
    if not texts:
        errors.append(f"{card.get('filename', 'card')}: no text to render")
    if CORRUPTION.search(joined):
        errors.append(f"{card.get('filename', 'card')}: repeated question marks or replacement characters found")
    if card.get("language", "ko") == "ko" and not HANGUL.search(joined):
        errors.append(f"{card.get('filename', 'card')}: Korean text expected but no Hangul found")
    if len(str(card.get("title", ""))) > 42:
        errors.append(f"{card.get('filename', 'card')}: title is too long for safe rendering")
    if len(card.get("bullets", [])) > 3:
        errors.append(f"{card.get('filename', 'card')}: use no more than 3 bullets")
    if any(len(str(item)) > 44 for item in card.get("bullets", [])):
        errors.append(f"{card.get('filename', 'card')}: a bullet is too long for safe rendering")
    if card.get("table"):
        table = card["table"]
        if len(table[0]) > 3 or len(table) > 6:
            errors.append(f"{card.get('filename', 'card')}: table must be at most 3 columns and 5 data rows")
    return errors


def wrap_kr(text: str, max_chars: int) -> list[str]:
    lines = []
    for raw in text.split("\n"):
        cur = ""
        for part in raw.split(" "):
            trial = part if not cur else cur + " " + part
            if len(trial) <= max_chars:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = part
        if cur:
            lines.append(cur)
    return lines


def save_card(card: dict, out_dir: Path) -> Path:
    bg, accent, dark, mid, pale = THEMES.get(card.get("theme", "gray"), THEMES["gray"])
    image = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(image)
    draw.rectangle([56, 48, 62, H - 48], fill=accent)
    draw.text((92, 52), card.get("eyebrow", ""), font=make_font(24, True), fill=accent)
    draw.line([92, 92, W - 72, 92], fill=pale, width=2)

    y = 122
    for line in wrap_kr(card.get("title", ""), 24):
        draw.text((92, y), line, font=make_font(48, True), fill=dark)
        y += 60

    if card.get("subtitle"):
        y += 2
        for line in wrap_kr(card["subtitle"], 42):
            draw.text((94, y), line, font=make_font(27), fill=mid)
            y += 38

    if card.get("bullets"):
        y = max(y + 28, 320)
        for number, bullet in enumerate(card["bullets"][:3], 1):
            draw.text((94, y + 2), f"{number:02d}", font=make_font(21, True), fill=accent)
            for line in wrap_kr(str(bullet), 46)[:2]:
                draw.text((152, y), line, font=make_font(27), fill=dark)
                y += 35
            draw.line([94, y + 8, W - 82, y + 8], fill=pale, width=1)
            y += 18

    if card.get("table"):
        table = card["table"]
        x0, y0 = 92, max(y + 22, 270)
        cols, rows = table[0], table[1:]
        table_width = 1018
        colw = table_width // len(cols)
        header_h = 48
        row_h = 50
        draw.rectangle([x0, y0, x0 + table_width, y0 + 5], fill=accent)
        for i, col in enumerate(cols):
            draw.text((x0 + i * colw + 14, y0 + 15), str(col), font=make_font(22, True), fill=dark)
        y = y0 + header_h
        for ridx, row in enumerate(rows[:5]):
            fill = bg if ridx % 2 == 0 else pale
            draw.rectangle([x0, y, x0 + table_width, y + row_h], fill=fill)
            for i, cell in enumerate(row):
                draw.text((x0 + i * colw + 14, y + 13), str(cell), font=make_font(21), fill=dark)
            y += row_h
        draw.line([x0, y, x0 + table_width, y], fill=accent, width=2)

    draw.text((92, H - 50), card.get("footer", "작성일 기준"), font=make_font(20), fill=mid)
    out_path = out_dir / card["filename"]
    image.save(out_path, quality=95)
    metadata = {
        "language": card.get("language", "ko"),
        "asset_role": card.get("role", "summary_card"),
        "contains_text": True,
        "rendered_text": card_text(card),
        "font": FONT,
        "font_bold": FONT_BOLD,
        "sha256": hashlib.sha256(out_path.read_bytes()).hexdigest(),
        "manual_pixel_review_required": True,
    }
    out_path.with_suffix(out_path.suffix + ".visual.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    if not Path(FONT).is_file() or not Path(FONT_BOLD).is_file():
        raise SystemExit("Korean font files are missing")
    cards = json.loads(Path(args.spec).read_text(encoding="utf-8-sig"))
    errors = [error for card in cards for error in validate_card(card)]
    if errors:
        raise SystemExit("BLOCKED\n- " + "\n- ".join(errors))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for card in cards:
        print(save_card(card, out_dir))


if __name__ == "__main__":
    main()
