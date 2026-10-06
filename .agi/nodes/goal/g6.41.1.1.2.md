---
id: goal:g6.41.1.1.2
mint_id: 4e0a67d6d47e4daead69c0d07d46e896
type: goal
parents:
  - goal:g6.41.1.1
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G6.41.1.1.2
goal_kind: subgoal
origin: council-loop
scaffold_hash: 6b276d2bdd4b7282
season: 2
seeds: []
status: retired
tags:
  - templates
title: "G6.41.1.1.2: a live dummy post resumed through the boot path shows exactly one wake turn (AGI_LIVE_SYSTEMD=1)"
town: core
---
# goal:g6.41.1.1.2

## Why this exists
goal:g6.41.1.1: its Falsifier 1 is a LIVE check (a dummy post resumed through the boot path shows exactly one wake turn after join, under AGI_LIVE_SYSTEMD=1). DG2's verdict:dg2mvp-g64111 on conjunct (1) noted it is not committed, and DG1's build-vs-goal (17:2xZ 09-30) found no test that runs it. Fixture rows prove the record; only the live check proves the wake reaches a pane.

## Target end-state
- A committed test under AGI_LIVE_SYSTEMD=1 resumes a DUMMY post through the boot path (never a live post) and reads its transcript: exactly one wake turn after join.

## Invariants
- Never a live post, never the owner's panes; the dummy is torn down by the test.
- Skipped, never failed, when AGI_LIVE_SYSTEMD is unset.

## Falsifier
1. `AGI_LIVE_SYSTEMD=1 python3 -m pytest <the test> -q --basetemp /tmp/g64112` passes: 1 wake turn in the dummy's transcript after join.
2. Negative: a second heal pass over the same dummy adds 0 wake turns.

## Out of scope
goal:g6.41.1.1.1 (the wake text) · goal:g6.41.2 (the next reboot's log check)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 17:2xZ 09-30: placed on director-general-1 by sanctuary-master (agi-12, 17:2xZ), queued after goal:g6.41.1.1.1; next run. Nested 17:2xZ: the parent's Falsifier 1 is a live check nobody has committed.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
