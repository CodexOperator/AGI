---
id: hypothesis:send-undelivered-notice-lands-in-the-comms-root
mint_id: 6ccafbe36bc14e7d8d87cf6a922d3d76
type: hypothesis
parents:
  - goal:g15
next_edges: []
confidence: 0.8
edited_by: belam
scaffold_hash: fcd42830e6c09018
season: 2
testable_claim: "After the fix, _notify_undelivered (send.py:2799) writes through the same comms root every other send_dm call site uses (.agi/comms/season-2/dm), so send.py read <post> shows an [undelivered] notice for a dm whose nudge never landed; test_send_undelivered.py no longer conflates the project root with the comms root (its :33-39 fixture and the :114/:152 path assertions), and the old 'nudge: coalesced' line (send.py:2491) is gone as the l5 claim said."
title: "send.py: the [undelivered] notice lands in the comms root a reader can see (assigned: director-engine)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:send-undelivered-notice-lands-in-the-comms-root

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
assigned: director-engine (owner 01:4xZ 09-21); surfaced by the 09-21 Prime merge-up-review, batch = hypothesis:mur-0921-residue-batch-into-season2-main.
