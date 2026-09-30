---
id: goal:g6.41.1.1
mint_id: bdc3d0ee6158488791c064e4ce25d49d
type: goal
parents:
  - goal:g6.41.1
next_edges: []
confidence: 0.85
edited_by: belam
goal_id: G6.41.1.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 3846d190fd510f39
season: 2
seeds: []
status: active
tags:
  - goal
  - g6
  - heal
  - reboot
  - wake
title: "G6.41.1.1: a session the boot path resumes gets exactly one first turn -- a reboot needs no human keystroke"
town: core
---
# goal:g6.41.1.1

# goal:g6.41.1.1

## Why this exists
goal:g6.41.1 (the posts survive an oomd kill; heal RESUMES dead seats): MEASURED at the planned reboot of 09-30 01:55Z by belam. At 02:02:47Z the boot path relaunched the Prime in tmux window @0 with `--resume` on its own transcript (tmux server parent = systemd --user), and heal's first pass (02:02:59Z) correctly saw it alive ("stale-row seat belam ... live session 284d4866 pid 3933 alive"). But NO first turn reached the resumed session, so it sat idle until the owner typed (owner: "I wonder why you failed to come back automatically we had a bunch of reboot guards and scripts"). A rotation's after_join sends the wake line; the reboot path sends none.

## Target end-state
- Every session the boot path resumes gets exactly ONE first turn after its join (the same wake text rotation's after_join delivers: the card's where-it-stops line + "you were resumed after a reboot"), so a reboot needs no human keystroke.
- The wake names the reboot (boot time from `uptime -s`), so the post knows its session crons and background tasks died with the process and re-arms them.

## Invariants
- One wake per resumed session per boot; a fresh (non-resumed) launch keeps its brief-as-first-turn, never a second wake.
- The wake is typed only into an idle input box (the strand rule of send.py wake).

## Falsifier
1. A dummy post resumed through the boot path shows exactly one wake turn in its transcript after join (test under AGI_LIVE_SYSTEMD=1, dummy session, never a live post).
2. Negative: zero resumed sessions idle with an empty first turn 2 min after boot on the next reboot (heal log, now timestamped: goal:g6.41.2).

## Out of scope
goal:g6.41.1 P2 (heal resumes dead seats instead of fresh launches) · goal:g6.41.2.

## OWNER 2026-09-30 02:0xZ, verbatim
"I wonder why you failed to come back automatically we had a bunch of reboot guards and scripts."

## Agent Notes
Assigned to **director-general-1**.
