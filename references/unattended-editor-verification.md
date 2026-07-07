# Unattended Editor Verification

Use this after browser transfer and before the final save or publish action. Write `editor-verification.json` in the dated run folder and validate it with `scripts/validate_editor_verification.py`.

## Account And Editor Health

- Confirm the visible Naver or Tistory account and blog name match the run contract.
- Confirm the editor exposes title, body, image, tag, save, and publish controls.
- Confirm no login, account-protection, permission, or unsaved-recovery dialog is present.
- For Tistory, confirm one editor tab, basic mode, no mode-switch action, no stale recovery state, and zero active uploads.
- Stop with `blocked` when the account is different, the session expired, or a challenge requires a person.

## Image Evidence

Record every image in editor order with:

- `index` and manifest `role`,
- whether the rendered image is visible rather than only selected for upload,
- whether its caption is present,
- whether nearby text matches the intended section anchor,
- its approximate character position in the clean body,
- whether Korean text shows question marks, boxes, missing glyphs, clipping, or replacement characters.

For long posts, require the scene-first image near the opening, at least one visual in the middle, and a later decision aid or checklist. Images grouped at the body ending fail even when the count is correct.

Require at least three photographic visuals, at least two non-AI origins, and context-problem-action-outcome coverage. Text cards require a recorded exception and are otherwise rejected. Compare the uploaded order with the manifest validated by `validate_visual_storyboard.py`.

Inspect the first, middle, and last image visually. Confirm image 1 is the representative image unless the manifest records an approved exception.

## Text And Final-State Evidence

- Compare the editor title exactly with the manifest.
- Compare the beginning and ending of the clean body and check total text length.
- Reject raw Markdown, prompts, placeholders, repeated question marks, and internal notes.
- Confirm at least three relevant tags and a visible affiliate disclosure when required.
- Confirm the closest visible Naver topic or Tistory category is selected and record its exact label.
- Confirm non-affiliate public copy contains no monetization or affiliate workflow language.
- For Tistory, reject any image caption or accessible image label that contains a body paragraph, exceeds 120 characters, or repeats a section heading with surrounding body text.
- For Tistory, confirm the complete body was transferred before image insertion and was not replaced afterward.
- Confirm every editor image fingerprint is unique, the total figure count matches the manifest, no empty/orphan figure remains, and no body block is duplicated.
- After the action, verify the title and time in the draft list or the title and URL on the public page.
- Record `final_state_verified: true` only from that observation, never from the click itself.

## Required Verification Shape

```json
{
  "platform": "naver",
  "title_exact": true,
  "body_chars": 2400,
  "body_text_clean": true,
  "raw_marker_found": false,
  "expected_image_count": 4,
  "actual_image_count": 4,
  "representative_image_index": 1,
  "tags_count": 8,
  "topic_or_category_selected": true,
  "topic_or_category_label": "생활 노하우",
  "non_affiliate_monetization_language_found": false,
  "editor_mode": "basic",
  "single_editor_tab": true,
  "mode_switch_used": false,
  "unsaved_recovery_present": false,
  "upload_in_progress": false,
  "caption_contamination_found": false,
  "long_caption_count": 0,
  "image_anchor_order_verified": true,
  "body_replaced_after_image_insert": false,
  "editor_figure_count": 4,
  "orphan_figure_count": 0,
  "duplicate_image_count": 0,
  "editor_image_sequence_unique": true,
  "duplicate_body_block_count": 0,
  "disclosure_required": false,
  "disclosure_present": false,
  "final_state_verified": true,
  "images": [
    {
      "index": 1,
      "role": "scene",
      "rendered": true,
      "caption_present": true,
      "anchor_found": true,
      "text_position": 120,
      "text_artifact_found": false
      ,"source_fingerprint": "sha256:example-unique-image-1"
    }
  ]
}
```

Do not store screenshots containing private account details in GitHub. Keep browser evidence only in the dated local run folder when needed for recovery.
