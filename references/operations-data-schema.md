# Operations Data Schema

Use this schema when storing blog performance in CSV or spreadsheet form. Store actual values only.

## Recommended Columns

Required:

- date_drafted
- date_published
- platform
- post_type
- title
- main_keyword
- keyword_cluster
- cluster_role
- duplicate_intent_risk
- affiliate_link_count
- views
- search_inflow_keywords
- affiliate_clicks
- affiliate_conversion
- notes

Optional:

- thumbnail_type
- title_pattern
- opening_pattern
- layout_pattern
- low_quality_risk_score
- exact_title_exposure
- main_keyword_exposure
- rewrite_action
- publication_status
- public_url
- image_count
- content_fingerprint
- checked_at_24h
- checked_at_72h
- checked_at_7d

## Usage

- Use `score_topic_candidates.py` before drafting.
- Use `analyze_performance_csv.py` after publishing data accumulates.
- Update `performance-log.md` only with interpreted lessons, not raw dumps.

## Interpretation Rules

- Do not treat one post as proof.
- Look for repeated patterns across 3 or more posts.
- Separate search demand from purchase intent.
- Track affiliate ratio so the blog does not become product-only.
- Compare posts at similar ages; do not compare a 24-hour post directly with a 30-day post without labeling the window.

