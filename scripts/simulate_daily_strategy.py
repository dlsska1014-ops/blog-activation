#!/usr/bin/env python3
"""Run synthetic strategy simulations for the blog-activation skill."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Topic:
    name: str
    post_type: str
    timeliness: int
    reader_pain: int
    search_demand: int
    monetization_fit: int
    trust_fit: int

    @property
    def total(self) -> int:
        return (
            self.timeliness
            + self.reader_pain
            + self.search_demand
            + self.monetization_fit
            + self.trust_fit
        )


SCENARIOS = {
    "electronics-payback": [
        Topic("electronics payback event conditions", "info-event", 5, 5, 4, 4, 5),
        Topic("budget purchase list for payback event", "shopping-guide", 5, 4, 4, 5, 4),
        Topic("random viral celebrity keyword", "news", 5, 2, 5, 1, 2),
        Topic("premium TV TOP 5", "affiliate", 4, 3, 4, 5, 3),
    ],
    "rainy-season": [
        Topic("dehumidifier choosing guide", "seasonal", 5, 5, 5, 5, 5),
        Topic("shoe dryer TOP 5", "affiliate", 5, 4, 4, 4, 5),
        Topic("rainy day quote collection", "low-fit", 4, 1, 3, 1, 2),
        Topic("mold prevention checklist", "info", 5, 5, 4, 3, 5),
    ],
    "family-gift": [
        Topic("parents gift by budget", "seasonal", 5, 5, 5, 5, 5),
        Topic("massage device TOP 5", "affiliate", 4, 4, 4, 5, 3),
        Topic("health miracle product", "reject", 4, 3, 4, 5, 1),
        Topic("gift wrapping checklist", "info", 3, 3, 3, 2, 5),
    ],
}


def choose_topics(topics: list[Topic]) -> list[Topic]:
    eligible = [topic for topic in topics if topic.total >= 18 and topic.trust_fit >= 3]
    selected: list[Topic] = []

    for desired_type in ("info-event", "seasonal", "affiliate"):
        matches = [topic for topic in eligible if desired_type in topic.post_type]
        if matches:
            selected.append(max(matches, key=lambda topic: topic.total))

    for topic in sorted(eligible, key=lambda topic: topic.total, reverse=True):
        if len(selected) >= 3:
            break
        if topic not in selected:
            selected.append(topic)

    return selected[:3]


def main() -> None:
    lines = ["# Blog Activation Strategy Simulation", ""]
    for scenario, topics in SCENARIOS.items():
        lines.append(f"## {scenario}")
        lines.append("")
        for topic in sorted(topics, key=lambda item: item.total, reverse=True):
            lines.append(f"- {topic.name}: {topic.total}/25 ({topic.post_type})")
        lines.append("")
        lines.append("Selected:")
        for topic in choose_topics(topics):
            lines.append(f"- {topic.name}: {topic.total}/25")
        lines.append("")

    output = Path("blog-activation-simulation-report.md")
    output.write_text("\n".join(lines), encoding="utf-8")
    print(output.resolve())


if __name__ == "__main__":
    main()
