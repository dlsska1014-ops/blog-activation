# Live Publish Runbook

Use this only when the user has explicitly requested draft-save or public publishing. Treat the latest explicit instruction in the current conversation as the run mode; do not repeatedly ask for confirmation for every post in the same approved batch.

## Run Contract

Record before touching an editor:

- Run date and target platforms.
- Target account or blog name visible in the editor.
- Mode: `draft-only` or `auto-publish`.
- Expected post count.
- Expected image count per post.
- Ordered visual roles and captions.
- Experience basis, privacy-safe evidence note, and sponsorship status.
- Reader question, `new_post` or `update_existing` action, cluster role, and canonical URL when updating.
- Intended internal links or a recorded reason that none are suitable.
- Fact freshness level, checked date, source records, and any strong-title evidence.
- Affiliate status and disclosure requirement.
- Dated working-folder ledger path.

Do not store login data, private browser state, or authentication material.

## Preflight Gate

For every post, require all of the following before editor transfer:

1. Final title and plain-text body exist.
2. Body contains no Markdown headings, table separators, code fences, image placeholders, or internal notes.
3. Tags are present and relevant.
4. `experience_basis` is recorded and consistent with the body; research-only posts contain no firsthand claims.
5. A short post has at least three usable images; a post of 1,800 characters or more has at least four unless a documented exception is approved.
6. Image 1 is scene-first; evidence-backed posts lead with an owned original photo. Later images provide evidence or explanation and a decision aid.
7. Each image opens successfully, has nonzero dimensions, and is visually checked for text errors, clipping, and topic mismatch.
   - For Korean cards, verify the actual pixels contain readable Korean rather than `??`, boxes, or missing glyphs.
8. Time-sensitive facts and non-self-created image sources include checked dates.
9. Affiliate and sponsored posts contain the required disclosure near the top; affiliate links are verified.
10. Every body visual has a functional caption; sourced visuals have reuse records and original photos have ownership records.
11. Korean editorial QA and internal-link QA are confirmed.
12. User-owned photos have full-resolution privacy notes, removed GPS metadata, and no near-duplicate frame in the selected set.
13. Every user-owned photo matches a prepared privacy sidecar; current and live facts remain inside their recheck window.

Run `scripts/validate_publish_package.py` when a manifest is available. A failed gate blocks draft-save and publishing until fixed.
Check `publication-receipts.jsonl` before retrying any post whose final action timed out.

## Editor Transfer

1. Open a new editor and verify the visible account/blog.
2. Insert the title and plain-text body.
3. Insert each image at its intended section, waiting for upload completion before continuing.
4. Add each approved caption directly below its visual.
5. Add tags and disclosure where required.
6. Add approved internal links with natural anchor text where planned.
7. Recount editor images from the editor DOM or visible canvas; file selection alone is not proof of upload.
8. Inspect the first screen, visual-role order, captions, and final section.
9. Search the editor text for raw markers such as `##`, `| --- |`, triple backticks, and `[이미지`.

Never publish when an upload is still processing, the editor state is ambiguous, or the image count is lower than planned.

## Commit And Verify

- In `draft-only`, save the draft and verify it appears in the draft list or editor state.
- In `auto-publish`, use the visible final publish control only after the preflight and editor checks pass.
- After publishing, verify the resulting public URL, displayed title, body ending, and image count.
- Follow `published-post-audit.md`: inspect the first, middle, and last public image and scan the public body for raw Markdown and internal notes.
- Confirm the first public image is the intended scene, not a low-resolution placeholder or card substituted out of order.
- Confirm the recent-post list contains the intended title once and that the URL resolves to that title.
- Record one receipt per platform: title, status, URL or draft identifier, image count, checked time, and any exception.
- Use `scripts/record_publication_receipt.py` so a verified duplicate is blocked by content fingerprint.

Use these status values:

- `verified`: target state and content were confirmed.
- `partial`: one platform or one post failed while others were verified.
- `blocked`: login, editor, source, link, or upload verification prevented a safe commit.
- `unknown`: an action may have occurred but its result could not be confirmed. Never report this as success.

## Failure Recovery

- If a tab or editor hangs, open a fresh editor tab and leave unrelated user tabs untouched.
- If an image upload fails, retry once with a local JPEG or PNG from a short upload-safe path, then recount images.
- If text transfer introduces formatting debris, clear the affected body and reinsert clean plain text.
- If the final action times out, inspect the post list or public URL before retrying to avoid duplicates.
- Do not create a replacement post until duplicate status is known.
- Report platform results separately; a Tistory failure does not erase a verified Naver result.
