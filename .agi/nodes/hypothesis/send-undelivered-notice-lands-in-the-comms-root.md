---
id: hypothesis:send-undelivered-notice-lands-in-the-comms-root
mint_id: 6ccafbe36bc14e7d8d87cf6a922d3d76
type: hypothesis
parents:
  - goal:g15
next_edges: []
confidence: 0.8
edited_by: a00-302e563b
scaffold_hash: fcd42830e6c09018
season: 2
testable_claim: "After the fix, _notify_undelivered (send.py:2799) resolves croot = comms_root(root) and passes THAT to send_dm, so its [undelivered] dm lands in the same comms root every other send_dm call site uses (.agi/comms/season-<N>/dm), and send.py read <post> shows an [undelivered] notice for a dm whose nudge never landed; test_send_undelivered.py no longer conflates the project root with the comms root (its fixture writes seats under the graph root, its direct send_dm calls pass the derived comms root, and it asserts the notice via the comms-root path and read_dms). The old \"nudge: coalesced\" line (send.py:2491) is KEPT, not gone: a busy send_dm emits BOTH the plain [undelivered-yet] <seat> line from _announce_nudge AND nudge: coalesced (<reason>) from _nudge_window, and the reason (pane busy (registry) / already nudged within 30s / no rendered box) is printed by no other seam."
title: "send.py: the [undelivered] notice lands in the comms root a reader can see (assigned: director-engine)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:send-undelivered-notice-lands-in-the-comms-root

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
assigned: director-engine (owner 01:4xZ 09-21); surfaced by the 09-21 Prime merge-up-review, batch = hypothesis:mur-0921-residue-batch-into-season2-main.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
CLAIM CORRECTION (parent a00-302e563b, on the a00-988fbdeb edit). This version rewrites testable_claim conjunct 3 from 'the old "nudge: coalesced" line (send.py:2491) is gone' to the measured machine: a busy send_dm emits BOTH the plain '[undelivered-yet] <seat>' line from _announce_nudge AND the 'nudge: coalesced (<reason>)' diagnostic from _nudge_window. WHY: the l5 claim's literal reading asked for the line's removal, but _nudge_window is called directly by wake/heal (send.py:2960 only wraps it for the send verb), where no _announce_nudge runs, so the diagnostic is the only signal that nothing was typed; and 16 test_send.py assertions pin it. The R1 bytes do land (send.py:2804 now passes comms_root(root) to send_dm) and the test fixture is de-conflated, so conjuncts 1 and 2 stay as written. Measured: probe_c_conjunct3.py -> both lines verbatim in one stderr capture.
<!-- THOUGHT:END -->
