#!/usr/bin/env python3
"""Create a dated blog draft workspace for the blog-activation skill."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


POST_TEMPLATE = """# {label}

## Topic

- Working title:
- Platform: Naver Blog first, Tistory adaptation optional
- Search intent:
- Target reader:
- Checked date:

## Research Notes

- Source 1:
- Source 2:
- Source 3:

## Draft Package

### Title Options

1.
2.
3.

### Opening


### Quick Summary


### Main Body


### Image Placement Notes

- Image 1:
- Image 2:
- Image 3:

### FAQ

1.
2.
3.

### Tags


### Draft-Save Checklist

- [ ] Facts checked
- [ ] Source/date notes included
- [ ] Images or image prompts prepared
- [ ] Naver spacing reviewed
- [ ] Tistory adaptation prepared if needed
- [ ] Publish disabled; draft-save only
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat(), help="Run date in YYYY-MM-DD format")
    parser.add_argument("--out", default=".", help="Output directory")
    args = parser.parse_args()

    out_dir = Path(args.out).expanduser().resolve() / f"blog-activation-{args.date}"
    out_dir.mkdir(parents=True, exist_ok=True)

    labels = [
        "01-info-news-explainer",
        "02-seasonal-search-post",
        "03-coupang-partners-top5",
    ]

    for label in labels:
        (out_dir / f"{label}.md").write_text(POST_TEMPLATE.format(label=label), encoding="utf-8")

    (out_dir / "research-log.md").write_text(
        f"""# Daily Research Log - {args.date}

## Trend Candidates

-

## High-Performing Blog Pattern Notes

-

## Selected Topics

1.
2.
3.

## Style Memory Updates To Consider

-
""",
        encoding="utf-8",
    )

    print(out_dir)


if __name__ == "__main__":
    main()
