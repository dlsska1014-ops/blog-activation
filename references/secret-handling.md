# Secret Handling

Use this file whenever credentials, affiliate data, cookies, tokens, or account-specific information could be involved.

## Never Store In GitHub

Do not store these in `SKILL.md`, references, scripts, logs, samples, screenshots, or GitHub commits:

- Naver ID, password, recovery email, phone number, cookies, session values.
- Tistory/Kakao login information.
- Coupang Partners ID, password, access tokens, private reports, payment information.
- API keys, `.env` values, browser cookies, exported session files.
- Personal addresses, phone numbers, resident numbers, business registration numbers, bank data.

## Safe Handling Rules

- Ask the user to log in directly in the browser when needed.
- Treat login state as temporary browser state, not skill data.
- Do not write secrets into local markdown files.
- Do not paste secrets into GitHub issues, commits, comments, or PRs.
- If a link contains tracking or affiliate parameters, keep only the final publish-ready link in the post draft and avoid storing account dashboards or private reports.

## If A Secret Appears

1. Stop before committing or uploading.
2. Remove the secret from the file.
3. Ask the user to rotate the credential if it may have been exposed.
4. If it was committed to GitHub, do not rely on deletion alone; treat it as compromised.

## Pre-Upload Check

Before GitHub upload, scan for:

- `password`
- `passwd`
- `token`
- `cookie`
- `secret`
- `client_secret`
- `access_key`
- `NAVER_`
- `COUPANG_`
- Korean words such as `비밀번호`, `쿠키`, `토큰`, `계정`, `주민`, `사업자번호`
