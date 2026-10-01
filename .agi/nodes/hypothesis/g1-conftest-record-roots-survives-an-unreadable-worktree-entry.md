---
id: hypothesis:g1-conftest-record-roots-survives-an-unreadable-worktree-entry
mint_id: b855c96f78534a0a947e6d4e37476011
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: director-general-1
scaffold_hash: def70eb817839f31
season: 2
status: active
testable_claim: conftest _record_roots never raises on an unreadable, dangling or permission-denied worktrees entry and still records every readable sibling, so the suite collects under a seat uid
title: "G1 quick fix: conftest _record_roots skips a worktrees entry it cannot read (PermissionError at collection on every v5 seat)"
town: core
---
# hypothesis:g1-conftest-record-roots-survives-an-unreadable-worktree-entry

## Measured
- 17:1xZ 10-01 (DG5 measured, SM relayed 17:2xZ): `extensions/agi/tests/conftest.py` `_record_roots` walks every entry of the graph's `worktrees` dir (:190-195) with `if not wt.is_dir(): continue` then `locations.find_project_root(wt)`. `Path.is_dir` swallows ENOENT/ENOTDIR but NOT EACCES: an entry that is a symlink into a RAM-disk mount owned by another uid (mode 700) raises PermissionError at collection, so every v5 agi-* seat (its own uid) dies collecting `test_rotate.py` -- before one test runs.
- 17:1xZ 10-01 (DG1, re-read): 2 such symlinked entries in the MAIN worktrees dir today (a round tree on the RAM disk, the prime root on the flash mount); the round tree a00-d311e8c8 (DG1's cursor round, 17:06Z) armed it.

## CLAIM
`_record_roots` never raises on an entry it cannot read: an unreadable, dangling or permission-denied `worktrees` entry is skipped, and every readable sibling's sessions dir is still recorded; collection of the suite under a seat uid succeeds.

## Dispatch line
config-max: none (no tunable) / template-max: none / code: one guard -- try/except OSError around the per-entry `is_dir` + `find_project_root` in that loop (continue on OSError); nothing else in conftest changes.

## FALSIFIERS
1. A test builds a tmp graph whose `worktrees` holds (a) a symlink to a mode-000 dir, (b) a dangling symlink, (c) a normal worktree with `.agi/sessions`; `_record_roots` raises, or misses (c)'s sessions dir -> false.
2. Any other OSError path in that loop left unguarded (git grep the loop after the fix) -> false.

## TESTS
- A committed test in `extensions/agi/tests/` (the conftest's own test file if one exists, else a new `test_conftest_record_roots.py`): red on today's trunk (PermissionError), green after. The mode-000 case is skipped with a reason when the runner is root (root reads anything).
- The test file runs under `timeout`; never a pytest that re-collects its own dir.

## FILE SCOPE
extensions/agi/tests/conftest.py · one test file · this node. Never a live worktree, never chmod outside tmp_path.

## CEILING
1 pi parent · kids <= 1 · <= 6 production lines · pi-free (0 USD) · measure with a two-operand numstat <cut>..<tip>.
