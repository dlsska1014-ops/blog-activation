# Image And Thumbnail Guide

Use this guide to plan blog visuals after reading `visual-asset-policy.md`. Thumbnails and body images have different rules: thumbnails should usually be custom AI-made for the article, while body images must be copyright-safe, sourced, official, user-provided, or self-created.

## Naver Blog Visual Rhythm

For most posts:

1. Scene-first AI thumbnail or owned/licensed photo after the opening.
2. Evidence image, official crop, or explanatory diagram after the quick answer.
3. A process image showing the action at the decision point.
4. An outcome, aftercare, or remaining-caution scene later in the article.

Avoid placing too many similar images in a row.
Use no deterministic text card in a normal post. Keep checklists and comparisons in body text or a native editor table. A long post should read visually as a small editorial photo essay, not a presentation deck.

## Thumbnail Formula

Good thumbnail text is short and specific:

- Main keyword.
- Benefit or question.
- Time cue if relevant.

Examples:

- "온누리 20% 페이백 체크"
- "장마철 제습기 고르는 법"
- "부모님 선물 TOP 5"
- "삼성 행사 구매 전 확인"

Keep thumbnail text to 8 to 16 Korean characters when possible.
Prefer 4 to 10 Korean characters when a scene already carries the context.

If exact Korean text must appear in the thumbnail, prefer generating a text-free AI background and adding Korean text with a deterministic card/text overlay workflow. Do not deliver AI-rendered Korean text until it has been visually checked.

Never pass Korean card text inline through PowerShell or another shell command. Save the copy in a UTF-8 JSON specification, render with `create_visual_cards.py`, validate its sidecar, and then inspect the image pixels at original resolution.

## Scene-First Thumbnail

Build the thumbnail around:

- One recognizable reader situation.
- One focal subject with clean surrounding space.
- Natural Korean context where relevant: family travel planning, a humid laundry room, a campsite setup, or a shopping comparison moment.
- Bright, believable light and realistic object proportions.
- Central safe space for an optional short overlay.

Avoid flat presentation-card backgrounds, floating icons, fake app screens, random Korean letters, and generic stock-photo poses.

Require physically coherent weather and light. Reject sunny scenes with added rain streaks, exaggerated HDR, cinematic haze, perfect object alignment, duplicated gear, and plastic-looking surfaces.

When an AI scene is generated, inspect hands, object geometry, logos, labels, reflections, and background text before adding an overlay.

## Visual Types

Use:

- AI-created topic thumbnails.
- Event summary cards.
- Benefit calculation cards.
- TOP 5 comparison tables.
- Buyer checklist images.
- Step-by-step process images.
- Copyright-safe body images from official, licensed, user-provided, or self-created sources.
- Product category collages only when product images are allowed and sourced appropriately.

Avoid:

- Misleading before/after images.
- Fake official-looking badges.
- Crowded text-heavy thumbnails.
- Images copied from other bloggers.
- Unsourced product/news images.

## Image Prompt Pattern

When generating a custom image, use:

Use case:
Scene and action:
Camera and crop:
Weather and available light:
Natural texture and imperfection:
Aspect ratio:
Text to avoid:
Brand safety:

Example:

Use case: photorealistic-natural
Scene and action: a Korean reader comparing purchase conditions at a dining table
Camera and crop: candid eye-level 35mm editorial photograph, room for mobile crop
Weather and available light: soft window light appropriate to the time of day
Natural texture and imperfection: ordinary paper curl, used notebook, slightly uneven arrangement
Aspect ratio: 16:9
Text to avoid: all text and logos
Brand safety: no fake official seal, no misleading discount claim

## Accessibility And Trust

- Use readable contrast.
- Do not put critical conditions only inside an image.
- Repeat important dates and conditions in text.
- If using product screenshots, cite checked date in the draft notes.
- Add a short functional caption below each body image.
- Keep critical facts in body text even when a card repeats them.
