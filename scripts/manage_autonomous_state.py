#!/usr/bin/env python3
"""Manage canary runs, overlap locks, and automatic pause state."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_STATE = {
    "version": 2,
    "canary_required": 3,
    "canary_completed": 0,
    "consecutive_failures": 0,
    "paused": False,
    "last_run": None,
    "require_editor_preflight": True,
}
FAILURE_STATUSES = {"partial", "blocked", "unknown"}
FAILURE_CLASSES = {
    "none",
    "content",
    "visual",
    "source",
    "transport",
    "observation_api",
    "authentication",
    "account_mismatch",
    "editor_surface",
    "commit_verification",
    "unknown",
}
RECOVERABLE_INFRA_FAILURES = {
    "transport",
    "observation_api",
    "authentication",
    "account_mismatch",
    "editor_surface",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--lock", type=Path)
    subparsers = parser.add_subparsers(dest="command", required=True)

    begin = subparsers.add_parser("begin")
    begin.add_argument("--run-id", required=True)
    begin.add_argument("--run-date", required=True)
    begin.add_argument("--preflight", type=Path)
    begin.add_argument("--max-age-minutes", type=int, default=30)

    finish = subparsers.add_parser("finish")
    finish.add_argument("--run-id", required=True)
    finish.add_argument("--status", required=True, choices=["verified", "partial", "blocked", "unknown"])
    finish.add_argument("--verified-drafts", type=int, default=0)
    finish.add_argument("--account-qa", action="store_true")
    finish.add_argument("--image-qa", action="store_true")
    finish.add_argument("--editor-qa", action="store_true")
    finish.add_argument("--failure-class", choices=sorted(FAILURE_CLASSES), default="none")
    finish.add_argument("--prepared-package", type=Path)
    finish.add_argument("--commit-attempted", action="store_true")

    resume = subparsers.add_parser("resume")
    resume.add_argument("--preflight", required=True, type=Path)
    resume.add_argument("--reason", required=True)
    resume.add_argument("--max-age-minutes", type=int, default=30)

    annotate = subparsers.add_parser("annotate-recovery")
    annotate.add_argument("--prepared-package", required=True, type=Path)
    annotate.add_argument("--failure-class", required=True, choices=sorted(RECOVERABLE_INFRA_FAILURES))
    annotate.add_argument("--source-run-id", required=True)
    annotate.add_argument("--reason", required=True)

    subparsers.add_parser("status")
    return parser.parse_args()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return dict(DEFAULT_STATE)
    data = json.loads(path.read_text(encoding="utf-8"))
    state = dict(DEFAULT_STATE)
    state.update(data)
    return state


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def lock_path(args: argparse.Namespace) -> Path:
    return args.lock or args.state.with_suffix(args.state.suffix + ".lock")


def read_lock(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def begin(args: argparse.Namespace, state: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    if state["paused"]:
        return 1, {"status": "blocked", "reason": "automation is paused after repeated failures"}

    preflight_digest = None
    preflight_checked_at = None
    if state.get("require_editor_preflight", True):
        if args.preflight is None:
            return 1, {"status": "blocked", "reason": "a passing editor preflight is required"}
        from validate_editor_preflight import validate_report

        report = json.loads(args.preflight.read_text(encoding="utf-8"))
        errors = validate_report(report, args.max_age_minutes)
        if errors:
            return 1, {"status": "blocked", "reason": "editor preflight failed", "errors": errors}
        if report.get("platform") != "naver":
            return 1, {"status": "blocked", "reason": "Naver preflight is required for Naver-first runs"}
        preflight_digest = hashlib.sha256(
            json.dumps(report, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()
        preflight_checked_at = report.get("checked_at")
    path = lock_path(args)
    existing = read_lock(path)
    if existing:
        return 1, {"status": "blocked", "reason": "another run owns the lock", "lock": existing}

    lock = {
        "run_id": args.run_id,
        "run_date": args.run_date,
        "started_at": now_iso(),
        "preflight_sha256": preflight_digest,
        "preflight_checked_at": preflight_checked_at,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as handle:
            json.dump(lock, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    except FileExistsError:
        return 1, {"status": "blocked", "reason": "another run created the lock"}

    canary = int(state["canary_completed"]) < int(state["canary_required"])
    return 0, {
        "status": "ready",
        "run_id": args.run_id,
        "canary_mode": canary,
        "effective_mode": "draft-only" if canary else "auto-publish",
        "canary_completed": state["canary_completed"],
        "canary_required": state["canary_required"],
        "preflight_checked_at": preflight_checked_at,
        "recovery_candidate": state.get("recovery_candidate"),
    }


def finish(args: argparse.Namespace, state: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    path = lock_path(args)
    current_lock = read_lock(path)
    if not current_lock or current_lock.get("run_id") != args.run_id:
        return 1, {"status": "blocked", "reason": "run does not own the active lock"}

    canary = int(state["canary_completed"]) < int(state["canary_required"])
    canary_verified = (
        args.status == "verified"
        and args.verified_drafts == 3
        and args.account_qa
        and args.image_qa
        and args.editor_qa
    )
    if canary and canary_verified:
        state["canary_completed"] = min(int(state["canary_required"]), int(state["canary_completed"]) + 1)

    failed = args.status in FAILURE_STATUSES or (canary and not canary_verified)
    state["consecutive_failures"] = int(state["consecutive_failures"]) + 1 if failed else 0
    if int(state["consecutive_failures"]) >= 2:
        state["paused"] = True
    failure_class = args.failure_class
    if failed and failure_class == "none":
        failure_class = "unknown"
    if not failed and failure_class != "none":
        return 1, {"status": "blocked", "reason": "verified runs must use failure-class none"}

    prepared_package = None
    if args.prepared_package is not None:
        prepared_package = args.prepared_package.resolve()
        if not prepared_package.exists() or not prepared_package.is_dir():
            return 1, {"status": "blocked", "reason": "prepared package directory does not exist"}

    state["last_run"] = {
        "run_id": args.run_id,
        "finished_at": now_iso(),
        "status": args.status,
        "verified_drafts": args.verified_drafts,
        "canary_verified": canary_verified,
        "failure_class": failure_class,
        "commit_attempted": bool(args.commit_attempted),
    }
    if (
        failed
        and failure_class in RECOVERABLE_INFRA_FAILURES
        and prepared_package is not None
        and not args.commit_attempted
    ):
        state["recovery_candidate"] = {
            "package_path": str(prepared_package),
            "source_run_id": args.run_id,
            "failure_class": failure_class,
            "recorded_at": now_iso(),
            "commit_attempted": False,
        }
    elif not failed:
        state.pop("recovery_candidate", None)
    write_json(args.state, state)
    path.unlink(missing_ok=True)
    return 0, {
        "status": "recorded",
        "canary_completed": state["canary_completed"],
        "canary_required": state["canary_required"],
        "consecutive_failures": state["consecutive_failures"],
        "paused": state["paused"],
    }


def resume(args: argparse.Namespace, state: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    if not state["paused"]:
        return 1, {"status": "blocked", "reason": "automation is not paused"}
    if read_lock(lock_path(args)):
        return 1, {"status": "blocked", "reason": "an active run lock exists"}
    reason = args.reason.strip()
    if len(reason) < 10:
        return 1, {"status": "blocked", "reason": "resume reason must describe the recovery"}

    from validate_editor_preflight import validate_report

    report = json.loads(args.preflight.read_text(encoding="utf-8"))
    errors = validate_report(report, args.max_age_minutes)
    if errors:
        return 1, {"status": "blocked", "reason": "editor preflight failed", "errors": errors}

    recovery = {
        "resumed_at": now_iso(),
        "reason": reason,
        "platform": report["platform"],
        "preflight_checked_at": report["checked_at"],
        "previous_run_id": (state.get("last_run") or {}).get("run_id"),
    }
    history = list(state.get("resume_history") or [])
    history.append(recovery)
    state["version"] = 2
    state["require_editor_preflight"] = True
    state["paused"] = False
    state["consecutive_failures"] = 0
    state["last_recovery"] = recovery
    state["resume_history"] = history[-20:]
    write_json(args.state, state)
    return 0, {
        "status": "resumed",
        "paused": False,
        "consecutive_failures": 0,
        "last_recovery": recovery,
    }


def annotate_recovery(args: argparse.Namespace, state: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    if not state["paused"]:
        return 1, {"status": "blocked", "reason": "recovery annotation requires paused state"}
    if read_lock(lock_path(args)):
        return 1, {"status": "blocked", "reason": "an active run lock exists"}
    last_run = state.get("last_run") or {}
    if last_run.get("run_id") != args.source_run_id:
        return 1, {"status": "blocked", "reason": "source run does not match the latest run"}
    package = args.prepared_package.resolve()
    if not package.exists() or not package.is_dir():
        return 1, {"status": "blocked", "reason": "prepared package directory does not exist"}
    reason = args.reason.strip()
    if len(reason) < 10:
        return 1, {"status": "blocked", "reason": "annotation reason must describe the evidence"}

    candidate = {
        "package_path": str(package),
        "source_run_id": args.source_run_id,
        "failure_class": args.failure_class,
        "recorded_at": now_iso(),
        "commit_attempted": False,
        "reason": reason,
    }
    state["version"] = 2
    state["require_editor_preflight"] = True
    state["recovery_candidate"] = candidate
    last_run["failure_class"] = args.failure_class
    last_run["commit_attempted"] = False
    state["last_run"] = last_run
    write_json(args.state, state)
    return 0, {"status": "annotated", "paused": True, "recovery_candidate": candidate}


def main() -> int:
    args = parse_args()
    try:
        state = load_state(args.state)
        if args.command == "begin":
            code, payload = begin(args, state)
        elif args.command == "finish":
            code, payload = finish(args, state)
        elif args.command == "resume":
            code, payload = resume(args, state)
        elif args.command == "annotate-recovery":
            code, payload = annotate_recovery(args, state)
        else:
            code, payload = 0, state
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "blocked", "reason": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
