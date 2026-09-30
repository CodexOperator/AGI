---
id: goal:g1.31.5.1.3
mint_id: b5e2fcf0f5bf4f89948e7617313ff305
type: goal
parents:
  - goal:g1.31.5.1
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.5.1.3
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 9b8f58dfc702fd11
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - pass-b3
  - missed
  - red
  - write.py
title: "G1.31.5.1.3: write.py _commit_write refuses to commit a path already dirty before the write, so a same-path hand edit stays visible to write_guard"
town: core
---
# goal:g1.31.5.1.3

## Why this exists
goal:g1.31.5.1: PASS B3 round `engine-delta-5`, verify file `.agi/sessions/workflows/runs/mur-pb3chunk3of20/verify_engine-delta-5.json`, `missed` row n83 (red: a shipped guard can be laundered). Re-read at HEAD d4b7ead17:
```
hand edit to node X (any post, shared worktree)
write.py <X> '<verb>'  -> read-modify-write of X (the hand edit rides along)
  _commit_write (write.py:4053)  :4088 git add -- X   :4089 git commit -m 'write.py: X' -- X
     commits the WORKTREE bytes of X, not only this write's delta
write_guard.py:79  git diff --name-only HEAD  -> X no longer listed  -> hand edit invisible
test_write_guard.py:674-680  pins only the ADJACENT case (another post's staged other.txt); same-path race untested
```

## Target end-state
- `extensions/agi/bin/write.py` `_commit_write` (:4053) commits a path only when its bytes before the write equalled HEAD's, or when this write created the path. If a path was already dirty against HEAD before the write, the write lands, stays UNCOMMITTED and is refused by name (exit `EXIT_UNCOMMITTED`, recovery line printed), so `write_guard.py check` still lists it.
- A committed test in `extensions/agi/tests/test_write_guard.py` runs in a tmp project: hand-edit node X, run `write.main([... X ...])`, then assert that `git diff --name-only HEAD` still lists X and that no commit carries the hand-edit line. A control row asserts that a clean X still becomes ONE exact-path commit (the `test_b4_w1b_every_write_verb_is_its_own_exact_path_commit` contract).

## Invariants
- A residue is closed by a reviewed round, never by a note.
- One writer per function: `_commit_write` is DG4's granted region (SM 09-30), next to DG4's hypothesis:a-write-refusal-names-the-index-truth. Both land from one post.
- `git commit -- <paths>` is still exact-path. `-a` is never used, and another post's staged file is never swept in.

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_write_guard.py -q -k 'hand_edit and laundered' --basetemp /tmp/g13151c` passes with ≥ 1 selected (rc 5 at HEAD d4b7ead17: no such test).
2. Negative: in that test's tmp project, `git grep -n HANDEDIT-FIXTURE HEAD -- .agi/nodes` returns zero hits after the refused write. The commit carries none of the hand-edit bytes.

## Out of scope
hypothesis:a-write-refusal-names-the-index-truth (DG4's own round in the same function; not this row) · goal:g1.31.5.1.1 · goal:g1.31.5.1.2 · goal:g1.31.5.2-.5 · goal:g1.31.1-.4 · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-4**.
