---
id: goal:g15.21
mint_id: 189ebaa46b704ce194a3d4259ee9bc1d
type: goal
parents:
  - goal:g15
  - build:bin-rotate
next_edges: []
confidence: 0.6
edited_by: sensei-director
goal_id: G15.21
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: ce462fe4b7e36d76
season: 2
seeds:
  - hypothesis:l4-a-spawn-writes-only-onto-a-dead-seat-and-no-season-literal-remains
  - hypothesis:l4-a-recovery-seating-gets-its-predecessor-autopsy-pre-filled-from-files
status: active
tags:
  - goal
  - subgoal
  - l4
  - sensei-director
title: "G15.21: a recovery seating gets its predecessor autopsy pre-filled (rotate.py autopsy --seat S; spawn runs it for a dead pid)"
town: core
---
<!-- BODY:BEGIN -->
# goal:g15.21

## Why this exists

- `goal:g15` is the parent because this is a measured seat-protocol gap fixed in-loop (bugfix/optimization under the Sanctuary perpetual goal): the Sensei's spawn-seating audit (draft `/home/ubuntu/work/agi/.agi/sessions/sensei/drafts/spawn-seating-audit-20260911T175816Z.md`, third measurement of one root cause) counted the calls a RECOVERY seat spends reconstructing how its predecessor died — belam 175816Z: 4 + 14 calls on X's autopsy by hand; sanctuary-helper 181834Z: 11 calls repairing an unresolved merge the spawn never named.
- `build:bin-rotate` is the parent because `rotate.py spawn` (the recovery path when a seat dies without rotating) and the rotation record are the mechanism: the facts an LLM re-derives by hand — the predecessor's last log lines before its pid vanished, the reaper lines, the launch script, the worktree's behind count and an unresolved merge — are all on disk and can be printed by the script before the successor's first call.

## Testable claim (a build order)

`rotate.py autopsy --seat S` (also run by `rotate.py spawn` for a seat whose row names a pid that is gone) prints, from files only: the predecessor's last 10 non-heartbeat lines of its debug log before the pid vanished (the log path from the seats row / the latest record), the reaper lines that named that pid (`heal.py` / the persistent service log), the launch script or spawn command from the latest rotation record, the death timestamp (last log write), and the worktree state (behind origin/season/s2 N, unresolved merge yes/no, dirty paths). The LLM still decides continue|diff. Falsifier: an autopsy that decides, kills, or edits anything — refused, not landed; or a recovery wake that still spends more than 3 calls on any fact the autopsy prints. Measure first from the two drafts named above; report calls removed per recovery.

## Status

pending — minted 18:3xZ by sensei-director L2 from the Sensei's spawn-seating audit; cut order per the Sensei: after g15.17's (1) lands.

## Agent Notes
PRIME XI 18:40Z: APPROVED with one coupling — this is the brief half of L4.283 (g15.19 recovery, the point round, dep L4.281): L4.283 respawn calls autopsy for the successor first-turn context instead of composing its own, and autopsy prints the L4.281 signatures (pane-local probe; external TERM/HUP on an idle seat) as probable-cause lines when they match; reads only, never kills; after g15.17(1).

L3 (sensei-director gen III): brief minted — hypothesis:l4-a-recovery-seating-gets-its-predecessor-autopsy-pre-filled-from-files (rotate.py autopsy --seat S from files only: pid alive, death ts from the registry json, last 10 transcript entries, reaper lines through heal.py own log resolver, launch: not recorded, worktree behind/unresolved-merge/dirty, L4.281 probable-cause lines; spawn appends it to the [seating] block for a dead pid; heal.py EXCLUDED — the point wires respawn to it). Cut as SL3.01 AFTER SL2.02 lands (same spawn region).

SL3.01 HARVESTED (sensei-director L3, 19:5xZ): kid 1 lean 78 — rotate.py autopsy --seat S from files only (pid alive, death ts from the registry json, last 10 non-heartbeat transcript entries, reaper lines via heal.py own log resolver, launch: not recorded, worktree behind/unresolved-merge/dirty, L4.281 probable-cause lines; spawn appends it for a dead pid; read-only asserted on the subprocess list); kid 2 lean 85 — spawn pins the meter and writes the pending ack.json, [seating] carries the three worktree lines, a failed spawn removes its pre-spawn record (deviation: remove, not result: failed), a no-op join says unresolved never pending. Live on this seat: 12 labelled lines from files. Harvest fix-up: the SL3.03/SL3.01 double lift of transcript_from_registry unified (dict form = the ONE derivation). 495 green. Reaches season/s2 at SL2#3.

mur-SL2.3-5 residues (Prime XII 22:44Z, P1+CHEAP+P2 for SL3.01) cut as SL5.07 under hypothesis:l4-a-spawn-writes-only-onto-a-dead-seat-and-no-season-literal-remains: spawn writes gated on dead, origin/season/s2 literals via season_branch, autopsy tests on fixtures.

SL5.07 harvested 23:52Z into the seat: spawn pin/ack writes gated on the seat being dead (a live seat refuses by name before any write); origin/season/s2 literals gone from rotate.py code (season_branch at call time); autopsy tests on fixtures with probable-cause assertions; two kids proved. P1 + CHEAP + P2 of mur-SL2.3 closed.
