# Autonomous Operations

Use this runbook when the blog is expected to operate without a person supervising each post. Autonomy means completing the approved workflow and stopping safely when evidence is weak. It does not mean bypassing platform review, disguising automation, or publishing through failed quality gates.

## Daily State Machine

Run these states in order and persist the result of each state in the dated package.

1. `research`: check current primary sources, recent blog patterns, prior topics, and recent performance.
2. `plan`: create three distinct candidates: information/trust, seasonal/search demand, and affiliate/buying intent.
3. `draft`: prepare complete Naver-first packages and optional Tistory adaptations.
4. `verify`: run fact, originality, natural Korean, visual, disclosure, duplicate-intent, and low-quality gates.
5. `decide`: run `scripts/decide_autonomous_run.py` against the daily plan and publication history.
6. `transfer`: publish only the selected item; draft-save the remaining eligible items.
7. `audit`: verify title, clean body, image count, disclosure, mode, URL or draft state, and recent-list duplication.
8. `learn`: record receipts and schedule 24-hour, 72-hour, and 7-day performance checks.

Never skip a state because the browser, source, image upload, or metric is inconvenient.

## Fail-Closed Rules

Draft-save instead of publishing when:

- a primary source cannot be rechecked within its freshness window,
- the topic overlaps a recent reader question,
- Korean editorial QA or visual QA is incomplete,
- an image is missing, broken, or unrelated to its section,
- affiliate disclosure or product evidence is incomplete,
- the editor state cannot be verified after a save or publish action,
- the latest receipt has an unknown or partial result for the same fingerprint,
- browser recovery would require guessing whether an action already succeeded.

Block the run instead of draft-saving when content contains unsupported firsthand claims, copied phrasing, private data, unsafe advice, or a duplicate verified fingerprint.

## Publication Budget

- Create three candidates per day, but publish at most one verified Naver post per day.
- Draft-save other eligible candidates for later review or scheduling.
- Publish no more than two affiliate-first posts in any rolling seven-day window.
- Keep verified non-affiliate posts strictly greater than affiliate-first posts in the same window.
- Do not publish affiliate-first posts on consecutive days.
- During traffic recovery, public defects, or missing metrics, prefer an information post and keep the affiliate candidate as a draft.
- Tistory is an adapted secondary channel. Do not paste the Naver body unchanged or publish an unverified duplicate package.

## Retry And Idempotency

- Give every package a content fingerprint and run id.
- Record `started`, `verified`, `partial`, `unknown`, or `blocked` for each platform action.
- Retry a browser action only after checking the receipt and current editor or post state.
- Never repeat a final save or publish action when a verified receipt already exists.
- Use bounded retries: one normal retry after a fresh observation, then stop with `partial` or `unknown`.
- Preserve the editor tab and package files when stopping so the next run can recover from evidence instead of memory.

## Human-Quality Standard

The goal is original, useful editorial work, not AI-detector evasion. A post is eligible only when:

- each paragraph has a clear job such as scene, fact, interpretation, caution, comparison, or next action,
- the opening answers a real reader situation rather than announcing the topic,
- factual claims have source and checked-date support,
- recommendations include limits, alternatives, and a truthful reason for selection,
- sentence and section rhythm varies because the content function varies,
- first-person wording describes work actually performed,
- images support nearby sections and captions explain their purpose,
- no sentence exists only to repeat a keyword or imitate a creator.

Do not insert random typos, fake anecdotes, invented purchases, artificial slang, or meaningless sentence variation to appear human.

## Automation Prompt Contract

An unattended scheduler must explicitly state:

- the workspace and `blog-activation` skill to use,
- the approved publication mode,
- the three-candidate portfolio and one-public-post daily budget,
- fail-closed behavior and receipt verification,
- that login data, session exports, authentication values, and private affiliate identifiers must never be written to files or GitHub,
- that the run must report `verified`, `partial`, `blocked`, or `unknown` for each platform.
