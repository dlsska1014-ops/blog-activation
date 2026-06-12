# Naver Draft Runbook

Use this when the user asks to prepare posts inside Naver Blog. Default to draft-save only.

## Safety Mode

- Do not publish unless the user explicitly asks and confirms the exact post.
- Do not bypass login, security, or account checks.
- Stop before any irreversible action.
- Keep affiliate disclosure visible in the draft body.

## Draft-Save Procedure

1. Open Naver Blog write editor.
2. Confirm the target blog account with the user if more than one account appears.
3. Insert title.
4. Insert body in Naver-friendly spacing.
5. Add image placeholders or uploaded images if the user has provided them.
6. Add tags.
7. Check first screen readability.
8. Save as draft.
9. Report the draft title and any missing assets.

## Body Transfer Format

Use this order:

1. Title.
2. Affiliate disclosure if applicable.
3. Opening.
4. Quick summary.
5. Main sections.
6. Table/checklist.
7. FAQ.
8. Closing.
9. Tags.

## Before Draft-Save Checklist

- Title is not too long.
- First 5 lines are useful without scrolling.
- Affiliate disclosure is present for Coupang Partners.
- Image placeholders are clear.
- No fake personal experience.
- No unsupported ranking or sales claim.
- Dates and conditions include checked date.
- Low-quality risk score is acceptable according to `low-quality-prevention.md`.
- Publish risk checklist has no stop conditions.

## Automation Notes

If browser automation is available, interact only with visible, confirmed controls. If the editor changes or a selector is uncertain, stop and ask for user confirmation rather than risking publication.
