#!/usr/bin/env python3
"""Append a publication receipt while blocking accidental verified duplicates."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


STATUSES = {"verified", "partial", "blocked", "unknown"}
MODES = {"draft-only", "auto-publish"}


def fingerprint(title: str, body_path: Path) -> str:
    body = body_path.read_text(encoding="utf-8")
    normalized = " ".join((title + "\n" + body).split()).casefold()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:20]


def load_receipts(path: Path) -> list[dict]:
    if not path.exists():
        return []
    receipts = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                receipts.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid ledger line {line_no}: {exc}") from exc
    return receipts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--platform", required=True, choices=["naver", "tistory"])
    parser.add_argument("--mode", required=True, choices=sorted(MODES))
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", required=True)
    parser.add_argument("--status", required=True, choices=sorted(STATUSES))
    parser.add_argument("--url-or-draft-id", default="")
    parser.add_argument("--image-count", type=int, default=0)
    parser.add_argument("--notes", default="")
    parser.add_argument("--allow-republish", action="store_true")
    args = parser.parse_args()

    ledger = Path(args.ledger).resolve()
    body_path = Path(args.body).resolve()
    if not body_path.is_file():
        raise SystemExit(f"body file not found: {body_path}")

    content_id = fingerprint(args.title, body_path)
    receipts = load_receipts(ledger)
    duplicate = any(
        item.get("platform") == args.platform
        and item.get("content_fingerprint") == content_id
        and item.get("status") == "verified"
        for item in receipts
    )
    if duplicate and not args.allow_republish:
        print("BLOCKED: verified publication already exists for this platform and content")
        return 2

    receipt = {
        "run_date": datetime.now().astimezone().date().isoformat(),
        "platform": args.platform,
        "mode": args.mode,
        "title": args.title,
        "status": args.status,
        "url_or_draft_id": args.url_or_draft_id,
        "image_count": args.image_count,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "content_fingerprint": content_id,
        "notes": args.notes,
    }
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(receipt, ensure_ascii=False) + "\n")
    print(f"RECORDED: {args.platform} {args.status} {content_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


