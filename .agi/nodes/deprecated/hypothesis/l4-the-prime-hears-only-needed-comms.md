---
id: hypothesis:l4-the-prime-hears-only-needed-comms
mint_id: 94b073b2cdb54f8a96f871a887128268
type: hypothesis
parents:
  - goal:g25.legacy-direct
next_edges: []
confidence: 0.9
edited_by: belam
scaffold_hash: cd0bccc13e567cfa
season: 2
status: deprecated
testable_claim: "goal:g15 (owner 2026-09-10 05:0xZ standing order; owner 2026-09-16 06:3xZ verbatim in doc:l4-owner-decisions: let us make it asap that Prime does not get the useless status DMs only direct comms that are needed; MEASURED at gen 21 wake: six thought-master status dms in 42 min 2026-09-14 17:14-17:56Z + one director done-line in the STARTUP inbox, and the after_join block typed 06:08Z then re-nudged (wake:idle) 06:23Z). CLAIM: (1) send.py CLI: a dm whose target is the prime_director row (default belam) from any sender but the Prime itself (name or belam- prefix) or AGI_ROLE=owner is refused BEFORE any write, exit 3, unless its text opens (after lstrip, case-insensitive) with one of PRIME_DM_TAGS = [merge-up] [decision] [rotation] [red] [rule] [complete] [owner]; every other inbox is untouched; in-process send() callers (closeout ask, reaper alarm, harvest line) are unaffected and already address the dispatcher/parent (L4.366, L4.372). (2) rotate.py after_join: when the block was TYPED into the successor pane, the delivery stamps the wake sidecar with the seat current unread digest via send._record_announced, so wake stays quiet until a NEW unread changes the digest; a refused typing stamps nothing. FALSIFIERS: an untagged CLI dm from a non-Prime seat lands in belam.md; a tagged one is refused; a typed after_join is re-nudged (wake:idle) on the next idle pass; test_send.py + test_after_join_service.py go red. EVIDENCE: extensions/agi/bin/send.py PRIME_DM_TAGS/_prime_dm_refusal; rotate.py after_join delivery block; 5 tests in test_send.py + 1 in test_after_join_service.py (395 passed). Written by the Prime directly under the owner 2026-09-16 ruling (small fixes written in directly under a g15 node when cheaper than a parent)."
thought_session: goal-glom-2026-09-19
title: "The Prime hears only needed comms: a dm to its inbox opens with a needed-tag or is refused; a typed after_join stamps the wake sidecar (Prime gen 21, 2026-09-16, FIXED IN-LOOP by the Prime on the owner order)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-prime-hears-only-needed-comms

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Retired at the L4 closeout (Prime retire list 2026-09-17 12:0xZ from survey hypothesis:a00-e1933e6a-176c0e, executed by sanctuary-master gen 7, status deprecated + moved under deprecated/hypothesis, mint id unchanged): fixed in-loop by the Prime directly.
