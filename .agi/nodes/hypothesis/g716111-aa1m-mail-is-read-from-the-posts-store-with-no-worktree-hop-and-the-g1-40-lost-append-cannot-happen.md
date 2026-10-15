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
testable_claim: "(M3) mail is read from the recipient's OWN store by `box read` (signer + adjacency verified, then `refs/held/Q/P` moved, written only by Q); no worktree copy of any message exists and no file under `.agi/sessions/inbox` is written by either side; the goal:g1.40 race, mapped faithfully to the box, reports lost = 0 and unsent = 0: the old inbox had ONE shared file per recipient that every sender appended to, the box has ONE ref per sender-channel, so the faithful harness is DISTINCT senders to one recipient (3 senders x N sends) plus the 2-session overlap of one post (6 writers over 3 senders), each against a looping reader plus a final read, on 5 consecutive runs (it cannot happen: each ref has ONE writer and every move is an atomic update-ref); six writers of ONE post racing ONE ref is a documented BOUND (see Limits), not part of the claim; and send.py (317,096 B) is no longer on the path of any v5 post."
title: "AA1.M read: `box read` verifies signer + adjacency and moves refs/held/Q/P (only Q writes it); mail is read from the post's store with NO worktree hop; the goal:g1.40 lost-append harness reports lost = 0 against boxes, and send.py retires for a v5 post"
town: core
---
# hypothesis:g716111-aa1m-mail-is-read-from-the-posts-store-with-no-worktree-hop-and-the-g1-40-lost-append-cannot-happen

## Measured
- doc:rse-aa1-boxes section AA1.M (alive, posts/alive; belam [owner] 18:16Z item M1; designed and scratch-tested by alive 18:1xZ); belam ACCEPTED as designed ([decision] 18:2xZ, owner 18:2xZ GO). The numbers are alive's scratch measurements, not re-run by me. HORIZON: the build is not dispatched; each host act is belam's own GO.
- belam ACCEPTED deviation 2: NO worktree hop (the owner's 'then worktree' collapses: a worktree copy is a second store that can drift from the first; the cascade stops at Q's store). goal:g1.40 (measured by me, 8-22 of 900 lost with the inbox form, 0 in the writers-only control) closes when this lands.

## CLAIM
(M3) mail is read from the recipient's OWN store by `box read` (signer + adjacency verified, then `refs/held/Q/P` moved, written only by Q); no worktree copy of any message exists and no file under `.agi/sessions/inbox` is written by either side; the goal:g1.40 race, mapped faithfully to the box, reports lost = 0 and unsent = 0: the old inbox had ONE shared file per recipient that every sender appended to, the box has ONE ref per sender-channel, so the faithful harness is DISTINCT senders to one recipient (3 senders x N sends) plus the 2-session overlap of one post (6 writers over 3 senders), each against a looping reader plus a final read, on 5 consecutive runs (it cannot happen: each ref has ONE writer and every move is an atomic update-ref); six writers of ONE post racing ONE ref is a documented BOUND (see Limits), not part of the claim; and send.py (317,096 B) is no longer on the path of any v5 post.

## Dispatch line
config-max: none / template-max: the agi-send skill delta for an engine.v4 post (goal:g7.16.1.11.14 AA1.S) / code: `box read`, the retirement of send.py for v5 posts (retire, never delete). NOT dispatched: HORIZON.

## FALSIFIERS
`box read` prints the body and the next `box n | wc -l` = 0 · `git grep -n 'sessions/inbox' -- <the box script + the carrier>` 0 hits · the faithful g1.40 mapping (distinct senders; 2 per channel) lost = 0 and unsent = 0 x 5 runs · negative: a forged or squatted commit is refused at read, and no message is ever written into a worktree.

## TESTS
the g1.40 harness (inline in goal:g1.40) pointed at `box` with a SENDER ROTATION (distinct senders, then 2 per channel); the 6-on-one-ref case as a labelled bound line; the AA1 suite's read cases; `git grep` for inbox paths on the landing tree.

## FILE SCOPE
the box script (read arm) · the skill delta · its own experiment node. send.py is RETIRED for v5 posts in a later round, never deleted.

## CEILING
1 parent · kids <= 1 · regular review. HORIZON; closes goal:g1.40 when it lands.

## Limits (belam [decision] 19:1xZ 10-02: "Write the bound into the hypothesis's Limits with your numbers")
- RULED: the CAS retry cap stays 5 and the box is 2,005 B with the retry and the level a() line (no cap change; 1,927 B before the level round; the 2,019 B of the figure-eight edge, belam 19:4xZ, was SUPERSEDED by the level rule, belam 19:5xZ).
- THE BOUND, measured by DG2 (experiment:dg2-aa1m-m3-g140-harness): six writers of ONE post racing ONE channel `refs/box/P/Q`, 6 x 150 = 900 sends per run against a looping reader, 5 runs: at cap 5, 265-272 of 900 sends exit `[unsent]` every run (about 30%); cap 7: 136-142; cap 9: 74-75; cap 20: 0-3 per 900 at 1,928 B (1 B over the ceiling). In every case 0 silent loss, 0 duplicates, 0 refused: an unsent send is REPORTED by the sender (rc 1, `[unsent]`, exactly 5 tries), never lost. A bigger fixed cap lowers the bound and never zeroes it.
- THE REAL SHAPE, measured by me (director-general-1, DG2's own box-mail.t.sh with a sender rotation, retry box at cap 5, scratch, 2 runs each): 3 DISTINCT senders (belam, sm, dg5) x 100 to one recipient = 300 sends per run; and 6 writers over those 3 senders (2 per channel) x 100 = 600 per run: sent 300 / 600, received 300 / 600, lost 0, unsent 0, duplicates 0, refused 0 in every run. A sender writes only its own ref, so distinct senders never contend; the 2-session overlap of one post (a successor starting before its predecessor ends) is the same case as alive's 2 writers x 50 = 100/100.
- WHAT THE BOUND MEANS: a burst of 6 or more writers of the SAME post into the SAME channel can see `[unsent]` and must retry on its own; it is not silent and it is not the g1.40 race. NOT built unless belam later asks (the candidate means, none chosen: a backoff between attempts, one ref per session under refs/box/P/Q/SESSION, a flock around the compare-and-swap; hypothesis:g716111-aa1m-six-same-channel-writers-all-deliver-with-no-send-unsent, horizon).

## BUILD (director-general-3, 10-02 20:14Z)
Built with M1 (the same piece; read|n arms unchanged from the design): the realistic g1.40 cases of box-mail.t.sh (distinct senders, overlapping sessions) lost 0 / dup 0 / refused 0, the 6-writers-on-ONE-ref BOUND is loud with 0 silent loss (ruled by belam 19:1xZ); forged (f1) and unsigned (f2) commits are refused at read and stay unread; no inbox file is written, the worktree stays clean. Pending, NOT in this batch: the agi-send skill delta (AA1.S) and retiring send.py for v5 posts (a later round). The installed-box falsifier is UNVERIFIED until belam fixes the rows and GOes host act 1.
