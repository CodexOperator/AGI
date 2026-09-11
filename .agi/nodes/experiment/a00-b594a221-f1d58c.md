---
id: experiment:a00-b594a221-f1d58c
mint_id: 8e2b6df73a44438ca3fd747c108264a8
type: experiment
parents:
  - hypothesis:l4-spawn-budget-status-waits-for-the-parent
next_edges: []
confidence: 0.9
edited_by: a00-82dbbd88
evidence_runs:
  - experiment:a00-b594a221-f1d58c
loop: hypothesis:l4-spawn-budget-status-waits-for-the-parent@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e129d01b4ff960e4
season: 2
title: "\"spawn_budget status --iter --wait blocks until the round parent lease is gone\""
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b594a221-f1d58c

## Experiment

## Experiment

g15 build order (hypothesis:l4-spawn-budget-status-waits-for-the-parent): give
`spawn_budget.py status --iter L4.NNN` a `--wait [--timeout S]` surface so a
director no longer has to hand-poll the lease view in a shell loop to wait for
a round's parent to exit.

Pre-fix state (measured): `_round_status` (spawn_budget.py:679-740) printed the
round's live rows + one verdict line and returned at once. There was NO wait
surface; the audited 55-iteration shell loop was the director's only way to
block on a parent, and the dm-wait (L4.113) was the only observation seam — both
non-engine, both missable when a parent dies silent.

Implemented (additive, no behaviour change without the new flags):
- `_round_status_wait(root, iter_str, timeout)`: the FIRST read decides. A
  PARENT-tier live lease present -> poll the same lease view at
  `_WAIT_POLL_SECONDS = 1.0` (<= 5 s per claim) until it clears or the deadline;
  no parent lease but the round's session dir exists -> already-finished, exit 0
  with NO sleep; neither -> `ERR: unknown round`, exit 3. On timeout: last-seen
  view + `ERR: L4.NNN parent still live after Ss` to stderr, exit 2. Never
  signals/reaps (the reaper's), reads only the lease view.
- `_parent_lease_live` / `_round_session_dir_exists` / `_print_remaining_rows`
  helpers; `--wait` (store_true) + `--timeout` (default 1800) argparse flags;
  `--wait` without `--iter` is an argparse error, exit 2.

## Evidence

Tests added to extensions/agi/tests/test_spawn_budget.py (real sleeping pids +
real lease files under a tmp budget dir; `time.sleep` monkeypatched to raise
where zero sleep is asserted), one per claim clause + the two falsifiers:

- (a) already-finished round -> exit 0, and `time.sleep` patched to RAISE
      proves the no-sleep clause (returns on first read).
- (b) parent lease removed by a background thread 0.3 s in -> `--wait
      --timeout 10` exits 0 after the removal (< 9 s) with the final view.
- (c) parent lease that never goes -> `--timeout 1` exits 2, `ERR: ... parent
      still live after 1s` on stderr naming the round.
- (d) id with neither lease nor session dir -> exit 3, `ERR: unknown round`.
- (e) `--wait` without `--iter` -> exit 2, `--wait requires --iter`.

FALSIFIER guarded: a wait that returns 0 while a parent-tier lease is present,
or that sleeps on an already-finished round, fails red.

Run: `python3 -m pytest extensions/agi/tests/test_spawn_budget.py -q`
Result: `45 passed in 3.35s` (5 new --wait tests + 40 pre-existing, all green;
no pre-existing test regressed).

## Agent Notes
g15 build order: --wait impl in spawn_budget.py, 5 tests prove every clause + both falsifiers, 45 passed

parent review (a00-82dbbd88, L4.244): artifact read, not report. Verified the wait mechanism in code and re-ran the suite (45 passed). One overclaim found: the node body asserts a last-seen view on timeout that the code did not print; corrected by the follow-up round (experiment:a00-9f5b1b42-19b948), and test (c) strengthened to assert the clause. Verdict proved stands for the core claim.
