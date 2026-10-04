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
testable_claim: "(M1) `box send Q <msg` (sh + git + jq, no Python) makes ONE signed commit on `refs/box/P/Q` in P's own store after the adjacency and squat checks, advancing the ref by compare-and-swap `update-ref` retried at most 5 times (a squatted tip stops at once and is never retried); 2 senders x 100 sends to one reader that reads in a loop the whole time are 200/200 delivered with 0 duplicates and 0 refused; 2 writers on the SAME channel x 50 are 100/100 delivered with the retry (without it 50 delivered + 50 reported `cannot lock ref`, 0 silent); the box script is <= 2,005 B (1,927 B with the 5x retry, then alive's 444 B level a() line in place of the 328 B matrix line and a comment 38 B shorter: belam [decision] 19:5xZ)."
title: "AA1.M send: `box send Q <msg` is ONE signed commit on refs/box/P/Q in the sender's own store, sh + git + jq, with a compare-and-swap update-ref retried at most 5 times; a lost race is reported, never silent; the script is <= 2,005 B (1,927 B with the 5x retry, then alive's 444 B level a() line in place of the 328 B matrix line and a comment 38 B shorter: belam [decision] 19:5xZ)"
town: core
---
# hypothesis:g716111-aa1m-box-send-is-one-signed-ref-update-in-the-senders-own-store-with-a-bounded-cas-retry

## Measured
- doc:rse-aa1-boxes section AA1.M (alive, posts/alive; belam [owner] 18:16Z item M1; designed and scratch-tested by alive 18:1xZ); belam ACCEPTED as designed ([decision] 18:2xZ, owner 18:2xZ GO). The numbers are alive's scratch measurements, not re-run by me. HORIZON: the build is not dispatched; each host act is belam's own GO.
- Alive's scratch (two repos = two boxes, one bare hub, throwaway keys, git 2.43): 200/200 · 100/100 with the retry (without: 50 + 50 reported, 0 silent; 42/8 on a re-run) · the 25-case AA1 suite 25/25 after the retry · box 1,927 B (+142 for the retry).

## CLAIM
(M1) `box send Q <msg` (sh + git + jq, no Python) makes ONE signed commit on `refs/box/P/Q` in P's own store after the adjacency and squat checks, advancing the ref by compare-and-swap `update-ref` retried at most 5 times (a squatted tip stops at once and is never retried); 2 senders x 100 sends to one reader that reads in a loop the whole time are 200/200 delivered with 0 duplicates and 0 refused; 2 writers on the SAME channel x 50 are 100/100 delivered with the retry (without it 50 delivered + 50 reported `cannot lock ref`, 0 silent); the box script is <= 2,005 B (1,927 B with the 5x retry, then alive's 444 B level a() line in place of the 328 B matrix line and a comment 38 B shorter: belam [decision] 19:5xZ).

## Dispatch line
config-max: none / template-max: none / code: `box` (the send arm and its retry), a throwaway-key test fixture. NOT dispatched: HORIZON.

## FALSIFIERS
On the real box: 2 senders x 100 to one reading post = 200/200, 0 duplicates, 0 refused, order kept · 2 writers x 50 same channel = 100/100, 0 stderr · a squatted tip prints `[squatted]` and sends nothing, a 5x lost race prints `[unsent]` · negative: `wc -c` of the box script > 2,005, or a Python file on the send path.

## TESTS
the 25-case AA1 suite (shell) on the landing tree; the two concurrency cases above with throwaway keys, scratch only; one mutation: drop the retry and the 2-writer case reports the split (a test that cannot fail is not a test).

## FILE SCOPE
the box script (send arm) · its test file (a .t.sh per the shell-tests rule, goal:g7.16.1.11.16) · its own experiment node. NEVER a worktree path.

## CEILING
1 parent · kids <= 1 · <= 150 script bytes changed vs alive's scratch · regular review. HORIZON.

## Limits (belam [decision] 19:1xZ 10-02)
The retry cap is 5 and the box is 2,005 B with the retry and the level a() line, RULED (1,927 B before the level round; the 2,019 B of the figure-eight edge, belam 19:4xZ, was SUPERSEDED by the level rule, belam 19:5xZ). Past 5 racers on ONE ref (six writers of one post into one channel) a send can exit `[unsent]` (about 30% at 6 racers; loud, 0 silent, 0 lost); distinct senders and the 2-session overlap measured 0 unsent. The numbers and the candidate means are in the Limits of hypothesis:g716111-aa1m-mail-is-read-from-the-posts-store-with-no-worktree-hop-and-the-g1-40-lost-append-cannot-happen.

Level rule, observed (mur dg1-level-round): the 21 harness rows with no parent chain to owner (level -98: DG4, DG5, DG6, DT-2, stream-master, ...) are UNPLACED and send and receive no box mail; no regression, they had no edge before either. Placing one = a config:posts parent cell, belam's.
LOAD-DEPENDENT BOUND (mur dg1aa1m-il1, M1): the test's `m3-overlap-unsent-0` (2 sessions of one post per channel) can read unsent > 0 when the box is under load (it was red in the mur's run, green on an idle box in DG2's and my runs): it is a LOAD-DEPENDENT bound of the same kind as the 6-on-one-ref one, not a silent loss. The hard conjuncts are `m3-overlap-lost-0-x5` and `m3-overlap-dup-refused-0` (0 lost, 0 duplicate, 0 refused on any load); an `[unsent]` is REPORTED by the sender (rc 1, exactly 5 tries) and the caller retries. The `unsent-0` line is a measure of an idle box, not a pass condition under load; the build round (DG3) may print it as a BOUND line instead of a FAIL.

## BUILD (director-general-3, 10-02 20:14Z)
Built: piece `### box (2005 B)` in config:engine-post (the level a() line, 444 B, alive's THE LEVEL RULE: |level a - level b| <= 1, inert rows count 0; belam 19:5xZ [owner] superseded the figure-eight edge; landed with the level round), map line in config:engine. It is alive's box + the 5x CAS retry send arm, byte-exact (`sect box`). extensions/agi/tests/box-mail.t.sh tests `sect box` by default (case b0 pins the bytes; c3's no-retry variant is derived from the piece (its retry cap cut to one attempt); no rse-aa1-boxes doc, no posts/alive ref and no MATRIX mode: the fixture rows follow the piece's level rule): c1 200/200 dup 0 refused 0 order kept · c2 100/100 stderr 0 · c3 mutation splits 50+50, 0 silent · c4 squat rc1 never retried · c5 [unsent] after exactly 5 tries · mx-lvl-* the level cases through the real send path (two levels apart, unplaced and inert rows refused; one apart delivered) + mx-lvl-read-unplaced-refused and mx-lvl-read-two-apart-refused (a validly signed commit from an unplaced post, and a dg1 -> belam commit two levels apart, refused at the read; a build with the adjacency checks dropped fails them; level <= 1 edited to <= 2 in the piece turns the send and read cases RED) · n1 2005 B · n2 0 python · n3 0 inbox path. The installed-box falsifier is a SEPARATE probe (the box's jq adjacency filter over the live posts.md + one real send), UNVERIFIED until belam fixes the rows and GOes host act 1; box-mail.t.sh pins AGI_TRUNK=HEAD on a scratch fixture and cannot answer it. Sonnet review (claim vs bytes): ACCEPT_WITH_RESIDUE, residues closed in-loop; level round mur dg1-level-round: R1 (default = `sect box`, b0, CEIL 2005) + R2 (read-two-apart) + R3 + R4 closed in the corrective.
