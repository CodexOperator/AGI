---
id: hypothesis:l3w4-rotation-announces-itself
mint_id: 7179faf5b5a54c58b9279909180a46c1
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-XIII
scaffold_hash: 2521f82c31196649
season: 2
testable_claim: "Every rotation that SUCCEEDS emits exactly one announcement to every live seat over the shared mail-alert channel of hypothesis:l3w4-shared-mail-alert (never a second channel, never tmux send-keys): rotate.py's spawn, loop and rotate-self paths each call ONE announce helper at the same moment the rotation record under .agi/sessions/rotations/ is written, the announcement names outgoing seat, successor name, generation before/after, trigger (meter fraction, --force, or fable-limit) and the handoff path, recipients are DERIVED from config:seats rows intersected with live tmux windows rather than hand-typed, room quorum is never posted into by the prime (the audience door is used instead), and a REFUSED or inconclusive rotation emits no announcement but does record why; proven by tests asserting each of the three paths emits one announcement carrying all five fields to every derived recipient, that a refused rotation emits none, and that recipient derivation drops a seat whose window is gone; then live, this prime's own next rotation announces itself with zero hand-typed send.py calls."
thought_session: rc-XIII
title: "Rotation announces itself: every seat learns of a rotation programmatically, on the shared alert channel"
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-rotation-announces-itself

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. OWNER ASK, 2026-09-08, verbatim via belam-S1-L3-XIII: "Make sure that during rotation everyone is aware you are rotating. Ideally it's done in a programmatic way."

WHY THIS IS NOT ALREADY DONE, measured before this brief was written, not assumed. `grep -n "announce|broadcast" extensions/agi/bin/rotate.py extensions/agi/bin/send.py` returns NOTHING. rotate.py writes a rich durable rotation record under .agi/sessions/rotations/*.json (built L3.39, proved: five observations, refusal records, evidence written before the own-window kill) and that record is read by NOBODY and sent to NOBODY. `rotate.py alarms --holder <seat>` DMs a seat that its OWN meter is due -- that is the opposite direction and it has never been switched on for anyone. So a seat learns that a peer rotated only if a human tells it. This session opened with the prime hand-DMing three seats plus one audience-quorum post to say "XII is out, XIII is in"; that hand-send IS the gap, and it is the fourth instance of the pattern HANDOFF section 6 item 63 names: built, tested, never wired (this, failures.py, the seat-pin generation guard, rotate.py alarms).

WHY IT MATTERS OPERATIONALLY, so the shape is not over-built. A seat that does not know the prime rotated will: DM a dead generation and wait on an answer that cannot come (master-sensei lost an hour to exactly this shape of silence this session); attribute a mid-flight instruction to the wrong director; and re-ask a question the previous generation already answered in a handoff it cannot see. None of that needs a protocol. It needs one message, sent by the machine, at the moment it becomes true.

HARD CONSTRAINT, non-negotiable: RIDE THE EXISTING CHANNEL. hypothesis:l3w4-shared-mail-alert (g15, IN FLIGHT this round as quorum round Q.05) is building the ONE shared alert side-channel for dm, room and audience, under the owner's own five constraints (no agent-side polling, survives mid-turn, distinguishable from the owner speaking, records that an alert was raised and when, one mechanism not three). This hypothesis MUST be a PAYLOAD on that channel, never a second delivery path. If that channel has not landed when you start, build the announce helper and its tests against send.py's existing dm plus audience verbs so the payload is correct and the delivery is swappable, and say plainly in your node that the last hop is pending on l3w4-shared-mail-alert. Do NOT invent tmux send-keys, a polling loop, or a parallel alert file. Pane injection is the prime impersonating the owner at a seat's prompt and the owner has called it out by name.

WHAT THE ANNOUNCEMENT MUST CARRY (five fields, all of them, because each one has already cost someone a turn): outgoing seat id and generation; successor name and generation; the trigger, spelled (meter fraction at rotation, --force, or the 99-percent fable-limit rule); the handoff path the successor is reading; and one line of "what is in flight" so a peer knows whether its own round is orphaned. Derive recipients -- do not hand-type them: config:seats rows intersected with live tmux windows, which is what seat_status.py already computes. A seat whose window is gone must drop out of the recipient set, and that must be a test.

WHERE IT FIRES: all three rotation paths -- spawn, loop, rotate-self -- at the SAME moment the rotation record is written, not before (a rotation that is refused must announce nothing) and not after the own-window kill (evidence and announcement both have to survive cleanup; L3.39 already established that ordering, follow it). A refused or inconclusive rotation records why and announces nothing. The prime never posts into room quorum; it uses the audience door, which is the rule the owner set and all-is-one built.

SCOPE: extensions/agi/bin/rotate.py plus its tests, and read-only use of send.py and seat_status.py. Do NOT touch .agi/nodes/.geometry/seats.md or config:seats rows -- that is the sanctuary-master's function alone. Do NOT touch moral:*. Do NOT stand up any seat. rotate.py has NO build node (HANDOFF section 6 item 49), so its bytes are outside the grid -- edit it as ordinary engine source with ordinary tools, then leave a thought; do not try to route it through write.py payload verbs and do not run level3.py.

PROVE: red-first tests, one per rotation path, asserting exactly one announcement carrying all five fields reaches every derived recipient; one asserting a refused rotation announces nothing; one asserting a seat with no live window is dropped from the recipient set. Then the live half, which is the only one that closes the owner's ask: the next real prime rotation must announce itself with zero hand-typed send.py calls, and the announcement must be readable in the recipients' dm files afterward. If you cannot exercise the live half in one round, say so and return inconclusive_lean_proved with the honest reason -- this loop has three examples this week of a claimed proved whose live half was never run, and every one of them cost a later generation more than the honest verdict would have.
