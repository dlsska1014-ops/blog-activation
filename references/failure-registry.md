# Failure Registry

Keep durable operational incidents here. Record cause, evidence, impact, corrective action, and a verification condition. Do not store account identifiers, login/session data, browser authentication data, credential material, or screenshots containing private account details.

## 2026-07-05 Naver Canary Blocked

- Run: `automation-20260705-110541`
- Classification: `transport`, `observation_api`, `authentication`
- Evidence: browser tab handoff timed out; later read-only recovery reached the Naver login page; the DOM snapshot method also returned an API compatibility error.
- Impact: three validated packages were not transferred; no save/publish action occurred; canary remained 1/3; the second consecutive incomplete run paused automation.
- Content status: editorial reuse, autonomous decision, and visual storyboard passed. This was not a content-quality failure.
- Corrective action:
  - add a read-only editor preflight before research and before transfer,
  - validate browser transport, login, account, editor reachability, and required controls,
  - permit one supported observation-method fallback without entering content,
  - require a fresh passing preflight for paused-state resume,
  - preserve failed-run evidence and recovery history.
- Verification condition: a current `editor-preflight.json` passes `validate_editor_preflight.py`, guarded resume succeeds, and one Naver draft-only canary verifies title, body, four-image placement, captions, tags, topic, and final draft-list state.
- Current status: mitigation implemented; operational recovery remains blocked until Naver login and editor controls pass the preflight.

## 2026-07-05 Follow-up Hardening

- Gap: preflight was documented but not enforced by the state machine.
- Gap: failure class and reusable validated packages were not persisted in autonomous state.
- Correction: `begin` now requires and hashes a passing Naver preflight; `finish` records a normalized failure class and a safe recovery candidate only when no commit was attempted.
- Verification: tests cover missing preflight rejection, preflight digest binding, failure-class persistence, prepared-package recovery, and safe legacy paused-state annotation.
- Applied state migration: the 2026-07-05 validated package is registered as the current recovery candidate with `authentication` as the primary failure class and `commit_attempted: false`; paused state remains active.

## 2026-07-07 Naver Preflight Blocked

- Run: `automation-20260707-175033`
- Classification: `authentication`
- Evidence: read-only Chrome preflight reached `https://blog.naver.com/GoBlogWrite.naver` but was redirected to Naver login; visible page title was `네이버 : 로그인`; required editor controls `image`, `tag`, and `save` were not verifiable.
- Impact: no research, image generation, editor input, draft-save, or publication occurred; canary remains 1/3; the prior recovery candidate from 2026-07-05 remains the next item to verify after login recovery.
- State note: `manage_autonomous_state.py begin` rejected the failed preflight before creating a lock, so `finish` could not record the blocked run and returned `run does not own the active lock`.
- Evidence files: `C:\Users\백인남-PC\Documents\Side Line\blog-activation-2026-07-07-preflight-blocked\editor-preflight.json`, `begin-result.json`, and `finish-attempt-result.json`.
- Corrective action: sign in to the intended Naver account in Chrome, confirm the blog editor opens without a login or protection screen, then rerun the automation so a fresh `editor-preflight.json` can pass within 30 minutes.
- Verification condition: `validate_editor_preflight.py` returns `ready` with `login_required: false`, `editor_reachable: true`, `account_match: true`, and all controls `title`, `body`, `image`, `tag`, `save` verified.

## 2026-07-07 Tistory Duplicate Image And Tag-Entry Near Miss

- Run: manual AdSense revenue-strategy post transfer after Naver publication.
- Classification: `editor_surface`, `image_anchor`, `metadata`
- Evidence: first Tistory image paste did not appear in the current viewport; a second HTML image method was attempted before figure recount; scrolling later showed duplicate hero images. A footer-area click also opened preview while trying to enter tags.
- Impact: duplicate image would have been saved if not manually removed; preview click could have caused false confidence that tags were entered. No public Tistory publish occurred.
- Corrective action:
  - require figure recount or anchor scroll after every Tistory image attempt before any retry,
  - block mixed image insertion methods unless the first method is verified to have inserted zero figures,
  - add tag-input verification and preview-open guard,
  - save only after duplicate count is zero and visible tags are reverified.
- Verification condition: next Tistory canary records `editor_figure_count == expected_image_count`, `duplicate_image_count: 0`, `tag_input_verified: true`, and `preview_opened_during_tag_entry: false` or closed-and-reverified.
