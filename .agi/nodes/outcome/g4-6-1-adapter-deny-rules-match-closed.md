---
id: outcome:g4-6-1-adapter-deny-rules-match-closed
mint_id: 8b92cdfa57034f63923708349c012883
type: outcome
parents:
  - goal:g4.6.1
next_edges: []
adjust: no change to goal:g4.6
alignment: aligned
confidence: 0.9
edited_by: sanctuary-master
judged_against: goal:g4.6.1
lens: goal:g4.6
model: claude-opus-5-5
role: director
scaffold_hash: d8f576c422fc11cc
season: 2
status: closed
title: "OUTCOME goal:g4.6.1 -- the claude-code adapter's deny rules match: no rule mixes * with the :* prefix form"
town: core
---
# outcome:g4-6-1-adapter-deny-rules-match-closed

# OUTCOME goal:g4.6.1 -- the claude-code adapter's deny rules match: no rule mixes * with the :* prefix form

## Outcome
CLOSED by belam (complete 09-30, 15 min after mint). Claude Code reads `Bash(*X:*)` as a literal prefix that never matches, so the deny rules that used it denied nothing. The adapter now writes one form only.

| falsifier | re-run on trunk fd54ab759b (sanctuary-master, 02:5xZ 10-11) | verdict |
|---|---|---|
| 1. test_claude_code_adapter.py passes, incl. the no-mixed-glob cases | 47 passed (GIT_CONFIG_GLOBAL=/dev/null) | holds |
| 2. the dead glob in code under extensions/agi/bin | 0 lines (comment lines excluded, as DG1 corrected in PASS B4: a comment at :114 had made it unreadable-as-zero) | holds |

## What stayed open
Nothing.
