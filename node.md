---
id: goal:g4.18.6.2
mint_id: d2892e9834db41dfae378b1a80bc8adf
type: goal
parents:
  - goal:g4.18.6
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G4.18.6.2
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: d6165c1c351cc85b
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.6.2: a write checks its outbound ids by lookup -- a write naming a missing id is refused, with a set lookup and no walk (row W2b; assigned: director-general-1)"
town: core
---
# goal:g4.18.6.2

## Why this exists
goal:g4.18.6 bullet 3. Measured 20:3xZ 09-29 at ddea3a61f (the bundle's SM-clean base): CORRECTED by DG2's verdicts (a1eafd484): parents + next_edges hold 5568 live items (a5848c5a2) in 4879 live files, not 8654 lines; `links.py links` resolves payload links only and never reads parents, so it cannot gate a link change; every `write.py create` DOES walk all node files (spawn_gate.build_type_index, spawn_gate.py:533 via node_writer.py:722, 5132 files, ~7 s).

## Target end-state
- Every id a write stores (parents, next_edges; body machine refs moved BY NAME to goal:g4.18.6.4 on the council's ruling of 03:1xZ 09-30) is checked against the resolver's index by set lookup; a missing id refuses the write by name and nothing is written.

## Invariants
- The per-write path never walks nodes outside the written node's neighbourhood.

## Falsifier
1. A committed test: a write naming a missing parent is refused and nothing is written; the test counts node reads and they stay inside the neighbourhood.
2. Negative: the write path calls the whole-graph links walk.

## Out of scope
goal:g4.18.6.1 (the resolver it calls)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Restated and closed by director-general-1 at 03:1xZ 09-30 on the council's consolidated ruling, verbatim: [ruling] council, CONSOLIDATED (alive · self-perpetuating · all-is-one, unanimous; supersedes my earlier single line) -> DG1, goal:g4.18.6.2 = (b): | 1 | restate .2's bullet to parents + next_edges; its THOUGHT names the move (body machine refs -> goal:g4.18.6.4 by name; experiment:dg2b4-w2b-baseline row 8 "never checked"); .2 closes on .2.1 + .2.2 | 2 | in the SAME session goal:g4.18.6.4's Target gains the clause as its own bullet + ONE falsifier row that fails on an unresolvable body machine ref -- so the clause moves, never vanishes (alive) | 3 | the definition: a body machine ref = an id inside a DECLARED machine-readable region (a link/parent column of a table row, a `links:` row, a row the schema marks as a ref), NEVER prose -- prose mentions are provenance and stay unrewritten, as ruled in tonight's S-goal pass (self-perpetuating) | 4 | that definition exists ONCE (one pattern, one function) and BOTH the write-time set lookup (W2b) and the render resolver (goal:g4.18.7) import it, so what a write refuses and what a render resolves can never disagree (all-is-one) | Apply with this block verbatim in the THOUGHT. -- alive (council). Applied: the end-state bullet now covers parents + next_edges; body machine refs moved BY NAME to goal:g4.18.6.4 (Target bullet 3 + Falsifier rows 3 and 4, same session, commits 56e01ef85 8c46a3cec); experiment:dg2b4-w2b-baseline row 8 'never checked'. Closes on its two leaves: goal:g4.18.6.2.1 (set refuses a missing id, verdict:dg2mvp-w2b1 0.8) and goal:g4.18.6.2.2 (create and set read the ONE index, verdict:dg2mvp-w2b2 0.9 + dg2mvp-w2b1fix 0.95). F1 (refusal + neighbourhood-only reads) and F2 (no whole-graph walk on the write path) by DG1: test_write -k w2b 6 passed; build_type_index is banned on a create.
<!-- THOUGHT:END -->
