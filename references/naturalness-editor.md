# Naturalness Editor

Use this as the final rewrite pass for Korean blog drafts. The goal is natural, useful writing, not hiding that tools were used.

## Rewrite Priorities

1. Replace generic openings with reader situations.
2. Replace vague claims with concrete conditions.
3. Add one caution or exception.
4. Vary sentence endings.
5. Break dense paragraphs with intentional spacing.
6. Remove exaggerated words unless the source supports them.
7. Check that affiliate disclosure is visible and natural.
8. Add one truthful editorial action when research was actually performed.
9. Replace repeated instruction endings with varied judgment, explanation, and next-action sentences.
10. Check that the opening and first visual describe the same reader situation.
11. Remove repeated long paragraphs and repeated generic phrases.
12. Check whether one formal ending dominates most sentences; revise the paragraph function, not only the suffix.
13. Remove prompts, TODOs, internal notes, and visible tool-generation disclosures.
14. Run `editorial-authenticity-gate.md` and revise paragraphs that repeat the same function or could belong to an unrelated article.
15. Reject fake typos, invented anecdotes, random slang, and mechanical ending swaps. Naturalness must come from specific thinking and truthful evidence.

## Common Generic Phrases To Replace

Instead of:

- "오늘은 ~에 대해 알아보겠습니다."
- "~에 대한 모든 것을 정리했습니다."
- "많은 분들이 궁금해하시는"
- "꼭 필요한 필수템"

Prefer:

- "행사 혜택은 좋아 보이지만, 조건을 놓치면 체감 혜택이 줄어들 수 있습니다."
- "구매 전에 먼저 볼 부분은 세 가지입니다."
- "이 글은 예산별로 어떤 선택이 현실적인지 정리한 글입니다."
- "이런 경우라면 추천하기 어렵습니다."
- "공식 안내를 다시 확인해보니, 먼저 볼 부분은 지역보다 객실 표시였습니다."
- "금액만 보면 단순해 보이지만 숙박 일수가 바뀌면 권종도 달라집니다."

## Sentence Ending Mix

Use a natural mix:

- "...입니다."
- "...해볼게요."
- "...좋습니다."
- "...확인해야 합니다."
- "...달라질 수 있습니다."
- "...먼저 보세요."

Do not force casual speech into serious topics.

## Final Human Read Check

Ask:

- Would a real operator write this after checking the sources?
- Is there a concrete reason this post exists today?
- Are recommendations balanced with cautions?
- Does the layout feel intentionally edited?
- Does the post avoid sounding like a generic summary?
- Is the first-person wording limited to work actually performed?
- Could any paragraph be moved to an unrelated article without changing it? If so, make it more specific.
- Do visual captions explain why each image matters?
- Does each paragraph perform a different job: scene, fact, interpretation, caution, comparison, or next action?
- Could any internal work note or generated-text marker appear in the public editor?

Set `naturalness_qa_confirmed: true` only after this pass and the automated package check both succeed.

This check improves reader quality. It must not be used to claim that a post is human-written or to evade an AI detector.
