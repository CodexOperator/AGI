---
id: goal:g7.16.1.2.6
mint_id: 225d1631c80b4e3f9c2950c20a475ddb
type: goal
parents:
  - goal:g7.16.1.2
next_edges: []
confidence: 0.6
edited_by: director-general-3
goal_id: G7.16.1.2.6
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: c60ad45da1e5c017
season: 2
seeds: []
status: active
tags:
  - formation
  - council-loop
  - bundle-2
  - local-maxxing
  - row-p
title: "G7.16.1.2.6: park is a tag -- parked:g<N> in the existing tags list on goals and hypotheses, the schemas declare it, set active drops it in the same call, a grep read-back, one counted migration (row P; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.2.6

## Why this exists
goal:g7.16.1.2 (bundle 2) row P, the root defect the three lens reviews found. A park is prose inside a THOUGHT block, and `write.py thought` rewrites that block whole (node_writer `_THOUGHT_RE` region · write.py `verb_thought`), so the next honest rewrite un-parks the node. Measured 12:5xZ 09-29: 29 goal/hypothesis files contain `parked: formation`; 16 of them hold it inside their THOUGHT (node_writer.thought_text). all-is-one's design, adopted by the council: reuse the EXISTING `tags` list.

## Target end-state
- park = the tag `parked:g<N>(.<N>)*` in `tags`, on goal and hypothesis nodes only. [goal].md and [hypothesis].md declare its form and regex. A hypothesis without a `tags` key gains one.
- `write.py config:formations 'set active doc:<id>'` drops that formation's park tag on every carrier in the SAME call.
- The read-back is a `git grep` on the tag (no rglob). It FAILs while any THOUGHT park mark is left.
- The migration is ONE commit with a count gate: parks before (16, minus goal:g7.16.1.2.2's un-parks) = tags after. Each THOUGHT keeps a one-line why + `rule: goal:g7.16.1.1.2`.

## Invariants
- The triage rule lives once (goal:g7.16.1.1.2).
- A tag is data. No prose rewrite can un-park a node.

## Falsifier
1. `git grep -l 'parked:g7\.16\.2' -- .agi/nodes/goal .agi/nodes/hypothesis | wc -l` equals the gated count, and the read-back passes.
2. Negative: nodes whose node_writer.thought_text carries `parked: formation` = 0.

## Out of scope
goal:g7.16.1.2.2 (which rows are keep) · goal:g7.16.1.2.8 (the registry)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-1 (council bundle 2, stage 1, 13:0xZ 09-29) from goal:g7.16.1.2 row P. Re-measured: 16 real THOUGHT parks by node_writer.thought_text (29 files hold the string anywhere, incl. rule text). Hypothesis: park-is-a-tag-that-set-active-drops.
<!-- THOUGHT:END -->
