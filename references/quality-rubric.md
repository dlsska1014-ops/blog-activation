# Quality Rubric

Score each draft from 1 to 5 in each category before delivery. Revise any post scoring below 31 out of 40. Mandatory visual and trust gates override the numeric score.

## Scoring Categories

1. Timeliness
   - Is the topic relevant today, this week, or this season?

2. Reader Usefulness
   - Does the post answer concrete questions?
   - Does it help the reader decide, buy, apply, compare, or avoid a mistake?

3. Fact Reliability
   - Are dates, prices, conditions, product claims, and benefit details checked?
   - Are uncertainties named?
   - Is the fact-freshness level correct, and are live or current claims still inside their recheck window?

4. Originality
   - Is the writing original rather than a close rewrite of another post?
   - Does it add comparison, interpretation, or practical framing?
   - Is the experience basis declared and consistent with the language?
   - Does the post answer a distinct reader question or deliberately update the canonical URL?

5. Human Editorial Presence
   - Does the first screen name a real reader situation and give an editorial priority?
   - Are first-person statements limited to work actually performed?
   - Are sentence rhythm, headings, bridges, and scenarios varied without becoming theatrical?

6. Visual Storytelling
   - Does the first visual show the topic situation rather than a generic text card?
   - Do scene, evidence, explanation, and decision-aid roles work together?
   - Are captions, source notes, and original-resolution checks complete?

7. Readability And Layout
   - Are paragraphs short enough for Naver Blog?
   - Are tables and image notes placed where they help?
   - Is the first screen compelling?
   - Are repeated paragraphs, dominant sentence endings, and internal work notes absent?

8. Monetization And Low-Quality Safety
   - For affiliate posts, is the product selection tied to real reader intent?
   - Is the disclosure included?
   - Does the post protect trust instead of pushing too hard?
   - Is the post distinct from recent posts?
   - Does it avoid keyword stuffing, copied structure, thin summaries, and excessive affiliate emphasis?
   - Does it add original comparison, checklist, FAQ, or decision support?

## Red Flags

Revise immediately if the draft:

- Starts with a generic encyclopedia-style introduction.
- Uses the same phrase repeatedly.
- Pretends to have personal experience.
- Makes unverifiable ranking or sales claims.
- Has no checked date for time-sensitive facts.
- Has affiliate links or recommendations without disclosure.
- Repeats another creator's structure too closely.
- Repeats the same reader intent as a recent post without adding new value.
- Uses many similar keywords unnaturally.
- Exists mainly to place affiliate links.
- Uses only repeated text-card visuals for a long post.
- Uses a generic card as the first image when a scene-first image is possible.
- Uses fake personal experience to sound more human.
- Uses an AI scene as evidence of a real visit or product test.
- Repeats broad forecast dates or generic definitions without a narrower reader decision.
- Shows duplicate titles, exposed generation labels, or near-identical visual sequences.
- Uses complete-guide, lowest-price, number-one, or guaranteed language without direct evidence.

## Mandatory Gates

Block delivery or publication when:

- A long post has fewer than four visuals without a documented exception.
- The visual package lacks a scene-first image.
- The visual package has fewer than three roles for a long post.
- Sourced visuals lack source, checked date, reuse basis, or a useful caption.
- Korean text-bearing images were not inspected at original resolution.
- The editorial-presence check scores below 5 out of 6.
- `experience_basis` is missing or contradicts firsthand language.
- Original photos lack an ownership basis, or sponsored content lacks disclosure.
- A high-risk duplicate is set to `new_post`, or the canonical/internal-link decision is missing.
- Korean editorial QA, original-photo privacy QA, GPS removal, or near-duplicate-image checks are incomplete.
- Fact freshness, owned-photo sidecar integrity, or strong-title evidence is missing.

## Final Polish Pass

Before handing over:

1. Strengthen the title.
2. Make the opening more situational.
3. Build a scene, evidence, and decision-aid visual sequence.
4. Add image roles, captions, placement notes, and source records.
5. Add tags.
6. Run `publish-risk-checklist.md`.
7. Run `low-quality-prevention.md`.
8. Confirm the approved draft-only or auto-publish mode.
9. Run `validate_publish_package.py` and stop on any advanced quality-gate failure.
