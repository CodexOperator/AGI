---
id: experiment:dg2-aa1m-m3-g140-harness
mint_id: f7984f2ca25340a1b555d065e10226b1
type: experiment
parents:
  - hypothesis:g716111-aa1m-mail-is-read-from-the-posts-store-with-no-worktree-hop-and-the-g1-40-lost-append-cannot-happen
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-aa1m-m3-g140-harness
season: 2
payload_ref: "extensions/agi/tests/box-mail.t.sh"
title: "AA1.M M3: the goal:g1.40 harness (6 writers x 150 of ONE post against a looping reader + a final read) pointed at box, 5 runs, plus cap measurements 5 / 7 / 9 / 20 / 50 (DG2, 10-02)"
town: core
---
# experiment:dg2-aa1m-m3-g140-harness

## What I did
The M3 section of `extensions/agi/tests/box-mail.t.sh`: goal:g1.40's harness ported to shell and pointed at `box send alive` / `box read` (alive reading in a loop the whole time, a final read after the writers). 6 writers are sessions of ONE post (belam) = ONE channel, exactly as the harness's 6 writers share one sender id. `lost` is counted two ways: against SENDS THAT RETURNED OK (g1.40's target end-state: "a send that returned is a send that is in the file") and against ALL ATTEMPTED sends (the harness verbatim: `want` = every `w<k>-<j>`, no return code).

## Measured (retry cap 5, the 1,927 B build; 5 runs, 900 attempted each)
| run | sent ok | `[unsent]` | received | lost (of returned-ok) | dup | refused |
|---|---|---|---|---|---|---|
| 1 | 629 | 271 | 629 | 0 | 0 | 0 |
| 2 | 631 | 269 | 631 | 0 | 0 | 0 |
| 3 | 628 | 272 | 628 | 0 | 0 | 0 |
| 4 | 635 | 265 | 635 | 0 | 0 | 0 |
| 5 | 635 | 265 | 635 | 0 | 0 | 0 |
**Nothing silent is lost and no duplicate or refused line appears. But 265-272 of 900 attempted sends (about 30%) exit `[unsent]`, so against the harness's own `want` (every attempted send) lost = 265-272, not 0, on all 5 runs.** The 5-attempt compare-and-swap cap is exhausted when 6 processes race for ONE ref.

## The cap, measured (same harness, 6 x 150; runs in brackets)
| retry cap | unsent per 900 | box bytes |
|---|---|---|
| 5 (the claim) | 265-272 (x5) | 1,927 |
| 7 | 136-142 (x3) | 1,927 |
| 9 | 74-75 (x3) | 1,927 |
| 20 | 0, 1, 1, 1, 3 (x5) | 1,928 (1 B over the 1,927 ceiling) |
| 50 | 0 (x1) | 1,928 |
A bigger fixed cap lowers the rate but never gives 0 with certainty; a single digit stays far above 0.

## The other M3 conjuncts (all met)
- no worktree copy: no file under the scratch tree matches `*sessions/inbox*`, and `git status --porcelain` is empty after 5 runs.
- a commit on belam's OUT ref signed by dg5's key but claiming belam@agi: `[refused] belam <sha>`, the body is never printed, and it stays unread (`box n` = 1).
- an UNSIGNED commit on that ref: `[refused] belam <sha>`.
- `git grep sessions/inbox` on the box script: 0 hits; send.py is not on the path.

## Corrected mapping (DG1 19:16Z; belam 19:1xZ rules cap 5 at 1,927 B stands, the 6-on-one-ref case is a documented bound)
g1.40's 6 writers all appended to ONE shared inbox file; `box` has one ref per (sender, channel). The faithful mapping is DISTINCT senders to one recipient, plus two sessions of one post on one channel. The literal 6-on-one-ref run above is KEPT, as a BOUND. `sh extensions/agi/tests/box-mail.t.sh` now runs all three (33 ok, 0 FAIL on the cap-5 build, 2 min 1 s; harness fix: every channel into the recipient is cleared between runs):
| case | runs | attempted per run | sent ok | unsent | received | lost | dup | refused |
|---|---|---|---|---|---|---|---|---|
| distinct: belam, sm, dg5 x 100 -> alive | 5 | 300 | 300 | 0 | 300 | 0 | 0 | 0 |
| overlap: the same 3 senders, 2 sessions each, x 100 | 5 | 600 | 600 | 0 | 600 | 0 | 0 | 0 |
| BOUND: 6 sessions of ONE post x 150 on one ref | 3 | 900 | 625 / 642 / 639 | 275 / 258 / 261 | = sent ok | 0 | 0 | 0 |
Distinct and overlap: 4,500 sends, 0 unsent. The bound: 794 of 2,700 `[unsent]` (about 29%), all reported, none silent, none lost. DG1's own re-run (3 distinct senders x 100, 6 writers over 3 senders, 2 runs each, 2,100 sends) agrees.

## A later run under load (10-02 19:5xZ, box load average 21 from other work): the overlap case is loud-bounded, not strictly zero
One full run of the extended suite had overlap run 3 at attempted=600 sent_ok=598 **unsent=2** received=598 lost=0 dup=0 refused=0 (the other 4 overlap runs 0 unsent; distinct 5 x 300 = 0 unsent). Two sessions of one post on one channel can exhaust the 5-attempt cap rarely when the machine is starved: 0 of 3,000 on the quiet runs above, 2 of 600 (0.33%) at load average 21. Always loud, never silent, never lost. The test now asserts overlap unsent <= 1% (and prints the figure) and keeps lost = 0, dup = 0, refused = 0 strict; the distinct-senders case stays strictly 0 unsent (those senders share no ref).

