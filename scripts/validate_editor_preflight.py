#!/usr/bin/env python3
"""Validate a read-only editor connectivity and authentication preflight report."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_EDITOR_CONTROLS = {"title", "body", "image", "tag", "save"}
FAILURE_CLASSES = {
    "transport",
    "observation_api",
    "authentication",
    "account_mismatch",
    "editor_surface",
    "unknown",
}


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def validate_report(
    report: dict[str, Any], max_age_minutes: int = 30, now: datetime | None = None
) -> list[str]:
    errors: list[str] = []
    if report.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if report.get("platform") not in {"naver", "tistory"}:
        errors.append("platform must be naver or tistory")

    checked_at = parse_time(report.get("checked_at"))
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    if checked_at is None:
        errors.append("checked_at must be an ISO-8601 timestamp")
    else:
        age_seconds = (current - checked_at).total_seconds()
        if age_seconds < -300:
            errors.append("checked_at is in the future")
        if age_seconds > max_age_minutes * 60:
            errors.append(f"preflight is older than {max_age_minutes} minutes")

    boolean_requirements = {
        "browser_connection_ok": True,
        "tab_control_ok": True,
        "login_required": False,
        "editor_reachable": True,
        "account_match": True,
        "controls_verified": True,
        "side_effects_performed": False,
    }
    for field, expected in boolean_requirements.items():
        if report.get(field) is not expected:
            errors.append(f"{field} must be {str(expected).lower()}")

    target_url = str(report.get("target_url") or "")
    page_title = str(report.get("page_title") or "")
    if not target_url.startswith("https://"):
        errors.append("target_url must be an https URL")
    login_signal = f"{target_url} {page_title}".lower()
    if "nidlogin" in login_signal or "로그인" in login_signal:
        errors.append("login page detected")

    controls = report.get("editor_controls")
    if not isinstance(controls, list):
        errors.append("editor_controls must be a list")
    else:
        missing = sorted(REQUIRED_EDITOR_CONTROLS - {str(item) for item in controls})
        if missing:
            errors.append("missing editor controls: " + ", ".join(missing))

    probe_method = report.get("probe_method")
    if probe_method not in {"dom_snapshot", "visible_dom", "accessibility", "screenshot_verified"}:
        errors.append("probe_method must record a supported observation method")
    if report.get("transport_error") not in {None, ""}:
        errors.append("transport_error must be empty")
    return errors


def classify_failure(report: dict[str, Any], errors: list[str] | None = None) -> str:
    """Return the safest operational failure class for a blocked preflight."""
    if errors is None:
        errors = validate_report(report)
    if not errors:
        return "unknown"

    target_url = str(report.get("target_url") or "").lower()
    page_title = str(report.get("page_title") or "").lower()
    transport_error = str(report.get("transport_error") or "")
    login_signal = f"{target_url} {page_title}"

    if report.get("browser_connection_ok") is not True or report.get("tab_control_ok") is not True:
        return "transport"
    if transport_error.strip():
        return "transport"
    if report.get("login_required") is True or "nidlogin" in login_signal or "로그인" in login_signal:
        return "authentication"
    if report.get("account_match") is False:
        return "account_mismatch"
    if report.get("editor_reachable") is False or report.get("controls_verified") is False:
        return "editor_surface"
    if any("probe_method" in error for error in errors):
        return "observation_api"
    return "unknown"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--max-age-minutes", type=int, default=30)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
        errors = validate_report(report, args.max_age_minutes)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        report = {}
        errors = [str(exc)]
    payload = {
        "status": "ready" if not errors else "blocked",
        "failure_class": "none" if not errors else classify_failure(report, errors),
        "errors": errors,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
