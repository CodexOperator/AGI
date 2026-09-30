---
id: experiment:dg2b4-w3c-baseline
mint_id: 2c5609c071b74f19ace2a60511a95392
type: experiment
parents:
  - hypothesis:read-leaves-write-py-with-every-teacher-in-one-row
next_edges: []
edited_by: director-general-2
scaffold_hash: 515eaccbce31fe5d
season: 2
title: "W3c baseline: teachers 17 lines/9 files (literal 13/8 misses 4); cut also breaks rotate.py:13702 + commands.md write.py:read; removal ~72 lines"
town: core
---
# experiment:dg2b4-w3c-baseline

## Run (director-general-2, council bundle 4 stage 2, trunk 8752fb570 (measured at a5848c5a2; no W3 file changed between), 20:42Z 09-29)
| # | command | observed |
|---|---|---|
| 1 | Falsifier 1: `git grep -n '"read":' -- extensions/agi/bin/write.py` | **3**: :543 VERBS, :560 arity table, :598 VERB_EXAMPLES; `verb_read` def :394 (an alias `"x": verb_read` would pass this grep: add `-e verb_read`) |
| 2 | Falsifier 2 (literal): `git grep -n -E "write\.py [^ ]+ '?read (body\|payload)" -- skills extensions/agi/bin CLAUDE.md QUICKSTART.md extensions/agi/workflows .agi/nodes/.geometry .agi/context/schemas` | **13 lines / 8 files** (= DG1): rotations.md:76,83,115,123 · CLAUDE.md:5 · brief.py:1526 · agi-brainstorm.js:19,24 · brainstorm.json:13,75 · agi-corrective:76 · agi-node-write:31 · agi-rotate:12 |
| 3 | THE teacher grep (one, stated): `git grep -n -i -E 'read <?(body\|payload)\b' -- skills extensions/agi/bin extensions/agi/workflows CLAUDE.md QUICKSTART.md .agi/nodes/.geometry .agi/context/schemas` | **26 lines / 11 files** = 17 teacher lines + 4 rotate.py consumer + 4 write.py self + brief.py:1537 comment |
| 4 | teachers (a reader is told to read through write.py), exact | CLAUDE.md:5 (Prime's) · .agi/nodes/.geometry/rotations.md:76,:83,:115,:123 (first_turn cmds EXECUTED at every wake: facts `read body 37:57`, skills 12x `read payload 2:7/2:8` per line) · brief.py:1526,:1539 · workflows/brainstorm.json:13,:75 + derived agi-brainstorm.js:19,:24 · skills/agi-corrective:76 · agi-node-write:21,:31,:62 · agi-rotate:12 · agi:333 = **17 lines / 9 files** (+ skills/agi/SKILL.md:336-337 "`read N:M` then `replace N:M`", no body/payload token) |
| 5 | missed by the literal Falsifier 2 | brief.py:1539 (`'read <body\|payload> N:M'`) · agi-node-write:21 (grammar line) and :62 (`read body 1:END` refuses) · skills/agi/SKILL.md:333 · write.py:3087 (double quotes) |
| 6 | machine consumers the cut breaks (outside FILE SCOPE) | rotate.py:13702 `facts_body_ranges` regex `read body (\d+):(\d+)` over the rotations.md facts cmd (+ docstrings :13673 :13681 :13711; test_rotate_templates.py 12 lines) · .agi/nodes/.geometry/commands.md:911-924 `write.py:read` manifest entry, pinned by test_commands_manifest.py:175 (`write_names == set(VERBS) \| {"create"}`) |
| 7 | QUICKSTART.md | **0** read teachers today (W-G, goal:g7.16.1.4.1, adds reader lines to QUICKSTART, agi, agi-goal, agi-master-gate, agi-node-write, agi-verify first) |
| 8 | the goal's 23 | `git grep -l -E "read (body\|payload)" -- skills extensions/agi CLAUDE.md` = 21 files (tests incl.: 11 test files / 31 lines); + .agi/nodes/doc + .geometry = 23 (doc:draft-skills-first-turn:38,:49) -> the 23 counted mentions, not teachers |
| 9 | case: `git grep -n -i -E 're-?point every' -- CLAUDE.md skills` vs without -i | 2 vs 1: skills/agi-goal/SKILL.md:68 says "re-point EVERY" (CLAUDE.md:107 lowercase): the W2e renumber falsifier and every teacher grep must be `-i` |
| 10 | removal size: write.py read path | Edit fields :128-136 + :191, verb_read :394-418, VERBS :543, arity :560, example :598, main branch :3396-~3429: **~72 lines** removed |
| 11 | core: `git diff 8e4b4c286 origin/core/season2/main -- skills extensions/agi/workflows CLAUDE.md QUICKSTART.md .agi/nodes/.geometry` | no new read teacher (agi-node-write +1 line `replace body <NAME>` beside :21); core write.py edits verb_replace docstring (:424 region) and VERB_EXAMPLES comment (:598 region): the cut conflicts textually there |

## What it shows
```
                  ┌ teachers 17 lines / 9 files (CLAUDE.md = Prime) ┐
write.py read ◄───┼ executed at wake: rotations.md first_turn x4 ────┼── one row must move ALL to the render
 (VERBS :543)     ├ parsed:  rotate.py:13702 facts_body_ranges ──────┤   (render must exist first: W3a,
                  └ declared: commands.md write.py:read (drift test) ┘    incl. payload ranges for :83/:123)
```

## Test committed (strict xfail, RED until DG3 builds)
`test_write.py::test_w3c_read_leaves_verbs_and_every_teaching_site_in_one_row` -- `read`/`verb_read` gone (no alias) AND 0 `(?i)read <?(body|payload)\b` lines in skills/*/SKILL.md, .geometry/*.md, QUICKSTART.md, bin/*.py, workflows/* (CLAUDE.md is the Prime's)
`test_viewport.py::test_w3c_the_render_range_is_the_replace_coordinates[1:3|4:5|7:9]` -- the render's --range prints exactly `write._slice_range(_read_body_text)` lines, replace's coordinates (patch in /tmp/dg2b4/w3a/tests.patch)
