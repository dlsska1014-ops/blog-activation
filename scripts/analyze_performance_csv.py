#!/usr/bin/env python3
"""Summarize blog performance CSV data for blog-activation."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


def as_int(value: str | None) -> int:
    if not value:
        return 0
    try:
        return int(float(value))
    except ValueError:
        return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", help="CSV using operations-data-schema.md columns")
    args = parser.parse_args()

    rows = list(csv.DictReader(Path(args.csv_path).open("r", encoding="utf-8-sig", newline="")))
    clusters: dict[str, int] = defaultdict(int)
    post_types: Counter[str] = Counter()
    titles: list[tuple[int, str]] = []
    affiliate_clicks: dict[str, int] = defaultdict(int)

    for row in rows:
        views = as_int(row.get("views"))
        clicks = as_int(row.get("affiliate_clicks"))
        cluster = row.get("keyword_cluster") or "(none)"
        post_type = row.get("post_type") or "(none)"
        title = row.get("title") or "(untitled)"
        clusters[cluster] += views
        post_types[post_type] += 1
        affiliate_clicks[cluster] += clicks
        titles.append((views, title))

    print("# Performance Summary")
    print(f"posts: {len(rows)}")
    print("\n## Top Titles By Views")
    for views, title in sorted(titles, reverse=True)[:5]:
        print(f"- {views}: {title}")

    print("\n## Views By Cluster")
    for cluster, views in sorted(clusters.items(), key=lambda item: item[1], reverse=True):
        print(f"- {cluster}: {views}")

    print("\n## Affiliate Clicks By Cluster")
    for cluster, clicks in sorted(affiliate_clicks.items(), key=lambda item: item[1], reverse=True):
        print(f"- {cluster}: {clicks}")

    print("\n## Post Type Mix")
    for post_type, count in post_types.most_common():
        print(f"- {post_type}: {count}")


if __name__ == "__main__":
    main()
