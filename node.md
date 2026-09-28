---
id: build:skills-agi-dispatch-SKILL.md
mint_id: fe64c6cd6b4e44f3a36723c2eba06abc
type: build
parents:
  - goal:g4.18.2
  - idea:engine-skill-doc
next_edges: []
build_kind: prose
edited_by: belam
link_ref: skills/agi-dispatch/SKILL.md
location: source_root
payload_ref: skills/agi-dispatch/SKILL.md
scaffold_hash: c4b906c47c83e0a9
season: 2
title: Skills agi dispatch SKILL.md
town: core
---
# build:skills-agi-dispatch-SKILL.md

`skills/agi-dispatch/SKILL.md` — a flow skill (goal:g4.18.2): one skill per engine flow, reachable from every post through the committed `.claude/skills/agi-dispatch` symlink. Posts' cards list it instead of carrying its rules.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
OWNER 06:4xZ 09-28 to belam, verbatim: "Again DE needs to use the board to post progress updates. Maybe add a correction to the goal harvest or goal lifecycle skill to remind roles to use the town board for progress tracking to help keep cards trim." -- ONE rule, one source: the progress row lives in agi-dispatch 5 (the harvest table, where progress happens); agi-goal carries a one-line pointer to it. Near miss: a line only in agi-goal satisfies the words and never fires, because a director reads agi-goal when it MINTS a goal, not when it harvests one.
<!-- THOUGHT:END -->
