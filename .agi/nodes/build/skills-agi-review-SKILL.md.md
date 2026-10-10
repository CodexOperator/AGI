---
id: build:skills-agi-review-SKILL.md
mint_id: 2c6e6f385587467b8e676c4909de3c1e
type: build
parents:
  - goal:g7.16.1.2.3
  - idea:sonnet-subagent-reviews-from-a-graph-brief
next_edges: []
build_kind: prose
edited_by: belam
link_ref: skills/agi-review/SKILL.md
location: source_root
model: claude-opus-5-5
role: prime_director
scaffold_hash: 03bd92d9b68e9e18
season: 2
title: Skills agi review SKILL.md
town: core
---
# build:skills-agi-review-SKILL.md

`skills/agi-review/SKILL.md` — a flow skill (goal:g4.18.2): review a merge range (BASE..TIP) as Sonnet subagents from the graph-held brief `doc:agi-review-brief` — review-lanes.sh cuts the range into area lanes, one Sonnet reviewer per lane, ONE adversarial Sonnet verifier over every lane's findings; the RED scans stay mechanical. Reachable through the committed `.claude/skills/agi-review` symlink. Replaces workflow.py reviews (owner 00:4xZ 10-10, verbatim on idea:sonnet-subagent-reviews-from-a-graph-brief). Used for PASS B5 and B6 and every merge-up gate since.
