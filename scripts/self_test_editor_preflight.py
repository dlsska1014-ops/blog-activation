#!/usr/bin/env python3
"""Self-test editor preflight validation and guarded autonomous resume."""

from __future__ import annotations

import importlib.util
import json
from datetime import datetime, timedelta, timezone
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


PREFLIGHT = load("validate_editor_preflight")
STATE = load("manage_autonomous_state")


def ready_report(checked_at: datetime) -> dict:
    return {
        "schema_version": 1,
        "platform": "naver",
        "checked_at": checked_at.isoformat(),
        "browser_connection_ok": True,
        "tab_control_ok": True,
        "target_url": "https://blog.naver.com/GoBlogWrite.naver",
        "page_title": "블로그 글쓰기",
        "login_required": False,
        "editor_reachable": True,
        "account_match": True,
        "controls_verified": True,
        "editor_controls": ["title", "body", "image", "tag", "save", "publish"],
        "probe_method": "visible_dom",
        "transport_error": "",
        "side_effects_performed": False,
    }


def main() -> int:
    now = datetime.now(timezone.utc)
    report = ready_report(now)
    assert PREFLIGHT.validate_report(report, now=now) == []

    expired = ready_report(now - timedelta(minutes=31))
    assert any("older" in error for error in PREFLIGHT.validate_report(expired, now=now))
    login = ready_report(now)
    login.update(
        {
            "target_url": "https://nid.naver.com/nidlogin.login",
            "page_title": "네이버 : 로그인",
            "login_required": True,
            "editor_reachable": False,
            "account_match": False,
            "controls_verified": False,
            "editor_controls": [],
        }
    )
    assert any("login" in error for error in PREFLIGHT.validate_report(login, now=now))
    assert PREFLIGHT.classify_failure(login, PREFLIGHT.validate_report(login, now=now)) == "authentication"

    transport = ready_report(now)
    transport.update(
        {
            "tab_control_ok": False,
            "editor_reachable": False,
            "account_match": False,
            "controls_verified": False,
            "editor_controls": [],
            "transport_error": "Tabs can only be moved to and from normal windows.",
        }
    )
    transport_errors = PREFLIGHT.validate_report(transport, now=now)
    assert PREFLIGHT.classify_failure(transport, transport_errors) == "transport"

    with TemporaryDirectory() as temporary:
        root = Path(temporary)
        state_path = root / "state.json"
        report_path = root / "preflight.json"
        state_path.write_text(
            json.dumps(
                {
                    "version": 1,
                    "canary_required": 3,
                    "canary_completed": 1,
                    "consecutive_failures": 2,
                    "paused": True,
                    "last_run": {"run_id": "blocked-run"},
                }
            ),
            encoding="utf-8",
        )
        report_path.write_text(json.dumps(report), encoding="utf-8")
        args = SimpleNamespace(
            state=state_path,
            lock=None,
            preflight=report_path,
            reason="login and editor controls verified after recovery",
            max_age_minutes=30,
        )
        code, payload = STATE.resume(args, STATE.load_state(state_path))
        assert code == 0 and payload["status"] == "resumed", payload
        state = STATE.load_state(state_path)
        assert state["paused"] is False and state["consecutive_failures"] == 0
        assert state["last_recovery"]["previous_run_id"] == "blocked-run"

        missing_preflight = SimpleNamespace(
            state=state_path,
            lock=None,
            run_id="missing-preflight",
            run_date="2026-07-05",
            preflight=None,
            max_age_minutes=30,
        )
        assert STATE.begin(missing_preflight, state)[0] == 1

        blocked_report_path = root / "blocked-preflight.json"
        blocked_report_path.write_text(json.dumps(transport), encoding="utf-8")
        blocked_begin_args = SimpleNamespace(
            state=state_path,
            lock=None,
            run_id="blocked-preflight-run",
            run_date="2026-07-05",
            preflight=blocked_report_path,
            max_age_minutes=30,
        )
        code, payload = STATE.begin(blocked_begin_args, STATE.load_state(state_path))
        assert code == 1 and payload["failure_class"] == "transport", payload
        state = STATE.load_state(state_path)
        assert state["last_run"]["blocked_stage"] == "editor_preflight"
        assert state["last_run"]["commit_attempted"] is False

        begin_args = SimpleNamespace(
            state=state_path,
            lock=None,
            run_id="recovery-run",
            run_date="2026-07-05",
            preflight=report_path,
            max_age_minutes=30,
        )
        code, payload = STATE.begin(begin_args, state)
        assert code == 0 and payload["preflight_checked_at"] == report["checked_at"], payload
        lock = STATE.read_lock(STATE.lock_path(begin_args))
        assert lock and len(lock["preflight_sha256"]) == 64

        package = root / "prepared-package"
        package.mkdir()
        finish_args = SimpleNamespace(
            state=state_path,
            lock=None,
            run_id="recovery-run",
            status="blocked",
            verified_drafts=0,
            account_qa=False,
            image_qa=True,
            editor_qa=False,
            failure_class="transport",
            prepared_package=package,
            commit_attempted=False,
        )
        code, _ = STATE.finish(finish_args, state)
        assert code == 0
        state = STATE.load_state(state_path)
        assert state["last_run"]["failure_class"] == "transport"
        assert state["recovery_candidate"]["package_path"] == str(package.resolve())

        migration_state_path = root / "migration-state.json"
        migration_state_path.write_text(
            json.dumps(
                {
                    "version": 1,
                    "canary_required": 3,
                    "canary_completed": 1,
                    "consecutive_failures": 2,
                    "paused": True,
                    "last_run": {"run_id": "legacy-blocked", "status": "blocked"},
                }
            ),
            encoding="utf-8",
        )
        annotate_args = SimpleNamespace(
            state=migration_state_path,
            lock=None,
            prepared_package=package,
            failure_class="authentication",
            source_run_id="legacy-blocked",
            reason="validated package exists and no editor commit was attempted",
        )
        code, payload = STATE.annotate_recovery(
            annotate_args, STATE.load_state(migration_state_path)
        )
        assert code == 0 and payload["paused"] is True, payload
        migrated = STATE.load_state(migration_state_path)
        assert migrated["version"] == 2 and migrated["paused"] is True
        assert migrated["recovery_candidate"]["failure_class"] == "authentication"

    print("PASS: editor preflight and guarded resume")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
