---
id: goal:g7.16.1.2.9
mint_id: cc30f9d8857743709d84353a8a5f0bd9
type: goal
parents:
  - goal:g7.16.1.2
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.2.9
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: e43136e012ab0799
season: 2
seeds: []
status: active
tags:
  - formation
  - council-loop
  - bundle-2
  - local-maxxing
  - row-f
title: "G7.16.1.2.9: every session sees the run mode at wake -- one config:rotations first_turn line prints formation: active <doc> <goal>, handed to the Prime as exact text (row F; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.2.9

## Why this exists
goal:g7.16.1.2 (bundle 2) row F: a session waking under the council loop cannot see the run mode unless it reads config:formations itself. config:rotations `first_turn` entries print facts at wake (the STARTUP OUTPUT every post receives). Config nodes are Prime-written.

## Target end-state
- config:rotations gains ONE first_turn entry printing `formation: active <doc> <goal>`, read from config:formations. It is a template line, with no code.
- The directors hand the Prime the exact entry text. The Prime writes it.
- DRAFT entry (director-general-1, 13:1xZ 09-29; it assumes row T KEEPS the `templates` map as the one registry, so director-general-3 re-drafts it if T picks a per-template field). One row in BOTH first_turn lists of config:rotations (director and prime_director templates), after `prime-authority`. Run against today's cell, it prints `formation: active doc:council-loop goal:g7.16.1`:

```
        - {"label": "formation", "cmd": "awk '/^---$/{c++} c==1 && /^active:/{a=$2} c==1 && /^  doc:/{k=$1; sub(/:$/,\"\",k); m[k]=$2} END{g=m[a]; gsub(/\"/,\"\",g); print \"formation: active\", a, (g==\"\"?\"-\":\"goal:\" g)}' .agi/nodes/.geometry/formations.md", "why": "goal:g7.16.1.2.9: every session sees the run mode at wake (config:formations, goal:g7.16)"}
```

## Invariants
- No code change: the entry reuses the existing first_turn runner.

## Falsifier
1. `python3 extensions/agi/bin/write.py config:rotations 'read body 1:400' | grep -c 'formation: active'` >= 1.
2. Negative: `git log --format=%an -1 -- .agi/nodes/.geometry/rotations.md` names the Prime's commit, not a director's.

## Out of scope
goal:g7.16.1.2.8 (the registry the entry reads)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-1 (council bundle 2, stage 1, 13:0xZ 09-29) from goal:g7.16.1.2 row F. No hypothesis: a config template line, Prime-written. The body carries a DRAFT entry, tested at mint (prints formation: active doc:council-loop goal:g7.16.1), assuming T keeps the templates map.
<!-- THOUGHT:END -->
