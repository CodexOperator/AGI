---
id: doc:council-job2-code-health
mint_id: a4afdf5b7b94403aad0006bfa3ab1045
type: doc
parents:
  - goal:g7.33
next_edges: []
edited_by: self-perpetuating
tags:
  - doc
  - council
  - job2
title: "Council job 2: code health of extensions/agi, one table"
---
# doc:council-job2-code-health
Owner's job via belam 07:16:40Z 11-05. Collated by self-perpetuating gen 39, 09:0xZ 11-05. Every row names its seat, its source file and its LIMITS.

| # | lens (seat) | measured on | headline | source |
|---|---|---|---|---|
| 1 | CRAP = cc^2 (1-cov)^3 + cc, cov 0/1 by function ENTRY (sp) | slim archive of ff5e31da23; 369 test files, 1 pytest process each, a tap recording every bin/ + src/ function entered | 3533 functions; 2966 entered (84.0%); 567 never entered; CRAP > 30: 279 (81 entered with cc > 30; 234 never entered with cc >= 5). By cc band, never entered: cc 1-4 333/1731 (19%), 5-10 145/1147 (13%), 11-30 71/556 (13%), 31+ 18/99 (18%) | /data/scratch/art/self-perpetuating/council-job2/crap-join-top40.txt |
| 1a | top CRAP (all cov 0) | same | grid.py cmd_unify 4290 (cc 65); reader_census.py cmd_repo 2756 (52); board_job.py cmd_commit 2450 (49); grid.py cmd_census 2352 (48), _unify_check 2162 (46), _unify_owner_batch 1640 (40); reader_census.py cmd_homes 1640 (40); grid.py _split_plan + cmd_split; graph_builder.py parse_pipelines 1482 (38) | the same file (40 rows) |
| 1b | files with most never-entered fns at cc >= 5 | same | src/agi_algos/graph_builder.py 31, bin/season_report.py 25, bin/grid.py 23, bin/board_job.py 8 | /data/scratch/art/self-perpetuating/council-job2/crap-join-top40.txt |
| 2 | DRY: duplicated 8-line windows (aio) | bin + src at aaa0374ba7: 166 .py, 91784 normalized lines | 305 duplicated windows, 58 groups, 1627 lines in duplicate blocks (1.8%). Top: the adapters (claude_code / copilot_cli / grok_bot / pi: groups 1, 4, 11-13, 15, 19), graph_builder.py (2, 3, 14), dispatch.py:3988 = :4133 (25 lines), chains.py, snapshot-build-site.py:96 = snapshot-goals.py:129, db_loader.py = loader.py (twice) | /data/scratch/art/all-is-one/council-job2-dry/ |
| 3 | the root vs CLAUDE.md (alive, 07:39:45Z) | the trunk root | CLAUDE.md:18 and :32 name a top-level src/ as live source: the root has none. Outside the 'allowed to exist' table: an EMPTY file whose name is a JSON object (blob e69de29b, added 8b853446b1 09-04), a committed __pycache__ (3 files), datasets (5356), experiments (96), sessions (24), context (19), TODO.md, context.md, package.json | alive's [word] 07:39:45Z, part 3 |
| 4 | tests that cannot fail, static (sp, notes 110) | tests at 1713ade7a9: 402 files, 8232 test functions | CONST 1 (test_heal_sweep.py:552: an asserted string, its `in` on the next line thrown away), TAUTO 3 (test_rotate.py:8506 HEAD == HEAD; test_crons_log_cap_declared_scope.py:98 bytes == bytes; test_workflow_round_manifests.py:250 asks a question it is not asking), NOCHECK 7; VACUOUS 222 is a coarse pointer list, never a finding | self-perpetuating's free-day notes 11-01, section 110 (scratch, outside the graph) |
| 4a | the same, as mutants (sp, notes 110-112) | scratch archives, one cell = one pytest process | 5 mutants: 3 killed by a sibling test (e.g. the heal dry-run line, the quarantine empty read), 2 survive every caller. ONE realistic: crons._trim_in_place keeping the HEAD (seek(0)) passes all 111 tests of the 7 files naming either trim | the same notes, sections 111-112 |
| 4b | the crons row (aio) | scratch copy | the keep-the-head mutant passes 24 tests of 3 files; a fixed test_crons_log_cap_declared_scope.py kills it; two empty stubs (test_rotate.py:4573 docstring only; renderers/test_ascii_summary.py:34 pass); one same-both-sides assert the static scan misses (test_crons_log_cap_copytruncate_mode.py:87) | aio [note] 08:07:05Z |
| 5 | checks that read NOTHING (sp, notes 113) | scratch project | links.py 'broken' counts PAYLOAD links only (link_ref / payload_ref), never edges, and exits 0 even with broken > 0: a reader must read the number, not the rc | the same notes, section 113 |

LIMITS (row 1): (a) cov is ENTRY, not lines: a function entered once counts as covered. (b) children run with python -I/-E are not tapped (their entries are missed). (c) only top-level extensions/agi/tests/test_*.py ran (no subdirectories, no .t.sh lanes). (d) the archive was SLIM by the memory rule (extensions/agi 904 files, skills 17, .agi/config.json, .agi/nodes/.geometry, .agi/context/schemas: 28 of 6040 .agi/nodes files, 22 of 446 .agi/context files), so 39 of 369 files ran RED on graph paths the archive left out (rc 1: 38, rc 2: 1; sampled: FileNotFoundError on .agi/context/media, goal and vision nodes absent; list in /data/scratch/art/self-perpetuating/council-job2/crap-red-lanes.txt). Their tests stopped early, so 84.0% is a LOWER bound on entry and 567 never-entered an UPPER bound. (e) 330 rc 0; max RSS 516 MB per process; 2534 tap files.
LIMITS (row 2): normalized 8-line windows of >= 160 chars; a duplicate is text, not behaviour.
WHAT IT SAYS: the grid.py unify/census/split family and reader_census are the high-cc code no top-level test enters (row 1a), and graph_builder.py is both the most duplicated (row 2) and the most unentered (row 1b). The checks that cannot fail are few and mostly covered by a sibling (row 4a); the one real hole is the crons trim (rows 4a, 4b), with its one-line fix already written (4b).
Nothing decided: each finding becomes its own goal:g7.33 round, by the council, never from this doc (SM [word] 09:0xZ 11-05).
