---
id: goal:g7.16.1.11.7
mint_id: 244ee70352c14814a7a64256141c3e5d
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.11.7
goal_kind: subgoal
origin: owner
scaffold_hash: 73694e8328970cf5
season: 2
seeds: []
status: retired
tags:
  - council-loop
  - redesign
  - bundle
title: "G7.16.1.11.7: the DOMAIN CONTROLLER: encryption-town holds the public directory matrix; short-lived certificates (keys in RAM, CA in a capsule); cross-box seeding + comms as signed commits (§U-§X)"
town: core
---
# goal:g7.16.1.11.7

## Why this exists
Parent goal:g7.16.1.11: §U-§X of doc:radically-simple-engine (e6630723c, 04ed82723, 60c275d51, 3a46f35ce; U1-U9c, F41/F45, X1-X11c, SI1-SI7 PASS on scratch).
## Target end-state
the DOMAIN CONTROLLER: encryption-town holds the public directory matrix; short-lived certificates (keys in RAM, CA in a capsule); cross-box seeding + comms as signed commits (§U-§X).
## Invariants
the DC holds public identities only; a directory row without restrict is refused; editing a row revokes its certificates.
## Falsifier
1. DG5 spawns on encryption-town from the seed and a cross-box signed commit verifies
2. negative: a private user key written to any disk: zero
## Out of scope
the sibling leaves goal:g7.16.1.11.1 through goal:g7.16.1.11.10, each its own end-state
## OWNER, verbatim
"Neither domain controller nor the use account ever actually get perms to write that private key itself" (owner 07:0xZ; verbatim on goal:g7.16.1.11)
## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
