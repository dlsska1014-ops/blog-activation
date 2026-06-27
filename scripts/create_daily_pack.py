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
- Template type:
- Topic score:
- Keyword cluster:
- Cluster role:
- Duplicate intent risk:
- Title A/B score:
- Layout pattern:
- Emoji/emoticon plan:

## Research Notes

- Source 1:
- Source 2:
- Source 3:
- Uncertainties:

## Draft Package

### Title Options

1.
2.
3.

### Title A/B Score

| Title | Type | Accuracy | Search fit | Click clarity | Trust | Distinction | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

### Opening


### Quick Summary


### Main Body


### Table Or Checklist


### Visual Storyboard

- Image 1 scene-first thumbnail: path / role / placement / caption / QA
- Image 2 evidence or explanation: path / role / placement / caption / source / reuse basis / QA
- Image 3 decision aid: path / role / placement / caption / source / reuse basis / QA
- Image 4 supporting visual: path / role / placement / caption / source / reuse basis / QA

### Visual Prompt Notes

- Thumbnail prompt:
- Evidence/diagram prompt:
- Checklist/comparison prompt:
- Text-card count:

### Layout And Tone Check

- First-screen pattern:
- Editorial presence score:
- Blank line rhythm:
- Emoji/emoticon count:
- Naturalness edits:

### Affiliate Link Plan

- Disclosure location:
- Affiliate link count:
- Non-affiliate value sections:
- Trust risk:

### FAQ

1.
2.
3.

### Tags


### Quality Rubric

- Timeliness:
- Reader usefulness:
- Fact reliability:
- Originality:
- Human editorial presence:
- Visual storytelling:
- Readability/layout:
- Monetization/low-quality safety:
- Total / 40:

### Draft-Save Checklist

- [ ] Facts checked
- [ ] Source/date notes included
- [ ] Long post has at least four visuals and three distinct roles
- [ ] First image is a scene-first thumbnail or photo, not a text card
- [ ] No more than two text cards; no consecutive text cards
- [ ] Every body visual has a useful caption and required source/reuse notes
- [ ] All images prepared and visually checked
- [ ] Korean card text verified at original resolution; no question marks, boxes, or clipping
- [ ] Expected visual text recorded in publish manifest
- [ ] Editor image count matches the plan
- [ ] Plain-text body has no Markdown or image placeholders
- [ ] Tags prepared
- [ ] Naver spacing reviewed
- [ ] Tistory adaptation prepared if needed
- [ ] Run mode recorded: draft-only or auto-publish
- [ ] Final state and URL/draft receipt verified
- [ ] Public first/middle/last images and recent-list duplication checked
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

| Candidate | Timeliness | Reader pain | Search demand | Monetization fit | Trust fit | Total |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## High-Performing Blog Pattern Notes

-

## Selected Topics

1.
2.
3.

## Keyword Clusters

| Topic | Cluster | Role | Duplicate risk | Decision |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Style Memory Updates To Consider

-

## Performance Notes To Fill Later

- Published/draft date:
- Views:
- Search inflow keywords:
- Clicks:
- Affiliate result:
- Lesson:

## Experiment

- Hypothesis:
- Variable changed:
- Metric to watch:
- Review date:

## Visual Plan

- Thumbnail scene and optional short overlay:
- First visual role:
- Evidence/explanation visual:
- Comparison/checklist visual:
- Supporting visual:
- Text-card count:

## Layout And Style Plan

- Influencer patterns observed:
- Reusable style lesson:
- Spacing rhythm:
- Emoji/emoticon rule:
- Naturalness edit:

## Search Exposure Follow-Up

- Exact title check date:
- Main keyword check date:
- Search inflow keywords:
- Action:
""",
        encoding="utf-8",
    )

    (out_dir / "publish-manifest.json").write_text(
        '{\n  "posts": []\n}\n', encoding="utf-8"
    )
    (out_dir / "publication-receipts.jsonl").touch()
    (out_dir / "run-contract.json").write_text(
        '{\n'
        '  "run_date": "' + args.date + '",\n'
        '  "platforms": ["naver"],\n'
        '  "mode": "draft-only",\n'
        '  "expected_post_count": 3,\n'
        '  "expected_image_count_per_long_post": 4,\n'
        '  "required_distinct_visual_roles": 3\n'
        '}\n',
        encoding="utf-8",
    )

    print(out_dir)


if __name__ == "__main__":
    main()
