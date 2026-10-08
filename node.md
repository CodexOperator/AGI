---
id: goal:g7.16.1.7.1.1
mint_id: 1135f62de4484d1e9d2fd51c7f9dc0e2
type: goal
parents:
  - goal:g7.16.1.7.1
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.7.1.1
goal_kind: subgoal
origin: council-loop
scaffold_hash: 05649157b1f148f2
season: 2
seeds: []
status: complete
tags:
  - templates
  - spawn
  - rotate
  - council-loop
thought_session: director-general-5
title: "G7.16.1.7.1.1: ONE stand-up verb -- spawn, rotate, heal recover and hand restart launch through one function, one scope-argv builder via mem_cap; N deferred recoveries = ONE [red]"
town: core
---
# goal:g7.16.1.7.1.1

## Why this exists
goal:g7.16.1.7.1 (7a, NOW in the council placement): the placement (alive 23:4xZ) absorbs by name, from the old bundle-5 list on goal:g7.16.1.4: B1 one launcher (heal._launch_recovered -> rotate._launch_window) · C3 one scope-argv builder through mem_cap · the R2 alert (N deferred recoveries -> ONE [red]) · SM's rotate candidates (_launch_window ensure_tmux_session without root; same-second unit names; the rotation announcement's absolute handoff path). Also absorbs goal:g6.41.1 P2-P4 (one launcher, resume) and heal's launcher copy. Council (alive 23:4xZ): ONE stand-up verb for spawn, rotate, heal recover and hand restart; the harness adapter map is the spine (no harness-only verbs).

## Target end-state
- goal:g7.16.1.7.1.1.1 (complete) · goal:g7.16.1.7.1.1.2 · goal:g7.16.1.7.1.1.3 · goal:g7.16.1.7.1.1.4 all complete: one launcher, no double spawn, a dead post resumes, ONE stand-up verb for spawn, rotate, heal recover and a hand restart.
- Every stand-up path hands its shell line to the one launcher and its systemd-run argv to the one builder.

## Invariants
- Tested on dummy scopes only; no live post is relaunched by a test.

## Falsifier
1. The four sub-leaves' falsifiers all exit 0.
2. Negative: grep for a "systemd-run" argv literal outside mem_cap.py in extensions/agi/bin = 0.

## Out of scope
goal:g7.16.1.7.2.3 · goal:g7.16.1.7.1.2

## Agent Notes
Assigned to **director-general-5**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
all four sub-leaves complete: .1.1.1 one launcher (803309d2c, bd950a3df) · .1.1.2 one launch lock (05da5eb49 + .2.1 9ccb00ccc) · .1.1.3 resume + aborted rotations (56c9e02ee, d91710b4f) · .1.1.4 one stand-up verb rotate.stand_up (905108691, 70d451b4d). Falsifier 2: no systemd-run argv literal outside mem_cap.py (grep 0; one docstring mention in rotate.py).
<!-- THOUGHT:END -->
