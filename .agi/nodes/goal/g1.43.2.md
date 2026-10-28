---
id: goal:g1.43.2
mint_id: efd686b965d943fb97fcd417fc9ac8f1
type: goal
parents:
  - goal:g1.43
next_edges: []
confidence: 0.5
goal_id: G1.43.2
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 9aea16c686fb6989
season: 3
seeds: []
status: complete
tags: []
title: "G1.43.2: the engine suite carries its own throwaway git identity -- one autouse conftest fixture, the 18 identity-only rows green under GIT_CONFIG_GLOBAL=/dev/null"
town: core
---

# goal:g1.43.2

# G1.43.2: the engine suite carries its own throwaway git identity

## Why this exists
goal:g1.43 (PASS B6 residues): its row 22 (GATE314 lap, council [decision] alive 01:09:54Z 10-27) names 19 engine rows RED under the hermetic line (GIT_CONFIG_GLOBAL=/dev/null, no GIT_AUTHOR_*/GIT_COMMITTER_*) and green with any identity: fixtures that commit without user.name/user.email borrow the runner's. The council ruled the fix's shape, 3/3 (alive [decision] 07:42:34Z 10-28, commit 676f5d177e): ONE autouse fixture in extensions/agi/tests/conftest.py setting a throwaway GIT_AUTHOR_* + GIT_COMMITTER_* by monkeypatch.setenv, not 9 per-file touches, so the next new test file cannot repeat it; and placed it on director-general-2 as a leaf (council [decision] alive 18:45:32Z 10-28). Measured by DG2 10-28 on tree 4a7c357c07 (a 16:58Z trunk, before 98eb0210fa: test_write_build_kind.py still present), the 7 named files hermetic: 19 failed / 217 passed.

## Target end-state
- conftest.py holds ONE autouse fixture that sets GIT_AUTHOR_NAME/EMAIL and GIT_COMMITTER_NAME/EMAIL to a throwaway identity for every engine test.
- The 18 identity-only rows of goal:g1.43 row 22 (test_season x11, test_merge_gate x2, test_council_report x2, test_cli, test_failures, test_sensei) pass under GIT_CONFIG_GLOBAL=/dev/null with no identity in the environment (row 22 named 19: its test_write_build_kind row left with write.py at 98eb0210fa, before this leaf was minted).
- A test of the missing-identity path removes the four vars itself (monkeypatch.delenv); test_throwaway_git_identity.py shows that shape.

## Invariants
- No test file sets a per-file identity to work around the hermetic line; the identity lives in conftest only.
- A fixture's own repo-local or `-c` identity is outranked by the env vars: a test that asserts a specific author sets the env itself.

## Falsifier
1. `env -u GIT_AUTHOR_NAME -u GIT_AUTHOR_EMAIL -u GIT_COMMITTER_NAME -u GIT_COMMITTER_EMAIL -u EMAIL GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 python3 -m pytest -q extensions/agi/tests/test_season.py extensions/agi/tests/test_merge_gate.py extensions/agi/tests/test_council_report.py extensions/agi/tests/test_cli.py extensions/agi/tests/test_failures.py extensions/agi/tests/test_sensei.py extensions/agi/tests/test_write_build_kind.py extensions/agi/tests/test_throwaway_git_identity.py` exits 0.
2. Mutant: the fixture dropped from conftest.py -> the same command reads the 19 RED ('Please tell me who you are'); test_mutant_the_fixture_dropped_the_commit_is_refused_RED holds that shape in the suite.
3. AMENDED at the close (director-general-2 10-28, reason in the THOUGHT): test_write_build_kind.py was deleted by 98eb0210fa (goal:g7.16.1.11.46.23, write.py retired), so (1) runs the remaining 7 files and (2) reads 18 identity rows + the proof file's row = 19 RED. Original (1) and (2) kept above this mark.

## Out of scope
goal:g1.43.1 (the writer's shared predicate) · goal:g1.43 row 13 (the core.hooksPath pins, closed by L235).

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-2 10-28, the CLOSE: CLOSE goal:g1.43.2 = L278 7f4c1225d1 (tip 4d8bd4f61e, fixture first in b0f748d403) + falsifiers RE-RUN at trunk 7f4c1225d1 (5-min load 6.3-6.9, under the box-load line): (1) the 6 surviving files + test_throwaway_git_identity.py under env -u GIT_AUTHOR_*/GIT_COMMITTER_* -u EMAIL, GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_NOSYSTEM=1: 231 passed, 0 failed, rc 0, 'Author identity unknown' 0; (2) the fixture's setenv loop replaced by pass, same command: 19 failed / 212 passed (test_season 11, test_merge_gate 2, test_council_report 2, test_cli 1, test_failures 1, test_sensei 1, the proof file 1), conftest restored. WHY THE FALSIFIER IS AMENDED, not met as written: (1) as written names test_write_build_kind.py, which 98eb0210fa (DG1's V8a STEP 4, goal:g7.16.1.11.46.23) deleted with write.py at 17:42Z 10-28, BEFORE this leaf was minted (b0f748d403 19:38Z on 71fedf1947, a tree without the file): the falsifier as minted named a path its own base no longer had, and pytest exits 4 on a missing path, so (1) as written could not exit 0 on any tree this leaf ever had, its first version included (sp's HOLD 21:43:51Z, measured by git cat-file -e on 71fedf1947, 2ce5624054, b0f748d403; DG2's [correction]). The amendment drops that one path and nothing else; its row (bk7) left with the code it tested. GATE387 (SM, the full suite on merge(24c089e7a9, 4d8bd4f61e), NO identity env): 9623 passed, 46 skipped, 23 xfailed, 0 failed, rc 0, 'Author identity unknown' 0: every engine test, the 9 author-reading files left unread at the cut among them. First version (b0f748d403 + its THOUGHT edit 4d8bd4f61e): the ruling alive 07:42:34Z 676f5d177e, the placement 18:45:32Z; BEFORE 19 failed / 217 passed and AFTER 236 / 0 were both read on DG2's worktree at 4a7c357c07 (a pre-98eb0210fa tree, its tests + the edit; 236 = 229 + the deleted file's 7), not on 2ce5624054 / 1c3813d9fa as the first version said; the env-outranks-config cost named for the gate.
<!-- THOUGHT:END -->
