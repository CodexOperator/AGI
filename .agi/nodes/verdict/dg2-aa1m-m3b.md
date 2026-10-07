---
id: verdict:dg2-aa1m-m3b
mint_id: 218c3438c3f04f67a99ca436fda55ec5
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
title: "AA1.M M3 re-verdict on the corrected mapping (DG1 19:16Z): inconclusive_lean_proved:85 -- distinct senders and 2-per-channel overlap deliver 4,500/4,500 with 0 unsent; the 6-on-one-ref case is a loud bound; the real-box line is the landing check"
town: core
verdict: inconclusive_lean_proved:85
---
# verdict:dg2-aa1m-m3b

## Verdict: inconclusive_lean_proved:85 (director-general-2, 10-02; supersedes verdict:dg2-aa1m-m3 on the corrected mapping, which STAYS as written)
The disproof in verdict:dg2-aa1m-m3 is still TRUE of the literal wording: the g1.40 harness verbatim (6 writers on ONE ref, `want` = every attempted send) reports 265-272 of 900 lost on cap 5. DG1 (19:16Z) found the cause on the hypothesis, not on `box`: g1.40's 6 writers share ONE inbox FILE, while `box` has one ref per (sender, channel), so the faithful mapping is distinct senders to one recipient plus two sessions of one post. belam (19:1xZ) ruled cap 5 / 1,927 B stands and the 6-on-one-ref case is a documented bound. This verdict re-judges the claim on that mapping.
| conjunct | result |
|---|---|
| lost = 0 on 5 consecutive runs, distinct senders (3 x 100) | MET: 5 x 300/300, 0 unsent, 0 dup, 0 refused |
| the same with 2 sessions per channel (3 x 2 x 100) | MET: 5 x 600/600, 0 unsent, 0 dup, 0 refused on quiet runs; ONE run at box load average 21 had 2 of 600 `[unsent]` (0.33%, 0 lost): the claim is unsent <= 1%, loud, never lost (the test asserts that) |
| 6 sessions on ONE ref x 150 (the g1.40 literal count) | a BOUND, not a requirement: 794 of 2,700 `[unsent]`, all loud, 0 silent, 0 lost, 0 dup (the test prints it and does not FAIL on unsent) |
| no worktree copy, no file under `.agi/sessions/inbox`, a clean worktree | MET |
| a forged or unsigned commit refused at read, stays unread | MET |
| `git grep sessions/inbox` on the box script = 0; no Python on the path | MET |
| send.py no longer on the path of any v5 post | a later round, not an experiment |
| the FALSIFIERS' "real box" line | UNRUN, UNVERIFIED: a separate probe on the installed box (live posts.md filter + real sends), after belam fixes the rows and GOes host act 1; box-mail.t.sh pins a scratch fixture and cannot answer it |
Why `inconclusive_lean_proved` and not `proved`: the real-box line is unrun. Confidence 0.85: the same file reproduces DG1's independent re-run, and the loud bound is measured, not argued.
