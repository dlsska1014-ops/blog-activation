# Live Publish Runbook

Use this only when the user has explicitly requested draft-save or public publishing. Treat the latest explicit instruction in the current conversation as the run mode; do not repeatedly ask for confirmation for every post in the same approved batch.

## Run Contract

Record before touching an editor:

- Run date and target platforms.
- Target account or blog name visible in the editor.
- Mode: `draft-only` or `auto-publish`.
- Expected post count.
- Expected image count per post.
- Affiliate status and disclosure requirement.
- Dated working-folder ledger path.

Do not store login data, private browser state, or authentication material.

## Preflight Gate

For every post, require all of the following before editor transfer:

1. Final title and plain-text body exist.
2. Body contains no Markdown headings, table separators, code fences, image placeholders, or internal notes.
3. Tags are present and relevant.
4. At least three usable images exist unless the user explicitly requests text-only output.
5. Image 1 is the topic thumbnail; images 2 and 3 support specific body sections.
6. Each image opens successfully, has nonzero dimensions, and is visually checked for text errors, clipping, and topic mismatch.
7. Time-sensitive facts and non-self-created image sources include checked dates.
8. Affiliate posts contain the required disclosure near the top and use only verified links.

Run `scripts/validate_publish_package.py` when a manifest is available. A failed gate blocks draft-save and publishing until fixed.
Check `publication-receipts.jsonl` before retrying any post whose final action timed out.

## Editor Transfer

1. Open a new editor and verify the visible account/blog.
2. Insert the title and plain-text body.
3. Insert each image at its intended section, waiting for upload completion before continuing.
4. Add tags and disclosure where required.
5. Recount editor images from the editor DOM or visible canvas; file selection alone is not proof of upload.
6. Inspect the first screen and final section.
7. Search the editor text for raw markers such as `##`, `| --- |`, triple backticks, and `[이미지`.

Never publish when an upload is still processing, the editor state is ambiguous, or the image count is lower than planned.

## Commit And Verify

- In `draft-only`, save the draft and verify it appears in the draft list or editor state.
- In `auto-publish`, use the visible final publish control only after the preflight and editor checks pass.
- After publishing, verify the resulting public URL, displayed title, body ending, and image count.
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

