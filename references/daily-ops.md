# Daily Operations

Use this runbook for daily blog operation.

## Morning Or Start-Of-Run

1. Read `blog-profile.md`, `voice-guide.md`, and `style-memory.md`.
2. Review `content-calendar.md` for seasonal timing.
3. Browse current sources from `research-sources.md`.
4. Build 6 to 10 topic candidates.
5. Score candidates using the trend scoring method.
6. Assign each topic to a role from `keyword-clusters.md`.
7. Run `duplicate-intent-check.md`.
8. Select:
   - One information/news/event post.
   - One seasonal/search-demand post.
   - One Coupang Partners TOP 5 post.
9. Check `low-quality-prevention.md` before committing to three daily posts.

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
10. Add image and thumbnail notes from `image-thumbnail-guide.md` and `visual-prompt-library.md`.
11. Run `naturalness-editor.md` as the final rewrite pass.
12. Score with `quality-rubric.md`.
13. Check low-quality risk with `low-quality-prevention.md`.
14. Check publishing risk with `publish-risk-checklist.md`.
15. Revise anything under 22/30 or with elevated low-quality risk.
16. Prepare optional Tistory adaptation.

## Draft-Save

Default to draft-only.

When browser automation is used:

1. Follow `naver-draft-runbook.md`.
2. Open the target platform.
3. Create a new post.
4. Insert title, body, tags, and image placeholders.
5. Save as draft.
6. Stop before publishing.

Ask for confirmation before any public publish action.

Before any GitHub upload or saved automation artifact, follow `secret-handling.md`.

## End-Of-Run

1. Summarize the three draft packages.
2. List source checks and uncertainties.
3. Suggest style-memory updates.
4. Record expected experiment in `performance-log.md` if the post is published later.

## Weekly Improvement

Once per week:

1. Review actual performance.
2. Identify winning title patterns.
3. Identify weak openings.
4. Update `style-memory.md`.
5. Fill `weekly-report-template.md`.
6. Update templates only if a pattern repeats across multiple posts.

When the user provides metrics, use `performance-input.md` before updating `performance-log.md`.

When the user asks why exposure is weak, use `search-exposure-check.md` and avoid assuming a single cause.

When rewriting published posts, use `rewrite-rules.md`.

When the user provides CSV performance data, use `operations-data-schema.md` and `analyze_performance_csv.py`.

When testing a new title, layout, thumbnail, or affiliate approach, record it in `experiment-log.md`.

When a post performs unusually well or poorly, review it with `post-mortem-review.md`.
