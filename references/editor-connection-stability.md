# Editor Connection Stability

Use this before research in unattended runs and again immediately before editor transfer. The purpose is to fail early when the browser transport, login, account, or editor controls are unavailable.

## Read-Only Preflight

1. Confirm the browser extension responds to one lightweight tab-list call.
2. Reuse or claim one confirmed blank tab. Do not navigate an unrelated user tab and do not create a replacement post.
3. Navigate to the official platform editor URL without typing content or clicking save/publish.
4. Record the final URL and page title.
5. Treat a Naver `nidlogin` URL, a login title, account protection, CAPTCHA, or challenge as `login_required: true` and `blocked`.
6. Confirm the target account/blog and the visible title, body, image, tag, and save controls.
7. Record which observation method worked: `dom_snapshot`, `visible_dom`, `accessibility`, or `screenshot_verified`.
8. If one observation API fails, use one supported fallback observation method. Do not perform editor input while transport capability is uncertain.
9. Write `editor-preflight.json` and run `scripts/validate_editor_preflight.py`.
10. Pass the same validated report to `manage_autonomous_state.py begin --preflight ...`; the state lock records its SHA-256 digest and checked time.

The report must contain no login data, browser authentication data, session exports, private identifiers, or credential material.

## Chrome Window Readiness

Before claiming or creating a tab, make sure Chrome has at least one ordinary browser window available. Popup, app, authentication, or game windows can let the extension answer tab-list calls while still failing tab moves or tab claims. If tab creation fails with a window-state error, or a just-listed blank tab cannot be claimed, classify the run as `transport` and stop before research.

Recovery steps:

1. Bring a normal Chrome window to the foreground.
2. Close or move aside popup/authentication windows that are not normal browser tabs.
3. Keep one ordinary `about:blank` tab available in that window.
4. Re-run the read-only preflight and require `tab_control_ok: true` before any source browsing, image generation, or editor input.

Do not continue from extension connectivity alone. A preflight only passes when both the extension and actual tab control work.

## Required Report

```json
{
  "schema_version": 1,
  "platform": "naver",
  "checked_at": "2026-07-05T03:00:00+00:00",
  "browser_connection_ok": true,
  "tab_control_ok": true,
  "target_url": "https://blog.naver.com/GoBlogWrite.naver",
  "page_title": "블로그 글쓰기",
  "login_required": false,
  "editor_reachable": true,
  "account_match": true,
  "controls_verified": true,
  "editor_controls": ["title", "body", "image", "tag", "save"],
  "probe_method": "visible_dom",
  "transport_error": "",
  "side_effects_performed": false
}
```

## Pause Recovery

- Never clear `paused` by directly editing the state file.
- Repair login or transport first, then produce a fresh passing preflight no older than 30 minutes.
- Resume only with `manage_autonomous_state.py resume --preflight ... --reason ...`.
- Resume resets the consecutive-failure counter but preserves the failed run and appends recovery history.
- After resume, run exactly one Naver draft-only canary. Do not perform a Tistory transfer in the same stabilization run.
- When a transport, authentication, account, or editor-surface failure happens before any save/publish attempt, pass `--failure-class` and `--prepared-package` to `finish`. The next `begin` returns this recovery candidate so it is checked before new content is created.
- For a legacy paused state that predates recovery-candidate fields, use `annotate-recovery` only when the latest run matches, the package directory exists, and evidence confirms no commit was attempted. This migrates state without unpausing it.

## Failure Classes

- `transport`: extension or tab control unavailable.
- `observation_api`: DOM/accessibility/screenshot observation cannot verify controls.
- `authentication`: login expired or account protection is visible.
- `account_mismatch`: the visible account/blog differs from the run contract.
- `editor_surface`: required controls are missing or the page is not the editor.
- `commit_verification`: save/publish may have happened but final state is not verified.

Record the class in the failure registry and receipt notes. Never treat transport or authentication recovery as content QA success.
