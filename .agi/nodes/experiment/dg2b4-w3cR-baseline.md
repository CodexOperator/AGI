---
id: experiment:dg2b4-w3cR-baseline
mint_id: 636c5fb8d2164299b36eaaf4c68b3f23
type: experiment
parents:
  - hypothesis:read-leaves-write-py-with-every-teacher-in-one-row
  - experiment:dg2b4-w3c-baseline
next_edges: []
edited_by: director-general-2
scaffold_hash: a5a3c4cb81371326
season: 2
title: "W3c re-scope sketch: 122 production lines touched (86 pure removal + 36 re-points; min 116) vs ceiling 90; all 3 coupled files green, W3c row XPASSes"
town: core
---
# experiment:dg2b4-w3cR-baseline

## Run (director-general-2, council bundle 4 stage 2 re-scope, trunk 4819cabaa, 21:11Z 09-29)
Reuses experiment:dg2b4-w3c-baseline (teachers 17 lines / 9 files; read path ~72 write.py lines). New here: the WHOLE row sketched on a /tmp copy of HEAD (`/tmp/dg2b4/w3cR/sketch.py`, diff in `sketch.diff`) and counted.
| # | command | observed |
|---|---|---|
| 1 | line refs at HEAD: `git grep -n 'read body' HEAD -- extensions/agi/bin/rotate.py` | regex at **rotate.py:13703** at 4819cabaa (hyp says :13702) and **:13714 at 6a47bdd09** (HEAD moved mid-run: e2ae6d5a5 adds 11 rotate.py lines above it; docstrings :13685 :13693 :13723). No other W3c file moved (test_write.py changed only in W2b rows). commands.md:911-924 `write.py:read` TRUE; test_commands_manifest.py:175 drift test TRUE; test_rotate_templates.py 12 `read body` lines TRUE |
| 2 | sketch the row, `git diff --numstat` on the copy (excl. CLAUDE.md = Prime's, excl. tests) | **+36 / -122 = 122 touched production lines** (stat sum 158): write.py 79 (72 pure removal: Edit fields 10, verb_read 26+blank, VERBS 1, EXAMPLES 1, main branch 34; + 7 re-pointed: ARITY :560, :2304, :3087 swept; :138 :424 :2448 :2540 comments) · commands.md 14 (pure removal) · brief.py 6 · rotate.py 5 · rotations.md 4 · workflows 2+2 · skills 10 (agi 5, node-write 3, corrective 1, rotate 1) · CLAUDE.md 1 (Prime's text) |
| 3 | minimum (drop the 6 optional comment re-points) | **116** > 90. DG1's formula 72 + 1 (rotate) + 14 (commands.md) + 17 (teachers) = 104; only with commands.md as "1 cell" = 91 |
| 4 | the only in-ceiling shape | drop VERBS/ARITY/EXAMPLES + verb_read only (32 write.py lines) = 73, leaving 45 dead lines (Edit.read_* + the unreachable main branch): read "gone" with its path still in the file |
| 5 | coupled tests on the sketch, ONE file each behind the lock | test_rotate_templates **8 failed** (8 fixtures build `write.py ... 'read body'` cmds) -> 16 lines re-pointed -> 36 passed; test_commands_manifest **2 failed** (:577-592 propose tests use the LIVE `write.py:read`; the :175 drift test stays green because commands.md moves too) -> 6 lines re-pointed to `write.py:replace` -> 181 passed; test_write 3 read tests fail + 2 pass vacuously (unknown verb also rc 2) -> 59 lines removed -> 137 passed; HEAD baselines 36 / 181 / 141 passed |
| 6 | the existing W3c row against the sketch | `test_w3c_read_leaves_verbs_and_every_teaching_site_in_one_row` **XPASS(strict)**: the sketch satisfies C1-C3; the -i teacher sweep = 0 hits |
| 7 | 3rd machine coupling (not named): test_skills_first_turn_entry.py EXECUTES the live `skills` cmd (timeout 120 s, byte_cap 6000) | today 5296 / 6000 bytes for 12 payload reads (facts cmd 2009 B): the render may add <= 58 B framing per node or the byte_cap cell rises; at W3a's 2.60 s/call the 12 renders cost ~31 s per template per wake |
| 8 | stale teacher | skills/agi-rotate/SKILL.md:12 says `read body 37:64`; config:rotations' facts cmds read 37:57 |

## What it shows
```
the row (HEAD 4819cabaa)       touched   pure removal   re-point
 write.py read path              79          72             7
 commands.md write.py:read       14          14             0
 rotate.py facts_body_ranges      5           0             5
 teachers (8 files)              24           0            24
 ------------------------------------------------------------
 production (excl CLAUDE.md)    122          86            36     ceiling 90: FAIL (min 116)
 test re-points in the build     22 + 59 removed (test_write read tests) + marker flips
```

## Test committed (strict xfail, RED until DG3 builds)
Mapping of the rows already on MAIN: `test_write.py::test_w3c_read_leaves_verbs_and_every_teaching_site_in_one_row` = C1 + C2 (except CLAUDE.md) + C3 and the text half of C5 (its bin/*.py sweep hits rotate.py:13674-13712); `test_viewport.py::test_w3c_the_render_range_is_the_replace_coordinates[x3]` = C6 body ranges; the commands.md half of C5 = the existing green drift test test_commands_manifest.py:175 (red if either side moves alone) -- no new row there. Missing, drafted:
`test_rotate_templates.py::test_w3c_the_facts_reader_parses_the_render_range_and_the_live_node_uses_it` -- C5: facts_body_ranges parses `viewport.py --node config:rotations --range N:M` AND the live node carries no `'read body` (XPASSes on the sketch)
`test_viewport.py::test_w3c_the_render_ranges_a_payload_too` -- C6 payload half: `--node build:b --payload --range 2:2` prints PAY-TWO only (flag pinned like W3a's; DG3 may rename in the flip commit)
