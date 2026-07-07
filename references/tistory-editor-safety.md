# Tistory Editor Safety

Use this before every automated Tistory editor session. Tistory TinyMCE selection, autosave, image captions, and editor tabs must be treated independently from Naver.

## Stabilization Mode

- Keep Tistory `draft-only` for its first three verified editor runs.
- Transfer one Tistory post per run until those three canaries pass.
- Use one editor tab only. Save and verify it before opening the next post in the same tab.
- Stay in basic mode. Do not open HTML or Markdown mode during unattended operation.
- Record the visible draft count before and after the manual draft-save action.

## Clean Editor Gate

Before typing, confirm:

- the expected blog name is visible,
- title, body, category, tag, attachment, and draft-save controls exist,
- no recovery, mode-switch, permission, or unsaved-content dialog is present,
- only one Tistory editor tab is open,
- the body contains no recovered text, image figure, or caption from an earlier attempt.

If an unsaved editor becomes corrupted, do not try to repair it with repeated `fill`, Select All, or a second editor tab. Confirm the manual draft count did not increase, discard the unsaved editor in the same tab, and restart only after a clean-editor check.

## Transfer Order

1. Insert the title.
2. Insert the complete adapted body once.
3. Verify the first and last 80 characters and the body length.
4. Select the existing category.
5. Add and recount at least three tags.
6. Insert images one at a time through a verified attachment flow.
7. After each image, verify the figure count, section anchor, and caption field before continuing.
8. Add only a concise caption or alt text while the image is selected.
9. If an image attempt appears to fail, recount figures and scroll to the intended anchor before trying a different insertion method. Do not use a second image method while the current figure count is unknown.
10. Recheck body beginning, ending, and length after all images.
11. Verify that every manifest image fingerprint appears exactly once, the total figure count equals the expected image count, and no body block repeats.
12. Verify zero active uploads, then use the requested final action.

Do not replace the body, paste a body chunk, or type multi-paragraph text after the first image is inserted. A selected image figure can redirect text into its caption.

## Image Rules

- Do not use clipboard image paste in unattended mode until a separate canary proves exact anchor placement in the current editor build.
- Do not mix clipboard image paste and HTML/data-URL image insertion in the same Tistory editor unless a post-attempt figure count proves the first attempt inserted zero figures.
- Do not assume the current cursor is the intended insertion point. Verify the nearby section anchor after every image.
- Reject a figure whose accessible name or caption contains a body paragraph, multiple sentences unrelated to the image, or more than 120 characters.
- Reject images grouped at the beginning or end when the manifest requires distributed section anchors.
- Treat a visible figure as upload evidence only when the upload counter is zero and the rendered image is visible.
- Count every figure, including empty placeholders and failed-upload remnants. The figure count must equal the expected image count.
- Compare manifest SHA-256 fingerprints or stable normalized source identifiers. Every editor image must be unique and appear exactly once.
- Treat repeated first/last body excerpts, duplicated section sequences, or repeated full paragraphs as body contamination.
- If a duplicate image appears, remove only the extra selected image once, recount figures, and continue only when the count matches the manifest. If duplicate removal cannot be verified, discard the editor instead of saving a contaminated draft.

## Tag And Preview Guard

- Enter tags only when the visible tag input or tag placeholder is clearly active.
- Do not use footer-area clicks as a proxy for tag entry; they can open preview or other controls.
- If preview opens while entering tags, close it, return to the editor, and re-locate the visible tag input before typing.
- Recount visible tags after entry and before draft-save or publish.

## Tab And Recovery Rules

- Never open a second Tistory editor tab to escape a stuck or contaminated editor.
- If the browser disconnects or a mode-switch confirmation appears, stop the run as `blocked` or `unknown`; do not retry the final action.
- Autosave text is not a verified draft. Only a manual draft-save followed by a draft-list or draft-count change can be recorded as verified.
- Do not let a Tistory failure trigger a Naver retry.

## Required Tistory Evidence

Record these fields in `editor-verification.json`:

- `editor_mode: basic`
- `single_editor_tab: true`
- `mode_switch_used: false`
- `unsaved_recovery_present: false`
- `upload_in_progress: false`
- `caption_contamination_found: false`
- `long_caption_count: 0`
- `image_anchor_order_verified: true`
- `body_replaced_after_image_insert: false`
- `editor_figure_count` equal to `expected_image_count`
- `orphan_figure_count: 0`
- `duplicate_image_count: 0`
- `editor_image_sequence_unique: true`
- `duplicate_body_block_count: 0`
- `draft_count_before` and `draft_count_after` for draft-only runs
- `tag_input_verified: true`
- `preview_opened_during_tag_entry: false` unless the preview was closed and tags were reverified

Any failed field blocks the Tistory final action.
