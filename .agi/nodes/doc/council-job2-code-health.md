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
Owner's job via belam 07:16:40Z 11-05. Collated by self-perpetuating gen 39, 09:0xZ 11-05; rows 1-1c re-measured at ONE sha by gen 56, 17:3xZ 11-08 (the owner's item 3 below, placed on this seat by alive's [decision] 23:25:38Z 11-07). Every row names its seat, its source file and its LIMITS.

## OWNER 2026-11-07 20:42:45Z (c:be72d519c116), verbatim
From belam's [owner] 20:47:15Z 11-07 (box commit 86a44591bf on refs/box/belam/sanctuary-master), item 3, the owner's words in quotes:
"We can also do a pass over the whole system to optimize it using crap and dry metrics. ... the best systems aren't the ones that have the most, its the ones that have the most taken away and still work as good or better than more complex ones. This is why in biology most organs, organelles, cells, chemicals, proteins, etc all have multiple functions. If a part every has only a single function it has a darn good reason to. ... we always wanna reuse existing channels and remix or swirl or rotate them in new unique ways. Less complexity is always better. The design isn't finished when there's nothing left to add, its finished when there's nothing left to take away."

## The table
| # | lens (seat) | measured on | headline | source |
|---|---|---|---|---|
| 1 | CRAP = cc^2 (1-cov)^3 + cc, cov 0/1 by function ENTRY (sp) | FULL archive of the trunk bb947547b2 (tree 045602af1f asserted, 269 MB); 370 test files, 1 pytest process each, a tap recording every bin/ + src/ function entered | 3539 functions; 2984 entered (84.3%); 555 never entered; CRAP > 30: 276 (85 entered with cc > 30; 225 never entered with cc >= 5). By cc band, never entered: cc 1-4 330/1734 (19%), 5-10 140/1149 (12%), 11-30 70/556 (13%), 31+ 15/100 (15%) | /data/scratch/art/self-perpetuating/council-job2-r2/O/join.out |
| 1a | top CRAP (all cov 0) | same | reader_census.py cmd_repo 2756 (cc 52); board_job.py cmd_commit 2450 (49); grid.py cmd_census 2352 (48), _unify_check 2162 (46), _unify_owner_batch 1640 (40); reader_census.py cmd_homes 1640 (40); graph_builder.py parse_pipelines 1482 (38). grid.py cmd_unify (cc 65, top at ff5e31da23) is now entered by a lane, so it reads CRAP 65 and left the top | the same file (40 rows) |
| 1b | files with most never-entered fns at cc >= 5 | same | src/agi_algos/graph_builder.py 31, bin/season_report.py 25, bin/grid.py 20, bin/board_job.py 8, bin/prereq_notice.py 7, bin/success_metrics.py 7 | the same file |
| 1c | CALLERS: functions no production code calls (sp, new) | the same tree, a static call graph over 899 files (0 unparsed) | 128 functions have 0 production callers; 24 of them are flagged as reached another way (DYN 1, IMPLICIT 20, OVERRIDE 3). The other 104 are CANDIDATES, 1911 lines: 56 called only from tests, 48 called from nowhere; 37 entered by some lane, 67 never. By cc: 1-4 68 fns / 681 lines, 5-10 23 / 507, 11-30 13 / 723, 31+ 0. Largest: graph_core/identity.py plan_reid 121 lines (cc 20), chain_engine/query_api.py coverage_report 95, seatsig/countersign.py promote 80, query_api.py next_best_hypothesis 60, rotate.py facts_body_ranges 55 | /data/scratch/art/self-perpetuating/council-job2-r2/O/callers.out + callers.tsv (one row per function) |
| 2 | DRY: duplicated 8-line windows (aio) | bin + src at aaa0374ba7: 166 .py, 91784 normalized lines | 305 duplicated windows, 58 groups, 1627 lines in duplicate blocks (1.8%). Top: the adapters (claude_code / copilot_cli / grok_bot / pi: groups 1, 4, 11-13, 15, 19), graph_builder.py (2, 3, 14), dispatch.py:3988 = :4133 (25 lines), chains.py, snapshot-build-site.py:96 = snapshot-goals.py:129, db_loader.py = loader.py (twice) | /data/scratch/art/all-is-one/council-job2-dry/ |
| 3 | the root vs CLAUDE.md (alive, 07:39:45Z) | the trunk root | CLAUDE.md:18 and :32 name a top-level src/ as live source: the root has none. Outside the 'allowed to exist' table: an EMPTY file whose name is a JSON object (blob e69de29b, added 8b853446b1 09-04), a committed __pycache__ (3 files), datasets (5356), experiments (96), sessions (24), context (19), TODO.md, context.md, package.json | alive's [word] 07:39:45Z, part 3 |
| 4 | tests that cannot fail, static (sp, notes 110) | tests at 1713ade7a9: 402 files, 8232 test functions | CONST 1 (test_heal_sweep.py:552: an asserted string, its `in` on the next line thrown away), TAUTO 3 (test_rotate.py:8506 HEAD == HEAD; test_crons_log_cap_declared_scope.py:98 bytes == bytes; test_workflow_round_manifests.py:250 asks a question it is not asking), NOCHECK 7; VACUOUS 222 is a coarse pointer list, never a finding | self-perpetuating's free-day notes 11-01, section 110 (scratch, outside the graph) |
| 4a | the same, as mutants (sp, notes 110-112) | scratch archives, one cell = one pytest process | 5 mutants: 3 killed by a sibling test (e.g. the heal dry-run line, the quarantine empty read), 2 survive every caller. ONE realistic: crons._trim_in_place keeping the HEAD (seek(0)) passes all 111 tests of the 7 files naming either trim | the same notes, sections 111-112 |
| 4b | the crons row (aio) | scratch copy | the keep-the-head mutant passes 24 tests of 3 files; a fixed test_crons_log_cap_declared_scope.py kills it; two empty stubs (test_rotate.py:4573 docstring only; renderers/test_ascii_summary.py:34 pass); one same-both-sides assert the static scan misses (test_crons_log_cap_copytruncate_mode.py:87) | aio [note] 08:07:05Z |
| 5 | checks that read NOTHING (sp, notes 113) | scratch project | links.py 'broken' counts PAYLOAD links only (link_ref / payload_ref), never edges, and exits 0 even with broken > 0: a reader must read the number, not the rc | the same notes, section 113 |

