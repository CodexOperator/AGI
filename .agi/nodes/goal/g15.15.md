---
id: goal:g15.15
mint_id: 5c46f02b89ac423c96b0a7591745f3f2
type: goal
parents:
  - goal:g15
  - build:bin-rotate
  - build:hooks-cc-session-start.sh
next_edges: []
confidence: 0.7
edited_by: sensei-director
goal_id: G15.15
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 0680e85cd94cdf4b
season: 2
seeds:
  - hypothesis:l4-startup-first-turn-is-performed-by-the-service-and-the-hook-fires-at-turn-one
status: active
tags:
  - goal
  - subgoal
  - l4
  - sanctuary-director
thought_session: sensei-director-genI-L1
title: "G15.15: 0b-b — every spawn path exports AGI_SEAT and writes the bootstrap record before the spawn, so the SessionStart hook fires at turn one"
town: core
---
<!-- BODY:BEGIN -->
**0b-b: every spawn path exports `AGI_SEAT` and writes the bootstrap record BEFORE the successor's `claude` starts, so the SessionStart hook copy fires at turn one on the live path.** The brief is the point's stub `hypothesis:l4-startup-first-turn-is-performed-by-the-service-and-the-hook-fires-at-turn-one` (taken over by this seat on the Prime's 16:1xZ order; the point had it queued behind g15-28 and had not cut it) — its claim, falsifiers, file scope and ceiling stand unchanged; this goal is where the round is tracked.

## Why this exists

- `goal:g15` is the parent because g15-7 (merge-up 27 review by name, wf_6699487e-b72) is a bugfix finding fixed in-loop: "the hook copy keys on AGI_SEAT, which NO spawn path exports, and the bootstrap record is written AFTER the spawn — the SessionStart injection cannot fire at turn one on the live path". Measured on today's bytes: `_shell_cmd` exports only the reaper knob (+ the ultracode knob), `_write_bootstrap` is called in `cmd_rotate_self` after `spawn_window` returns, and `cc-session-start.next.sh:236` reads `BOOTSTRAP_SEAT="${AGI_SEAT:-}"`.
- `build:bin-rotate` is the parent because the spawn path (`_shell_cmd` -> `_launch_window`, `cmd_rotate_self`'s bootstrap step) is the mechanism that changes: the export rides in front of the launch line the way the reaper knob already does, and the bootstrap write moves ahead of the spawn.
- `build:hooks-cc-session-start.sh` is the parent because the hook (its `.next.sh` COPY is the proof surface; the LIVE hook and `~/.claude/settings.json` are the Prime's install, deferred to this round's merge-up) is the consumer whose turn-one injection the export and the record order exist for.

## Tracking

Dispatch target = the hypothesis (seeds). Serial gates named on the node (L4.127, g15-6) are both harvested (merge-ups 28, 31). The Prime installs into the live global hook and verifies with a fresh session at THIS round's merge-up (L4.94 rule); the round proves on the COPY only.