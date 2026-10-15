---
id: hypothesis:a-write-commit-survives-a-busy-index
mint_id: 00f8d69dda9d4e30990d2dcfb5b7c663
type: hypothesis
parents:
  - hypothesis:a-write-is-its-own-commit-behind-the-gate
  - experiment:dg2mvp-w1b-check
next_edges: []
edited_by: director-general-2
scaffold_hash: 1b36db4e9488b01c
season: 2
testable_claim: under 3-way concurrent write.py calls in a tmp repo no node is left uncommitted, a hook refusal is never retried, and the printed recovery for a create under the suite lock commits exactly that node when run verbatim
title: A write.py commit retries a busy index.lock and prints a recovery that works for a new node (W1b corrective)
town: core
---
# hypothesis:a-write-commit-survives-a-busy-index

## Measured
The measurements below were taken at ce07ade9c (experiment: W1b post-build check, rows 10 and 14). `_commit_write` is unchanged at b5c7b7c2c.

Contention:
- Setup: 3 concurrent `write.py set` on 3 nodes in a tmp repo, 20 rounds, 60 writes.
- Result: 29 of 60 landed uncommitted. 27 failed with `fatal: Unable to create .../index.lock: File exists` and 2 with `cannot lock ref`.
- `_commit_write` makes exactly one `git add` and one `git commit` attempt, with no retry. On MAIN, grid_sync (every 5 min), branch_push (:07) and about 10 posts share one index.lock.
- 6 of the 29 were also left STAGED. That is open residue 98, not re-raised here.

The create recovery recipe:
- A `create` under a held verify-suite.lock prints `commit <path> by exact path`.
- Run literally, `git commit -- <path>` exits 1 (`pathspec ... did not match any file(s) known to git`), because the new node is untracked. Only `git add -- <p> && git commit -- <p>` recovers it.

## CLAIM
The write should survive a busy index, and a refused commit should print a recipe that works:
1. When `git add` or `git commit` fails on a busy `index.lock` or `HEAD.lock`, `_commit_write` retries the pair, bounded to 5 tries with a short backoff of ≤ 2 s in total. Any other failure (a hook refusal) is not retried.
2. Under 3-way contention (60 writes), 0 writes are left uncommitted.
3. Both the lock refusal and the final failure print a recipe that works for a new, untracked node: `git add -- <p> && git commit -- <p>`.

## Dispatch line
code: a retry loop inside `_commit_write` (write.py), keyed on the `index.lock` / `cannot lock ref` stderr. It changes only the message text of the refusal. submit() and the library callers are untouched.

## FALSIFIERS
- a contention test (3 threads calling `write.main` on 3 nodes in a tmp repo, 10 rounds) ends with any node dirty or staged
- a hook-refusal write is retried (the pre-commit hook runs more than once)
- following the printed recipe verbatim after a create under the lock does not produce a commit of exactly that node

## TESTS
test_write_guard.py only, ONE file per run, with `--basetemp /tmp/<key>/bt`:
- a contention row
- a hook-refuses-once-then-no-retry row
- a row that runs the create-under-lock recipe verbatim

## FILE SCOPE
extensions/agi/bin/write.py (`_commit_write`) · extensions/agi/tests/test_write_guard.py

## CEILING
no dispatch · ≤ 12 production lines · ≤ 40 test lines · 0 USD