LIMITS (row 1, at bb947547b2): (a) cov is ENTRY, not lines: a function entered once counts as covered. (b) children run with python -I/-E are not tapped (their entries are missed). (c) only top-level extensions/agi/tests/test_*.py ran (370 files; no subdirectories, no .t.sh lanes). (d) the archive is FULL this time, so the 39 slim-archive reds of 11-05 are gone; 8 files ran rc 1 (test_media_fm1, fm2, html, video, sibling, walk; test_dispatch_model_fence; test_p1_ab), not attributed here: their tests may have stopped early, so 84.3% is a LOWER bound on entry and 555 never-entered an UPPER bound. (e) 362 rc 0, 0 skipped; max RSS 517 MB per process; 2613 tap files. (f) one archive, so the tree did not move under the lanes, which ran 23:2xZ 11-07 to 17:36Z 11-08 at nice 19, each waiting while another post ran pytest or load5 was over 8.
LIMITS (row 1c): static: a call by name through getattr, a string table, a subprocess argv or a CLI verb is missed unless a flag names it (the DYN prefixes, IMPLICIT, OVERRIDE), so a CANDIDATE is a function to READ before any cut, never a cut by itself; test refs count names, not calls.
LIMITS (row 2): normalized 8-line windows of >= 160 chars; a duplicate is text, not behaviour.
WHAT IT SAYS: the grid.py unify/census family and reader_census are still the high-cc code no top-level test enters (row 1a), and graph_builder.py is both the most duplicated (row 2) and the most unentered (row 1b). Row 1c is the owner's 'taken away' list in its first form: 104 functions, 1911 lines, that no production code calls by name; each is read before it is cut, since a static graph misses dynamic calls. The checks that cannot fail are few and mostly covered by a sibling (row 4a); the one real hole is the crons trim (rows 4a, 4b), with its one-line fix already written (4b).
Nothing decided: each finding becomes its own goal:g7.33 round, by the council, never from this doc (SM [word] 09:0xZ 11-05).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
self-perpetuating gen 56, 11-08 (v2): rows 1-1b re-measured on a FULL archive at one sha (bb947547b2), because v1's slim archive turned 39 lanes red on graph paths it left out; row 1c (callers) added as the first list of what could be taken away, per the owner's item 3 now quoted above with its chunk id. Rows 2-5 are unchanged from v1.
<!-- THOUGHT:END -->
