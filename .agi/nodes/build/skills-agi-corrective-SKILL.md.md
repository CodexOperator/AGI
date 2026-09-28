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
OWNER 2026-09-28 05:0xZ to director-engine, verbatim: "If the residue is pure text fixes just do them yourself and batch into the next mur. Add that as a rule to the corrective issue skill". This version: §3 gains a first triage row (every residue pure text -> no corrective round, the director fixes it on the loop branch and batches the range into the NEXT mur) and §3a draws the flow. Measured why: of 15 correctives this seat queued 04:0x-04:5xZ (EG.32-46), 5 were node-text only (EG.38 39 40 45 46) -- each would have cost a parent + kid round for write.py edits. Near miss: a MIXED round stays a corrective (its text items ride in it), so a code residue is never downgraded to a director hand-edit.
<!-- THOUGHT:END -->
