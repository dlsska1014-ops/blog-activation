#!/usr/bin/env python3
"""Compare consecutive complete traffic windows from a date,views CSV."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("--window", type=int, default=7)
    args = parser.parse_args()
    if args.window < 2:
        raise SystemExit("window must be at least 2")

    rows = []
    with Path(args.csv_path).open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append((date.fromisoformat(row["date"]), int(float(row["views"]))))
    rows.sort()
    required = args.window * 2
    if len(rows) < required:
        raise SystemExit(f"need at least {required} complete daily rows")

    previous = rows[-required:-args.window]
    latest = rows[-args.window:]
    previous_avg = sum(value for _, value in previous) / args.window
    latest_avg = sum(value for _, value in latest) / args.window
    change = 0.0 if previous_avg == 0 else (latest_avg - previous_avg) / previous_avg * 100
    status = "recovery" if change <= -25 else "watch" if change < 0 else "stable-or-growing"

    print(f"previous: {previous[0][0]}..{previous[-1][0]} avg={previous_avg:.2f}")
    print(f"latest: {latest[0][0]}..{latest[-1][0]} avg={latest_avg:.2f}")
    print(f"change: {change:.1f}%")
    print(f"status: {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


