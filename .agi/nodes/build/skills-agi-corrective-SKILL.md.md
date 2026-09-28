---
id: build:skills-agi-corrective-SKILL.md
mint_id: f15b8f39fa1a4c279e5c8ea1925c397f
type: build
parents:
  - goal:g4.18.2
  - idea:engine-skill-doc
next_edges: []
build_kind: prose
edited_by: director-engine
link_ref: skills/agi-corrective/SKILL.md
location: source_root
payload_ref: skills/agi-corrective/SKILL.md
scaffold_hash: 0cd66e3d80538957
season: 2
title: Skills agi corrective SKILL.md
town: local-maxxing
---
# build:skills-agi-corrective-SKILL.md

`skills/agi-corrective/SKILL.md` — a flow skill (goal:g4.18.2): merge-up-review residue -> triage -> the orders written onto the hypothesis node as a `## CORRECTIVE DH.<N>` section -> corrective round cut from the loop tip -> re-mur. Reachable from every post through the committed `.claude/skills/agi-corrective` symlink; cards list it instead of carrying its rules.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
OWNER 2026-09-28 05:1xZ to director-engine, verbatim: "Well ok if you’re just gonna run text fixes as subagents let’s just change the skill rule to say dispatch kids on opus cc harness instead for text fixes. Or sonnet, whatever model you used for the subagents. The templates and configs should support it. Just change the skill to explain how it works. Let prime know if you need any changes that only he can make." + "And let them run parallel using the CC memory limits" + "There’s a memory guard skill". Earlier (05:0xZ): "If the residue is pure text fixes just do them yourself and batch into the next mur. Add that as a rule to the corrective issue skill". This version: §3a = a claude-code TEXT-FIX KID per pure-text round, all dispatched at once, one batched mur. Measured: dispatch.py --dry-run --tier kid --harness claude-code --branch --orders resolves `claude -p --model claude-sonnet-5` in a 2G scope (spawn.memory_max); harnesses.claude-code.max_live is the per-harness parallel cell (spawn_budget.py:580), absent today. Near miss: `--tier parent` gives claude-opus-5, not a current id, and a parent spawns pi-free kids of its own -- so Opus text kids wait on the Prime's row; the rule ships on Sonnet, which works today.
<!-- THOUGHT:END -->
