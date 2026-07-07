#!/usr/bin/env python3
"""Self-test unattended state, reuse, and editor verification gates."""

from __future__ import annotations

import importlib.util
import json
from datetime import datetime, timezone
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


def state_args(
    state: Path,
    command: str,
    preflight: Path,
    run_id: str = "run-1",
    status: str = "verified",
):
    return SimpleNamespace(
        state=state,
        lock=None,
        command=command,
        run_id=run_id,
        run_date="2026-06-29",
        preflight=preflight,
        max_age_minutes=30,
        status=status,
        verified_drafts=3,
        account_qa=True,
        image_qa=True,
        editor_qa=True,
        failure_class="none" if status == "verified" else "unknown",
        prepared_package=None,
        commit_attempted=False,
    )


def editor_payload() -> dict:
    return {
        "platform": "naver",
        "title_exact": True,
        "body_chars": 2400,
        "body_text_clean": True,
        "raw_marker_found": False,
        "expected_image_count": 4,
        "actual_image_count": 4,
        "editor_figure_count": 4,
        "orphan_figure_count": 0,
        "duplicate_image_count": 0,
        "editor_image_sequence_unique": True,
        "duplicate_body_block_count": 0,
        "representative_image_index": 1,
        "tags_count": 8,
        "topic_or_category_selected": True,
        "topic_or_category_label": "생활 노하우",
        "non_affiliate_monetization_language_found": False,
        "disclosure_required": False,
        "disclosure_present": False,
        "final_state_verified": True,
        "images": [
            {"index": 1, "role": "scene", "rendered": True, "caption_present": True, "anchor_found": True, "text_position": 100, "text_artifact_found": False, "source_fingerprint": "sha256:image-1"},
            {"index": 2, "role": "evidence", "rendered": True, "caption_present": True, "anchor_found": True, "text_position": 750, "text_artifact_found": False, "source_fingerprint": "sha256:image-2"},
            {"index": 3, "role": "diagram", "rendered": True, "caption_present": True, "anchor_found": True, "text_position": 1350, "text_artifact_found": False, "source_fingerprint": "sha256:image-3"},
            {"index": 4, "role": "checklist", "rendered": True, "caption_present": True, "anchor_found": True, "text_position": 2050, "text_artifact_found": False, "source_fingerprint": "sha256:image-4"},
        ],
    }


def tistory_payload() -> dict:
    payload = editor_payload()
    payload.update(
        {
            "platform": "tistory",
            "mode": "draft-only",
            "topic_or_category_label": "일상",
            "editor_mode": "basic",
            "single_editor_tab": True,
            "mode_switch_used": False,
            "unsaved_recovery_present": False,
            "upload_in_progress": False,
            "caption_contamination_found": False,
            "long_caption_count": 0,
            "image_anchor_order_verified": True,
            "body_replaced_after_image_insert": False,
            "draft_count_before": 2,
            "draft_count_after": 3,
        }
    )
    return payload


