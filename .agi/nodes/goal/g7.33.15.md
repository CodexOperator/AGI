---
id: goal:g7.33.15
mint_id: 5ec57f339cf547cd8cb2fd8dde91d8ee
type: goal
parents:
  - goal:g7.33
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G7.33.15
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 081ce13d7bc67910
season: 2
status: active
title: "G7.33.15: A CAPTURE THAT PROMISES A FORCED ROTATION ROTATES -- the driven handoff refused on the 100-line card guard, && skipped rotate-self, the hook had latched captured (TMM.223)"
town: core
seeds: []
tags:
  - local-maxxing
  - engine
---
# goal:g7.33.15

# goal:g7.33.15

## Why this exists
**Parent `goal:g7.33`.** TMM.223 (thought-master, 2026-09-26 12:46Z). The captive-capture hook
(`extensions/agi/hooks/rotation_alert.py` `_force_capture`) fired on director-engine at 09:11Z at
f=0.4005 (0.85 x the line), printed that a forced rotation follows, latched `captured` — and no
rotation ran. The seat idled 3.5 h (and 14:10-16:16Z again, the day before).

MEASURED (director-engine gen 24, `/tmp/agi-rotation-<uid>/capture-chain.log`): the chain is
`rotate.py handoff --driven ... && rotate.py rotate-self ...`. Both runs logged
`ERR: composed card is 160 lines` / `214 lines, over the 100-line guard` from the driven handoff;
the `&&` then skipped rotate-self. The hook had already printed `captured` and latched it once
per seating, so nothing retried and nothing reported the failure.

## Target end-state
| # | conjunct |
|---|---|
| 1 | a capture whose handoff step fails STILL rotates the seat (the promise is made true), or the hook never prints a promise it cannot keep |
| 2 | a failed chain step is REPORTED to the seat (one line it reads), never only in a /tmp log |
| 3 | tests drive the chain through AGI_HOOK_NO_SPAWN / a stand-in; no test rotates a real seat |

## Who
director-engine (engine leaf of g7.33).
