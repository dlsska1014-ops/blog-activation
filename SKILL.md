---
name: blog-activation
description: Plan, research, visually storyboard, draft, and publish or draft-save daily Korean blog posts for Naver Blog first and Tistory second, including trend/news explainers, seasonal search topics, event-shopping guides, and Coupang Partners TOP 5 posts. Use when the user asks to operate or grow a Korean blog, learn original reusable patterns from current high-performing Naver Blog and Tistory posts, create natural influencer-quality writing without copying or fake experience, improve thumbnails/body images, automate editor transfer, or update blog style memory.
---

# Blog Activation

## Overview

Use this skill to run a daily Korean blog content workflow: research current topics, learn durable writing/layout patterns from high-performing Naver Blog and Tistory posts, draft three posts, and prepare them for draft-save in the user's blogs. Prioritize Naver Blog output; adapt to Tistory only after the Naver draft is complete.

Do not copy or closely paraphrase other blog posts. Use public sources to understand reader intent, then write original posts with clear source attribution where facts, prices, events, or policies matter.

## Workflow

1. Confirm the run mode:
   - Default to `draft-only` when no publication instruction exists.
   - Honor the latest explicit `draft-only` or `auto-publish` instruction for the current batch; do not repeatedly reconfirm every post in an already approved batch.
   - For browser transfer, record the target account, platform, post count, image count, affiliate status, and mode without storing login/session data.
   - For unattended or recurring runs, read `references/autonomous-operations.md` and create a persisted run id, state, publication budget, and fail-closed contract before research.
   - Run `scripts/manage_autonomous_state.py begin` before research. Obey its `effective_mode`; the first three verified unattended runs are always `draft-only` canaries.

2. Build the daily topic board:
   - Read `references/blog-profile.md`, `references/voice-guide.md`, and `references/style-memory.md` before choosing topics.
   - Read `references/evidence-and-experience-policy.md` and identify whether reusable user-owned photos or user-provided experience notes exist.
   - Use `references/research-sources.md` to decide where to check current sources.
   - Use `references/daily-topic-gate.md` to reject weak topics before drafting.
   - Use `references/reader-intent-map.md` to match each topic to the correct structure.
   - Use `references/content-calendar.md` for seasonal planning and `references/keyword-clusters.md` to assign each topic a cluster role.
   - Use `references/duplicate-intent-check.md` to reject posts that overlap recent reader intent.
   - Use `references/content-portfolio-loop.md` to decide `new_post` or `update_existing`, preserve canonical URLs, and plan useful internal links before drafting.
   - Read `references/traffic-recovery-mode.md` when recent traffic falls or public defects exist. Continue planning three candidates, but publish at most one verified Naver post per day while recovery mode is active.
   - Find current topics inside the active `blog-profile.md` pillars first. Expand into an unrelated category only when the blog's own data or a clearly adjacent reader need supports it.
   - Include one Coupang Partners candidate topic for a TOP 5 recommendation post.
   - During recovery mode, treat the affiliate topic as a candidate or draft rather than a mandatory daily publication, and limit affiliate-first publishing to two posts per week.
   - Prefer topics where readers have urgent questions: eligibility, dates, price/value, steps, comparison, risk, best picks, or "what should I buy/do now?"
   - When authentic user evidence exists, prioritize one photo-backed place, facility, camping, or product-use candidate over a broad generic explainer.
   - When it does not exist, keep the package `research_only`; never imitate a visit or hands-on review.

3. Learn from high-performing blog examples:
   - Read `references/daily-influencer-scan.md` before observing current examples.
   - Visit recent high-performing Naver Blog posts first through Naver Blog, Naver blog search, and Naver search result blog/popular-content blocks.
   - Visit recent high-performing Tistory posts through Tistory site pages, Tistory search/category paths when available, and search results scoped to `site:tistory.com`.
   - Extract reusable patterns only: title hooks, opening rhythm, spacing, section order, image placement ideas, table use, comparison blocks, conclusion style, and comment-inducing questions.
   - Do not imitate a specific creator's unique voice, personal claims, photos, or proprietary structure.
   - Use `references/influencer-style-learning.md` to convert observations into abstract, reusable style lessons.
   - Use `references/editorial-presence-guide.md` to convert those lessons into an original reader scene, editorial priority, visual proof, and practical close.
   - Record observations in `references/influencer-scan-log.md` as abstract pattern notes, not copied text.
   - Update `references/style-memory.md` only with durable patterns that appear repeatedly or are supported by real performance.

