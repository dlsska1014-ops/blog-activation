# Published Post Audit

Use this immediately after every public publish and when reviewing existing posts.

## Audit Three Surfaces

1. Public post text:
   - correct title and body ending,
   - no Markdown headings, table pipes, backticks, image placeholders, prompt text, or internal notes,
   - disclosure and links are visible where required.
2. Public post visuals:
   - planned image count is present,
   - open the first, middle, and last image on the rendered page,
   - Korean text is readable and matches the approved source,
   - no clipping, repeated image, upload placeholder, or unexpected blur.
3. Blog list and duplication:
   - the new title appears once in the recent-post list,
   - the public URL resolves to the intended title,
   - no retry created a second post with the same title or content fingerprint.

## Required Evidence

Record:

- URL and checked time.
- Displayed title.
- Public image count.
- First/middle/last image result.
- Raw-marker scan result.
- Recent-list duplicate result.
- Final status: `verified`, `partial`, `blocked`, or `unknown`.

A publish click or returned URL is not enough. If any visual contains unreadable text, classify the result as `partial` and do not reuse that image set.

## Existing-Post Recovery

- Do not mass-delete posts.
- Identify the canonical post before editing or removing a duplicate.
- Regenerate corrupted visuals from clean UTF-8 source text.
- Replace images only after local visual QA passes.
- Convert raw Markdown into native editor text or tables.
- Remove internal notes and recheck the public page.
- Preserve the original URL when repairing the canonical post when possible.


