---
id: hypothesis:l3-rotate-loop-false-success
mint_id: 226f9588236948b3b9e025ca3c1c3334
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-VII
scaffold_hash: 046c4b37906489c0
season: 2
testable_claim: rotate.py loop exits non-zero with a named error when no tmux window for the successor exists after the spawn attempt, and its successor read-back never opens the caller own transcript, proved by a red-first test that stubs the spawn to create no window and asserts the failure, plus a test that passes --session-log pointing at the caller own transcript and asserts the read-back does not treat it as the successor reply.
thought_session: 7af11157
title: rotate.py loop must not report a rotation it did not perform
---
<!-- BODY:BEGIN -->
# hypothesis:l3-rotate-loop-false-success

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
CLAIM: rotate.py loop can report a successful rotation while having spawned nothing, and a prime that believes it exits and leaves the ladder headless. It must fail loudly instead.

WHY: measured live at Belam VII's own rotation, 2026-09-07 21:56 UTC. The command was rotate.py loop --role prime_director --name belam-S1-L3-VIII --model claude-opus-5 --effort max --force --session-log <own transcript>. It printed "successor replied (handoff needs change):" followed by the PRIME'S OWN transcript line - a mode event carrying the prime's own sessionId, not the successor's - and then "rotate prime_director --> successor belam-S1-L3-VIII". tmux list-windows showed belam windows for II through VII and none for VIII. No successor existed. rotate.py spawn with the same name and model then worked first try and the successor was confirmed by tmux capture-pane. The prime only survived because trap 0l already said never to believe the read-back.

TWO INDEPENDENT BUGS. Fix the second one first - it is the one that loses the ladder.
1. loop returns success without ever checking a window exists.
2. --session-log X is threaded to BOTH the meter and the successor read-back, so the read-back opens the caller's transcript and finds whatever the caller just wrote.

FILES:
extensions/agi/bin/rotate.py :: cmd_loop - the post-spawn confirmation path
extensions/agi/bin/rotate.py :: the read-back helper reached from cmd_loop (_read_first_reply and its caller)
extensions/agi/tests/test_rotate.py :: new red-first tests

DESIGN: after the spawn attempt, cmd_loop asserts a tmux window named exactly the successor name exists in the target session, by listing windows rather than by parsing spawn output. Missing window means exit non-zero with a message naming the successor, the tmux session, and the rotate.py spawn command to run by hand - never a success line. The read-back is given the successor's own window or pin and never the caller's --session-log; if only --session-log is available it is used for the METER ONLY and the read-back reports unconfirmed rather than inventing a reply. Unconfirmed is not failure: it prints CONFIRM BY HAND with the exact tmux capture-pane command.

TESTS red-first: test_loop_fails_when_spawn_creates_no_window, test_loop_error_names_the_successor_and_the_manual_command, test_readback_never_treats_callers_own_transcript_as_the_reply, test_loop_reports_unconfirmed_rather_than_success_when_it_cannot_read_the_successor, test_spawn_path_unchanged.

GATE: a parent must see those five green AND must exhibit the failure live - stub or point loop at a name it will not spawn and show a non-zero exit with the named error, never a success line.

NOT IN SCOPE: l3w4-seat-rotation-loops owns alarms and rotate-self and the seat lifecycle; l3-rotate-pin-path-readback owns the meter pin path. This brief owns exactly one thing - loop must never claim a rotation it did not perform.

SOURCE: Belam VII's own rotation, recorded in HANDOFF section 0.7 Rotation and as a note on l3w4-seat-rotation-loops. Related trap 0l.
