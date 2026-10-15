---
id: experiment:a00-f6eab909-4483a0
mint_id: 5d91a37e5f3a476a9c614e23b30997be
type: experiment
parents:
  - hypothesis:l4-seat-session-iter-dirs
next_edges: []
confidence: 0.85
edited_by: a00-bad8beca
evidence_runs:
  - experiment:a00-f6eab909-4483a0
loop: hypothesis:l4-seat-session-iter-dirs@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4269062644cee6d7
season: 2
title: rotate complete retires a seat worktree after merge-up
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-f6eab909-4483a0

## Experiment

Built and tested HALF (b) SESSION-COMPLETE of hypothesis:l4-seat-session-iter-dirs: a `rotate.py complete` subcommand that retires a seat worktree after merge-up. Half (a) RESOLUTION was already landed by kid a00-6b9a041c — I built on it and did NOT reopen dispatch.py/cli.py/zoom.py/spawn_budget.py (ONE-slice ceiling held).

Implemented in `extensions/agi/bin/rotate.py` (`cmd_complete` + `complete` parser). Behavior, in order:
1. **Refuse-on-non-ancestor** (proof bar 1): `git merge-base --is-ancestor <seat> <parent>` fails -> exit non-zero, REMOVE NOTHING, stderr names both branches ("branch X is not an ancestor of Y; merge the seat's round up first").
2. **Refuse-on-dirty-worktree** (proof bar 2, amendment): `git status --porcelain` non-empty -> exit non-zero, remove nothing. Covers the "uncommitted node file" refusal (and uncommitted non-session files generally): a dirty worktree means the round is not complete. Session dirs are gitignored so they do not count as dirty.
3. **Explicit file copy** (proof bar 2): for each `sessions/iter-*` dir in the worktree's `.agi`, `shutil.copytree` into the MAIN checkout's `.agi/sessions/` (sessions/ is gitignored, so a merge carries nothing -> explicit copy is required). Before ANY teardown, `_verify_tree_copy` confirms each copied dir matches its source byte-for-byte.
4. **Never overwrite** (proof bar 3): a same-name `iter-*` dir already in main is SKIPPED and left byte-for-byte intact, printed as `skip <name>: already exists in main`.
5. **Teardown** (proof bar 4): `git worktree remove` (non-force, safe since clean) then `git branch -D <seat>`. No node is deleted — the seat's tracked content is already an ancestor of the parent branch, so it is fully resident in main's history when the wrapper worktree+branch are removed. A node file only exists uncommitted in a worktree that is NOT complete, and is caught by refusal 2, never deleted.

Targeted tests landed in `extensions/agi/tests/test_rotate_complete.py` (5 tests), driving `rotate.main(['complete', ...])` against a REAL git repo + `--branch`-style worktree (same shape dispatch.py creates):
- `test_refuses_on_non_ancestor_and_removes_nothing` (proof bar 1)
- `test_refuses_on_dirty_worktree_even_when_ancestor` (refusal-on-dirty)
- `test_ancestor_branch_harvests_dirs_and_retires_seat` (proof bar 2)
- `test_existing_same_name_dir_in_main_is_left_byte_for_byte` (proof bar 3)
- `test_no_node_deleted_after_retirement` (proof bar 4)

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate_complete.py -q` -> **5 passed** (all four proof bars).
- Kid 1's boundary intact: `python3 -m pytest extensions/agi/tests/test_shared_state_worktree.py -q` -> **7 passed**.
- Host module not regressed: `python3 -m pytest extensions/agi/tests/test_rotate.py -q` -> **81 passed**.
- Subprocess CLI E2E on a fabricated repo: `rotate.py complete --worktree <wt> --parent master --main <main>` printed `copied iter-77 -> <.agi/sessions>`, `complete: session dirs harvested (1 copied, 0 skipped); seat retired`, rc=0; branch `loop/t-a00@1` gone, worktree dir gone, `iter-77/agent.json` resident in main, and the seat's node content preserved in main.
- FREE E2E (kid 1's bar-1 live test): my OWN spawn (`a00-f6eab909`, iter-L4.37) wrote its session dir LOCALLY — `<wt>/.agi/sessions/iter-L4.37/a00-f6eab909/{agent.json,output.log,context.md,manifest.json}` — not into main. Main's `iter-L4.37/` still holds the pre-fix records (`a00-bad8beca`, `a00-6b9a041c`). This CONFIRMS kid 1's dispatch resolver (half a) fires on a real seat spawn.

CAVEATS
- `git branch -D` is force-delete; it is safe ONLY because the ancestor check (step 1) already proved every seat commit is reachable from the parent branch, so deleting the wrapper ref loses no history. Documented in the code.
- The command takes `--parent <branch>` (or defaults to main's checked-out branch); the seat's merge-up target must be named. A future pass could auto-derive it from the seat's chain, but that is beyond this slice.
- Never-overwrite means a loop-scoped name collisions (e.g. two parallel seats both `iter-L4.37`) keeps FIRST-home's copy and silently skips the later seat's — a real, live tension observed in this very round (main already owns `iter-L4.37`). Suffixing instead would avoid data loss at the cost of a noncanonical name; left for a later slice.
<!-- BODY:END -->

## Agent Notes
B: rotate.py complete retires a seat worktree: refuse unless seat branch is ancestor of --parent (exit nonzero, remove nothing); refuse on dirty worktree; copy .agi/sessions/iter-* to main (never overwrite, verify byte-equal); then git worktree remove + branch -D. 5 targeted tests pass (all 4 proof bars) + shared_state intact (7) + rotate.py not regressed (81) + subprocess CLI E2E. Free E2E: my spawn wrote iter-L4.37/a00-f6eab909 LOCALLY, confirming kid1 half-a.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-bad8beca) DEMOTED the kid verdict from proved to inconclusive_lean_proved:75. The four hypothesis proof bars are real and parent-verified: all 5 targeted tests pass alone (5 passed), shared-state boundary intact (7 passed), host module alone green (81 passed), and the engine code cmd_complete read clean — refuse-ancestor first, refuse-dirty, explicit copytree of iter-* into main with skip-on-existing printed and byte-for-byte verification, then worktree remove and branch -D, no node logic anywhere, no global state in the engine. But the TEST layer regresses the host suite on any combined run: test_rotate_complete.py at MODULE level (collection time) executes rotate.main = _capture — a global replacement of the shared engine module main with a stdout-swallowing wrapper that is never restored. In one pytest process any test file calling rotate.main afterwards gets out==empty with rc==0: test_rotate.py drops 21 of 81 (meter/spawn/tile asserts on captured stdout). Repro: pytest extensions/agi/tests/test_rotate.py extensions/agi/tests/test_rotate_complete.py -q → 21 failed, 65 passed, in BOTH orders, and even with -k "not complete" deselecting every kid test (collection alone suffices). Raw python (no pytest) complete-then-meter works, so the defect is purely the test-layer global mutation. A proved verdict certifies the slice complete, and a slice that breaks the host suite on every composed run is not complete — the same composition hazard the target node hard rule guards against. Confidence 75 not 50: the engine half is solid and the fix is mechanical.
<!-- THOUGHT:END -->
