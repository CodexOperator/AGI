---
id: hypothesis:l5-the-two-captive-rotation-triggers-share-one-in-flight-latch-per-seat
mint_id: 7c47d049cb6249efb6bd0936c2a44169
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
edited_by: belam
scaffold_hash: a2802ec10bded4f0
season: 2
testable_claim: "(1) rotate.py exposes one seam `_rotation_in_flight(root, seat) -> str | None` reading the rotation record/sequence the running rotate-self already writes (the 'in flight' value the rotation-alert line prints), and BOTH captive triggers -- rotation_alert.py's hook path at f >= the line and cmd_alarms/_master_rotate's poll -- call it first and print 'captive rotate held: <seat> in flight since <ts>' instead of spawning when it names a rotation younger than the role timeout; a stale in-flight marker older than the timeout does not hold. (2) cmd_alarms's help text describes the master-path rotate (no dm) and the dead `--comms-root` flag is removed from the alarms subparser (its only consumer, the dm path, is gone). FALSIFIERS: a seat over the line with a rotation in flight for which either trigger still spawns a second rotate-self; a stale marker (older than the timeout) that holds a needed rotation; a live alarms tick whose help still says dm. TESTS red-first: with a fresh in-flight marker both trigger seams spawn nothing and print the hold by name; with none, exactly one spawn; with a marker older than the timeout, one spawn; the alarms parser refuses --comms-root by name. FILE SCOPE: extensions/agi/bin/rotate.py, rotation_alert.py; tests/test_rotate_alarms.py (or the slice-2 test file), test_rotation_alert.py. CEILING: <=8 production lines."
thought_session: dissolve-legacy-2026-09-19
title: "SM.142 (mur-c01a1a03d residue 3 + 4, director-sanctuary 07:4xZ 09-19; SM.135 slice 2 follow-on; goal:g15): the two captive triggers -- rotation_alert.py's hook path and rotate.py's alarms poll -- consult ONE in-flight latch per seat before spawning, so a director past the line is rotated once, never twice"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-the-two-captive-rotation-triggers-share-one-in-flight-latch-per-seat

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
