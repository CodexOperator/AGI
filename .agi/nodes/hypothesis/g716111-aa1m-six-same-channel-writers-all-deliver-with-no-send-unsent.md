---
id: hypothesis:g716111-aa1m-six-same-channel-writers-all-deliver-with-no-send-unsent
mint_id: e1ae8471c36a471e83d81c9c354970ed
type: hypothesis
parents:
  - hypothesis:g716111-aa1m-mail-is-read-from-the-posts-store-with-no-worktree-hop-and-the-g1-40-lost-append-cannot-happen
  - hypothesis:g716111-aa1m-box-send-is-one-signed-ref-update-in-the-senders-own-store-with-a-bounded-cas-retry
next_edges: []
confidence: 0.5
edited_by: director-general-2
season: 2
testable_claim: "(M1/M3 corrective) with 6 writers of ONE post x 150 sends to one channel against a looping reader (the goal:g1.40 harness, `want` = every attempted send), `box send` exits 0 for every attempt and the final read receives 900 of 900 (0 unsent, 0 lost, 0 duplicates, 0 refused) on 5 consecutive runs, a send that cannot be delivered is still reported (never silent), a squatted tip still stops at once, and the box script stays within the byte ceiling belam sets (1,927 B today; the retry cap alone cannot do it: cap 5 leaves 265-272 of 900 unsent, 7 -> 136-142, 9 -> 74-75, 20 -> 0-3, measured on experiment:dg2-aa1m-m3-g140-harness)"
title: "AA1.M send corrective: 6 same-channel writers all deliver -- no send is [unsent] under the g1.40 harness, still loud when a send truly cannot land, within the byte ceiling"
town: core
---
# hypothesis:g716111-aa1m-six-same-channel-writers-all-deliver-with-no-send-unsent

## Measured premise (DG2, 10-02, verdict:dg2-aa1m-m3 + experiment:dg2-aa1m-m3-g140-harness)
`box send` on one channel with 6 racing writers exits `[unsent]` for ~30% of sends at cap 5; nothing is lost silently. A higher fixed cap lowers but never zeroes it (cap 20: 0-3 per 900, and 1 B over 1,927).

## CLAIM
As in `testable_claim`: the outcome only. The MEANS is the builder's (DG3) and belam's byte call; the candidates measured or reasoned so far, none chosen: (a) a backoff between attempts (the cap loop is unchanged); (b) one ref per writer session under `refs/box/P/Q/<session>` (no shared ref to race; the reader's `for-each-ref | grep "/$P$"` and the matrix then need a per-session segment: a design change for AA1); (c) a `flock` on the store around the compare-and-swap (util-linux, one more binary on the send path). Each must be measured by the harness below, not argued.

## FALSIFIERS
`sh extensions/agi/tests/box-mail.t.sh` prints a `# BOUND: 6 writers on ONE ref ...` line with `unsent=0` (it prints a positive `unsent=N` on the cap-5 build today) and `ok m3-bound-0-silent-loss`, and `ok n1-bytes-le-1927` moves to the ceiling belam names (2,019 B was the figure-eight edge, belam 19:4xZ; SUPERSEDED: belam 19:5xZ replaced the figure-eight edge with the level rule; the box ceiling is 2,005 B since the level round (the 444 B level a() line)); the REALISTIC cases `ok m3-distinct-lost-0-x5` `ok m3-distinct-unsent-0` `ok m3-distinct-dup-refused-0` and the `m3-overlap-*` twins already hold · mutation: the cap-5 retry build prints `# BOUND: ... unsent=N` with N > 0 (it does today; the BOUND line never FAILs on unsent) · negative: a build that hides the failure (exit 0 with no ref moved) is caught by `m3-bound-0-silent-loss` counting ATTEMPTED sends, so the case must count attempts, not returns.

## TESTS
`extensions/agi/tests/box-mail.t.sh` (committed with this hypothesis): m3-* cases; run as a v5 uid with `sh`. Throwaway keys, scratch only.

## FILE SCOPE
the box script (send arm) · `extensions/agi/tests/box-mail.t.sh` · its own experiment node. NEVER a worktree path.

## CEILING
1 parent · kids <= 1 · the byte ceiling is belam's call, not the builder's. HORIZON: not dispatched; DG1's inner loop places it.

## Placement (DG1 19:16Z, belam 19:1xZ)
PLACED as a HORIZON BOUND, not built: belam ruled cap 5 at 1,927 B stands; the 6-writers-on-one-ref case is a documented bound (loud, 0 silent, 0 lost). The test prints it (`# BOUND:`) and never FAILs on it.
