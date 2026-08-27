---
id: "outcome:session-management-r1-r1"
mint_id: ebab71c32fb3403a8a56b88811a2e40a
next_edges:
  - bigger_outcome:session-management-r1
parents:
  - mvp:session-management-r1-r1
tags:
  - session-management-r1
  - session
  - outcome
title: Session Management Outcome
type: outcome
---

# Session Management Outcome

## Input Shape
- Graph: nodes/ directory with YAML frontmatter files
- Git: clean working tree with recent commit

## Output Shape
- Restored graph identical to captured state
- Fidelity: 100% (committed state)
- Chains: preserved
- Git HEAD: preserved

## Behavior
- Save: commit nodes/ directory
- Crash: git checkout HEAD -- nodes/
- Restore: loader reads YAML, reconstructs graph

## Edge Cases
- Uncommitted files: NOT preserved (expected - git only tracks committed files)
- Corrupt YAML: loader skips with warning
- Empty nodes/: produces empty graph
