# Editorial Authenticity Gate

Use this after the first complete draft and before layout or browser transfer. The purpose is to produce truthful, specific Korean editorial writing. Do not use this gate to evade AI detection or platform safeguards.

## Paragraph Function Pass

Label every non-heading paragraph as one of:

- `scene`: a concrete reader situation,
- `fact`: sourced information,
- `interpretation`: what the fact changes for the reader,
- `comparison`: meaningful differences or tradeoffs,
- `caution`: exception, limit, or who should skip,
- `action`: the next practical step,
- `bridge`: a short transition that is necessary for flow.

Revise when three adjacent paragraphs perform the same function, when a paragraph could be pasted into an unrelated article, or when a bridge adds no meaning.

## Specificity Pass

Require all of the following:

- one concrete reader question,
- one reason the post matters on the checked date,
- at least two decision criteria,
- at least one caution or exception,
- one next action that does not depend on an affiliate click,
- source attribution for every current or live fact.

For affiliate posts also require:

- a visible disclosure before recommendations,
- selection criteria before product links,
- a distinct use case and caution for every product,
- at least two useful non-affiliate sections,
- a conclusion that remains useful if all links are removed.

## Language Pass

Block or rewrite:

- generic announcements such as `오늘은 ~ 알아보겠습니다`,
- repeated `정리해보겠습니다`, `추천드립니다`, or `도움이 되셨길 바랍니다`,
- unsupported superlatives and certainty,
- a uniform list of similarly sized paragraphs,
- mechanical alternation of sentence endings,
- decorative questions that the article never answers,
- fake colloquial errors, typos, or invented personal memories,
- copied hooks or a recognizable creator's signature phrase.

Prefer concrete nouns, ordinary connective language, and varied paragraph length that follows the reader's decision process.

## Independent Read

Perform a second pass without looking at the draft outline. Ask:

1. What exact question does this answer?
2. Which paragraph contains the most useful original judgment?
3. Which claim would be most damaging if stale or wrong?
4. Which paragraph sounds reusable or generic?
5. Would the article still help if product links disappeared?

Set `editorial_authenticity_confirmed: true` only after answering all five in package notes and revising the weak paragraph.

