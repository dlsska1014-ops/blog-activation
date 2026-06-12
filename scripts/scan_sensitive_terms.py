#!/usr/bin/env python3
"""Scan skill files for terms that may indicate accidental secrets."""

from __future__ import annotations

import argparse
from pathlib import Path


TERMS = [
    "password",
    "passwd",
    "token",
    "cookie",
    "secret",
    "client_secret",
    "access_key",
    "NAVER_",
    "COUPANG_",
    "비밀번호",
    "쿠키",
    "토큰",
    "주민",
    "사업자번호",
]

ALLOWLIST_FILES = {
    "SKILL.md",
    "references/daily-ops.md",
    "references/naver-draft-runbook.md",
    "references/publish-risk-checklist.md",
    "references/secret-handling.md",
    "scripts/scan_sensitive_terms.py",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=".", help="Directory to scan")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    hits: list[str] = []

    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".py", ".yaml", ".yml", ".txt"}:
            continue
        rel = path.relative_to(root).as_posix()
        if rel in ALLOWLIST_FILES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for term in TERMS:
            if term.lower() in text.lower():
                hits.append(f"{rel}: {term}")

    if hits:
        print("Potential sensitive terms found:")
        for hit in hits:
            print(f"- {hit}")
        raise SystemExit(1)

    print("No sensitive terms found.")


if __name__ == "__main__":
    main()
