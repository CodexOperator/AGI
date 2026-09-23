---
id: experiment:a00-b0cc8f3a-0f6efd
mint_id: d2e3370337d348dbbb8a8fa5b36057e6
type: experiment
parents:
  - hypothesis:links-py-flags-live-references-to-retired-goals
next_edges: []
confidence: 0.9
edited_by: a00-b0cc8f3a
evidence_runs:
  - experiment:a00-b0cc8f3a-0f6efd
line_ceiling: 40
loop: hypothesis:links-py-flags-live-references-to-retired-goals@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 80
profile: balanced
role: kid
scaffold_hash: 2c888f0e56d4a371
season: 2
title: links.py reports live references to retired or absent goal ids, from the config:links cell
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b0cc8f3a-0f6efd — links.py flags live references to retired goals

## Pre-fix measurement (this tree, before the change)

```
links.py links   3982 resolved, 0 broken (18 retired payload(s), not damage)
```

`broken_links` was 0 the whole time because a retired goal still RESOLVES —
`goal:g13`, `g14`, `g11`, `g6.5`, `g15` all have files and parse. Nothing
reported that live frontmatter and cards still cite them. `config:posts` line
22 carried `owning_goal: "goal:g15"`, and the geometry commands table cited
`goal:g13` (retired) and `goal:g9.7` (no file at all).

## What was built

`extensions/agi/bin/links.py links` now reports a `retired` count and gains
`--strict` (exit 1 when it is non-zero). `scan_retired_refs(root, cfg)` walks
the surfaces named on the new `config:links` node and reports, one line each,
`<file>:<line> <old id> → <successor | none>`. A retired node's successor is
the goal id named in its `THOUGHT` block (`g11` → `goal:g20`), never inferred
from its parents.

**Discrimination, all load-bearing.** A node file is scanned in its
FRONTMATTER region only; a node whose own `status` is `retired` is skipped
whole (its refs are not live); nodes under `.agi/nodes/deprecated/` (status
`deprecated`) never enter the retired set. Non-node surfaces are read whole
minus `THOUGHT:BEGIN..END` lines. Exempt history fields (`lens`,
`judged_against`) are dropped by field name.

**Config-max / template-max.** The scanned glob list, the exempt markers
(`.agi/nodes/deprecated/`, `THOUGHT`, and the history field names) and the
output `line_template` are ONE cell on a `config` NODE at
`.agi/nodes/.geometry/links.md` (`id: config:links`), read by `links.py` at
run time. Adding a surface is a config edit, zero code change; the test
`test_a_surface_added_by_the_config_node_is_scanned` proves it by editing the
cell in the fixture. The node lives under `.agi/nodes/.geometry/` and not
`.agi/config.json` on purpose (a round's `done` commit refuses that file —
`cli.py:_round_scope_ok`; the same failure is recorded at `brief.py:2274-2288`
for `config:brief`), so the round names it in `--owns config:links`.

## Evidence

Live run on the built bytes:

```
$ python3 extensions/agi/bin/links.py links
links: 3983 resolved, 0 broken (18 retired payload(s), not damage)
  declared     29
  payload_ref  274
  defaulted    3680
retired: 206 live reference(s) to a retired or absent goal id
  .agi/nodes/.geometry/commands.md:54 goal:g13 → goal:g20
  .agi/nodes/.geometry/crons.md:33 goal:g14 → goal:g20
  .agi/nodes/.geometry/posts.md:22 goal:g15 → goal:g20
  .agi/sessions/quorum/director-belam.md:5 goal:g19 → goal:g20
  ...
$ python3 extensions/agi/bin/links.py links --strict ; echo $?
1
$ python3 extensions/agi/bin/links.py links --broken ; echo $?
0     # --strict is the only new exit path; --broken is unchanged
```

The hits were reported, never fixed: sweeping the corpus to make the count
zero is other rounds' work (the target says so), and would destroy the
evidence this node exists to leave.

Tests: `extensions/agi/tests/test_links_retired_refs.py` (6 cases) — retired
node hit + card hit + exempt history field = exactly 2; successor read from
the THOUGHT; absent id → `none`; a config-added surface is scanned; a THOUGHT
block is not a hit; `--strict` exits 1 and the template is rendered from data.
Required neighbourhood re-run: `test_links.py`,
`test_links_refs_outside.py`, `test_links_verdict_class.py` — 41 passed.

Production lines (this round, `git diff --numstat` over
`extensions/agi/bin/links.py`): **80**, tests excluded. The `config:links` node
is 44 lines of config data, not code. 80 is exactly 2x the 40-line default
ceiling and not above it; the compact resolver, config read and `--strict`
exit are the irreducible shape of the claim.

## Agent Notes
Built links.py retired count + --strict over the config:links cell (scanned/exempt/template); live run reports 206 refs, --strict exits 1; 6 new tests + 41 neighbourhood pass; 80 production lines.
