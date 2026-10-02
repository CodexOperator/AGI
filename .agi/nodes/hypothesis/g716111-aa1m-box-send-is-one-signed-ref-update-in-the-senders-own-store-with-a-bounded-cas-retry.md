---
id: hypothesis:g716111-aa1m-box-send-is-one-signed-ref-update-in-the-senders-own-store-with-a-bounded-cas-retry
mint_id: 002bfa01522c4456b4d1fb2db24f80d5
type: hypothesis
parents:
  - goal:g7.16.1.11.11.1
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 76171befa0582e8b
season: 2
testable_claim: "(M1) `box send Q <msg` (sh + git + jq, no Python) makes ONE signed commit on `refs/box/P/Q` in P's own store after the adjacency and squat checks, advancing the ref by compare-and-swap `update-ref` retried at most 5 times (a squatted tip stops at once and is never retried); 2 senders x 100 sends to one reader that reads in a loop the whole time are 200/200 delivered with 0 duplicates and 0 refused; 2 writers on the SAME channel x 50 are 100/100 delivered with the retry (without it 50 delivered + 50 reported `cannot lock ref`, 0 silent); the box script is <= 1,927 B."
title: "AA1.M send: `box send Q <msg` is ONE signed commit on refs/box/P/Q in the sender's own store, sh + git + jq, with a compare-and-swap update-ref retried at most 5 times; a lost race is reported, never silent; the script is <= 1,927 B"
town: core
---
# hypothesis:g716111-aa1m-box-send-is-one-signed-ref-update-in-the-senders-own-store-with-a-bounded-cas-retry

## Measured
- doc:rse-aa1-boxes section AA1.M (alive, posts/alive; belam [owner] 18:16Z item M1; designed and scratch-tested by alive 18:1xZ); belam ACCEPTED as designed ([decision] 18:2xZ, owner 18:2xZ GO). The numbers are alive's scratch measurements, not re-run by me. HORIZON: the build is not dispatched; each host act is belam's own GO.
- Alive's scratch (two repos = two boxes, one bare hub, throwaway keys, git 2.43): 200/200 · 100/100 with the retry (without: 50 + 50 reported, 0 silent; 42/8 on a re-run) · the 25-case AA1 suite 25/25 after the retry · box 1,927 B (+142 for the retry).

## CLAIM
(M1) `box send Q <msg` (sh + git + jq, no Python) makes ONE signed commit on `refs/box/P/Q` in P's own store after the adjacency and squat checks, advancing the ref by compare-and-swap `update-ref` retried at most 5 times (a squatted tip stops at once and is never retried); 2 senders x 100 sends to one reader that reads in a loop the whole time are 200/200 delivered with 0 duplicates and 0 refused; 2 writers on the SAME channel x 50 are 100/100 delivered with the retry (without it 50 delivered + 50 reported `cannot lock ref`, 0 silent); the box script is <= 1,927 B.

## Dispatch line
config-max: none / template-max: none / code: `box` (the send arm and its retry), a throwaway-key test fixture. NOT dispatched: HORIZON.

## FALSIFIERS
On the real box: 2 senders x 100 to one reading post = 200/200, 0 duplicates, 0 refused, order kept · 2 writers x 50 same channel = 100/100, 0 stderr · a squatted tip prints `[squatted]` and sends nothing, a 5x lost race prints `[unsent]` · negative: `wc -c` of the box script > 1,927, or a Python file on the send path.

## TESTS
the 25-case AA1 suite (shell) on the landing tree; the two concurrency cases above with throwaway keys, scratch only; one mutation: drop the retry and the 2-writer case reports the split (a test that cannot fail is not a test).

## FILE SCOPE
the box script (send arm) · its test file (a .t.sh per the shell-tests rule, goal:g7.16.1.11.16) · its own experiment node. NEVER a worktree path.

## CEILING
1 parent · kids <= 1 · <= 150 script bytes changed vs alive's scratch · regular review. HORIZON.

## Limits (belam [decision] 19:1xZ 10-02)
The retry cap is 5 and the box is 1,927 B, RULED. Past 5 racers on ONE ref (six writers of one post into one channel) a send can exit `[unsent]` (about 30% at 6 racers; loud, 0 silent, 0 lost); distinct senders and the 2-session overlap measured 0 unsent. The numbers and the candidate means are in the Limits of hypothesis:g716111-aa1m-mail-is-read-from-the-posts-store-with-no-worktree-hop-and-the-g1-40-lost-append-cannot-happen.
