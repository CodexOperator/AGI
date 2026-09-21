---
id: hypothesis:l3w1-goal-kind-perpetual
mint_id: 593c27ea384141d092075c6e42baee27
type: hypothesis
parents:
  - goal:g5
next_edges: []
edited_by: ubuntu
scaffold_hash: a7c73509c2933a42
season: 1
testable_claim: "goal_kind: perpetual is a legal goal kind (legacy long-term accepted forever, like phasing-out), G1, g15 and g16 carry it, GOALS.md renders a Perpetual section for such goals with no complete or retired column, and snapshot-goals.py --render --check still round-trips byte-identical"
title: L3w1 goal kind perpetual
---
# hypothesis:l3w1-goal-kind-perpetual

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
WAVE 1 (brief .agi/context/l3-command-ladder-brief.md section 2.6, owner decisions 1.2): long-term goals become perpetual, broadly worded on purpose, one director each; there is no active goal count (max_goals_active already deleted in L3.04). FILES: .agi/context/schemas/[goal].md (goal_kind enum gains perpetual; long-term stays accepted as a legacy alias), extensions/agi/bin/snapshot-goals.py (render: a Perpetual section listing perpetual goals with title and one-line summary, no complete or retired column; retire stays legal), the three goal nodes G1 (config-maxxing), g15, g16 set goal_kind perpetual through write.py, tests. Do not reword any goal body; the perpetual directors reword their own goals in wave 2. VERIFY: red-first tests for the schema enum, for the render section, and for the round trip; snapshot-goals.py --render --check byte-identical on this repo; links.py schema shows no new violations; smoke count unchanged. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Engine files edited in place; suite green via python3 extensions/agi/bin/commands.py run tests. Do not commit, push, or run grid.py commit.
