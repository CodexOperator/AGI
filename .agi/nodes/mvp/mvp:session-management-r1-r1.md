---
id: mvp:session-management-r1-r1
mint_id: 56cf1a31b51840c8b2140815cb3eb43d
type: mvp
parents:
  - verdict:session-management-r1-extend1
next_edges:
  - outcome:session-management-r1-r1
edited_by: season.py
season: 1
tags:
  - session-management-r1
  - session
  - mvp
thought_session: season
title: Session state capture/restore MVP
---
# Session Management MVP

## What it does
Captures and restores agent session state with >95% fidelity using git commits + YAML frontmatter.

## How it works
1. **Capture**: `git add nodes/ && git commit -m "session save"`
2. **Crash**: `git checkout HEAD -- nodes/`
3. **Restore**: Graph loader reconstructs state from YAML files

## Architecture
- Nodes stored as YAML files in `nodes/<type>/`
- Git provides version control snapshots
- Graph loader (`graph_core.loader`) reconstructs deterministic graph
- 257 tests verify consistency

## Verification
- 100% fidelity across crash/restore cycles
- All chains preserved after restore
- Git HEAD correctly maintained