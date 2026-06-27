# Advanced Quality Gates

Use these gates before editor transfer. A failed mandatory gate blocks draft-save and public publishing.

## Content Intent Gate

Record an `intent_decision` object for every post:

- `action`: `new_post` or `update_existing`
- `reader_question`: the one concrete question answered by this post
- `duplicate_risk`: `low`, `medium`, or `high`
- `difference_note`: the new value compared with the closest existing post
- `cluster_key`: the durable topic family
- `cluster_role`: `pillar`, `event_update`, `buying_guide`, `mistake_faq`, `affiliate`, or `experience_report`
- `canonical_url`: required for `update_existing`
- `update_summary`: required for `update_existing`; state exactly what changed

Use `update_existing` when only a date, price, condition, or small factual detail changed. Do not publish a high-risk duplicate as a new post. The three daily posts must answer different reader questions.

## Internal Link Gate

Add zero to three genuinely related existing posts. Record each link with:

- `url`
- `anchor`
- `relevance`

Link a pillar to useful support posts and link support or affiliate posts back to the most relevant canonical guide. Do not force unrelated links. When no suitable post exists, record `internal_link_note` explaining the gap so it can become a future cluster task.

## Korean Editorial Gate

Run the final body through the package validator and a human read. Block:

- repeated long paragraphs,
- one formal sentence ending dominating most of a sufficiently long draft,
- repeated generic opening phrases,
- visible prompts, TODOs, internal notes, or tool-generation disclosures,
- a first visual that describes a different scene from the opening.

Set `naturalness_qa_confirmed: true` only after revising flagged text. Do not game the checker with random endings; improve the paragraph's function and rhythm.

## Original Photo Safety Gate

Use `original_photo` only when the image and supplied notes support a visit or hands-on claim. Use `owned_context_photo` for a user-owned scene that illustrates the topic but does not prove a visit, purchase, or product result.

Prepare either owned-photo role with `scripts/prepare_owned_photo.py`. For every owned photo, record:

- `ownership_basis`
- `privacy_qa_confirmed`
- `privacy_note`
- `location_metadata_removed`
- a matching `.privacy.json` sidecar whose hash matches the uploaded file

Inspect the full-resolution image for faces, children, vehicle plates, home numbers, receipts, screens, QR codes, school or workplace identifiers, and reflections. Crop, blur, or reject risky images. Strip GPS metadata before transfer. Reject burst frames and near-duplicate angles.

Automated checks can detect GPS metadata and visual similarity but cannot guarantee that all private details are absent. Manual original-resolution review remains mandatory.

Near-duplicate detection applies to selected user-owned photos, not diagrams or text cards. It combines structural similarity with resized pixel difference so visually distinct cards are not rejected as duplicate photos.

## Fact Freshness Gate

Record `fact_freshness` with `stable`, `current`, or `live` level, checked date, source records, and QA confirmation. Recheck current facts within 7 days and live facts within 1 day. Require an official, primary, or merchant source for current and live claims.

Remove risky title claims by default. If `완벽`, `무조건`, `역대`, `최저가`, `1위`, or `폭발` remains, record direct `title_claim_evidence` tied to a current source.

## Transfer Decision

Transfer only when all are true:

- intent action and canonical decision are valid,
- Korean editorial QA is confirmed,
- internal-link QA is confirmed,
- every original photo passes privacy and metadata checks,
- fact freshness and strong-title evidence pass,
- existing visual, disclosure, source, tag, and experience gates pass.

Record failed gates as `blocked`; do not silently downgrade them to warnings.