4. Create three daily drafts:
   - Draft 1: experience-backed place/camping/use post when authentic evidence exists; otherwise an information/news explainer.
   - Draft 2: seasonal or search-demand post matched to the blog theme.
   - Draft 3: Coupang Partners TOP 5 post, selected for seasonal demand, buyer intent, likely order value, and practical usefulness.
   - Use the closest structure from `references/post-templates.md`.
   - Use `references/sample-bank.md` for synthetic title, opening, section, and layout variations.
   - Use `references/writing-patterns-ko.md` for natural Korean first-screen, paragraph rhythm, title, and closing patterns.
   - Use `references/editorial-presence-guide.md` to add truthful editorial presence without inventing personal use or visits.
   - Use `references/evidence-and-experience-policy.md` to label observed, official, inferred, and recommended content correctly.
   - Use `references/layout-spacing-guide.md`, `references/emoji-emoticon-guide.md`, and `references/naturalness-editor.md` for final Naver Blog editing.
   - Use `references/editorial-authenticity-gate.md` for an independent paragraph-function and specificity pass. Improve genuine editorial value; never optimize for AI-detector evasion.
   - Run `scripts/check_editorial_reuse.py` against recent owned drafts and published bodies. Block excessive phrase reuse even when the current draft is otherwise original.
   - Use `references/advanced-quality-gates.md` to record the intent decision, Korean editorial QA, internal-link QA, and original-photo privacy state.
   - Use `references/trust-language-filter.md` to remove overclaims, fake experience, and unsupported certainty.
   - Use `references/fact-freshness-policy.md` when the post depends on current facts.
   - Record `stable`, `current`, or `live` fact freshness for every package; remove unsupported strong title claims.
   - Use `references/title-ab-testing.md` to score title candidates before draft-save.
   - Use `references/monetization-strategy.md` to separate traffic, trust, and conversion goals before choosing revenue topics.
   - Use `references/affiliate-scoring.md` before selecting Coupang Partners products.
   - Use `references/affiliate-link-density.md` to keep affiliate link count and weekly ratio trust-first.
   - Use `scripts/score_revenue_topics.py` when the user provides a CSV of revenue topic candidates.
   - Use `references/product-category-playbooks.md` for recurring product categories.
   - For each draft include title options, target reader, search intent, outline, body copy, image placement notes, tags, and draft-save checklist.

5. Prepare draft-save output:
   - Naver Blog: write with short paragraphs, generous spacing, scannable headings, image insertion notes, and natural Korean phrasing.
   - Tistory: adapt into a slightly more structured article with headings, tables, source notes, and SEO-friendly title/description.
   - Keep facts current by browsing when the topic involves dates, prices, laws, promotions, product rankings, or platform rules.
   - Score drafts with `references/quality-rubric.md` and revise posts below the threshold.
   - Use `references/visual-asset-policy.md` before preparing images. Prefer a strong user-owned hero photo; use a scene-first AI thumbnail only when authentic scene evidence is unavailable, then mix copyright-safe evidence, explanation, and decision-aid visuals.
   - For posts of 1,800 characters or more, require at least four visuals, three distinct roles, a non-card first visual, and no more than two text cards.
   - Record each visual's path, role, caption, text status, visual-QA result, and source/reuse notes in the publish manifest.
   - Use `scripts/prepare_owned_photo.py` for every user-owned image. Use `original_photo` for supported experience evidence and `owned_context_photo` for neutral research-only context.
   - Inspect private details at full resolution, confirm the privacy sidecar, and reject burst or near-duplicate owned-photo frames.
   - Use `references/image-thumbnail-guide.md` to plan thumbnails, summary cards, comparison images, and checklist images.
   - Use `references/visual-prompt-library.md` when generating thumbnail, summary card, checklist, or comparison image prompts.
   - Use `references/visual-text-integrity.md` for every Korean text-bearing image. Keep Korean copy in UTF-8 files, reject repeated question marks, and visually inspect original-resolution pixels.
   - Use `references/naver-draft-runbook.md` if the user asks to place content into Naver Blog as a draft.
   - Use `references/live-publish-runbook.md` for every browser-based draft-save or public publishing run.
   - Use `references/tistory-publish-runbook.md` when Tistory is included; adapt structure, metadata, image alt text, and category instead of pasting the Naver body unchanged.
   - Run `scripts/validate_publish_package.py` before editor transfer when a package manifest is available.
   - For unattended runs, run `scripts/decide_autonomous_run.py` after package validation. Publicly publish at most the selected item and draft-save other eligible items.
   - Read `references/unattended-editor-verification.md`, write `editor-verification.json`, and run `scripts/validate_editor_verification.py` before recording success.
   - Treat failures from intent, fact freshness, strong-title evidence, naturalness, internal links, owned-photo privacy, sidecar integrity, GPS, or near-duplicate-image checks as publication blockers.
   - Use `references/publish-risk-checklist.md` and `references/low-quality-prevention.md` before draft-save or public publishing.
   - Block the final action unless the editor image count, clean body text, tags, disclosure, and intended mode are verified.
   - After the final action, verify the URL or draft state and report each platform separately as verified, partial, blocked, or unknown.
   - Use `references/published-post-audit.md` to inspect public text, first/middle/last images, and recent-list duplication before reporting success.
   - Record results with `scripts/record_publication_receipt.py` and refuse an accidental second verified action for the same platform and content fingerprint.
   - Finish unattended state only after receipts are written. Two consecutive partial, blocked, unknown, or incomplete canary results pause the scheduler state.

