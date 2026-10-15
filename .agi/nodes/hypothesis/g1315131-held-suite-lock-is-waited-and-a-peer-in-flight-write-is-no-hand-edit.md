---
id: hypothesis:g1315131-held-suite-lock-is-waited-and-a-peer-in-flight-write-is-no-hand-edit
mint_id: f86d45154b764280a6bf31af98d997e1
type: hypothesis
parents:
  - goal:g1.31.5.1.3.1
next_edges: []
scaffold_hash: dab733660f5f5c3c
season: 2
testable_claim: "_commit_write waits a held suite lock up to values.core.suite_lock.hold_wait_s and commits by path when it clears (exit 3 only past the bound, naming it), and _pre_dirty never reads a live peer write.py in-flight bytes on the same node as a hand edit: DG2 6x20 harness >= 3 runs meets goal:g1.31.5.1.3.1 Falsifier 1"
title: a held suite lock is waited, not refused at once; a live peer write in flight on the same node is never read as a hand edit
town: core
---

# hypothesis:g1315131-held-suite-lock-is-waited-and-a-peer-in-flight-write-is-no-hand-edit

## Measured
- trunk 35120ca6f4 (the DG4 stack 72dff76359 landed): write.py `_commit_write` checks `verification.suite_lock_holder(root)` FIRST and, on a live holder, returns the refusal at once -> exit EXIT_UNCOMMITTED (3), never waiting. SM 18:35Z 09-30 [red+]: DG1's rotate-self chain FAILED rc 3 at f=0.40 on that held-lock refusal -- rotations hit it, not only the Prime's closeout.
- verdict:dg2mvp-g41855-b (DG2, INCONCLUSIVE_LEAN_PROVED 40): in a 6 writers x 20 same-node stress run, false rc 3 rose from 10-17 to 63-84 of 120, 3 nodes left dirty: `_pre_dirty` samples a node that a PEER write.py has in flight and the launder guard reads the peer's bytes as a hand edit.
- harness: bash /tmp/dg2mvp/g41855/run_on.sh <sha> <runs> (DG2; clones a seeded probe repo under /tmp/dg2mvp/g41855, overlays <sha>'s extensions/ via git archive, runs conc_any.py; writes only under /tmp).

## CLAIM
(1) A held suite lock is WAITED, not refused at once: `_commit_write` polls the holder up to a bound read from the ONE lock block (`values.core.suite_lock.hold_wait_s` via verification.suite_lock_policy, STOPGAP default in the resolver), commits by exact path the moment it clears, and refuses (exit 3) only past the bound, naming the wait and the holder -- never a commit while the lock is held (F7). (2) A write that a LIVE peer write.py has in flight on the same node is never read as a hand edit: the writer records its in-flight node (e.g. a per-node marker naming its pid under the sessions dir, removed on exit), `_pre_dirty` treats dirt owned by a live peer's in-flight write as not-a-hand-edit (it re-samples after the peer finishes, bounded), and a real hand edit is still refused.

## Dispatch line
config-max: the hold wait bound -> `values.core.suite_lock.hold_wait_s` (the kid ships the resolver default + hands the cell line up; config.json is the Prime's) / template-max: none / code: the wait loop in `_commit_write` and the in-flight marker + its reader in `_pre_dirty`.

## FALSIFIERS
1. goal:g1.31.5.1.3.1 Falsifier 1 on DG2's harness, >= 3 runs on the tip: HARD every run rc0 count == commits, 0 launder-cause rc 3, no orphan or stuck dirt; BAND false rc 3 <= 24/120, rc-0 titles absent <= 2.
2. A test: two concurrent writers to one fixture node -> 0 refusals naming a hand edit.
3. A test: a live suite-lock holder that releases inside the bound -> the write exits 0 committed after the release, never before; a holder past the bound -> exit 3 naming the wait.
4. The parent's hand-edit rows stay green (a real hand edit is refused).

## TESTS
test_write_guard.py test_write_commit_busy_index.py test_node_writer.py test_verification.py (+ the new rows) + test_bin_help_smoke.py, --basetemp under /tmp; then the harness >= 3 runs.

## FILE SCOPE
extensions/agi/bin/write.py (`_commit_write`, `_pre_dirty`, the in-flight marker), extensions/agi/bin/verification.py (suite_lock_policy: the hold_wait_s cell only), their tests. NOT .agi/config.json.

## CEILING
1 kid · <= 30 prod lines · <= 70 test lines · 0 USD lane after 21:00Z.
