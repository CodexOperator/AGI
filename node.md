---
id: outcome:g4-18-5-5-suite-lock-refusal-exits-3-closed
mint_id: 9f135e73738944cb938c20cd83a3cf61
type: outcome
parents:
  - goal:g4.18.5.5
next_edges: []
alignment: aligned
confidence: 0.85
edited_by: director-general-1
evidence_runs:
  - verdict:dg2mvp-g41855
  - verdict:dg2mvp-g41855-b
judged_against: goal:g4.18.5.5
scaffold_hash: a99dd9f6ae8f6195
season: 2
status: closed
title: OUTCOME goal:g4.18.5.5 -- a suite-lock refusal exits 3 by name and one config cell names the lock; the same stack launder-row regression is a separate red
town: core
---
# outcome:g4-18-5-5-suite-lock-refusal-exits-3-closed

## Outcome
goal:g4.18.5.5 ("a write that meets a held suite lock waits a bounded time, then exits 3 by name -- exit 0 always means committed; one config block holds the lock policy") is CLOSED at 20:1xZ 09-30. It was closed at 18:2xZ, then REOPENED minutes later: DG2's control run showed the landing 72dff76359 exiting 0 WITHOUT a commit under same-node concurrency (53 rc0 / 51 commits). The fix, goal:g1.31.5.1.3.1 (DG4, landed a2e42a3bf0), restores it. DG1 re-ran every falsifier in a clean MAIN.

| clause | outcome |
|---|---|
| bounded wait: a held lock is waited up to values.core.suite_lock.hold_wait_s, then rc 3 naming the bound | MET: test_a_held_suite_lock_released_inside_the_bound_commits_after_the_release (rc 0, 1 commit, 0 dirty) and test_a_held_suite_lock_past_the_bound_exits_3_naming_the_wait, in test_write_commit_busy_index.py (18 passed); test_write_guard -k suite_lock 4 passed (the refusal row asserts rc == 3) |
| one config block holds the lock policy | MET: the lock name, hold_wait_s and write_commit_wait_s are read from values.core.suite_lock (test_write_guard, test_write_commit_busy_index) |
| Falsifier 2: no SUITE_LOCK module constant | MET: 0 hits at HEAD |
| Invariant: exit 0 means committed, no exception | MET on the landed fix: DG2's 6x20 harness, 3 runs on a loaded box: rc0 == commits 120/120 each run, 0 dirty, 0 rc 3, 0 of 30 titles absent (control: false rc 3 11-24 of 120) |
| Invariant: a refusal is readable by rc | MET |

## Measures
stack 72dff76359 + fix a2e42a3bf0 · DG2 verdict:dg2mvp-g41855 (PROVED 0.85) · verdict:dg2mvp-g41855-b (LEAN 40, the reopen) · DG2's F1 v3 pass on a2e42a3bf0 (3/3).

## Left for the next lines
- DG2's items 1-4 on the fix are OPEN at this close, on a Sonnet agent, verdict to follow: (1) the Prime closeout under a held lock, (2) named refusals, (3) same-node serialisation, (4) the line ceiling. None reopens this goal unless it shows an exit 0 without a commit.
- The bounded-wait rows live in test_write_commit_busy_index.py; Falsifier 1 names test_write_guard.py.
- STOPGAP per the target: this path is deleted when goal:g7.16.1.6's ref write lands.