6. Improve the system:
   - Use `references/daily-ops.md` as the runbook for daily execution.
   - Use `references/performance-log.md` to record actual results when the user provides views, keywords, clicks, or conversion data.
   - Use `references/performance-input.md` when the user provides post results, search inflow, clicks, comments, or conversion data.
   - Use `references/search-exposure-check.md` after publication when the user asks to inspect indexing, search inflow, or weak exposure.
   - Use `references/rewrite-rules.md` when improving old posts or reacting to weak exposure/click/conversion signals.
   - Use `references/experiment-log.md` to define controlled writing, layout, title, image, and affiliate experiments.
   - Use `references/post-mortem-review.md` when a post performs unusually well or poorly.
   - Use `references/operations-data-schema.md` and `scripts/analyze_performance_csv.py` when the user provides CSV performance data.
   - Use `references/weekly-report-template.md` after seven daily runs or whenever the user asks for a performance review.
   - Update style memory only when a lesson is reusable and supported by repeated observation or real performance.
   - When metrics are available, compare performance at consistent 24-hour, 72-hour, and 7-day windows before changing strategy.
   - Use the blog's own winning posts and inflow queries to update `blog-profile.md`, `style-memory.md`, and future topic scores.
   - Use `references/content-portfolio-loop.md` to compare equal-age results, change one major experiment variable at a time, consolidate duplicates, and strengthen orphan posts.
   - Use publication receipts as the only source of truth for autonomous retries. Never infer success from a click, timeout, or missing browser response.

## Resources

