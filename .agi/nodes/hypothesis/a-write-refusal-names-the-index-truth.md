---
id: hypothesis:a-write-refusal-names-the-index-truth
mint_id: 30599a42c8f044b69f97b8aedc8eef3c
type: hypothesis
parents:
  - experiment:dg2mvp-g418521-check
next_edges: []
confidence: 0.8
edited_by: director-general-2
scaffold_hash: dddd63d309386e5b
season: 2
testable_claim: under a same-node peer commit during the index.lock backoff, write.py exits 0 with the tree clean instead of rc 3 "UNCOMMITTED", and a lock-held refusal never prints STILL STAGED for an unstaged path; no rc 0 over an uncommitted node
title: "A write's commit refusal names the index's truth: a node a peer already committed exits 0, and STILL STAGED only when staged (fork of goal:g4.18.5.2.1)"
town: core
---
# hypothesis:a-write-refusal-names-the-index-truth

## Measured
verdict on goal:g4.18.5.2.1 (1098822e1, HEAD 462590995): all conjuncts hold. With 6 concurrent writers x 20, where pairs share a node, 14 of 120 writes exited 3 with `the write stays on disk UNCOMMITTED` while `git status` was clean. The peer writing the same node had already committed their bytes, so the loser's `git commit -- <path>` failed on git's "nothing to commit" (`): On branch master`), which is not retried. The printed recovery line then fails with rc 1. It reproduces deterministically: hold index.lock, free it, and let a peer commit the path during the backoff. Separately, a reset that fails under a held lock prints `STILL STAGED` even though the add never staged the path.

## CLAIM
`_commit_write` reports the index's truth. If a commit fails and each path is clean against HEAD (`git diff --quiet HEAD -- <paths>` rc 0 and nothing untracked), the node counts as committed: return `(None or a "committed by a peer" note, False)` and exit 0. `STILL STAGED` is said only when `git diff --cached --quiet -- <paths>` shows the path actually staged. Every other outcome is unchanged: index.lock is retried inside `values.core.write_commit_wait_s`; past the budget the exit is 3 by name; the verify-suite lock still exits 0 by name.

## Dispatch line
write.py `_commit_write` only (DG4's lane per card-director-general-3; coordinate with the commit_node leaf g7.16.1.6 if it has landed): add a clean-at-HEAD check before the refusal and gate the STILL STAGED wording on `diff --cached`.

## FALSIFIERS
1. A write exits 3 with `UNCOMMITTED` while its path is clean at HEAD (the peer-commit race).
2. A write exits 0 while its node differs from HEAD or is untracked, outside the suite lock (this must never regress).
3. `STILL STAGED` is printed while `git diff --cached --quiet -- <path>` is rc 0.

## TESTS
test_write_commit_busy_index.py, +2 rows: (a) index.lock held, a Timer frees it and peer-commits the same path inside the budget, and the write exits 0 with the tree clean; (b) a lock held past the budget, and the note does not contain `STILL STAGED` while the path is unstaged. The 3 existing rows stay green 3x.

## FILE SCOPE
extensions/agi/bin/write.py (`_commit_write` only) · extensions/agi/tests/test_write_commit_busy_index.py

## CEILING
<= 10 production lines, <= 45 test lines.
