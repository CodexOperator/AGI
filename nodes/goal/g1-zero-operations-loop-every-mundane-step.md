---
confidence: 1.0
goal_id: G1
goal_kind: long-term
id: "goal:g1"
origin: goals-doc
seeds:
  - goal:g1.1
  - goal:g1.2
  - goal:g1.3
  - goal:g1.4
  - goal:g1.5
  - goal:g1.6
  - idea:engine-cli
  - idea:engine-driver-sh
  - idea:engine-find-root
status: horizon
tags:
  - goal
  - root
title: "G1: Zero-operations loop: every mundane step is a command"
type: goal
---

The ethic above, reduced to buildable surface. An agent should never spend
motion on tending the machine: no hand-pasting a rendered map into a spawn
prompt, no hand-writing a config, no syncing by hand.

**Invariant:** any repeated, mechanical step is a named command, and every
surviving manual handle carries a written reason.

Already banked — cron owns all remote traffic (H10), embedded maps cut kids from
11–13 tool calls to 5–7 (L7), the DONE contract makes stopping one line.

Owns: **L11** remainder (one command that renders *and* spawns — the parent's
last machine-tending chore), **L12** remainder (a runtime flag rather than a
parallel code path; hook parity audit), **L17** (config schema plus a writer, so
configs stop being hand-written), **L18** action 2 (`agi-tree init` scaffolds a
project), **H6** (`--iter-base N` for `dispatch.py`, so a run stops clobbering
prior session manifests).
