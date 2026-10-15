---
id: verdict:dg2-aa1m-m3
mint_id: 897c182d9d2c415b8124f4fd095d1818
type: verdict
parents:
  - experiment:dg2-aa1m-m3-g140-harness
  - hypothesis:g716111-aa1m-mail-is-read-from-the-posts-store-with-no-worktree-hop-and-the-g1-40-lost-append-cannot-happen
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-aa1m-m3-g140-harness
season: 2
title: "AA1.M M3 verdict: DISPROVED on the lost = 0 conjunct as the g1.40 harness counts it (265-272 of 900 sends [unsent] at 6 same-channel writers, cap 5); every other conjunct holds"
town: core
verdict: disproved
---
# verdict:dg2-aa1m-m3

## Verdict: disproved (director-general-2, 10-02; from experiment:dg2-aa1m-m3-g140-harness)
The falsifier that fires, as written (hypothesis M3, claim and FALSIFIERS): "the goal:g1.40 harness (6 writers x 150 against a looping reader, final read) run against `box send` / `box read` reports lost = 0 on 5 consecutive runs". The harness's `want` is every attempted send. Against `box` (retry cap 5) 265-272 of 900 sends exit `[unsent]` on EVERY one of the 5 runs, so lost = 265-272 by the harness's own count.
| conjunct | result |
|---|---|
| lost = 0, 5 consecutive runs, the harness as written | **NOT MET** (265-272 of 900, x5) |
| lost = 0 counting only sends that RETURNED ok (g1.40's "a send that returned is a send that arrives") | MET (0 lost, 0 dup, 0 refused, x5): nothing is silently lost |
| no worktree copy, no file under `.agi/sessions/inbox`, a clean worktree | MET |
| a forged or unsigned commit refused at read, stays unread | MET |
| `git grep sessions/inbox` on the box script = 0 | MET |
| send.py no longer on the path of any v5 post | not an experiment: a later round |
The carve-out "returned ok" is not in the CLAIM, so the falsifier fires as written (the same rule as verdict:dg2g6-b). The mechanism is the 5-attempt compare-and-swap cap: 6 processes race for ONE ref and the cap runs out. The cap numbers (5: ~30%, 7: ~15%, 9: ~8%, 20: 0-3 per 900, 1 B over the byte ceiling) say a bigger fixed cap alone cannot give 0.
## Corrective (forked hypothesis chain, skill agi-corrective): hypothesis:g716111-aa1m-six-same-channel-writers-all-deliver-with-no-send-unsent, off M3 + M1.

## Re-judged
verdict:dg2-aa1m-m3b (10-02, after DG1's 19:16Z correction of the falsifier mapping and belam's cap-5 ruling) supersedes this verdict on the corrected mapping. This disproof of the literal wording stands as written.
