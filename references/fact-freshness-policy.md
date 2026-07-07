# Fact Freshness Policy

Use this to decide when browsing and checked dates are mandatory.

## Always Recheck

Browse or otherwise verify current sources for:

- Event dates.
- Product prices.
- Stock or availability.
- Benefit rates.
- Eligibility rules.
- Public policy.
- Platform rules.
- Search engine, AdSense, ad consent, CMP, TCF, AI-search, or monetization platform policy claims.
- Product rankings or review counts.
- Affiliate disclosure rules.

## Checked Date Format

Use:

- Checked date: YYYY-MM-DD
- Source:
- What was checked:
- What may change:

## Manifest Levels

Record a `fact_freshness` object for every publish package.

- `stable`: durable definitions or user-supplied observations; recheck within 90 days before transfer.
- `current`: events, policies, product specifications, benefits, and seasonal conditions; recheck within 7 days.
- `live`: prices, stock, rankings, review counts, application status, and rapidly changing availability; recheck within 1 day.

Include `checked_date`, `fact_qa_confirmed`, and `source_records`. Each source record needs a source name, URL, type, checked date, and the exact claim it supports. Current and live content require at least one official, primary, or merchant source.

For stable posts without an external source, record a clear `fact_note` explaining the basis. Do not use an old checked date merely to satisfy the field.

## Title Claim Gate

Words such as `완벽`, `무조건`, `역대`, `최저가`, `1위`, and `폭발` create a higher evidence burden. Remove them by default. If a precise claim is essential and verifiable, record `title_claim_evidence` and connect it to a current source record.

## Draft Language

For changing facts, write:

- "작성일 기준"
- "공식 안내 기준"
- "행사 조건은 변경될 수 있으니 결제 전 확인이 필요합니다"
- "가격과 재고는 수시로 달라질 수 있습니다"

## Reject Or Delay

Reject or delay a post if:

- The main benefit cannot be verified.
- Prices or product claims are central but unavailable.
- A source contradicts the planned angle.
- The post would mislead readers if conditions changed.
- A current or live source record is stale at editor-transfer time.
- A strong title claim has no direct, current evidence.
- A pasted source text contains exact policy dates, CPC/CTR/RPM averages, or revenue-drop percentages that have not been verified against a current official or primary source.
