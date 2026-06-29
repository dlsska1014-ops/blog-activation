#!/usr/bin/env python3
"""Self-test unattended state, reuse, and editor verification gates."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace


def load(name: str):
    path = Path(__file__).with_name(name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


STATE = load("manage_autonomous_state")
REUSE = load("check_editorial_reuse")
EDITOR = load("validate_editor_verification")


def state_args(state: Path, command: str, run_id: str = "run-1", status: str = "verified"):
    return SimpleNamespace(
        state=state,
        lock=None,
        command=command,
        run_id=run_id,
        run_date="2026-06-29",
        status=status,
        verified_drafts=3,
        account_qa=True,
        image_qa=True,
        editor_qa=True,
    )


def editor_payload() -> dict:
    return {
        "title_exact": True,
        "body_chars": 2400,
        "body_text_clean": True,
        "raw_marker_found": False,
        "expected_image_count": 4,
        "actual_image_count": 4,
        "representative_image_index": 1,
        "tags_count": 8,
        "disclosure_required": False,
        "disclosure_present": False,
        "final_state_verified": True,
        "images": [
            {"index": 1, "role": "scene", "rendered": True, "caption_present": True, "anchor_found": True, "text_position": 100, "text_artifact_found": False},
            {"index": 2, "role": "evidence", "rendered": True, "caption_present": True, "anchor_found": True, "text_position": 750, "text_artifact_found": False},
            {"index": 3, "role": "diagram", "rendered": True, "caption_present": True, "anchor_found": True, "text_position": 1350, "text_artifact_found": False},
            {"index": 4, "role": "checklist", "rendered": True, "caption_present": True, "anchor_found": True, "text_position": 2050, "text_artifact_found": False},
        ],
    }


def main() -> int:
    with TemporaryDirectory() as temporary:
        root = Path(temporary)
        state_path = root / "state.json"
        state = STATE.load_state(state_path)
        code, payload = STATE.begin(state_args(state_path, "begin"), state)
        assert code == 0 and payload["effective_mode"] == "draft-only", payload
        code, _ = STATE.begin(state_args(state_path, "begin", "overlap"), state)
        assert code == 1
        code, payload = STATE.finish(state_args(state_path, "finish"), state)
        assert code == 0 and payload["canary_completed"] == 1, payload

        for number in (2, 3):
            state = STATE.load_state(state_path)
            args = state_args(state_path, "begin", f"run-{number}")
            assert STATE.begin(args, state)[0] == 0
            finish_args = state_args(state_path, "finish", f"run-{number}")
            assert STATE.finish(finish_args, state)[0] == 0
        state = STATE.load_state(state_path)
        code, payload = STATE.begin(state_args(state_path, "begin", "run-4"), state)
        assert code == 0 and payload["effective_mode"] == "auto-publish", payload
        STATE.finish(state_args(state_path, "finish", "run-4"), state)

        failure_state_path = root / "failure-state.json"
        for number, status in ((1, "partial"), (2, "unknown")):
            failure_state = STATE.load_state(failure_state_path)
            begin_args = state_args(failure_state_path, "begin", f"failure-{number}")
            assert STATE.begin(begin_args, failure_state)[0] == 0
            finish_args = state_args(failure_state_path, "finish", f"failure-{number}", status)
            assert STATE.finish(finish_args, failure_state)[0] == 0
        failure_state = STATE.load_state(failure_state_path)
        assert failure_state["paused"] is True and failure_state["consecutive_failures"] == 2
        assert STATE.begin(state_args(failure_state_path, "begin", "failure-3"), failure_state)[0] == 1

        repeated = " ".join(["장마철 캠핑 준비물은 출발 전에 배수와 대피 동선을 확인해야 합니다"] * 20)
        distinct = " ".join(["여름철 냉장고 전력 사용량은 문을 여는 횟수와 설정 온도에 따라 달라집니다"] * 20)
        draft_words = REUSE.normalize(repeated)
        repeated_score, repeated_run = REUSE.compare(draft_words, REUSE.normalize(repeated))
        distinct_score, _ = REUSE.compare(draft_words, REUSE.normalize(distinct))
        assert repeated_score == 1.0 and repeated_run >= 18
        assert distinct_score < 0.18

        payload = editor_payload()
        assert EDITOR.validate(payload) == []
        for index, image in enumerate(payload["images"]):
            image["text_position"] = 2100 + index
        assert any("clustered" in error or "too late" in error for error in EDITOR.validate(payload))

    print("PASS: unattended safety gates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
