#!/usr/bin/env python3
"""Score blog topic candidates from a simple CSV file."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


FIELDS = ["timeliness", "reader_pain", "search_demand", "monetization_fit", "trust_fit"]


def as_int(value: str) -> int:
    number = int(value)
    if number < 1 or number > 5:
        raise ValueError("scores must be 1 to 5")
    return number


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", help="CSV with topic and score columns")
    args = parser.parse_args()

    path = Path(args.csv_path)
    rows = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            total = sum(as_int(row[field]) for field in FIELDS)
            row["total"] = str(total)
            row["decision"] = "use" if total >= 18 and as_int(row["trust_fit"]) >= 3 else "reject"
            rows.append(row)

    rows.sort(key=lambda row: int(row["total"]), reverse=True)

    for row in rows:
        print(f"{row.get('topic', '(untitled)')}: {row['total']}/25 - {row['decision']}")


if __name__ == "__main__":
    main()
