# Daily Operations

Use this runbook for daily blog operation.

## Contents

- Start-of-run research and topic selection
- Drafting and visual storyboard
- Draft-save or publication
- End-of-run and weekly improvement

## Morning Or Start-Of-Run

1. For unattended runs, read `autonomous-operations.md`, run `manage_autonomous_state.py begin`, obey its canary mode, and recover any prior `partial` or `unknown` action before starting new work.
2. Read `blog-profile.md`, `voice-guide.md`, and `style-memory.md`.
3. Read `evidence-and-experience-policy.md` and check whether the user supplied reusable photos or experience notes for a proven content pillar.
4. Review `content-calendar.md` for seasonal timing.
5. Read `daily-influencer-scan.md`.
6. Visit current Naver Blog examples for the day's target topic families.
7. Visit current Tistory examples for the day's target topic families.
8. Record abstract observations in `influencer-scan-log.md`.
9. Browse current factual sources from `research-sources.md`.
10. Classify each candidate's facts as `stable`, `current`, or `live` with `fact-freshness-policy.md`; reject stale or weak primary-source support.
11. Build 6 to 10 topic candidates and label each candidate's evidence basis.
12. Score candidates using the trend scoring method.
13. Assign each topic to a role from `keyword-clusters.md`.
14. Run `duplicate-intent-check.md`.
15. Use `content-portfolio-loop.md` to decide `new_post` or `update_existing`, record the canonical URL and update summary, and plan zero to three useful internal links.
16. Select:
   - One experience-backed post when authentic evidence exists; otherwise one information/news/event post.
   - One seasonal/search-demand post.
   - One Coupang Partners TOP 5 post.
17. Check `low-quality-prevention.md` before committing to three daily posts.
18. Compare the latest complete 7-day traffic window with the previous one when data is available.
19. If `traffic-recovery-mode.md` is triggered, create three candidates but select only one non-affiliate item for possible public publishing.

## Drafting

1. Choose the closest template from `post-templates.md`.
2. Record `experience_basis` and a privacy-safe evidence note before writing the opening.
3. Use `sample-bank.md` to vary the title, opening, and layout without copying real creators.
4. Use `writing-patterns-ko.md` for natural Korean title, first screen, and paragraph rhythm.
5. Use `editorial-presence-guide.md` to define the reader scene, editorial priority, truthful first-person moves, and practical closing.
6. Generate and score titles with `title-ab-testing.md`.
7. For Coupang Partners posts, score candidates with `affiliate-scoring.md`, check `affiliate-link-density.md`, and use `product-category-playbooks.md`.
8. Draft for Naver Blog first.
9. Apply `layout-spacing-guide.md` for spacing, section rhythm, and mobile readability.
10. Apply `emoji-emoticon-guide.md` only where tone fits.
11. Add source notes and checked dates.
12. Record `fact_freshness`; remove strong title claims unless direct evidence is recorded.
13. Read `visual-asset-policy.md` and create a visual storyboard before generating any image.
14. Use the strongest user-owned scene photo first when available. Use `original_photo` only for supported experience and `owned_context_photo` for neutral context. Prepare either with `prepare_owned_photo.py`.
15. Prepare body images that match the section content using copyright-safe sources:
   - official/source screenshots with checked-date notes,
   - licensed/free-use images with source and license notes,
   - user-provided images,
   - self-created summary, checklist, comparison, or diagram cards.
16. Add image paths, roles, captions, source/copyright notes, and placement notes directly into each draft.
17. For posts of at least 1,800 characters, require four visuals, three distinct roles, and no more than two text cards.
18. Use `image-thumbnail-guide.md` and `visual-prompt-library.md` to refine visual rhythm and prompts.
19. Run `naturalness-editor.md` as the final rewrite pass.
20. Run `editorial-authenticity-gate.md` as an independent read and record the five answers.
21. Run `check_editorial_reuse.py` against recent owned post bodies and revise excessive phrase reuse.
22. Use `advanced-quality-gates.md` to confirm content intent, fact freshness, internal links, Korean editorial quality, and owned-photo privacy.
23. Score with `quality-rubric.md`.
24. Check low-quality risk with `low-quality-prevention.md`.
25. Check publishing risk with `publish-risk-checklist.md`.
26. Revise anything under 31/40 or with a failed mandatory gate.
27. Prepare optional Tistory adaptation.

## Draft-Save

Default to draft-only.

When browser automation is used:

1. Follow `live-publish-runbook.md` and the platform runbook.
2. Record the current run contract, including the latest explicit draft/publish instruction.
3. Validate the prepared package with `validate_publish_package.py`.
4. For unattended runs, run `decide_autonomous_run.py` with the daily plan and receipt history.
5. Open a new post and insert clean plain text, tags, the scene-first thumbnail, and copyright-safe body images in manifest order.
6. Verify the editor image count and scan for raw Markdown or placeholders.
7. Publish only the selected candidate; draft-save other eligible candidates.
8. Verify the resulting state and record a platform-specific receipt before any retry.
9. Write and validate `editor-verification.json`, including image positions, captions, representative image, tags, and final state.
10. For Tistory, follow `tistory-publish-runbook.md` and use the adapted body rather than pasting the Naver version unchanged.
11. Run `manage_autonomous_state.py finish` only after all receipts and verification files are complete.

Do not report success from a click alone. Report only verified results and label partial or unknown outcomes honestly.

Before any GitHub upload or saved automation artifact, follow `secret-handling.md`.

## End-Of-Run

1. Summarize the three draft packages.
2. List AI thumbnail prompts or generated thumbnail paths.
3. List body image sources, copyright-safety notes, and uncertainties.
4. List image roles and final captions in editor order.
5. Report each post's experience basis and whether firsthand language was allowed.
6. Suggest style-memory updates.
7. Record expected experiment in `performance-log.md` if the post is published later.
8. Keep any style-memory update separate from raw scan notes; update only durable patterns.
9. Record each platform as verified, partial, blocked, or unknown with URL/draft state and image count.
10. Schedule evidence collection at roughly 24 hours, 72 hours, and 7 days when metrics are available; never invent unavailable values.
11. Record the single experiment variable and canonical/internal-link decision for later comparison.

## Weekly Improvement

Once per week:

1. Review actual performance.
2. Identify winning title patterns.
3. Identify weak openings.
4. Update `style-memory.md`.
5. Fill `weekly-report-template.md`.
6. Update templates only if a pattern repeats across multiple posts.
7. Compare equal-age windows and identify which exact inflow questions produced visits.
8. Adjust the next week's content mix toward proven clusters before adding new categories.
9. Use `content-portfolio-loop.md` to consolidate duplicates, strengthen orphan posts, and preserve canonical URLs.

When the user provides metrics, use `performance-input.md` before updating `performance-log.md`.

When the user asks why exposure is weak, use `search-exposure-check.md` and avoid assuming a single cause.

When rewriting published posts, use `rewrite-rules.md`.

When the user provides CSV performance data, use `operations-data-schema.md` and `analyze_performance_csv.py`.

When testing a new title, layout, thumbnail, or affiliate approach, record it in `experiment-log.md`.

When a post performs unusually well or poorly, review it with `post-mortem-review.md`.
