# Visual Text Integrity

Use this whenever an image contains Korean text.

## Root Risk

Question marks inside an uploaded image usually mean the text was corrupted before rendering. Naver cannot restore it. A valid JPEG or PNG and a successful upload do not prove readable Korean.

Common causes:

- Passing Korean inline through a shell or command channel with the wrong encoding.
- Saving a card specification in a legacy encoding.
- Rendering with a font that lacks Korean glyphs.
- Trusting file dimensions instead of looking at the pixels.

## Required Workflow

1. Store all Korean card copy in a UTF-8 or UTF-8-BOM JSON specification file.
2. Do not embed Korean card text directly in a shell command.
3. Render Korean with a verified font such as Malgun Gothic or another installed Korean font.
4. Reject source text containing the replacement character or repeated question marks.
5. Open every rendered image at original resolution and visually inspect all text.
6. Record the exact expected text and `visual_qa_confirmed: true` in the publish manifest only after inspection.
7. After upload, inspect the actual editor image and then the public post image. Local-file review alone is insufficient.

## Stop Conditions

Block draft-save and publication when:

- Korean is shown as `??`, boxes, missing glyphs, or mojibake.
- Text is clipped, too small, low contrast, or outside the card.
- The rendered text differs from the approved copy.
- A text-bearing image has no visual review record.
- The public page was not visually checked after publication.

Use `scripts/create_visual_cards.py` for deterministic Korean cards and `scripts/audit_visual_assets.py` to validate its source-text sidecars. The audit script does not replace pixel-level visual inspection.


