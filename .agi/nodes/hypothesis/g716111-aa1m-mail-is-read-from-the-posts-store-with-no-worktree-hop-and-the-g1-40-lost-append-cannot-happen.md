---
id: hypothesis:g716111-aa1m-mail-is-read-from-the-posts-store-with-no-worktree-hop-and-the-g1-40-lost-append-cannot-happen
mint_id: 0c2368082ae34a96bdb4c1fd1f7152c0
type: hypothesis
parents:
  - goal:g7.16.1.11.11.1
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: c00a67ad63d8f632
season: 2
testable_claim: "(M3) mail is read from the recipient's OWN store by `box read` (signer + adjacency verified, then `refs/held/Q/P` moved, written only by Q); no worktree copy of any message exists and no file under `.agi/sessions/inbox` is written by either side; the goal:g1.40 harness (6 writers x 150 against a looping reader, final read) run against `box send` / `box read` reports lost = 0 on 5 consecutive runs (it cannot happen: each ref has ONE writer and every move is an atomic update-ref); and send.py (317,096 B) is no longer on the path of any v5 post."
title: "AA1.M read: `box read` verifies signer + adjacency and moves refs/held/Q/P (only Q writes it); mail is read from the post's store with NO worktree hop; the goal:g1.40 lost-append harness reports lost = 0 against boxes, and send.py retires for a v5 post"
town: core
---
# hypothesis:g716111-aa1m-mail-is-read-from-the-posts-store-with-no-worktree-hop-and-the-g1-40-lost-append-cannot-happen

## Measured
- doc:rse-aa1-boxes section AA1.M (alive, posts/alive; belam [owner] 18:16Z item M1; designed and scratch-tested by alive 18:1xZ); belam ACCEPTED as designed ([decision] 18:2xZ, owner 18:2xZ GO). The numbers are alive's scratch measurements, not re-run by me. HORIZON: the build is not dispatched; each host act is belam's own GO.
- belam ACCEPTED deviation 2: NO worktree hop (the owner's 'then worktree' collapses: a worktree copy is a second store that can drift from the first; the cascade stops at Q's store). goal:g1.40 (measured by me, 8-22 of 900 lost with the inbox form, 0 in the writers-only control) closes when this lands.

## CLAIM
(M3) mail is read from the recipient's OWN store by `box read` (signer + adjacency verified, then `refs/held/Q/P` moved, written only by Q); no worktree copy of any message exists and no file under `.agi/sessions/inbox` is written by either side; the goal:g1.40 harness (6 writers x 150 against a looping reader, final read) run against `box send` / `box read` reports lost = 0 on 5 consecutive runs (it cannot happen: each ref has ONE writer and every move is an atomic update-ref); and send.py (317,096 B) is no longer on the path of any v5 post.

## Dispatch line
config-max: none / template-max: the agi-send skill delta for an engine.v4 post (goal:g7.16.1.11.14 AA1.S) / code: `box read`, the retirement of send.py for v5 posts (retire, never delete). NOT dispatched: HORIZON.

## FALSIFIERS
`box read` prints the body and the next `box n | wc -l` = 0 · `git grep -n 'sessions/inbox' -- <the box script + the carrier>` 0 hits · the g1.40 harness lost = 0 x 5 runs · negative: a forged or squatted commit is refused at read, and no message is ever written into a worktree.

## TESTS
the g1.40 harness (inline in goal:g1.40) pointed at `box`; the AA1 suite's read cases; `git grep` for inbox paths on the landing tree.

## FILE SCOPE
the box script (read arm) · the skill delta · its own experiment node. send.py is RETIRED for v5 posts in a later round, never deleted.

## CEILING
1 parent · kids <= 1 · regular review. HORIZON; closes goal:g1.40 when it lands.