def main() -> int:
    with TemporaryDirectory() as temporary:
        root = Path(temporary)
        state_path = root / "state.json"
        preflight_path = root / "preflight.json"
        preflight_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "platform": "naver",
                    "checked_at": datetime.now(timezone.utc).isoformat(),
                    "browser_connection_ok": True,
                    "tab_control_ok": True,
                    "target_url": "https://blog.naver.com/GoBlogWrite.naver",
                    "page_title": "블로그 글쓰기",
                    "login_required": False,
                    "editor_reachable": True,
                    "account_match": True,
                    "controls_verified": True,
                    "editor_controls": ["title", "body", "image", "tag", "save"],
                    "probe_method": "visible_dom",
                    "transport_error": "",
                    "side_effects_performed": False,
                }
            ),
            encoding="utf-8",
        )
        state = STATE.load_state(state_path)
        code, payload = STATE.begin(state_args(state_path, "begin", preflight_path), state)
        assert code == 0 and payload["effective_mode"] == "draft-only", payload
        code, _ = STATE.begin(state_args(state_path, "begin", preflight_path, "overlap"), state)
        assert code == 1
        code, payload = STATE.finish(state_args(state_path, "finish", preflight_path), state)
        assert code == 0 and payload["canary_completed"] == 1, payload

        for number in (2, 3):
            state = STATE.load_state(state_path)
            args = state_args(state_path, "begin", preflight_path, f"run-{number}")
            assert STATE.begin(args, state)[0] == 0
            finish_args = state_args(state_path, "finish", preflight_path, f"run-{number}")
            assert STATE.finish(finish_args, state)[0] == 0
        state = STATE.load_state(state_path)
        code, payload = STATE.begin(state_args(state_path, "begin", preflight_path, "run-4"), state)
        assert code == 0 and payload["effective_mode"] == "auto-publish", payload
        STATE.finish(state_args(state_path, "finish", preflight_path, "run-4"), state)

        failure_state_path = root / "failure-state.json"
        for number, status in ((1, "partial"), (2, "unknown")):
            failure_state = STATE.load_state(failure_state_path)
            begin_args = state_args(failure_state_path, "begin", preflight_path, f"failure-{number}")
            assert STATE.begin(begin_args, failure_state)[0] == 0
            finish_args = state_args(failure_state_path, "finish", preflight_path, f"failure-{number}", status)
            assert STATE.finish(finish_args, failure_state)[0] == 0
        failure_state = STATE.load_state(failure_state_path)
        assert failure_state["paused"] is True and failure_state["consecutive_failures"] == 2
        assert STATE.begin(state_args(failure_state_path, "begin", preflight_path, "failure-3"), failure_state)[0] == 1

        repeated = " ".join(["장마철 캠핑 준비물은 출발 전에 배수와 대피 동선을 확인해야 합니다"] * 20)
        distinct = " ".join(["여름철 냉장고 전력 사용량은 문을 여는 횟수와 설정 온도에 따라 달라집니다"] * 20)
        draft_words = REUSE.normalize(repeated)
        repeated_score, repeated_run = REUSE.compare(draft_words, REUSE.normalize(repeated))
        distinct_score, _ = REUSE.compare(draft_words, REUSE.normalize(distinct))
        assert repeated_score == 1.0 and repeated_run >= 18
        assert distinct_score < 0.18

        payload = editor_payload()
        assert EDITOR.validate(payload) == []
        missing_topic = editor_payload()
        missing_topic["topic_or_category_selected"] = False
        assert any("topic or category" in error for error in EDITOR.validate(missing_topic))
        tistory = tistory_payload()
        assert EDITOR.validate(tistory) == []
        contaminated = tistory_payload()
        contaminated["caption_contamination_found"] = True
        assert any("caption" in error for error in EDITOR.validate(contaminated))
        repeated_image = tistory_payload()
        repeated_image["images"][3]["source_fingerprint"] = repeated_image["images"][0]["source_fingerprint"]
        repeated_image["duplicate_image_count"] = 1
        repeated_image["editor_image_sequence_unique"] = False
        assert any("duplicate" in error or "unique" in error for error in EDITOR.validate(repeated_image))
        orphan_figure = tistory_payload()
        orphan_figure["editor_figure_count"] = 5
        orphan_figure["orphan_figure_count"] = 1
        assert any("orphan" in error or "figure count" in error for error in EDITOR.validate(orphan_figure))
        repeated_body = tistory_payload()
        repeated_body["duplicate_body_block_count"] = 2
        assert any("duplicated blocks" in error for error in EDITOR.validate(repeated_body))
        switched = tistory_payload()
        switched["editor_mode"] = "html"
        switched["mode_switch_used"] = True
        assert any("basic mode" in error for error in EDITOR.validate(switched))
        duplicate_save = tistory_payload()
        duplicate_save["draft_count_after"] = 4
        assert any("exactly one" in error for error in EDITOR.validate(duplicate_save))
        for index, image in enumerate(payload["images"]):
            image["text_position"] = 2100 + index
        assert any("clustered" in error or "too late" in error for error in EDITOR.validate(payload))

    print("PASS: unattended safety gates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
