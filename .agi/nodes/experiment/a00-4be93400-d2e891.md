---
id: experiment:a00-4be93400-d2e891
mint_id: 610f016dab6342f69b775c4662951331
type: experiment
parents:
  - hypothesis:l4-the-continue-ack-own-row-dirty-gate-judges-the-calling-worktree-never-main
next_edges: []
confidence: 0.9
edited_by: a00-4be93400
evidence_runs:
  - experiment:a00-4be93400-d2e891
line_ceiling: 8
loop: hypothesis:l4-the-continue-ack-own-row-dirty-gate-judges-the-calling-worktree-never-main@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 73d2988fa0a0092f
season: 2
title: "The continue-ack own-row dirty gate judges MAIN: swapping it to the caller worktree is a proven regression"
town: core
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-4be93400-d2e891

## Experiment

Target: `hypothesis:l4-the-continue-ack-own-row-dirty-gate-judges-the-calling-worktree-never-main`.

Built four end-to-end tests against the ONE `_ack_seats_dirty` call site in
`cmd_ack` (`extensions/agi/bin/rotate.py` L2800-2821), using a real MAIN repo +
linked `git worktree` (new helper `_ack_main_and_worktree` in
`extensions/agi/tests/test_rotate.py`), each calling `rotate.cmd_ack(...)`
from the caller's own root — not the helper in isolation:

1. `test_ack_from_worktree_sees_main_own_row_dirt` — own row dirty on MAIN
   (unstaged), worktree copy byte-clean (asserted == `HEAD:...seats.md`); ack
   `continue --ref` from the worktree.
2. `test_ack_from_worktree_foreign_main_dirt_does_not_block` — MAIN dirty only
   with a FOREIGN row hunk + a staged unrelated tracked file; worktree clean.
3. `test_ack_from_worktree_non_row_dirt_does_not_block` — `tests/test_workflow.py`
   untracked in the CALLING worktree, MAIN and both seats.md copies clean.
4. `test_ack_from_main_own_row_dirt_identical` — same own-row dirt, caller = MAIN.

Then the anticipated fix — swap the gate's `id_root` for the caller's `root`
("the gate takes the caller's root; one call site", CEILING 8) — was applied
literally to the call site (both `_git_toplevel` and both `_ack_seats_dirty`
lines, leaving the commit path on `id_root`), the tests rerun, and the swap
reverted. `git diff --numstat -- extensions/agi/bin/rotate.py` after revert is
empty: **0 production lines shipped**.

## Evidence

Current bytes, all four pass:

```
$ python3 -m pytest extensions/agi/tests/test_rotate.py -k "ack_from_worktree or ack_from_main_own_row" -q
....                                                                     [100%]
4 passed, 321 deselected, 2 warnings in 0.69s
```

With the naive swap applied (gate on the caller's root):

```
>       assert code == 3, out.err
E       AssertionError:
E       assert 0 == 3
.../extensions/agi/tests/test_rotate.py:7554: AssertionError
=========================== short test summary info ============================
FAILED extensions/agi/tests/test_rotate.py::test_ack_from_worktree_sees_main_own_row_dirt
1 failed, 3 passed, 321 deselected, 3 warnings in 1.13s
```

Full file after revert:

```
$ python3 -m pytest extensions/agi/tests/test_rotate.py -q
325 passed, 349 warnings in 59.76s
```

## What the experiment proves

- **Claim (1) is FALSE as code stands.** `_shared_graph_root` always resolves
  MAIN (its own docstring says so), and the gate is evaluated against
  `id_root = _shared_graph_root(Path(root))`. From a worktree, MAIN's own-row
  dirt is REFUSED rc 3 (test 1); the calling worktree's own copy is never
  consulted. The literal claim — "the gate judges the CALLING worktree, never
  MAIN" — is disproved.
- **The anticipated fix is a regression, mechanically.** Nothing writes a
  worktree's `posts.md`/`seats.md` (`_write_identity_cells` routes through
  `_shared_graph_root`), so the worktree copy is stale-but-clean **always**. A
  gate reading it returns `None` unconditionally, and test 1 flips 3 -> 0: the
  ack proceeds while MAIN's own row is mid-edit by another writer, and
  `_ack_commit_seats(id_root=MAIN)` then stages own-row-only content off HEAD
  and overwrites the pre-dirty cell. That is exactly the r3b/g15.24
  double-write this gate exists to prevent. The swap must not ship.
- **Claim (2) holds.** From MAIN `_shared_graph_root(root) == root`, so test 4
  is the same rc-3 refusal as test 1's current-bytes behaviour.
- **Claim (3)'s trigger cannot be `_ack_seats_dirty`.** `_seats_diff_has_own_row`
  runs `git diff [--cached] -- <seats.md rel>` — pathspec-scoped to ONE file —
  and `_diff_owns_row` keys the hunk on the seat's own `name` cell. Test 3
  proves an untracked `tests/test_workflow.py` in the calling worktree does NOT
  block an ack (rc 0). No other dirty/blocking gate exists in `cmd_ack`
  (grep over L2582-3100: the only "dirty" reads are this one gate). So the
  21:00Z `diff` halt was not this code path — it was an agent-level defensive
  answer, not a gate refusal. No production fix was warranted.
- Claim (4)'s first sub-claim ("dirty MAIN + clean worktree -> continue") is
  also false — it refuses by design (test 1). Its second sub-claim is
  self-contradictory: a dirty FOREIGN row never refuses (documented g15.24
  behaviour, `test_ack_foreign_dirty_row_does_not_block`).

## Consequence

No `rotate.py` change. The four tests are the permanent regression net: test 1
is the falsifier that fails the instant anyone swaps the gate to the caller's
root.

## Agent Notes
Gate is evaluated on MAIN (id_root=_shared_graph_root) not the calling worktree; 4 e2e main+worktree tests added. Literal swap to caller root applied-then-reverted: safety test flips 3->0 (MAIN own-row dirt silently ignored, g15.24 double-write protection defeated). 0 production lines; test_rotate.py 325 passed.
