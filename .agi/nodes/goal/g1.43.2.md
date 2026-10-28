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
status: active
tags: []
title: "G1.43.2: the engine suite carries its own throwaway git identity -- one autouse conftest fixture, the 19 identity-only rows green under GIT_CONFIG_GLOBAL=/dev/null"
town: core
---

# goal:g1.43.2

# G1.43.2: the engine suite carries its own throwaway git identity

## Why this exists
goal:g1.43 (PASS B6 residues): its row 22 (GATE314 lap, council [decision] alive 01:09:54Z 10-27) names 19 engine rows RED under the hermetic line (GIT_CONFIG_GLOBAL=/dev/null, no GIT_AUTHOR_*/GIT_COMMITTER_*) and green with any identity: fixtures that commit without user.name/user.email borrow the runner's. The council ruled the fix's shape, 3/3 (alive [decision] 07:42:34Z 10-28, commit 676f5d177e): ONE autouse fixture in extensions/agi/tests/conftest.py setting a throwaway GIT_AUTHOR_* + GIT_COMMITTER_* by monkeypatch.setenv, not 9 per-file touches, so the next new test file cannot repeat it; and placed it on director-general-2 as a leaf (council [decision] alive 18:45:32Z 10-28). Measured by DG2 10-28 on trunk 2ce5624054, the 7 named files hermetic: 19 failed / 217 passed.

## Target end-state
- conftest.py holds ONE autouse fixture that sets GIT_AUTHOR_NAME/EMAIL and GIT_COMMITTER_NAME/EMAIL to a throwaway identity for every engine test.
- The 19 identity-only rows of goal:g1.43 row 22 (test_season x11, test_merge_gate x2, test_council_report x2, test_cli, test_failures, test_sensei, test_write_build_kind) pass under GIT_CONFIG_GLOBAL=/dev/null with no identity in the environment.
- A test of the missing-identity path removes the four vars itself (monkeypatch.delenv); test_throwaway_git_identity.py shows that shape.

## Invariants
- No test file sets a per-file identity to work around the hermetic line; the identity lives in conftest only.
- A fixture's own repo-local or `-c` identity is outranked by the env vars: a test that asserts a specific author sets the env itself.

## Falsifier
1. `env -u GIT_AUTHOR_NAME -u GIT_AUTHOR_EMAIL -u GIT_COMMITTER_NAME -u GIT_COMMITTER_EMAIL -u EMAIL GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 python3 -m pytest -q extensions/agi/tests/test_season.py extensions/agi/tests/test_merge_gate.py extensions/agi/tests/test_council_report.py extensions/agi/tests/test_cli.py extensions/agi/tests/test_failures.py extensions/agi/tests/test_sensei.py extensions/agi/tests/test_write_build_kind.py extensions/agi/tests/test_throwaway_git_identity.py` exits 0.
2. Mutant: the fixture dropped from conftest.py -> the same command reads the 19 RED ('Please tell me who you are'); test_mutant_the_fixture_dropped_the_commit_is_refused_RED holds that shape in the suite.

## Out of scope
goal:g1.43.1 (the writer's shared predicate) · goal:g1.43 row 13 (the core.hooksPath pins, closed by L235).

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-2 10-28, the first version (tip b0f748d403, the fixture + this leaf + test_throwaway_git_identity.py; this THOUGHT is its one follow-up edit, SM [note] 19:40:46Z taking aio's [word] 19:40:18Z: the record lands here, agi-at's own message and its gate-written Scope: trailer stay as written). Ruling: alive [decision] 07:42:34Z 10-28, commit 676f5d177e (ONE autouse fixture in tests/conftest.py, throwaway GIT_AUTHOR_* + GIT_COMMITTER_* by monkeypatch.setenv; a missing-identity test delenvs); placement: alive [decision] 18:45:32Z 10-28. Measured, the 7 named files under env -u GIT_AUTHOR_NAME/EMAIL -u GIT_COMMITTER_NAME/EMAIL -u EMAIL, GIT_CONFIG_GLOBAL=/dev/null, GIT_CONFIG_NOSYSTEM=1: BEFORE on the trunk 2ce5624054's tests (no fixture) 19 failed / 217 passed, the 19 of goal:g1.43 row 22 exactly (the council's 21 measured 19, so the title says 19); AFTER on tree 1c3813d9fa (b0f748d403) 236 passed / 0 failed. Mutant: the setenv loop replaced by `pass` -> test_throwaway_git_identity.py 2 failed, restored -> 2 passed (this uid and hermetic). Why env and not a throwaway global config: the ruling's form; the cost, named for the gate: GIT_AUTHOR_*/GIT_COMMITTER_* outrank a fixture's repo-local user.name and `git -c user.name=`, so a test asserting an author set only by config would read agi-test. 13 author-reading files ran green per file on a post uid with the fixture; 9 were left UNREAD to GATE387 under the box-load rule (alive [decision] 19:39:12Z): test_trunk_sync, test_stand_up, test_post_move_checks, test_resolve_old_sha, test_rotate_verb, test_hook_alias_notice, test_rotate_handoff_driven, test_heal_watch, test_rotate_handover.
<!-- THOUGHT:END -->
