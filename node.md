---
id: build:skills-agi-memory-guard-SKILL.md
mint_id: a1df0faa5fd145c4ba7d5dbbf4e8e114
type: build
parents:
  - goal:g4.18.2
  - idea:engine-skill-doc
next_edges: []
build_kind: prose
edited_by: thought-master
link_ref: skills/agi-memory-guard/SKILL.md
location: source_root
payload_ref: skills/agi-memory-guard/SKILL.md
scaffold_hash: 7f47ece111f6c6e3
season: 2
title: Skills agi memory guard SKILL.md
town: core
---
# build:skills-agi-memory-guard-SKILL.md

`skills/agi-memory-guard/SKILL.md` — a flow skill (goal:g4.18.2): reading, finding, stopping and freeing on the shared box (memory, io, disk, orphan and stage scopes, never-print sources), reachable from every post through the committed `.claude/skills/agi-memory-guard` symlink. Posts' cards list it instead of carrying these traps.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version (thought-master, 09-27 19:2xZ). OWNER in the thought-master pane 19:22:48Z 09-27, verbatim: "Sounds like we need a memory guard skill so you can offload all those traps there 
  This is owner typing in directly". (1) Content = the thought-master card traps memory / io / disk / stages / relaunch / holds+ / printing, collapsed to rules; each card entry is replaced by the pointer `skill agi-memory-guard`. (2) Scope named by the traps it carries: the box (memory, io, disk, processes), not spend or dispatch (agi-dispatch) -- one skill per flow. (3) Parents [goal:g4.18.2, idea:engine-skill-doc] = the shape every flow skill uses ([build].md parent_shapes [goal, idea]). (4) Claude posts see it through the committed .claude/skills symlink at once; the only written listings (doc:unified-master-brief Skills line, config:rotations facts) are the Prime's -- asked by [rule].
<!-- THOUGHT:END -->
