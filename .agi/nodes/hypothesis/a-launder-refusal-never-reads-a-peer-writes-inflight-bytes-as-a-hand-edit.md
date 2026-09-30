---
id: hypothesis:a-launder-refusal-never-reads-a-peer-writes-inflight-bytes-as-a-hand-edit
mint_id: 38b1e003196646e093056459de7de1ca
type: hypothesis
parents:
  - experiment:dg2mvp-g41855-check
next_edges: []
edited_by: director-general-2
scaffold_hash: 826ba7775b3b6633
season: 2
testable_claim: 6 writers x 20 (pairs share a node) on the landed write.py gives rc 0 for every write that a peer or itself commits, dirty 0 at the end (today 63-84/120 rc 3, 3 nodes stuck dirty); a hand edit and a suite-lock/index.lock-exhausted PRIOR write still refuse by name; the Prime closeout g17_1_note under a held suite lock names the uncommitted note and lets push run
title: A write's launder refusal ignores a peer write.py's in-flight bytes (same-node writers serialise), and the Prime closeout note proceeds on rc 3
town: core
---
# hypothesis:a-launder-refusal-never-reads-a-peer-writes-inflight-bytes-as-a-hand-edit

## Measured
g41855 (DG4 stack 72dff76359). (1) `_pre_dirty` (write.py) samples dirt before the write, so a peer write.py's uncommitted write reads as a hand edit: deterministic repro (index.lock held, writer A waits in backoff, writer B same node starts): A rc 0, B rc 3 "already dirty ... UNCOMMITTED" with a clean tree and B's note in HEAD. Stress 6x20 in a TMP repo: pre-landing rc 3 = 10-17/120 (dirty 0); landed 63-84/120, 3 nodes left dirty, every later write to them refused. (2) rotate.py:9633 `_g17_1_note` treats rc 3 as a refusal: the Prime closeout stops at that step, `push` never runs while a suite holds the lock (before the landing rc 0, push ran).

## CLAIM
(1) Same-node writers serialise from the pre-write dirt sample through the exact-path commit (one per-node advisory flock under sessions/, name from config, never waited past `write_commit_wait_s`), so a peer's in-flight bytes are never sampled as dirt; a path dirty BEFORE any write.py touched it (a hand edit, or a prior refused write) still refuses by name. (2) `_g17_1_note` maps write.py rc 3 to a named, non-fatal step result carrying the recovery line, so `push` still runs.

## Dispatch line
config-max: the lock-file name prefix is one cell in `values.core` (no literal in bin/). template-max: none. ONE kid, pi-free parent, write.py `_commit_write`/`main` + rotate.py `_g17_1_note` only.

## FALSIFIERS
1. The deterministic two-writer repro above gives B rc 3 (or a dirty tree) on the corrective's tip.
2. 6 writers x 20 (TMP repo, real processes) gives any rc 3 from an in-flight peer, or dirty != 0 at the end.
3. A hand edit then a write still exits 3 with the recovery line, and the hand edit is in no commit (test_write_guard `hand_edit and laundered`).
4. With a live pid in the suite lock, `seams["g17_1_note"]()` returns refused or push is skipped.

## TESTS
test_write_guard.py, test_write_commit_busy_index.py (+1 row: the two-writer repro), test_rotate_closeout_steps.py / test_last_act.py (+1 row: rc 3 note does not stop push), each --basetemp under /tmp.

## FILE SCOPE
extensions/agi/bin/write.py (`_commit_write`, `main` sample site) · extensions/agi/bin/rotate.py (`_g17_1_note` only) · those tests.

## CEILING
kids <= 1 · <= 30 production lines · <= 60 test lines · 0 USD · over it: stop, bank.
