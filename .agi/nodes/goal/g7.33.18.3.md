---
id: goal:g7.33.18.3
mint_id: c8d06e77aefa494d9b3601bca48f6b34
type: goal
parents:
  - goal:g7.33.18
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G7.33.18.3
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 981d1e646dba1e9b
season: 2
seeds: []
spawn_check: unverified
spawn_check_reason: schema 'goal' is discriminated on 'goal_kind', which this node does not set
status: active
tags:
  - local-maxxing
  - engine
title: "G7.33.18.3: ONE read-only read-back probe -- prints g7.33.18's table for the box it runs on, ok/drift per row (assigned: director-engine)"
town: core
---
# goal:g7.33.18.3

# goal:g7.33.18.3

WORLD-AFTER: ONE read-only read-back probe prints goal:g7.33.18's table (layer · the value on THIS box · the value SIZING wants · ok/drift) for the box it runs on, from the box's own files and `systemctl show` reads -- no write, no sudo, no unit change.

ACCEPTANCE: a committed test drives it over a tmp-root fixture + a stubbed `systemctl show` and gets the table; run read-only on local-town it prints every row with no drift against the measured values; exits non-zero on any drift, naming the row.