- Read `references/blog-profile.md` to keep the blog's niche, audience, and editorial stance consistent.
- Read `references/evidence-and-experience-policy.md` before topic selection and whenever a draft may contain first-person visits, product use, owned photos, or sponsorship.
- Read `references/voice-guide.md` before writing or revising Korean blog copy.
- Read `references/research-sources.md` before topic research.
- Read `references/daily-topic-gate.md` before selecting daily topics.
- Read `references/reader-intent-map.md` before outlining each post.
- Read `references/official-source-notes.md` when summarizing Naver exposure or affiliate disclosure principles.
- Read `references/secret-handling.md` whenever credentials, cookies, affiliate account data, or private account information may appear.
- Read `references/editorial-playbook.md` before drafting posts.
- Read `references/platform-guidelines.md` when preparing Naver or Tistory draft-save formatting.
- Read `references/layout-spacing-guide.md` when preparing Naver Blog body spacing, section rhythm, and mobile readability.
- Read `references/emoji-emoticon-guide.md` before using emoji, emoticons, or visual markers.
- Read `references/daily-influencer-scan.md` before visiting current Naver Blog or Tistory examples for style learning.
- Read `references/influencer-style-learning.md` when learning from high-performing blog posts.
- Read `references/editorial-presence-guide.md` before the final rewrite when the post should feel human-edited or influencer-quality without copying.
- Read and update `references/influencer-scan-log.md` after each daily observation pass.
- Read `references/naturalness-editor.md` for the final natural Korean rewrite pass.
- Read `references/editorial-authenticity-gate.md` before setting editorial QA complete.
- Read `references/autonomous-operations.md` for recurring, unattended, or auto-publish runs.
- Read `references/unattended-editor-verification.md` for account, image placement, caption, and final-state evidence in unattended runs.
- Read `references/trust-language-filter.md` before finalizing recommendations, affiliate sections, and benefit claims.
- Read `references/fact-freshness-policy.md` before drafting time-sensitive or source-dependent posts.
- Read `references/content-calendar.md` for monthly, weekly, and seasonal planning.
- Read `references/keyword-clusters.md` to build pillar/support/affiliate topic clusters without duplication.
- Read `references/duplicate-intent-check.md` before drafting posts that resemble recent topics.
- Read `references/content-portfolio-loop.md` before deciding whether to create a new URL, update a canonical post, or place internal links.
- Read `references/advanced-quality-gates.md` before editor transfer to enforce content-intent, Korean editorial, link, and photo-safety blockers.
- Read `references/monetization-strategy.md` before planning AdPost, AdFit, AdSense, Coupang Partners, sponsored, or product-comparison revenue work.
- Read `references/affiliate-guidelines.md` before writing Coupang Partners content.
- Read `references/affiliate-scoring.md` before choosing affiliate product categories or TOP 5 products.
- Read `references/affiliate-link-density.md` before adding affiliate links or planning weekly affiliate ratio.
- Read `references/product-category-playbooks.md` before drafting recurring product category posts.
- Read `references/visual-asset-policy.md` before generating thumbnails, collecting body images, using official screenshots, or inserting product/event visuals.
- Read `references/image-thumbnail-guide.md` when planning visual assets, thumbnail text, image prompts, or in-post image rhythm.
- Read `references/visual-text-integrity.md` before rendering or uploading any Korean text-bearing image.
- Read `references/visual-prompt-library.md` when generating or planning thumbnail, summary card, checklist, FAQ, or comparison visuals.
- Read `references/naver-draft-runbook.md` when preparing or automating Naver Blog draft-save.
- Read `references/live-publish-runbook.md` for browser transfer, image verification, publishing, receipts, duplicate prevention, and recovery.
- Read `references/tistory-publish-runbook.md` for Tistory adaptation, metadata, editor checks, and result verification.
- Read `references/publication-ledger.md` before retrying timed-out saves or publications.
- Read `references/published-post-audit.md` after every public publish and when reviewing existing posts for visual or formatting defects.
- Read `references/post-templates.md` to select the correct article structure.
- Read `references/title-ab-testing.md` before selecting final post titles.
- Read `references/quality-rubric.md` before final delivery.
- Read `references/publish-risk-checklist.md` before publishing, draft-save, or final delivery of sensitive/time-sensitive posts.
- Read `references/low-quality-prevention.md` before creating multiple daily posts, affiliate-heavy posts, or posts that target similar keywords.
- Read `references/sample-bank.md` to vary titles, openings, closings, and layout patterns without copying other creators.
- Read `references/writing-patterns-ko.md` when improving Korean tone, opening, title, paragraph rhythm, and closing.
- Read `references/daily-ops.md` for a complete daily operating runbook.
- Read `references/performance-log.md` when reviewing published results or improving future topic selection.
- Read `references/performance-input.md` when converting real performance data into next actions.
- Read `references/search-exposure-check.md` when reviewing published post exposure, search inflow, or indexing concerns.
- Read `references/traffic-recovery-mode.md` when the latest 7-day average declines, new posts receive weak inflow, or public quality defects are found.
- Read `references/rewrite-rules.md` before rewriting existing posts.
- Read `references/experiment-log.md` when planning or evaluating blog optimization tests.
- Read `references/post-mortem-review.md` when reviewing unusually strong or weak posts.
- Read `references/operations-data-schema.md` when storing or analyzing performance CSV data.
- Read `references/weekly-report-template.md` for weekly performance summaries.
- Read and update `references/style-memory.md` when the user asks to learn from current influencer posts or refresh the blog style.
- Use `scripts/create_daily_pack.py` to create a dated folder with three markdown draft templates and a research log.
- Use `scripts/prepare_owned_photo.py` to auto-orient, resize, strip metadata, blur selected regions, and create a verifiable privacy sidecar for user-owned images.
- Use `scripts/self_test_quality_gates.py` after changing the validator, photo workflow, fact freshness, visual roles, or package schema.
- Use `scripts/simulate_daily_strategy.py` to test topic selection and output structure against synthetic scenarios before major skill updates.
- Use `scripts/score_topic_candidates.py` when the user provides a CSV of topic candidates and scores.
- Use `scripts/score_revenue_topics.py` when the user provides a CSV of monetization candidates and wants revenue-priority scoring.
- Use `scripts/analyze_performance_csv.py` when the user provides a CSV of published post performance data.
- Use `scripts/analyze_traffic_windows.py` to compare consecutive complete traffic windows and trigger recovery mode consistently.
- Use `scripts/scan_sensitive_terms.py` before uploading skill changes to GitHub when any account, automation, affiliate, or browser-login work was discussed.
- Use `scripts/validate_publish_package.py` before browser transfer to catch stale facts, unsupported strong title claims, duplicate reader questions, invalid canonical decisions, repeated or internal-note text, unsafe owned-photo records, sidecar mismatches, GPS metadata, near-duplicate owned photos, missing links, missing images, card-only packages, raw Markdown, weak tags, and disclosure failures.
- Use `scripts/record_publication_receipt.py` after every draft-save or publish attempt to record status and block accidental verified duplicates.
- Use `scripts/decide_autonomous_run.py` to enforce the three-candidate plan, rolling affiliate ratio, one-public-post budget, quality gates, and duplicate receipts.
- Use `scripts/self_test_autonomous_run.py` after changing autonomous publication, content-mix, or retry rules.
- Use `scripts/manage_autonomous_state.py` to enforce canary mode, overlap locks, failure counts, and automatic pause state.
- Use `scripts/check_editorial_reuse.py` to compare a draft with recent owned bodies before editor transfer.
- Use `scripts/validate_editor_verification.py` to reject broken, clustered, uncaptioned, or unverified editor transfers.
- Use `scripts/self_test_unattended_safety.py` after changing canary, lock, reuse, or editor-verification rules.
- Use `scripts/create_visual_cards.py` with UTF-8 JSON specifications for deterministic Korean cards and `scripts/audit_visual_assets.py` before upload.

