#!/usr/bin/env python3
"""Score blog topic candidates from a simple CSV file."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


BASE_FIELDS = ["timeliness", "reader_pain", "search_demand", "monetization_fit", "trust_fit"]
EVIDENCE_FIELDS = ["proven_cluster_fit", "specificity", "original_evidence"]


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
            fields = BASE_FIELDS + EVIDENCE_FIELDS if all(row.get(field) for field in EVIDENCE_FIELDS) else BASE_FIELDS
            total = sum(as_int(row[field]) for field in fields)
            maximum = len(fields) * 5
            row["total"] = str(total)
            evidence_ok = not all(row.get(field) for field in EVIDENCE_FIELDS) or as_int(row["original_evidence"]) >= 3
            row["maximum"] = str(maximum)
            row["decision"] = "use" if total / maximum >= 0.72 and as_int(row["trust_fit"]) >= 3 and evidence_ok else "reject"
            rows.append(row)

    rows.sort(key=lambda row: int(row["total"]), reverse=True)

    for row in rows:
        print(f"{row.get('topic', '(untitled)')}: {row['total']}/{row['maximum']} - {row['decision']}")


if __name__ == "__main__":
    main()

