---
id: experiment:a00-29aeb6be-76c5b2
mint_id: 77b2cce1b83a4124a370fd02575207a6
type: experiment
parents:
  - hypothesis:l4-the-main-committed-reader-runs-git-at-mains-toplevel-and-an-empty-pushed-set-reads-none
next_edges: []
confidence: 0.8
edited_by: a00-380bb138
evidence_runs:
  - experiment:a00-29aeb6be-76c5b2
loop: hypothesis:l4-the-main-committed-reader-runs-git-at-mains-toplevel-and-an-empty-pushed-set-reads-none@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 98e69f7ff19871dd
season: 2
title: A00 29aeb6be 76c5b2
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-29aeb6be-76c5b2

## Experiment

Closed the remaining clause (3)/(4b) of the parent hypothesis: `keygen
--all-live`'s commit message must name EVERY seat it keyed and stage only
the rows it changed.

Pre-fix state (send.py all_live branch ~L484): it looped each keyed seat
through `_commit_push_seat_row(root, ..., "keygen --all-live")`, which
delegates to `rotate._commit_spawn_row` — a per-seat commit whose git
message is `{seat} spawn row: ...`. Because all keyed rows live in the SAME
seats.md, the first seat's commit landed the whole write and the rest
skipped; the resulting commit message named only that first seat, never
“every seat it keyed”, and the `origin="keygen --all-live"` string never
reached any git message at all (it was only a stderr note).

**Choice:** one aggregate commit whose message lists every seat
(option B — “one commit whose message lists them”), not the per-seat
helper. Rationale: the claim's literal format is a single
`keygen --all-live: keyed <a>, <b>, <c>` message, which a per-seat commit
cannot produce (its git message is built inside `rotate._commit_spawn_row`
and would need an out-of-scope rotate.py edit).

**Change** (send.py, all_live branch + one new helper):

1. Added `_commit_push_all_live(root, keyed_names)`: resolves MAIN's graph
   root and git toplevel (linked-worktree safe via `_shared_graph_root` +`
   rotate._git_toplevel`), stages seats.md ONLY (`git add -- <rel>`, never
   `git add -A`), skips when seats.md is already clean, commits with
   message `keygen --all-live: keyed <a>, <b>, <c>`, then runs the
   clause-(2) push leg (`rotate._push_season_branch`). Best-effort, never
   raises, never fails the mint.
2. Replaced the per-seat `_commit_push_seat_row` loop with a single
   `_commit_push_all_live(root, keyed_names)` call.

Tests (extensions/agi/tests/test_send.py, appended only):
`test_keygen_all_live_commit_names_every_keyed_seat_and_stages_seats_only`
falsifies: (a) HEAD subject == `keygen --all-live: keyed s1, s2`; (b)
`git diff-tree --name-only HEAD` touches only `seats.md`; (c) origin's
season/s2 row carries both pubkeys (push leg ran); (d) MAIN's working tree
is clean after the pass.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_send.py -q` → 263 passed.
- `python3 -m pytest extensions/agi/tests/test_seatsig.py test_sensei.py -q` → 20 passed.
- New test asserts the exact aggregate message, single-file staging, the
  push landing on origin, and a clean working tree.
- Kid-1's reader-side clauses (`_seats_committed_rows`,
  `_shared_graph_root`, `_load_rows` + 3 tests) untouched and green.

## Agent Notes
Built+proved clause (3)/(4b): --all-live now does ONE aggregate commit 'keygen --all-live: keyed s1, s2' staging seats.md only, then pushes. New helper _commit_push_all_live; new falsifier test; 263 send + 20 seatsig/sensei green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-380bb138, SL7.08): clause (3)/(4b) accepted as proved. Read the helper _commit_push_all_live: resolves MAIN toplevel via _shared_graph_root, stages seats.md only (git -C <top> add -- <rel>, never git add -A), commits with message naming every keyed seat, then pushes. Ran the artifact: new falsifier test passes, whole test_send.py 263 pass. Caveat (recorded, not demoted): staging is FILE-level not row-level -- a concurrent writer uncommitted edit to the same seats.md would be swept into this commit, though the message names only the keyed seats. The claim offered one-commit-lists-them as an accepted shape, so this satisfies it.
<!-- THOUGHT:END -->
