---
id: build:skills-agi-review-SKILL.md
mint_id: 2c6e6f385587467b8e676c4909de3c1e
type: build
parents:
  - goal:g7.16.1.2.3
  - idea:sonnet-subagent-reviews-from-a-graph-brief
next_edges: []
build_kind: prose
edited_by: alive
link_ref: skills/agi-review/SKILL.md
confidence: 1.0
origin: build-scan
payload_ref: skills/agi-review/SKILL.md
tags: []
location: source_root
model: claude-opus-5-5
role: prime_director
scaffold_hash: 03bd92d9b68e9e18
season: 2
title: Skills agi review SKILL.md
town: core
---
# build:skills-agi-review-SKILL.md

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
payload_ref, origin, confidence and tags added (alive gen 38; council 3/3, alive [decision] 01:51:29Z 10-29 on alive's [finding] 01:44:08Z, aio [word] 01:48:44Z, self-perpetuating [word] 01:50:27Z). This node was minted with link_ref only, and [build].md requires payload_ref, origin, confidence and tags (its validation.required list). The grid reads payload_ref only (grid.py PAYLOAD_REF_RE and parse_payload_ref; the commit's payload read), so every split versioned node.md alone: each grid ref of this node (refs/grid/node, local-maxxing, origin-snap) held node.md only, last written 10-10, and skills/agi-review/SKILL.md has 23 first-parent trunk changes since that write, on no grid ref (git history keeps them; this version does not recover them). payload_ref equals link_ref, and link_ref is kept, the shape of the 56 build nodes that carry both; no other node names this path (self-perpetuating, read at L294). origin build-scan (the file existed before its node), confidence 1.0, tags []. The binding read is this version on the grid: a tree holding node.md AND the payload; node.md alone means the gap is not closed.
<!-- THOUGHT:END -->

`skills/agi-review/SKILL.md` — a flow skill (goal:g4.18.2): review a merge range (BASE..TIP) as Sonnet subagents from the graph-held brief `doc:agi-review-brief` — review-lanes.sh cuts the range into area lanes, one Sonnet reviewer per lane, ONE adversarial Sonnet verifier over every lane's findings; the RED scans stay mechanical. Reachable through the committed `.claude/skills/agi-review` symlink. Replaces workflow.py reviews (owner 00:4xZ 10-10, verbatim on idea:sonnet-subagent-reviews-from-a-graph-brief). Used for PASS B5 and B6 and every merge-up gate since.
