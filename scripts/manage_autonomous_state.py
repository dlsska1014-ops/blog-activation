#!/usr/bin/env python3
"""Manage canary runs, overlap locks, and automatic pause state."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_STATE = {
    "version": 1,
    "canary_required": 3,
    "canary_completed": 0,
    "consecutive_failures": 0,
    "paused": False,
    "last_run": None,
}
FAILURE_STATUSES = {"partial", "blocked", "unknown"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--lock", type=Path)
    subparsers = parser.add_subparsers(dest="command", required=True)

    begin = subparsers.add_parser("begin")
    begin.add_argument("--run-id", required=True)
    begin.add_argument("--run-date", required=True)

    finish = subparsers.add_parser("finish")
    finish.add_argument("--run-id", required=True)
    finish.add_argument("--status", required=True, choices=["verified", "partial", "blocked", "unknown"])
    finish.add_argument("--verified-drafts", type=int, default=0)
    finish.add_argument("--account-qa", action="store_true")
    finish.add_argument("--image-qa", action="store_true")
    finish.add_argument("--editor-qa", action="store_true")

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
    path = lock_path(args)
    existing = read_lock(path)
    if existing:
        return 1, {"status": "blocked", "reason": "another run owns the lock", "lock": existing}

    lock = {"run_id": args.run_id, "run_date": args.run_date, "started_at": now_iso()}
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
    state["last_run"] = {
        "run_id": args.run_id,
        "finished_at": now_iso(),
        "status": args.status,
        "verified_drafts": args.verified_drafts,
        "canary_verified": canary_verified,
    }
    write_json(args.state, state)
    path.unlink(missing_ok=True)
    return 0, {
        "status": "recorded",
        "canary_completed": state["canary_completed"],
        "canary_required": state["canary_required"],
        "consecutive_failures": state["consecutive_failures"],
        "paused": state["paused"],
    }


def main() -> int:
    args = parse_args()
    try:
        state = load_state(args.state)
        if args.command == "begin":
            code, payload = begin(args, state)
        elif args.command == "finish":
            code, payload = finish(args, state)
        else:
            code, payload = 0, state
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "blocked", "reason": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())

