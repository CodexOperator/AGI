---
id: goal:g7.16.1.11.23
mint_id: a0508c7cde5241e78d9759a1b28527ff
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: director-general-1
goal_id: G7.16.1.11.23
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: d1986eb683b7c022
season: 2
seeds:
  - goal:g7.16.1.11
status: horizon
tags:
  - council
  - v5
  - belam
  - session-name
  - g7.16.1.11
title: "G7.16.1.11.23: belam v5 session is named belam-s2-<roman generation> (I = the session that filed this), set at the rotation and not by hand; no loop number; every other post session name unchanged"
town: core
---
# goal:g7.16.1.11.23

## Why this exists
goal:g7.16.1.11: belam is the one post now on the new engine whose app-list session name is the old loop-numbered one (belam-S2-L5-XXII); the owner asked for the season and the generation in it and no loop number. The boot cell .agi/nodes/.geometry/engine.md:94 renders `claude --remote-control \(.name)` for every claude-code post (checked at trunk 13779f1ba0), so a post's session name IS its row name; no cell carries a different session name and nothing counts a generation into one. This leaf is the sibling of goal:g7.16.1.11.17 (belam on v5, complete), which left the name as it was.

## OWNER 2026-10-09 01:2xZ, verbatim (via belam belam-s2-I [owner] 01:2xZ)
"Also your session name is missing the season name and your generation. No need to include loop number anymore" · "Just belam-s2-I and you can restart since it's new engine ... Can rename your session next rotation not needed immediately".

## Target end-state
- belam's v5 session is named `belam-s2-<roman generation>`: the generation restarts at I with the session that filed this leaf (belam-s2-I), its successor is belam-s2-II, and no loop number appears.
- The name is set by the rotation that seats the successor, never by hand in a row or a window, and the owner's app list shows it.
- Only belam's session is renamed: every other post's session name is still its row name, byte for byte.

## Invariants
- The mint id and the post's row name `belam` do not change; only the session name does (a session name is not a post name, and no other node reads it as one).
- Nothing is renamed immediately: the first name change is at the next rotation (owner: "not needed immediately").
- The rule is data in the graph (a cell the boot render reads), not a branch on the name `belam` in the render's code.

## Falsifier
1. A lane in extensions/agi/tests renders the boot cell for a belam row at generation I, II and a later one and reads `--remote-control belam-s2-I`, `belam-s2-II` and the roman numeral of that generation; `bash <lane>` exits 0 only then.
2. Negative: the same render for every other claude-code row is byte-identical to the render at trunk 13779f1ba0 (diff empty), and `git grep -n 'belam-s2-' -- .agi/nodes/.geometry/posts.md` shows 0 hits (the name is derived at the rotation, not hand-written into the row). If the council moves the cell, the negative follows the cell.

## Out of scope
The post name `belam` and every other post's session name · the loop number itself (retired from the name by the owner) · the old setup's window names (belam-S2-L5-*) · renaming the live session before the next rotation · goal:g7.16.1.11.15 phase W (the council's flow-rotation design; this leaf only needs the rotation to set the name).

## Agent Notes
Assigned to **director-general-1** (filed 10-09 by belam's [owner] 01:2xZ; placement and design are the council's, belam).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-09 01:3xZ: filed on belam [owner] belam-s2-I 01:2xZ (owner verbatim in the body). HORIZON, not active: the owner said not needed immediately and the placement + design are the council. Checked on the bytes: engine.md:94 renders claude --remote-control (.name) for every claude-code post, so the session name is the row name today; the leaf asks for a derived belam-only name set at the rotation. The sibling .17 left the name alone. No prior version.
<!-- THOUGHT:END -->
