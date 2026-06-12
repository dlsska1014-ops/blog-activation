---
name: blog-activation
description: Plan, research, draft, and prepare daily Korean blog posts for Naver Blog first and Tistory second, including trend/news explainers, seasonal search topics, event-shopping guides, and Coupang Partners TOP 5 recommendation posts. Use when the user asks to operate or grow a Korean blog, analyze high-performing Naver/Tistory influencer posts, create reader-focused drafts, prepare posts as drafts rather than publishing, or update blog writing/style memory from recent Korean blog trends.
---

# Blog Activation

## Overview

Use this skill to run a daily Korean blog content workflow: research current topics, learn durable writing/layout patterns from high-performing Naver Blog and Tistory posts, draft three posts, and prepare them for draft-save in the user's blogs. Prioritize Naver Blog output; adapt to Tistory only after the Naver draft is complete.

Do not copy or closely paraphrase other blog posts. Use public sources to understand reader intent, then write original posts with clear source attribution where facts, prices, events, or policies matter.

## Workflow

1. Confirm the run mode:
   - Default to `draft-only`: prepare posts for blog draft-save, not public publishing.
   - Treat `auto-publish` as disabled unless the user explicitly enables it after stabilization.
   - If login, browser automation, affiliate links, or live posting are involved, confirm the target account and action before modifying live content.

2. Build the daily topic board:
   - Read `references/blog-profile.md`, `references/voice-guide.md`, and `references/style-memory.md` before choosing topics.
   - Use `references/research-sources.md` to decide where to check current sources.
   - Find current Korean search/trend/news topics relevant to consumer decisions, seasonal needs, public benefits, electronics, household goods, finance-lite explainers, local events, and practical how-to information.
   - Include one Coupang Partners candidate topic for a TOP 5 recommendation post.
   - Prefer topics where readers have urgent questions: eligibility, dates, price/value, steps, comparison, risk, best picks, or "what should I buy/do now?"

3. Learn from high-performing blog examples:
   - Review recent Naver Blog first, then Tistory examples for similar topics.
   - Extract reusable patterns only: title hooks, opening rhythm, spacing, section order, image placement ideas, table use, comparison blocks, conclusion style, and comment-inducing questions.
   - Do not imitate a specific creator's unique voice, personal claims, photos, or proprietary structure.
   - Update `references/style-memory.md` only with durable patterns that can be reused across posts.

4. Create three daily drafts:
   - Draft 1: information/news explainer based on current issue or event.
   - Draft 2: seasonal or search-demand post matched to the blog theme.
   - Draft 3: Coupang Partners TOP 5 post, selected for seasonal demand, buyer intent, likely order value, and practical usefulness.
   - Use the closest structure from `references/post-templates.md`.
   - Use `references/sample-bank.md` for synthetic title, opening, section, and layout variations.
   - Use `references/affiliate-scoring.md` before selecting Coupang Partners products.
   - For each draft include title options, target reader, search intent, outline, body copy, image placement notes, tags, and draft-save checklist.

5. Prepare draft-save output:
   - Naver Blog: write with short paragraphs, generous spacing, scannable headings, image insertion notes, and natural Korean phrasing.
   - Tistory: adapt into a slightly more structured article with headings, tables, source notes, and SEO-friendly title/description.
   - Keep facts current by browsing when the topic involves dates, prices, laws, promotions, product rankings, or platform rules.
   - Score drafts with `references/quality-rubric.md` and revise posts below the threshold.
   - Use `references/image-thumbnail-guide.md` to plan thumbnails, summary cards, comparison images, and checklist images.
   - Use `references/naver-draft-runbook.md` if the user asks to place content into Naver Blog as a draft.
   - Use `references/publish-risk-checklist.md` and `references/low-quality-prevention.md` before draft-save or public publishing.

6. Improve the system:
   - Use `references/daily-ops.md` as the runbook for daily execution.
   - Use `references/performance-log.md` to record actual results when the user provides views, keywords, clicks, or conversion data.
   - Use `references/performance-input.md` when the user provides post results, search inflow, clicks, comments, or conversion data.
   - Use `references/weekly-report-template.md` after seven daily runs or whenever the user asks for a performance review.
   - Update style memory only when a lesson is reusable and supported by repeated observation or real performance.

## Resources

- Read `references/blog-profile.md` to keep the blog's niche, audience, and editorial stance consistent.
- Read `references/voice-guide.md` before writing or revising Korean blog copy.
- Read `references/research-sources.md` before topic research.
- Read `references/secret-handling.md` whenever credentials, cookies, affiliate account data, or private account information may appear.
- Read `references/editorial-playbook.md` before drafting posts.
- Read `references/platform-guidelines.md` when preparing Naver or Tistory draft-save formatting.
- Read `references/affiliate-guidelines.md` before writing Coupang Partners content.
- Read `references/affiliate-scoring.md` before choosing affiliate product categories or TOP 5 products.
- Read `references/image-thumbnail-guide.md` when planning visual assets, thumbnail text, image prompts, or in-post image rhythm.
- Read `references/naver-draft-runbook.md` when preparing or automating Naver Blog draft-save.
- Read `references/post-templates.md` to select the correct article structure.
- Read `references/quality-rubric.md` before final delivery.
- Read `references/publish-risk-checklist.md` before publishing, draft-save, or final delivery of sensitive/time-sensitive posts.
- Read `references/low-quality-prevention.md` before creating multiple daily posts, affiliate-heavy posts, or posts that target similar keywords.
- Read `references/sample-bank.md` to vary titles, openings, closings, and layout patterns without copying other creators.
- Read `references/daily-ops.md` for a complete daily operating runbook.
- Read `references/performance-log.md` when reviewing published results or improving future topic selection.
- Read `references/performance-input.md` when converting real performance data into next actions.
- Read `references/weekly-report-template.md` for weekly performance summaries.
- Read and update `references/style-memory.md` when the user asks to learn from current influencer posts or refresh the blog style.
- Use `scripts/create_daily_pack.py` to create a dated folder with three markdown draft templates and a research log.
- Use `scripts/simulate_daily_strategy.py` to test topic selection and output structure against synthetic scenarios before major skill updates.
- Use `scripts/scan_sensitive_terms.py` before uploading skill changes to GitHub when any account, automation, affiliate, or browser-login work was discussed.

## Editorial Rules

- Write original, helpful content. Do not scrape, reproduce, or spin other creators' posts.
- Avoid fake personal experience. If experience is not provided by the user, use neutral wording such as "구매 전 확인할 점" instead of pretending to have used a product.
- Make writing feel natural by varying sentence length, adding concrete reader questions, using everyday Korean, and placing light emoticons only where they fit the blog's tone.
- Do not overuse emoji, decorative punctuation, or exaggerated claims. Use them as seasoning, not structure.
- Add affiliate disclosure for Coupang Partners posts.
- For promotions, products, rankings, and news, cite or name the source basis and include the checked date in the draft notes.
- Do not store credentials, cookies, tokens, private affiliate dashboard data, or account-specific secrets in GitHub or skill files.
- Avoid thin, duplicate, keyword-stuffed, or affiliate-heavy posts that do not add original reader value.
- Keep publication mode as draft-only unless the user explicitly instructs otherwise.

## Output Format

For each daily run, return:

1. Daily topic board with selected three posts.
2. Source/research notes with dates checked.
3. Three complete draft packages.
4. Draft-save checklist for Naver Blog and optional Tistory adaptation.
5. Suggested updates for `style-memory.md` if new durable patterns were found.
