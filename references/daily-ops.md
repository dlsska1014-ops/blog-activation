# Daily Operations

Use this runbook for daily blog operation.

## Morning Or Start-Of-Run

1. Read `blog-profile.md`, `voice-guide.md`, and `style-memory.md`.
2. Review `content-calendar.md` for seasonal timing.
3. Read `daily-influencer-scan.md`.
4. Visit current Naver Blog examples for the day's target topic families.
5. Visit current Tistory examples for the day's target topic families.
6. Record abstract observations in `influencer-scan-log.md`.
7. Browse current factual sources from `research-sources.md`.
8. Build 6 to 10 topic candidates.
9. Score candidates using the trend scoring method.
10. Assign each topic to a role from `keyword-clusters.md`.
11. Run `duplicate-intent-check.md`.
12. Select:
   - One information/news/event post.
   - One seasonal/search-demand post.
   - One Coupang Partners TOP 5 post.
13. Check `low-quality-prevention.md` before committing to three daily posts.
14. Compare the latest complete 7-day traffic window with the previous one when data is available.
15. If `traffic-recovery-mode.md` is triggered, create three candidates but select only one for public publishing.

## Drafting

1. Choose the closest template from `post-templates.md`.
2. Use `sample-bank.md` to vary the title, opening, and layout without copying real creators.
3. Use `writing-patterns-ko.md` for natural Korean title, first screen, and paragraph rhythm.
4. Generate and score titles with `title-ab-testing.md`.
5. For Coupang Partners posts, score candidates with `affiliate-scoring.md`, check `affiliate-link-density.md`, and use `product-category-playbooks.md`.
6. Draft for Naver Blog first.
7. Apply `layout-spacing-guide.md` for spacing, section rhythm, and mobile readability.
8. Apply `emoji-emoticon-guide.md` only where tone fits.
9. Add source notes and checked dates.
10. Read `visual-asset-policy.md`.
11. Prepare a custom AI thumbnail concept or generated thumbnail for each post based on the final draft topic and opening.
12. Prepare body images that match the section content using copyright-safe sources:
   - official/source screenshots with checked-date notes,
   - licensed/free-use images with source and license notes,
   - user-provided images,
   - self-created summary, checklist, comparison, or diagram cards.
13. Add image paths, source/copyright notes, and placement notes directly into each draft.
14. Use `image-thumbnail-guide.md` and `visual-prompt-library.md` to refine visual rhythm and prompts.
15. Run `naturalness-editor.md` as the final rewrite pass.
16. Score with `quality-rubric.md`.
17. Check low-quality risk with `low-quality-prevention.md`.
18. Check publishing risk with `publish-risk-checklist.md`.
19. Revise anything under 22/30 or with elevated low-quality risk.
20. Prepare optional Tistory adaptation.

## Draft-Save

Default to draft-only.

When browser automation is used:

1. Follow `live-publish-runbook.md` and the platform runbook.
2. Record the current run contract, including the latest explicit draft/publish instruction.
3. Validate the prepared package with `validate_publish_package.py`.
4. Open a new post and insert clean plain text, tags, generated thumbnail, and copyright-safe body images.
5. Verify the editor image count and scan for raw Markdown or placeholders.
6. Save or publish according to the approved mode.
7. Verify the resulting state and record a platform-specific receipt.
8. For Tistory, follow `tistory-publish-runbook.md` and use the adapted body rather than pasting the Naver version unchanged.

Do not report success from a click alone. Report only verified results and label partial or unknown outcomes honestly.

Before any GitHub upload or saved automation artifact, follow `secret-handling.md`.

## End-Of-Run

1. Summarize the three draft packages.
2. List AI thumbnail prompts or generated thumbnail paths.
3. List body image sources, copyright-safety notes, and uncertainties.
4. Suggest style-memory updates.
5. Record expected experiment in `performance-log.md` if the post is published later.
6. Keep any style-memory update separate from raw scan notes; update only durable patterns.
7. Record each platform as verified, partial, blocked, or unknown with URL/draft state and image count.
8. Schedule evidence collection at roughly 24 hours, 72 hours, and 7 days when metrics are available; never invent unavailable values.

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

When the user provides metrics, use `performance-input.md` before updating `performance-log.md`.

When the user asks why exposure is weak, use `search-exposure-check.md` and avoid assuming a single cause.

When rewriting published posts, use `rewrite-rules.md`.

When the user provides CSV performance data, use `operations-data-schema.md` and `analyze_performance_csv.py`.

When testing a new title, layout, thumbnail, or affiliate approach, record it in `experiment-log.md`.

When a post performs unusually well or poorly, review it with `post-mortem-review.md`.