## Editorial Rules

- Write original, helpful content. Do not scrape, reproduce, or spin other creators' posts.
- Avoid fake personal experience. If experience is not provided by the user, use neutral wording such as "구매 전 확인할 점" instead of pretending to have used a product.
- Record `experience_basis` for every package and block firsthand language in `research_only` posts.
- Record one concrete reader question, a `new_post` or `update_existing` action, a cluster role, and a useful internal-link decision for every package.
- Make writing feel natural by varying sentence length, adding concrete reader questions, using everyday Korean, and placing light emoticons only where they fit the blog's tone.
- Aim for truthful, specific editorial quality rather than detection avoidance. Never add fake mistakes, invented memories, random slang, or fabricated use experience to disguise tool assistance.
- Treat layout, blank lines, image placement, emoji/emoticon use, and title rhythm as part of the writing quality, not afterthoughts.
- Treat influencer-like quality as specific reader framing, truthful editorial judgment, visual proof, and balanced cautions; do not manufacture personal experience or excitement.
- Strip location metadata and inspect private details before using original photos; automated checks do not replace full-resolution human review.
- Keep factual claims on an explicit expiry clock and prefer canonical updates over new URLs when only current conditions changed.
- Do not overuse emoji, decorative punctuation, or exaggerated claims. Use them as seasoning, not structure.
- Add affiliate disclosure for Coupang Partners posts.
- For promotions, products, rankings, and news, cite or name the source basis and include the checked date in the draft notes.
- Do not store credentials, cookies, tokens, private affiliate dashboard data, or account-specific secrets in GitHub or skill files.
- Avoid thin, duplicate, keyword-stuffed, or affiliate-heavy posts that do not add original reader value.
- Keep publication mode as draft-only unless the user explicitly instructs otherwise; then follow that instruction for the approved batch and verify every final result.
- In autonomous mode, create three candidates but publish at most one verified Naver post per day, no more than two affiliate-first posts per rolling seven days, and never affiliate-first posts on consecutive days.
- Keep the first three verified unattended runs in draft-only canary mode. Do not bypass a paused state or an active run lock.

## Output Format

For each daily run, return:

1. Daily topic board with selected three posts.
2. Content-portfolio decision with reader questions, `new_post` or `update_existing`, cluster roles, canonical URLs, and internal-link plans.
3. Source/research notes with dates checked.
4. Three complete draft packages with an experience basis and evidence note.
5. Visual storyboard with a scene-first thumbnail, image roles, captions, sources, copyright/privacy notes, and placement.
6. Draft-save checklist for Naver Blog and optional Tistory adaptation.
7. Daily influencer scan summary and any suggested `style-memory.md` updates if durable patterns were found.
8. Autonomous decision report with publish, draft-save, blocked, retry, and receipt status for every candidate.
