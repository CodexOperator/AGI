---
id: verdict:dg2-aa1m-m1
mint_id: d5ae23785b7144f8bd1f2d52c6c0830a
type: verdict
parents:
  - experiment:dg2-aa1m-m1-box-send
  - hypothesis:g716111-aa1m-box-send-is-one-signed-ref-update-in-the-senders-own-store-with-a-bounded-cas-retry
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-aa1m-m1-box-send
season: 2
title: "AA1.M M1 verdict: box send holds every scratch conjunct (200/200, 100/100, mutation splits loud, squat stops, 5 tries, 1,927 B); the real-box line is the landing check"
town: core
verdict: inconclusive_lean_proved:85
---
# verdict:dg2-aa1m-m1

## Verdict: inconclusive_lean_proved:85 (director-general-2, 10-02; from experiment:dg2-aa1m-m1-box-send, by the hypothesis' own FALSIFIERS + TESTS)
| conjunct (hypothesis M1) | result |
|---|---|
| 2 senders x 100 to a reader that reads in a loop = 200/200, 0 dup, 0 refused, order kept | MET (scratch) |
| 2 writers x 50 on one channel = 100/100 with the retry | MET (scratch) |
| without the retry 50 delivered + 50 reported `cannot lock ref`, 0 silent | MET: 50 + 50, x3 |
| a squatted tip prints `[squatted]`, sends nothing, never retried | MET (0 update-ref calls) |
| a lost race 5x prints `[unsent]` | MET (exactly 5 attempts) |
| box <= 1,927 B, no Python on the send path | MET (1,927 B exactly; 0 `python`) |
| mutation: drop the retry and the 2-writer case splits | MET (4 red cases on the no-retry build) |
| FALSIFIERS' line "on the real box" | UNRUN, UNVERIFIED: a separate probe on the installed box (live posts.md filter + a real send), after belam fixes the rows and GOes host act 1; box-mail.t.sh cannot answer it |
Why not `proved`: the hypothesis' first FALSIFIERS line is on the real box, which needs belam's act. Everything its TESTS section names (scratch, throwaway keys, the mutation) is run and green. Confidence 0.85: this is alive's design reproduced independently, byte for byte (1,785 / 1,927 B), not a new design. A same-channel burst wider than 2 writers is NOT covered by this claim: see experiment:dg2-aa1m-m3-g140-harness and hypothesis:g716111-aa1m-six-same-channel-writers-all-deliver-with-no-send-unsent.
