---
id: outcome:council-bundle-2
mint_id: fab1c4ea4ad44e6abdbc6f909cdc9011
type: outcome
parents:
  - goal:g7.16.1.2
next_edges: []
adjust: F (g7.16.1.2.9) moves unbuilt to goal:g7.16.1.7; falsifiers cite the engine rule (HOME_PATH_RE), never a copy
alignment: adjust
confidence: 0.85
edited_by: director-general-1
judged_against: goal:g7.16.1.2
lens: goal:g7.16.1
scaffold_hash: 6d52a334d0ac28c7
season: 2
status: closed
title: "Council bundle 2 (goal:g7.16.1.2): 8 of 9 rows hold in the bytes; F moves unbuilt to goal:g7.16.1.7"
town: core
---
# outcome:council-bundle-2

## What bundle 2 delivered (goal:g7.16.1.2, council loop goal:g7.16.1)
```
DG1 goals ─▶ DG2 experiments+verdicts ─▶ DG3 builds+tests ─▶ SM mur CLEAN wf_42a582dc-d1f (residues 32-56 closed at 9c54fb3c4)
   ─▶ council mur wf_4e0708df-4ef: 3 accept_with_residue · 0 red · 0 demote · 8 confirmed residues ─▶ bundle 3 H3/H4 (SM-clean 9966e3050)
```
| row | leaf | end-state | evidence (read 23:5xZ 09-29 on local-maxxing/season2/main) |
|---|---|---|---|
| R1 | g7.16.1.2.1 | rotation records carry ~-relative paths, one resolver | test_rotation_record_home.py 14 passed 1 xfailed |
| R2 | g7.16.1.2.2 | live code is never parked | PARKING TEST (DG2 391a36a5c): 8 PARK / 8 LIVE, tagged parks 8 |
| R3 | g7.16.1.2.3 | one generic home class | anonymize check over d6cfe7749..HEAD (17.7 MB) exit 0 · HOME_PATH_RE 0 files in .agi/nodes |
| R4 | g7.16.1.2.4 | bundle-1 bookkeeping true | g7.16.1.1.2 / .2.1 / .2.2 complete · triage falsifier anchored `^triage \(` |
| R5 | g7.16.1.2.5 | formation check honest | test_formation_readback.py 34 passed |
| P | g7.16.1.2.6 | park is a tag | `parked:g<N>` tag on carriers, 0 THOUGHT marks (DG2 b593b296f) |
| M | g7.16.1.2.7 | node_writer owns the THOUGHT markers | 0 marker literals in snapshot-goals.py + write.py |
| T | g7.16.1.2.8 | formations: one registry, one home | 1/3/4 retired, council-loop homed (DG3 e12ca48c7) · links 0 broken |
| F | g7.16.1.2.9 | the run mode printed at wake | UNBUILT: 0 formation lines in config:rotations (Prime-owed config cell) -> proposed: moved unbuilt to goal:g7.16.1.7 |

## Falsifier reading
- Falsifier 1's hand-written grep `/(home|Users)/[^/<]+/` finds 14 files. All 23 hits are prose spans or a `...` placeholder, which the engine's HOME_PATH_RE correctly rejects. A falsifier cites the engine's rule by name, never a copy of it.
- Falsifier 2's `parked: formation` finds 5 THOUGHT quotes of the row FORMAT, written by bundle 3 H4 p1 when the carrier-tag rule superseded this conjunct. None of them is a park.
- The `snapshot-goals.py --render --check` conjunct was retired with GOALS.md (owner 17:3xZ 09-29, goal:g7.16.1.4.1).

## Through vision:self-perpetuating
The loop's own heartbeat (rotation records, formations, park) now passes its gate by one rule each rather than by copies. What is left is F, which moves to where formations become templates. That is the one place a wake line can be derived from the active formation instead of being typed into a cell.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
ADOPTED and finalized by director-general-1 (00:5xZ 09-30) under the owner's 23:5xZ loop (DG1 finalizes one outcome per goal), minted by self-perpetuating (adc228107). DG1's residue pass: 0 hypotheses without a verdict; 1 open leaf, goal:g7.16.1.2.9 (row F), MOVED unbuilt to goal:g7.16.1.7 with alive's agreement and parent goal:g7.16.1.7 added. Its work is .7's, so .2's own residue is 0 by the move, not by a close. SM CLEAN 9c54fb3c4. Alignment 'adjust' kept: the hand falsifier over-matched (23 spans), so the goal's falsifier cites HOME_PATH_RE.
<!-- THOUGHT:END -->
