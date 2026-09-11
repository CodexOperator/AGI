---
id: hypothesis:l4-a-first-seating-sends-the-sensei-the-same-alert-a-rotation-does
mint_id: de98d39b092e46739d8f377d8bfadc96
type: hypothesis
parents:
  - goal:g15.17
  - hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-and-the-successor-one
next_edges: []
edited_by: sensei-director
scaffold_hash: 5bcaf4ee6e802467
season: 2
testable_claim: "OWNER 16:2xZ (Prime dm 16:22Z, verbatim): 'sensei should still get an auto-nudge for any new seat starting up same way he gets an alert for any rotation happening'. Goal goal:g15.17 (parents + '## Why this exists' there). MEASURE FIRST: _announce_rotation (rotate.py ~2584) callers — cmd_loop :1522 and cmd_rotate_self :5669 only; cmd_spawn :1221, cmd_seats_launch :2003 and a hand launch (this seat, sensei-director, launched by the Prime at 16:10Z and recorded by hand at 1c73bc7d4) send nothing; show the Sensei's dm file (send.py read --dm master-sensei --all from MAIN) has no seating line for sensei-director. BUILD: (1) ONE composer, ONE shape: a first seating emits the [rotation-alert] dm with trigger: first-seating, generation 0 -> 1, carrying seat, window @id, ref (when the join has it, else 'ref: (pending ack)'), pid, session id, transcript path — to the same derived recipients (_derive_receivers: live seats; the Sensei among them); delivery failure never fails the seating. (2) Senders: cmd_spawn and cmd_seats_launch after the window is up and the registry join (_successor_window_id + the ~/.claude/sessions/<pid>.json join rotate-self already performs — reuse, never re-implement); a HAND launch is covered by rotate.py ack --seat S --gen 1 (no predecessor): it sends the same dm when no seating record exists for that seat + generation; the seating is recorded as <sessions>/rotations/<seat>.<TS>.seating.json (same dir as rotation records; rotation 'rotate-self'|'seating' field). (3) RED-FIRST TESTS on fixtures (window_path seam, fake send): spawn emits the seating text with every field; ack --gen 1 emits when no seating record exists and does NOT double-send when one does; the text is the composer's shape (one test asserts the same composer produces both). Neighbours test_rotate.py, test_rotate_startup.py, test_send.py (fake tmux only) green. FALSIFIERS: a spawn/seats-launch after which the Sensei's dm has no seating line; a second dm for the same seat + gen. FILE SCOPE: extensions/agi/bin/rotate.py (cmd_spawn / cmd_seats_launch tails, cmd_ack, _announce_rotation) + tests. EXCLUDED: send.py (import only), config:*, hooks, heal.py. CEILING: up to 2 kids, the parent merges every kid branch into the round branch before done:. SERIAL behind goal:g15.16's round (both edit the announcer) — the director cuts this only after that harvest."
thought_session: sensei-director-genI-L1
title: a first seating (spawn, seats-launch, or a hand launch acked at gen 1) emits the same rotation-alert dm a rotation does, with trigger first-seating
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-first-seating-sends-the-sensei-the-same-alert-a-rotation-does

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
