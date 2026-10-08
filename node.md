---
id: goal:g7.16
mint_id: e4b3e68394164a47847333d1929c70df
type: goal
parents:
  - goal:g7
next_edges: []
confidence: 0.6
edited_by: director-general-3
goal_id: G7.16
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: a9c65ef0496021ea
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
thought_session: g1-g7-rewrite-2026-09-19
title: "G7.16: Formations -- each formation a subgoal carried by one template node; ONE cell (config:formations active) names the running one"
---
<!-- BODY:BEGIN -->
# goal:g7.16

## Why this exists
goal:g7 (Sanctuary): the keep runs the posts, and a formation is WHICH posts run and how they hand work down. The owner, 09-29 10:1xZ, verbatim: "Formations that are live are under .geometry,  while having formations overall should be a goal like 7.16, then the formations themselves as subgoals nested under 7.16. They can go straight into template build nodes, and picking a run mode is just a matter of setting a specific template active, setting all others inactive as part of that call." Until 09-29 this node WAS the two-step formation; that body now lives verbatim in goal:g7.16.2.

## Target end-state
- Every formation is a subgoal of this goal, carried by ONE template node of the role-template kind (`type: doc`): goal:g7.16.1 (the council loop, doc:council-loop) and goal:g7.16.2 (the two-step, doc:l4-formation-2-texas-two-step). The other templates (doc:formation-local-town, doc:l4-formation-1-prime-only, -3-hybrid-gradual-expansion, -4-full-activation) are registered and gain a subgoal when one is run.
- Each template names its posts (`## Posts`) and the agi-post steps (`## Stand up / take down`).
- ONE cell, config:formations `active`, names the running template, and its `templates` map pairs each template with its goal. Switching = ONE `write.py config:formations 'set active doc:<id>'` (Prime / owner). verification.py's `formation` check reads it back and lists the nodes whose THOUGHT carries `parked: formation <that goal>` as wakeable.

## Invariants
- Exactly one formation is active at any moment.
- No formation template is deleted; a superseded one is retired (deprecated + moved).

## Falsifier
1. `python3 -c "import sys; sys.path.insert(0,'extensions/agi/bin'); import verification; from pathlib import Path; r=verification.check_formation(Path('.agi')); print(r.status, r.note); sys.exit(r.status!='PASS')"` exits 0 and prints one `PASS active doc:<id> <goal>` line.
2. Negative: `python3 -m pytest extensions/agi/tests/test_formation_readback.py -q --basetemp /tmp/b1a` exits 0, and its 0-active and 2-active rows FAIL the check.

## Out of scope
goal:g7.32.6 · goal:g7.31.3.3 (the messaging and spawn redesigns a formation runs on)

## Agent Notes
Assigned to **belam**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Retitled and split by director-general-3 (council bundle 1 row A, goal:g7.16.1.1.5), on the owner's 09-29 10:1xZ words quoted in Why this exists. The two-step body (every owner quote and measured protocol, unchanged) moved VERBATIM to goal:g7.16.2, so this node keeps its mint_id and becomes the umbrella. The near miss was renumbering this node into g7.16.2: that would have moved the mint_id and the grid history away from the umbrella that g7.16.1 already hangs under. The cell config:formations is config-type, so it is Prime/owner-only (write.py refused director-general-3 by name, goal:g12); the check reads SKIP until it is minted.
<!-- THOUGHT:END -->
