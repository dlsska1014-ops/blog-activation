#!/usr/bin/env python3
"""Detect excessive phrase reuse against recent owned blog drafts."""

from __future__ import annotations

import argparse
import json
import re
from difflib import SequenceMatcher
from pathlib import Path


WORD_RE = re.compile(r"[가-힣A-Za-z0-9]+")
IGNORED_PREFIXES = ("출처:", "확인일:", "이 포스팅은 쿠팡", "이 게시물은 쿠팡")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", required=True, type=Path)
    parser.add_argument("--corpus", required=True, type=Path)
    parser.add_argument("--threshold", type=float, default=0.18)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def normalize(text: str) -> list[str]:
    lines = [line for line in text.splitlines() if not line.strip().startswith(IGNORED_PREFIXES)]
    return [word.casefold() for word in WORD_RE.findall("\n".join(lines))]


def shingles(words: list[str], width: int = 5) -> set[tuple[str, ...]]:
    return {tuple(words[index : index + width]) for index in range(max(0, len(words) - width + 1))}


def candidates(corpus: Path, draft: Path) -> list[Path]:
    if corpus.is_file():
        paths = [corpus]
    else:
        paths = [path for path in corpus.rglob("*") if path.suffix.lower() in {".txt", ".md"}]
    draft_resolved = draft.resolve()
    return sorted(path for path in paths if path.resolve() != draft_resolved)


def compare(draft_words: list[str], other_words: list[str]) -> tuple[float, int]:
    draft_shingles = shingles(draft_words)
    other_shingles = shingles(other_words)
    union = draft_shingles | other_shingles
    jaccard = len(draft_shingles & other_shingles) / len(union) if union else 0.0
    longest = SequenceMatcher(None, draft_words, other_words, autojunk=False).find_longest_match().size
    return jaccard, longest


def main() -> int:
    args = parse_args()
    draft_words = normalize(args.draft.read_text(encoding="utf-8"))
    if len(draft_words) < 80:
        print(json.dumps({"status": "blocked", "reason": "draft is too short for reuse analysis"}, ensure_ascii=False))
        return 2

    rows = []
    for path in candidates(args.corpus, args.draft):
        other_words = normalize(path.read_text(encoding="utf-8", errors="ignore"))
        if len(other_words) < 80:
            continue
        score, longest = compare(draft_words, other_words)
        rows.append({"path": str(path), "jaccard": round(score, 4), "longest_word_run": longest})
    rows.sort(key=lambda item: (item["jaccard"], item["longest_word_run"]), reverse=True)
    failures = [row for row in rows if row["jaccard"] >= args.threshold or row["longest_word_run"] >= 18]
    payload = {
        "status": "blocked" if failures else "pass",
        "threshold": args.threshold,
        "compared_files": len(rows),
        "failures": failures[:10],
        "closest": rows[:5],
    }
    output = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    print(output)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
