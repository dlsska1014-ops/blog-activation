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
   - For each draft include title options, target reader, search intent, outline, body copy, image placement notes, tags, and draft-save checklist.

5. Prepare draft-save output:
   - Naver Blog: write with short paragraphs, generous spacing, scannable headings, image insertion notes, and natural Korean phrasing.
   - Tistory: adapt into a slightly more structured article with headings, tables, source notes, and SEO-friendly title/description.
   - Keep facts current by browsing when the topic involves dates, prices, laws, promotions, product rankings, or platform rules.

## Resources

- Read `references/editorial-playbook.md` before drafting posts.
- Read `references/platform-guidelines.md` when preparing Naver or Tistory draft-save formatting.
- Read `references/affiliate-guidelines.md` before writing Coupang Partners content.
- Read and update `references/style-memory.md` when the user asks to learn from current influencer posts or refresh the blog style.
- Use `scripts/create_daily_pack.py` to create a dated folder with three markdown draft templates and a research log.

## Editorial Rules

- Write original, helpful content. Do not scrape, reproduce, or spin other creators' posts.
- Avoid fake personal experience. If experience is not provided by the user, use neutral wording such as "구매 전 확인할 점" instead of pretending to have used a product.
- Make writing feel natural by varying sentence length, adding concrete reader questions, using everyday Korean, and placing light emoticons only where they fit the blog's tone.
- Do not overuse emoji, decorative punctuation, or exaggerated claims. Use them as seasoning, not structure.
- Add affiliate disclosure for Coupang Partners posts.
- For promotions, products, rankings, and news, cite or name the source basis and include the checked date in the draft notes.
- Keep publication mode as draft-only unless the user explicitly instructs otherwise.

## Output Format

For each daily run, return:

1. Daily topic board with selected three posts.
2. Source/research notes with dates checked.
3. Three complete draft packages.
4. Draft-save checklist for Naver Blog and optional Tistory adaptation.
5. Suggested updates for `style-memory.md` if new durable patterns were found.
