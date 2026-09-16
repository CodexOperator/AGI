---
id: hypothesis:l4-sl04-residue-ack-and-latch-fixes
mint_id: 44bbd915f2da444982d5797a237e5662
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: e866d53f546b9fdc
season: 2
testable_claim: "SL.04 review residue (belam 07:27Z, ACCEPT WITH RESIDUE on merge-up range a0c6c1252..c52a26f8c, 8 real defects; items 1/2/5/6 already recorded as a THOUGHT deviation on hypothesis:l4-non-prime-genless-remaining-five-identity-records-latch-readers-sensei-handoff): the remaining 4 CODE items. CLAIM: (3) _compose_seating_announcement (rotate.py:5292) prints \"ack --seat --gen\" for a non-prime post -- cmd_ack refuses --gen on a non-prime seat (post-SM.243, ack is session-id-keyed) -- route the announcement line through _ack_call_args (the shared helper cmd_ack itself uses) so it prints the correct non-prime ack invocation. (4) the after_join second-input line (rotate.py:12584) has the identical bug -- same fix, same helper. (7) _sweep_dead_hook_latches (rotate.py:9292-9302) globs only hook-<seat>-gen*.lock, so a dead SESSION-id-keyed latch (post-SM.243 shape) is never swept -- one dead file leaks per re-seat; widen the glob (or add a session-id-keyed pattern) so both shapes are covered. (8) the by-name --gen refusal (rotate.py:2404-2407) prints a corrective line missing --ref/--text -, so a copied-and-pasted diff submits EMPTY text and rotate-self silently reads it as continue -- the refusal message must include a complete, pasteable command. FALSIFIERS: any of the two announcement call sites still printing --gen for a non-prime post after the fix; a dead session-keyed latch file surviving a full sweep pass; the --gen refusal line still missing --ref/--text -. TESTS: extend test_rotate.py (announcement call-site assertions x2, latch sweep fixture with a session-keyed dead file, refusal-message content assertion). FILE SCOPE: rotate.py only (the four named regions), test_rotate.py. CEILING: <=60 production lines, ONE kid -- all four are small, independent, same-file fixes."
title: L4 sl04 residue ack and latch fixes
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sl04-residue-ack-and-latch-fixes

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
