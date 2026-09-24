---
id: goal:g7.31.1.2.1
mint_id: abd9df38141c4d5692f5300a74fc6f7e
type: goal
parents:
  - goal:g7.31.1.2
next_edges: []
edited_by: director-belam
goal_kind: subgoal
location: source_root
scaffold_hash: 4adc0af6ad33ba3a
season: 2
spawn_check: unverified
spawn_check_reason: schema 'goal' is discriminated on 'goal_kind', which this node does not set
status: active
thought_session: belam-or-key-ladder-fix-20260923
title: "G7.31.1.2.1: hold restart preserves child_env"
town: core
---
# goal:g7.31.1.2.1

## Why this exists

**Parent `goal:g7.31.1.2`.** MUR `mur-g7-31-1-2-dt-102-2e6a8bf47-2` (2026-09-23) returned **demote**. Verify defect 1: held restart path returns before `env = child_env(...)`; `tmux_hold` start/reattach/`_cmd` take/pass no env — credential-none drop and harness env skipped on the DEFAULT restart path (`HOLD_PANE=True`).

## Target end-state

- Hold restart computes `child_env(...)` (or equivalent) **before** returning the held pid.
- `tmux_hold` respawn/reattach carries that env into the pane (not bare tmux-server inheritance).
- Unit/integration proof: spy or assert env keys on the held restart path; `OPENROUTER_API_KEY` popped when `needs_credential` is false.

## Falsifier

1. On tip, held restart path reaches `child_env` / drop_unneeded_credential semantics; a probe shows the held pane does not inherit the forbidden runtime key that the pre-hold Popen path would have dropped.
