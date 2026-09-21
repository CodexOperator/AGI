---
id: goal:s33
mint_id: 70fc9c0443ec43bc89f18b769187a114
type: goal
parents:
  - goal:g15
next_edges: []
confidence: 1.0
edited_by: season.py
goal_id: S33
goal_kind: short-term
heading_level: 2
origin: goals-doc
scaffold_hash: 38059e6af16cef9f
season: 1
seeds: []
status: active
tags:
  - goal
  - root
  - short-term
thought_session: season
title: "S33: The docs say what the tree does now"
---
# goal:s33

## Agent Notes
"Owner ask, 2026-09-04. After loop L1 (L1.08 to L1.11) the docs drifted: QUICKSTART.md still describes pre-L1 state (CC-only dispatch, iter-NNN numbering, kits, render-context), CLAUDE.md and skills/agi/SKILL.md carry rules for things that no longer exist or now exist (claude-code harness real, loop-scoped ids real, build-site cohort retired, evidence gate on the commit path, spawn.parallel semantics, workspace weekly budget). Commit to one sweep: every claim in QUICKSTART.md, CLAUDE.md, skills/agi/SKILL.md and HANDOFF.md section 5 is checked against the tree and corrected or deleted, with the commit citing what was stale. Falsifier: a test that greps the docs for retired names (render-context.py, payloads/, grid.py checkout as a live command, context/kits) and fails on any hit outside a sentence that marks it retired."

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
"Minted by the L1.08 director at the owner request; standalone because it spans every doc."
<!-- THOUGHT:END -->