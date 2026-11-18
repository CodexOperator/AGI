---
id: goal:g5.4.3.3
mint_id: 5d9dc73c335544ed83c13c7e050236ef
type: goal
parents:
  - goal:g5.4.3
next_edges: []
confidence: 0.5
goal_id: G5.4.3.3
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 4d5c7606b1c8203d
season: 3
seeds: []
status: active
tags:
  - report
  - schema
  - owner
title: "G5.4.3.3: a report node schema with four kinds (research presentation, research paper, algo-optimized video, SEO-optimized blog post), shaped by the council"
town: core
---

# goal:g5.4.3.3

## Why this exists
goal:g5.4.3 (the Meme Master post: the owner's presentation and the paper after it). It ran one presentation (deck v1.x) and one paper (L608's P1-P3 experiments, verdicts L623, L624, L627, draft v0.3) through the graph, each as an ad hoc doc node with no shared shape. The paper route grew a reusable review shape (idea, hypotheses, experiments with a plant control and blind scorers, verdicts, fixes folded into the next draft); the presentation never had one. The owner asked, 11-18, for the council to formalize a report node schema over four kinds (verbatim below).

## OWNER 2026-11-18 15:2xZ, verbatim (via meme-master)
"We will improve our presentation and paper processes as we go along. Ask council to formalize "report" node schema with types "research presentation, research paper, algo-optimized video, SEO-optimized blog post." They can optionally make it a type of the doc node with subtypes. However they wanna matrix it out."

## Target end-state
- One schema file under .agi/context/schemas/ defines a report node, its four kinds (research presentation, research paper, algo-optimized video, SEO-optimized blog post), its required fields and its legal parents; the shape (a new type, or doc with a subtype field, or a matrix such as kind x stage or kind x audience) is the council's choice, recorded with its reason in the schema file.
- The schema registry reads it, and `links.py schema` checks report nodes against it like any other type.
- The two report routes already run (deck v1.x, paper v0.x) are expressible in it: each could be re-typed as a report node of its kind without losing a field.

## Invariants
- No paper or deck text enters the graph through this schema: a report node points to its private artifact by sha, as doc:draft-paper-v0 does.
- An existing node is never deleted to fit the schema; a re-type is an edit in place or a retire, never a git rm.

## Falsifier
1. `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] && ls .agi/context/schemas/ | grep -qiE 'report' && grep -qiE 'research presentation' .agi/context/schemas/*report*.md && grep -qiE 'research paper' .agi/context/schemas/*report*.md && grep -qiE 'video' .agi/context/schemas/*report*.md && grep -qiE 'blog' .agi/context/schemas/*report*.md` exits 0 (or, if the council chooses doc + subtype, the same four kinds grep green in [doc].md and this falsifier is amended to that path in the same commit).
2. Negative: `python3 extensions/agi/bin/links.py schema` reports 0 report-kind nodes missing a required field once the schema lands.

## Out of scope
goal:g5.4.3.1 and goal:g5.4.3.2 (the presentation and the paper themselves) · deck v1.2's two owner defects (notes split across slides; low-resolution text), which ride the deck's next version · the Cloudflare Pages publish of the deck.

## Agent Notes
Assigned to **the council (plasma · less-is-more · remix)**.
