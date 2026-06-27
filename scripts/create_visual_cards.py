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
    "blue": ("#f7fbff", "#2477b3", "#17324d", "#4e6175", "#ffffff"),
    "green": ("#f4fbf8", "#21806b", "#173d35", "#4d665e", "#ffffff"),
    "brown": ("#fbfaf5", "#8a5a1f", "#3d2b17", "#6a5a45", "#ffffff"),
    "gray": ("#f7f7f5", "#5f6f73", "#273133", "#596568", "#ffffff"),
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
    if len(card.get("bullets", [])) > 4:
        errors.append(f"{card.get('filename', 'card')}: use no more than 4 bullets")
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
    draw.rectangle([0, 0, W, 96], fill=accent)
    draw.rectangle([0, H - 72, W, H], fill=dark)
    draw.rounded_rectangle([58, 132, 1142, 586], radius=18, fill=pale)
    draw.text((72, 30), card.get("eyebrow", ""), font=make_font(32, True), fill="white")

    y = 166
    for line in wrap_kr(card.get("title", ""), 21):
        draw.text((92, y), line, font=make_font(58, True), fill=dark)
        y += 72

    if card.get("subtitle"):
        y += 4
        for line in wrap_kr(card["subtitle"], 36):
            draw.text((96, y), line, font=make_font(30), fill=mid)
            y += 42

    if card.get("bullets"):
        y = max(y + 18, 376)
        for bullet in card["bullets"][:4]:
            draw.ellipse([98, y + 9, 114, y + 25], fill=accent)
            for line in wrap_kr(str(bullet), 42)[:2]:
                draw.text((128, y), line, font=make_font(28), fill=dark)
                y += 36
            y += 8

    if card.get("table"):
        table = card["table"]
        x0, y0 = 88, 260
        cols, rows = table[0], table[1:]
        colw = 1024 // len(cols)
        header_h = 46
        row_h = 48
        draw.rectangle([x0, y0, x0 + 1024, y0 + header_h], fill=dark)
        for i, col in enumerate(cols):
            draw.text((x0 + i * colw + 18, y0 + 10), str(col), font=make_font(23, True), fill="white")
        y = y0 + header_h
        for ridx, row in enumerate(rows[:5]):
            fill = "white" if ridx % 2 == 0 else "#f7f8f6"
            draw.rectangle([x0, y, x0 + 1024, y + row_h], fill=fill)
            for i, cell in enumerate(row):
                draw.text((x0 + i * colw + 18, y + 12), str(cell), font=make_font(21), fill=dark)
            y += row_h
        draw.rectangle([x0, y0, x0 + 1024, y], outline="#c9d0ca", width=2)

    draw.text((72, H - 52), card.get("footer", "작성일 기준"), font=make_font(24), fill="white")
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
