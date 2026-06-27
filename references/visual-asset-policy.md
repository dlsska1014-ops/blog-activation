# Visual Asset Policy

Use this before preparing images for Naver Blog or Tistory drafts.

## Contents

- Core and copyright rules
- Thumbnail and body-image workflows
- Placement and diversity gates
- Manifest, source, rejection, and delivery rules

## Core Rule

Treat thumbnails and body images as different assets.

- Thumbnail: use the strongest user-owned scene photo when available. Otherwise create a scene-first custom AI image that matches the article's topic, reader problem, season, and emotional hook.
- Body images: use copyright-safe visuals that directly support the written section.

Do not use copied images from other bloggers, news sites, shopping pages, or social posts unless the user owns them or the license clearly allows reuse.

## Thumbnail Workflow

For every daily Naver draft, choose the hero asset after checking the experience basis. Do not generate an AI thumbnail merely to replace a stronger owned photo.

The thumbnail should:

- Match the actual article topic, not a generic blog card.
- Show the reader situation or benefit visually with one clear focal subject.
- Look like an editorial photograph or a polished original illustration, not a slide template.
- Avoid brand logos, fake official marks, celebrity faces, copied product photos, or misleading discount badges.
- Prefer a text-free AI scene. If exact Korean text matters, add a short deterministic overlay after generation and keep it inside the central safe area.
- Avoid sensational before/after imagery, exaggerated money claims, or medical/safety implications.
- Reject malformed hands, unreadable objects, random letters, fake interfaces, and accidental logos.

Thumbnail prompt fields:

- Article title:
- Reader situation:
- Visual subject:
- Mood:
- Required text, if any:
- Text to avoid:
- Brand/copyright constraints:
- Aspect ratio: 16:9

## Body Image Workflow

For each body section, choose the safest useful visual type:

1. Self-created visual:
   - summary card,
   - checklist image,
   - comparison table,
   - flowchart,
   - simple diagram.
2. Official or public-source screenshot:
   - use only when it is needed to explain an event, policy, application path, or product condition,
   - include source name and checked date in draft notes,
   - crop only the relevant part,
   - do not imply endorsement or affiliation.
3. User-provided image:
   - use when the user confirms they own or can use it.
   - record `ownership_basis` and the observation date when the image supports a current condition,
   - keep the image tied to the supplied note rather than inventing a new story.
   - inspect faces, children, plates, addresses, receipts, screens, QR codes, identifying signs, and reflections at full resolution,
   - strip GPS metadata before editor transfer,
   - record `privacy_qa_confirmed`, `privacy_note`, and `location_metadata_removed`.
   - run `scripts/prepare_owned_photo.py` to auto-orient, resize, remove metadata, and optionally blur user-selected regions,
   - prepare once without confirmation, inspect the output at full resolution, then rerun with `--confirm-manual-review` only when the privacy check is complete,
   - use `original_photo` only as experience evidence and `owned_context_photo` for neutral research-only context.
4. Licensed/free stock image:
   - use only from sources with clear reuse terms,
   - record the source URL and license note.
5. Affiliate/product image:
   - use only when the affiliate platform or merchant terms allow it,
   - otherwise use a self-created category illustration or comparison card instead.

When copyright status is unclear, do not insert the image. Use a self-created card or AI-generated generic illustration instead.

Owned-photo preparation:

```powershell
python scripts/prepare_owned_photo.py source.jpg prepared.jpg --blur 120,80,240,160
# Inspect prepared.jpg at full resolution, then confirm only after the review.
python scripts/prepare_owned_photo.py source.jpg prepared.jpg --blur 120,80,240,160 --confirm-manual-review
```

Use blur coordinates from the source image after EXIF orientation is applied. The generated `.privacy.json` belongs beside the prepared image and must not contain private narrative or account data.

For every text-bearing image, read `visual-text-integrity.md`. A file existing on disk is not proof that Korean rendered correctly.

## Placement Standard

For most Naver posts:

1. Scene-first AI thumbnail, original photo, owned context photo, or licensed photo after the opening.
2. Source-backed evidence, official screenshot, or explanatory diagram near the first factual section.
3. Comparison table, checklist, or decision aid where the reader must choose.
4. Optional final visual only when it adds a new function.

Never place images only for decoration. Each image should answer a reader question, reduce confusion, or make scanning easier.

For experience-backed posts, original photos may exceed four when each image proves a different condition or step. Do not insert near-duplicates, burst-series frames, or repeated angles merely to imitate high image counts.

## Visual Diversity Gate

For posts of 1,800 Korean characters or more:

- Use at least four visuals.
- Use at least three distinct visual roles.
- Use no more than two text-card roles.
- Never place two text cards consecutively.
- Make the first visual a scene, original photo, or licensed photo rather than a text card.
- Include at least one evidence or explanation role and one decision-aid role.

For shorter posts, three visuals are acceptable only when they still include a scene-first image and at least two distinct roles.

Allowed role names for publish manifests:

- `ai_scene_thumbnail`
- `original_photo`
- `owned_context_photo`
- `licensed_photo`
- `official_screenshot`
- `source_evidence`
- `diagram`
- `comparison_table`
- `checklist_card`
- `summary_card`
- `faq_card`
- `product_image`
- `category_illustration`

Treat `comparison_table`, `checklist_card`, `summary_card`, and `faq_card` as text-card roles.

## Visual Manifest

Record every visual as an object with:

- `path`
- `role`
- `caption`
- `contains_text`
- `visual_qa_confirmed`
- `source_url`, `checked_date`, and `reuse_basis` when the visual is sourced, official, licensed, or a product image
- `ownership_basis` when the role is `original_photo` or `owned_context_photo`
- `privacy_qa_confirmed`, `privacy_note`, and `location_metadata_removed` for either owned-photo role
- a matching `.privacy.json` sidecar created by `prepare_owned_photo.py` for either owned-photo role

Use the same order as the editor. The first manifest visual must be the first image in the article.

## Source Note Format

Record this for every non-AI, non-self-created body image:

- Image purpose:
- Source:
- URL:
- Checked date:
- License/reuse basis:
- What may change:

## Rejection Rules

Reject an image if:

- It was copied from another blog.
- It contains a creator's personal photo, unique layout, watermark, or branded thumbnail.
- The license or reuse permission is unclear.
- It uses a brand logo in a way that looks official.
- It overstates a benefit, discount, ranking, product performance, or personal experience.
- It is not connected to the nearby paragraph.
- It repeats the same template role as the preceding image.
- It is an AI scene presented as if it were a real visit or product test.
- Any Korean is replaced by question marks, boxes, missing glyphs, or mojibake.
- It was not opened at original resolution and visually checked.
- It exposes a face, child, plate, address, receipt, screen, QR code, identifying sign, or reflection without a clear safe-use decision.
- It still contains GPS metadata.
- It is a user-owned photo perceptually near-duplicate to another selected user-owned photo.

## Delivery Requirement

Every daily run should include:

- Thumbnail prompt or generated thumbnail path for each post.
- Body image list with source/copyright notes.
- Placement notes tied to exact sections.
- A role and useful caption for every image.
- A warning list for any image still needing verification before draft-save.
- Exact expected card text and a recorded visual-QA result for every text-bearing image.
