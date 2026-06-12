#!/usr/bin/env python3
"""Score revenue-oriented blog topic candidates from CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


FIELDS = [
    "timeliness",
    "buyer_intent",
    "order_value",
    "search_demand",
    "trust_fit",
    "original_value",
    "low_quality_safety",
]


def as_int(value: str, field: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be an integer from 1 to 5") from exc
    if number < 1 or number > 5:
        raise ValueError(f"{field} must be 1 to 5")
    return number


def decide(total: int, trust_fit: int, low_quality_safety: int) -> str:
    if trust_fit < 3 or low_quality_safety < 3:
        return "reject"
    if total >= 30:
        return "strong"
    if total >= 25:
        return "use"
    if total >= 20:
        return "support"
    return "reject"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", help="CSV with topic and revenue score columns")
    args = parser.parse_args()

    path = Path(args.csv_path)
    rows = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = [field for field in FIELDS if field not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit(f"missing columns: {', '.join(missing)}")

        for row in reader:
            scores = {field: as_int(row[field], field) for field in FIELDS}
            total = sum(scores.values())
            row["total"] = str(total)
            row["decision"] = decide(
                total,
                scores["trust_fit"],
                scores["low_quality_safety"],
            )
            rows.append(row)

    rows.sort(key=lambda row: int(row["total"]), reverse=True)

    for row in rows:
        topic = row.get("topic", "(untitled)")
        reason = row.get("reason", "").strip()
        suffix = f" - {reason}" if reason else ""
        print(f"{topic}: {row['total']}/35 - {row['decision']}{suffix}")


if __name__ == "__main__":
    main()
