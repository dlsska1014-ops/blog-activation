# Visual Quality Standard

Use this after the visual storyboard and before generating, downloading, rendering, or uploading assets. The target is an editorial blog rhythm led by believable photography, not a deck of generated cards.

## Default Four-Scene Storyboard

For a long information or seasonal post, prefer:

1. `context`: a wide scene showing the reader's actual situation near the opening.
2. `problem`: a closer detail showing what is wrong, risky, confusing, or worth checking.
3. `action`: a medium or close process scene showing the practical response described in the article.
4. `outcome`: a later scene showing the safe result, aftercare, comparison condition, or remaining caution without a misleading before/after claim.

Use at least three photographic visuals and at least two non-AI origins. Text cards are disabled by default. Put checklists, rankings, and decision criteria in the body text or a native editor table unless a data-heavy exception is documented.

For affiliate posts, prefer merchant-authorized product images plus real category context. Do not generate fake versions of recognizable products or interfaces.

## Photographic Realism

Every photographic visual must pass:

- weather and light agree across the entire frame,
- equipment, hands, furniture, buildings, reflections, and shadows have plausible geometry,
- surfaces retain ordinary wear, wrinkles, moisture, dust, or texture instead of plastic smoothness,
- the composition looks observed rather than perfectly staged or symmetrically arranged,
- no random writing, labels, logos, duplicated objects, or impossible controls appear,
- the scene matches the nearby paragraph and does not imply a real visit, product test, or official event when it is only illustrative.

Never add synthetic rain, snow, crowds, smoke, damage, or product results over a licensed or owned photograph. Cropping, exposure, color correction, and privacy-safe redaction are acceptable; changing the factual scene is not.

## Natural AI Scene Prompt

Use AI only when a suitable owned or clearly licensed photograph is unavailable. Use no more than two AI scenes in a normal long post, generate at least two independent candidates for each scene, and select after original-resolution review. Keep the people, location type, weather, equipment family, and color treatment consistent across related AI scenes without pretending they document one real visit.

Prompt structure:

```text
Use case: photorealistic-natural
Asset type: Korean editorial blog scene
Scene: the exact reader situation and physically consistent weather
Subject: one practical action, with plausible objects and proportions
Camera: eye-level or documentary angle, 35mm or 50mm look, moderate depth of field
Light: available natural light appropriate to the stated time and weather
Texture: ordinary wear, fabric wrinkles, moisture, imperfect arrangement
Composition: candid and useful, not centered like an advertisement; room for mobile crop
Text: none
Constraints: no brand marks, no identifiable faces, no fake interface, no dramatic effects
Avoid: synthetic rain streaks, HDR glow, perfect symmetry, plastic surfaces, duplicated gear, random labels, stock-photo gestures, cinematic spectacle
```

Do not add title text during image generation. Text-free thumbnails are the default. Add a short deterministic overlay only when the scene cannot communicate the topic by itself.

## Card And Diagram Standard

- Default to no card.
- Set `allow_text_card: true` and record `text_card_exception` only when a compact visual comparison is materially clearer than body text or a native editor table.
- Use a card only when it reduces a real decision to a small number of conditions.
- Keep one headline, up to three short rows or bullets, and generous margins.
- Avoid thick title bars, footer bars, giant headings, nested panels, decorative icons, and template colors repeated across posts.
- Use a neutral editorial layout with a small accent, readable Korean, and no more than 25 percent text coverage.
- Prefer a photographed process, annotated source crop, or simple diagram when the same point can be shown rather than written again.
- A diagram must use believable scale, direction, and labels. Reject clip-art shapes that look like a children's worksheet unless that style is intentional for the audience.

## Sequence And Placement

- Place the hero within the first 20 percent of body text.
- Place at least one visual between 25 and 60 percent and another after 60 percent for long posts.
- Keep at least one meaningful paragraph between visuals unless two images form a deliberate before/after or comparison pair.
- Use varied crops and distances: wide scene, medium process, close detail, decision aid.
- Captions should explain what the reader should notice, not repeat the filename or heading.

## Manifest Fields

For every visual record:

- `origin`: `owned`, `licensed`, `official`, `merchant`, `ai_generated`, or `self_created`
- `purpose`
- `story_role`: `context`, `problem`, `action`, `evidence`, or `outcome`
- `section_anchor`
- `placement_ratio`: number from 0 to 1
- `opened_original_resolution`
- `candidate_count`: required for AI-generated visuals
- `text_density`: required for text cards
- `template_reuse`: required for text cards
- `quality_checks`: the applicable realism and polish checks

Run `scripts/validate_visual_storyboard.py` before editor transfer. Set `visual_qa_confirmed: true` only after it passes and every selected file has been visually inspected.
