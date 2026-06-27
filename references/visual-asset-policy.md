# Visual Asset Policy

Use this before preparing images for Naver Blog or Tistory drafts.

## Contents

- Core and copyright rules
- Thumbnail and body-image workflows
- Placement and diversity gates
- Manifest, source, rejection, and delivery rules

## Core Rule

Treat thumbnails and body images as different assets.

- Thumbnail: create a scene-first custom AI image that matches the article's topic, reader problem, season, and emotional hook. A recognizable place, object, room, product category, or action should be visible.
- Body images: use copyright-safe visuals that directly support the written section.

Do not use copied images from other bloggers, news sites, shopping pages, or social posts unless the user owns them or the license clearly allows reuse.

## Thumbnail Workflow

For every daily Naver draft, prepare one main thumbnail prompt and generate or request a thumbnail image unless the user asks for text-only output.

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
4. Licensed/free stock image:
   - use only from sources with clear reuse terms,
   - record the source URL and license note.
5. Affiliate/product image:
   - use only when the affiliate platform or merchant terms allow it,
   - otherwise use a self-created category illustration or comparison card instead.

When copyright status is unclear, do not insert the image. Use a self-created card or AI-generated generic illustration instead.

For every text-bearing image, read `visual-text-integrity.md`. A file existing on disk is not proof that Korean rendered correctly.

## Placement Standard

For most Naver posts:

1. Scene-first AI thumbnail, original photo, or licensed photo after the opening.
2. Source-backed evidence, official screenshot, or explanatory diagram near the first factual section.
3. Comparison table, checklist, or decision aid where the reader must choose.
4. Optional final visual only when it adds a new function.

Never place images only for decoration. Each image should answer a reader question, reduce confusion, or make scanning easier.

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
- Any Korean is replaced by question marks, boxes, missing glyphs, or mojibake.
- It was not opened at original resolution and visually checked.

## Delivery Requirement

Every daily run should include:

- Thumbnail prompt or generated thumbnail path for each post.
- Body image list with source/copyright notes.
- Placement notes tied to exact sections.
- A role and useful caption for every image.
- A warning list for any image still needing verification before draft-save.
- Exact expected card text and a recorded visual-QA result for every text-bearing image.
