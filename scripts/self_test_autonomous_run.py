#!/usr/bin/env python3
"""Self-test the autonomous daily content decision guard."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).with_name("decide_autonomous_run.py")
SPEC = importlib.util.spec_from_file_location("decide_autonomous_run", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def post(post_id: str, kind: str, score: int = 34) -> dict:
    affiliate = kind in MODULE.AFFILIATE_KINDS
    return {
        "id": post_id,
        "title": f"title-{post_id}",
        "kind": kind,
        "reader_question": f"question-{post_id}",
        "cluster_key": f"cluster-{post_id}",
        "quality_score": score,
        "low_quality_risk": 2,
        "mandatory_gates_passed": True,
        "naturalness_qa_confirmed": True,
        "editorial_authenticity_confirmed": True,
        "self_similarity_qa_confirmed": True,
        "fact_qa_confirmed": True,
        "visual_qa_confirmed": True,
        "body_chars": 2200,
        "image_count": 4,
        "affiliate_link_count": 5 if affiliate else 0,
        "disclosure_present": affiliate,
        "content_fingerprint": f"fp-{post_id}",
    }


def main() -> int:
    plan = {
        "run_date": "2026-06-29",
        "mode": "auto-publish",
        "posts": [post("info", "information", 35), post("season", "seasonal", 33), post("aff", "affiliate", 36)],
    }
    history = [
        {"run_date": "2026-06-27", "status": "verified", "action": "publish", "kind": "information"},
        {"run_date": "2026-06-26", "status": "verified", "action": "publish", "kind": "seasonal"},
    ]
    result = MODULE.decide(plan, history)
    assert result["publish"] == ["aff"], result
    assert sorted(result["draft_save"]) == ["info", "season"], result

    plan["recovery_mode"] = True
    result = MODULE.decide(plan, history)
    assert result["publish"] == ["info"], result

    plan["recovery_mode"] = False
    plan["canary_mode"] = True
    result = MODULE.decide(plan, history)
    assert result["publish"] == [], result
    assert len(result["draft_save"]) == 3, result

    broken = post("broken", "affiliate")
    broken["disclosure_present"] = False
    broken_plan = {"run_date": "2026-06-29", "mode": "auto-publish", "posts": [post("a", "information"), post("b", "seasonal"), broken]}
    result = MODULE.decide(broken_plan, history)
    assert result["blocked"][0]["id"] == "broken", result
    assert "broken" not in result["publish"] + result["draft_save"], result

    duplicate_history = history + [{"run_date": "2026-06-28", "status": "verified", "action": "publish", "content_fingerprint": "fp-a"}]
    result = MODULE.decide(broken_plan, duplicate_history)
    assert any(item["id"] == "a" for item in result["blocked"]), result

    print("PASS: autonomous run guard")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
