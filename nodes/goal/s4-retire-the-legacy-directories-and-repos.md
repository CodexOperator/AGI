---
confidence: 1.0
goal_id: S4
goal_kind: short-term
heading_level: 2
id: "goal:s4"
mint_id: 351125dd5d3942a2aa032920cb12771c
order: 75
origin: goals-doc
seeds: []
status: horizon
tags:
  - goal
  - root
  - short-term
title: "S4: Retire the legacy directories and repos"
type: goal
---

Housekeeping carried from TODO **C1–C6**, gated on bug-sweep clearance and
grouped here because none of it is worth its own long-term goal:

- `~/autoresearch-tree/` local directory (C1) and the
  `CodexOperator/autoresearch-tree` repo (C2) — archive rather than delete.
- The old pi fallback under `~/.pi/agent/git/.../extensions/autoresearch-tree/`
  (C3), pending verification that nothing resolves through it.
- The modularNN spike worktree (C4) and legacy `~/.hermes/agi/` artifacts (C5).
- `.claude/skills/gitnexus/*/SKILL.md` accidentally tracked (C6).

Do these last. Every one is a deletion, and the two data-loss defects this
project has already paid for both arrived as routine cleanup.
