---
id: config:links
mint_id: 9816595f4df14534b63c9880909012cd
type: config
parents:
  - hypothesis:links-py-flags-live-references-to-retired-goals
next_edges: []
edited_by: a00-b0cc8f3a
locations: {}
season: 2
title: "config:links — the ONE links cell: scanned surfaces, exempt markers, the hit-line template"
town: local-maxxing
links:
  scanned: [".agi/nodes/**/*.md", "extensions/agi/briefs/**/*", ".agi/sessions/quorum/*.md", "CLAUDE.md", "QUICKSTART.md", "skills/agi/SKILL.md"]
  exempt: [".agi/nodes/deprecated/", "THOUGHT", "lens", "judged_against"]
  line_template: "{file}:{line} {old} → {succ}"
---

# config:links

The ONE `links` cell (`hypothesis:links-py-flags-live-references-to-retired-goals`):
`links.py links` reads THIS node to decide what to scan for live references to a
retired or absent goal id, what to exempt, and how each hit prints. Adding or
removing a surface is one line here, never a code change.

It lives in a `config` node rather than `.agi/config.json` on purpose, for the
same reason `config:brief` does: a round's own `done` commit refuses
`.agi/config.json` by rule (`cli.py:_round_scope_ok`), so a cell there is absent
from the landed branch and a fresh checkout cannot render. A config node the
round names in `--owns` is committed.

- `scanned` — repo-relative globs, resolved against `locations.source_root`.
  A file under `<root>/nodes/` is scanned in its FRONTMATTER region only;
  every other surface is scanned whole, minus its `THOUGHT` blocks.
- `exempt` — three kinds, discriminated by shape: a trailing `/` is a path
  prefix whose files are skipped whole; the bare word `THOUGHT` drops lines
  inside a `THOUGHT:BEGIN..END` block; anything else names a frontmatter field
  whose lines are skipped (the history fields `lens` / `judged_against`).
- `line_template` — the output line, rendered with `{file}`, `{line}`, `{old}`
  and `{succ}`; `succ` is the goal id the retired node's `THOUGHT` block names,
  or the word `none`. The format is data here, not an f-string in `links.py`.

A retired goal RESOLVES, so `links.py links` has never faulted it; the retired
count is a second number precisely because `broken_links` is 0 for this defect.
