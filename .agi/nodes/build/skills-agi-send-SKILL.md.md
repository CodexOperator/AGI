---
id: build:skills-agi-send-SKILL.md
mint_id: 1d1aa6b3e708408b8e82b738a651cf42
type: build
parents:
  - goal:g4.18.2
  - idea:engine-skill-doc
next_edges: []
build_kind: prose
edited_by: thought-master
link_ref: skills/agi-send/SKILL.md
location: source_root
payload_ref: skills/agi-send/SKILL.md
scaffold_hash: 19fd95c728a41e5d
season: 2
title: Skills agi send SKILL.md
town: core
---
# build:skills-agi-send-SKILL.md

`skills/agi-send/SKILL.md` — a flow skill (goal:g4.18.2): one skill per engine flow, reachable from every post through the committed `.claude/skills/agi-send` symlink. Posts' cards list it instead of carrying its rules.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
thought-master 09-27 23:44Z: §2 row "read returns empty -> phantom: nothing else" REPLACED -- it contradicted the owner's 02:28Z rule ("Check dm file directly nudges have been buggy") -- by: read empty is not proof; check the dm files + inbox file + rooms directly; plus a row for the background watcher keyed on ts. OWNER in the thought-master pane 23:44:06Z, verbatim: "It may have been the prime, the send skill should have something about checking dm files directly in case phantoms arrive". Measured the same turn: every comms file changed in 20 min + every room's newest block + send.py rooms/peek -> no missed message for thought-master (the nudge was the marker).
<!-- THOUGHT:END -->
