#!/usr/bin/env python3
"""Choose a safe publish candidate and draft-save actions for a daily blog plan."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


AFFILIATE_KINDS = {"affiliate", "buying_guide", "affiliate_top5"}
NON_AFFILIATE_KINDS = {"information", "news", "seasonal", "event", "experience"}
REQUIRED_POST_FIELDS = {
    "id",
    "title",
    "kind",
    "reader_question",
    "cluster_key",
    "quality_score",
    "low_quality_risk",
    "mandatory_gates_passed",
    "naturalness_qa_confirmed",
    "editorial_authenticity_confirmed",
    "self_similarity_qa_confirmed",
    "fact_qa_confirmed",
    "visual_qa_confirmed",
    "body_chars",
    "image_count",
    "affiliate_link_count",
    "disclosure_present",
    "content_fingerprint",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--history", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.exists():
        return []
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid history JSON on line {line_number}: {exc}") from exc
    return rows


def as_date(value: str) -> date:
    return datetime.fromisoformat(value[:10]).date()


def is_affiliate(post: dict[str, Any]) -> bool:
    return post.get("kind") in AFFILIATE_KINDS


def validate_post(post: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    missing = sorted(REQUIRED_POST_FIELDS - post.keys())
    if missing:
        return ["missing fields: " + ", ".join(missing)]

    if post["kind"] not in AFFILIATE_KINDS | NON_AFFILIATE_KINDS:
        reasons.append("unsupported post kind")
    if not str(post["reader_question"]).strip():
        reasons.append("reader question is empty")
    if int(post["quality_score"]) < 31:
        reasons.append("quality score is below 31")
    if int(post["low_quality_risk"]) > 3:
        reasons.append("low-quality risk exceeds 3")
    for field in (
        "mandatory_gates_passed",
        "naturalness_qa_confirmed",
        "editorial_authenticity_confirmed",
        "self_similarity_qa_confirmed",
        "fact_qa_confirmed",
        "visual_qa_confirmed",
    ):
        if post[field] is not True:
            reasons.append(f"{field} is not true")
    if int(post["body_chars"]) >= 1800 and int(post["image_count"]) < 4:
        reasons.append("long post has fewer than four images")
    if is_affiliate(post):
        if post["disclosure_present"] is not True:
            reasons.append("affiliate disclosure is missing")
        links = int(post["affiliate_link_count"])
        if links < 1 or links > 5:
            reasons.append("affiliate link count must be between 1 and 5")
    elif int(post["affiliate_link_count"]) != 0:
        reasons.append("non-affiliate post contains affiliate links")
    return reasons


def choose_publishable(
    run_date: date,
    eligible: list[dict[str, Any]],
    history: list[dict[str, Any]],
    recovery_mode: bool,
) -> dict[str, Any] | None:
    window_start = run_date - timedelta(days=6)
    verified = [
        row
        for row in history
        if row.get("status") == "verified"
        and row.get("action", row.get("mode")) in {"publish", "auto-publish"}
        and row.get("run_date")
        and window_start <= as_date(row["run_date"]) <= run_date
    ]
    affiliate_count = sum(bool(row.get("affiliate")) or row.get("kind") in AFFILIATE_KINDS for row in verified)
    non_affiliate_count = len(verified) - affiliate_count
    yesterday = run_date - timedelta(days=1)
    affiliate_yesterday = any(
        as_date(row["run_date"]) == yesterday
        and (bool(row.get("affiliate")) or row.get("kind") in AFFILIATE_KINDS)
        for row in verified
    )

    non_affiliate = [post for post in eligible if not is_affiliate(post)]
    affiliate = [post for post in eligible if is_affiliate(post)]
    allow_affiliate = (
        not recovery_mode
        and affiliate_count < 2
        and non_affiliate_count >= affiliate_count + 2
        and not affiliate_yesterday
    )

    pool = non_affiliate
    if allow_affiliate and affiliate:
        pool = affiliate
    if not pool:
        pool = non_affiliate or (affiliate if allow_affiliate else [])
    if not pool:
        return None
    return max(pool, key=lambda post: (int(post["quality_score"]), -int(post["low_quality_risk"]), post["id"]))


def decide(plan: dict[str, Any], history: list[dict[str, Any]]) -> dict[str, Any]:
    run_date = as_date(plan["run_date"])
    posts = plan.get("posts", [])
    result: dict[str, Any] = {
        "run_date": run_date.isoformat(),
        "mode": plan.get("mode", "draft-only"),
        "publish": [],
        "draft_save": [],
        "blocked": [],
        "warnings": [],
    }
    if len(posts) != 3:
        result["warnings"].append("daily plan must contain exactly three candidates")

    questions: set[str] = set()
    fingerprints = {
        row.get("content_fingerprint")
        for row in history
        if row.get("status") == "verified" and row.get("content_fingerprint")
    }
    eligible = []
    for post in posts:
        reasons = validate_post(post)
        normalized_question = " ".join(str(post.get("reader_question", "")).split()).casefold()
        if normalized_question in questions:
            reasons.append("duplicate reader question in daily plan")
        questions.add(normalized_question)
        if post.get("content_fingerprint") in fingerprints:
            reasons.append("fingerprint already has a verified receipt")
        if reasons:
            result["blocked"].append({"id": post.get("id"), "reasons": reasons})
        else:
            eligible.append(post)

    affiliate_candidates = sum(is_affiliate(post) for post in posts)
    if affiliate_candidates > 1:
        result["warnings"].append("daily plan contains more than one affiliate candidate")
    if not any(not is_affiliate(post) for post in posts):
        result["warnings"].append("daily plan has no non-affiliate candidate")

    mode = plan.get("mode", "draft-only")
    if mode == "auto-publish" and not bool(plan.get("canary_mode")) and len(posts) == 3:
        selected = choose_publishable(run_date, eligible, history, bool(plan.get("recovery_mode")))
    else:
        selected = None
    if bool(plan.get("canary_mode")):
        result["warnings"].append("canary mode forces draft-only transfer")
    if selected:
        result["publish"].append(selected["id"])
    result["draft_save"] = [post["id"] for post in eligible if post is not selected]
    result["status"] = "ready" if eligible else "blocked"
    return result


def main() -> int:
    args = parse_args()
    try:
        result = decide(load_json(args.plan), load_jsonl(args.history))
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"BLOCKED: {exc}")
        return 2
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0 if result["status"] == "ready" else 1


if __name__ == "__main__":
    raise SystemExit(main())
