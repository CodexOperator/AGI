---
id: goal:g7.16.1.11.46.1
mint_id: 21b9e09ff25f43ecba39663166ae7698
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.8
edited_by: belam
goal_id: G7.16.1.11.46.1
goal_kind: subgoal
origin: goal
seeds: []
tags:
  - brainstorm
  - V0
role: prime_director
season: 3
status: complete
title: "G7.16.1.11.46.1: V0 -- a claude post restarts into its own session (--resume the id in ~/.session), never -c"
town: local-maxxing
---
# goal:g7.16.1.11.46.1

## Why this exists
goal:g7.16.1.11.46, wave 0 (doc:brainstorm-unify §22 V0, card atom 2.1): at the 03:45Z 10-23 reboot the Prime's pane ran `claude -c go`, which resumes the NEWEST transcript in the project dir; the Fable fork shares the Prime's home and had been active more recently, so the fork came up at the Prime's post. It was restored by hand.

## Target end-state
- The agi-run piece (config:engine-wrap), for a claude harness: a fresh start runs `--session-id <new uuid>`; every other start runs `--resume <id>` with the id read from ~/.session when that transcript exists, else the newest transcript once (the old choice, then pinned); no transcript at all keeps `-c`. The id is written to ~/.session (600) at every start.
- A fork started beside a post (same home, newer transcript) cannot take the post at a restart.
- It reaches a live pane when the box's boot pin (/etc/agi/carry.env AGI_TRUNK) moves to a trunk that carries it; moving the pin is a host act, banked for the owner in doc:card-belam §6.

## Invariants
- `c` keeps its meaning (empty = fresh), so the rotation-alert line and fresh-alert.t.sh are unchanged.
- A pi harness is untouched (its agi-run arm is dormant, engine-wrap N12).

## Falsifier
1. `sh extensions/agi/tests/session-pin.t.sh` exits 0 (9 lanes, including b: own id + a newer foreign transcript resumes the own id, and m: the piece without the line is RED).
2. Negative: `sh extensions/agi/tests/fresh-alert.t.sh`, `claude-upsell.t.sh`, `boxwake-unit.t.sh`, `post-env.t.sh` each exit 0 (nothing else in agi-run moved).

## Out of scope
The pin move (host act, owner) · V1 identity chain (wave 2).

## Agent Notes
Assigned to **belam**.
