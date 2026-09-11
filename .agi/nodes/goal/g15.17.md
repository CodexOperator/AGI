---
id: goal:g15.17
mint_id: d583d38c95534ae38545894e445e0259
type: goal
parents:
  - goal:g15
  - build:bin-rotate
next_edges: []
confidence: 0.6
edited_by: sensei-director
goal_id: G15.17
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 5fdf9685ab3c8cf2
season: 2
seeds:
  - hypothesis:l4-a-first-seating-sends-the-sensei-the-same-alert-a-rotation-does
  - hypothesis:l4-a-first-seating-is-a-rotation-without-a-predecessor
status: active
tags:
  - goal
  - subgoal
  - l4
  - sanctuary-director
thought_session: sensei-director-genI-L1
title: "G15.17: a first seating sends the Sensei the same alert a rotation does (spawn, seats-launch, hand launch via ack --gen 1)"
town: core
---
<!-- BODY:BEGIN -->
**A FIRST SEATING sends the Sensei the same alert a rotation does.** Owner, 2026-09-11 16:2xZ, verbatim (relayed by the Prime's 16:22Z dm): "sensei should still get an auto-nudge for any new seat starting up same way he gets an alert for any rotation happening" — the dm carries seat, window @id, ref, pid, session id, transcript path. Today only `rotate-self` sends it.

## Why this exists

- `goal:g15` is the parent because this is a gap in the seat protocol's mechanism fixed in-loop: this very seat was hand-launched by the Prime at 16:10Z and the Sensei learned of it from the Prime's prose, not from the engine — the same silence for every `spawn` / `seats-launch` / hand launch.
- `build:bin-rotate` is the parent because `_announce_rotation` (rotate.py, called from `cmd_loop` :1522 and `cmd_rotate_self` :5669 only) is the mechanism: the composer and the derived-recipient set already exist; the first-seating paths (`cmd_spawn`, `cmd_seats_launch`, and `ack --gen 1` for a hand launch) never call it.

## Testable claim (a build order)

(1) One composer, one shape: a first seating emits the `[rotation-alert]` dm with `trigger: first-seating` (generation `0 -> 1`), carrying seat, window @id, ref (when the join has it — else named absent), pid, session id, transcript path, to the same derived recipients (`_derive_receivers`: live seats, the Sensei among them); delivery failure never fails the seating. (2) Senders: `rotate.py spawn` and `seats-launch` after the window is up and the registry join (`_successor_window_id` + the `~/.claude/sessions/<pid>.json` join rotate-self already performs); a HAND launch is covered by `rotate.py ack --seat S --gen 1` (no predecessor) sending the same dm when no seating record exists for that seat + generation — recorded as `<sessions>/rotations/<seat>.<TS>.seating.json` (one record per seating, the same dir as rotation records, so the Sensei's `status --record latest` sees it). (3) Red-first tests on fixtures (window_path seam): spawn emits the seating text with the fields; ack gen 1 emits when no seating record and does NOT double-send when one exists; the text is the composer's shape. Neighbours `test_rotate.py`, `test_rotate_startup.py`, `test_send.py` (fake tmux) green.

**Falsifiers:** a spawn or seats-launch after which the Sensei's dm file has no seating line; a second dm for the same seat + gen. **FILE SCOPE:** `extensions/agi/bin/rotate.py` (`cmd_spawn` / `cmd_seats_launch` tails, `cmd_ack`, the announcer) + tests. EXCLUDED: `send.py` (import only), `config:*`, hooks. **CEILING:** 1 parent, up to 2 kids. **SERIAL** behind `goal:g15.16`'s round — both edit the announcer; cut after it is harvested.

## Agent Notes
DIRECTOR sensei-director 16:4xZ: second brief added from the Sensei's 16:38Z measurement of THIS seat's first seating (hand-spawned 16:10Z: no STARTUP OUTPUT, no facts; 22 of the first 40 calls are what the director template gives a rotated seat free — 13 engine-source reads, three --help): rotate.py spawn / seats-launch run the role's first_turn and append STARTUP OUTPUT, write the bootstrap record at gen 1, and share the seating record with the alert brief. Both briefs are serial behind g15.15 (SL1.03) and g15.16; one parent may take both as two kids (same spawn tail).
