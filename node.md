---
id: goal:g4.18.6.4
mint_id: 3e9ff27780dc4dba9529706c07609ad4
type: goal
parents:
  - goal:g4.18.6
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G4.18.6.4
goal_kind: subgoal
origin: goals-doc
scaffold_hash: c24daa52235904bc
season: 2
seeds: []
status: active
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.6.4: the link lines store mint ids -- a counted migration, one type dir per round, links 0 broken after each, owner quotes and prose untouched (row W2d; assigned: director-general-1)"
town: core
---
# goal:g4.18.6.4

## Why this exists
goal:g4.18.6 bullet 1. Measured 20:3xZ 09-29 at ddea3a61f (the bundle's SM-clean base): 4881 live node files carry 8654 frontmatter link lines (parents + next_edges items); `links.py links` resolves 5035, 0 broken; write.py runs NO whole-graph walk today (the full walk runs in metrics.py on every --smoke and in verify).

## Target end-state
- Every parents / next_edges item and every machine reference stores the 32-hex mint id; prose references and owner quotes stay verbatim.
- One type dir per round, each with a before/after count gate; after the last round the address form in link fields is retired (goal:g4.18.6.3's dual accept closes).

## Invariants
- active + deprecated node count never drops; broken links = 0 after every round.

## Falsifier
1. `links.py links` prints 0 broken after each round, and the round's count gate matches (link lines before = mint-id lines after, for that dir).
2. Negative: a parents / next_edges item in `.agi/nodes` that is not a 32-hex mint id after the last round.

## Out of scope
goal:g4.18.6.5 (the re-point rule retires after this)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-1 (council bundle 4, stage 1, 20:3xZ 09-29): 8654 link lines are too many for one round. Hypothesis: link-lines-migrate-to-mint-ids-counted.
<!-- THOUGHT:END -->
