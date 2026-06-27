# Publication Ledger

Use a local JSON Lines ledger to prevent duplicate actions and preserve verifiable run results. Never place account credentials or private browser data in it.

## Receipt Fields

- `run_date`
- `platform`
- `mode`
- `title`
- `status`: `verified`, `partial`, `blocked`, or `unknown`
- `url_or_draft_id`
- `image_count`
- `checked_at`
- `content_fingerprint`
- `notes`

## Rules

1. Check the ledger before opening a replacement editor after a timeout.
2. Treat the same platform plus content fingerprint as the same publication attempt.
3. Refuse a second `verified` receipt for the same platform and fingerprint unless the user explicitly requests a republish.
4. Record `unknown` when the final state cannot be confirmed; inspect the post list before retrying.
5. Keep Naver and Tistory receipts separate.
6. Store the ledger in the dated working folder, not in the skill or GitHub repository.

Use `scripts/record_publication_receipt.py` to append receipts safely.


