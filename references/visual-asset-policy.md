# Visual Asset Policy

Use this before preparing images for Naver Blog or Tistory drafts.

## Core Rule

Treat thumbnails and body images as different assets.

- Thumbnail: create a custom AI image that matches the article's topic, reader problem, season, and emotional hook.
- Body images: use copyright-safe visuals that directly support the written section.

Do not use copied images from other bloggers, news sites, shopping pages, or social posts unless the user owns them or the license clearly allows reuse.

## Thumbnail Workflow

For every daily Naver draft, prepare one main thumbnail prompt and generate or request a thumbnail image unless the user asks for text-only output.

The thumbnail should:

- Match the actual article topic, not a generic blog card.
- Show the reader situation or benefit visually.
- Avoid brand logos, fake official marks, celebrity faces, copied product photos, or misleading discount badges.
- Use minimal Korean text only if text rendering can be verified. If exact Korean text matters, create the text layer deterministically with a card script instead of relying on AI text.
- Avoid sensational before/after imagery, exaggerated money claims, or medical/safety implications.

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

1. AI thumbnail or first image after the opening.
2. Summary card after the quick answer.
3. Body image matched to the current section, such as an official screenshot, checklist, map-like diagram, comparison table, or product category illustration.
4. Final checklist or FAQ card only if it adds value.

Never place images only for decoration. Each image should answer a reader question, reduce confusion, or make scanning easier.

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
- Any Korean is replaced by question marks, boxes, missing glyphs, or mojibake.
- It was not opened at original resolution and visually checked.

## Delivery Requirement

Every daily run should include:

- Thumbnail prompt or generated thumbnail path for each post.
- Body image list with source/copyright notes.
- Placement notes tied to exact sections.
- A warning list for any image still needing verification before draft-save.
- Exact expected card text and a recorded visual-QA result for every text-bearing image.

