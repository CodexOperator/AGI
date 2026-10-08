---
id: hypothesis:l3w1-tier0-director-brief
mint_id: 2247843963354af78f0dc48122d8b9bf
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: ubuntu
scaffold_hash: a94048ed1129449c
season: 1
testable_claim: brief.py assembles a head and a director template for the tier-0 GLM director role (one per LT subgoal) and the tier-1 GLM parent role, both carrying the prayers, the Michael line, the readings by role and the decision method plus a spawn primitive, and dispatch.py --role director --ladder-tier 0 launches one through the pi harness
title: L3w1 tier0 director brief
---
# hypothesis:l3w1-tier0-director-brief

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
WAVE 1 (brief section 1.9 and 2.1, wave 3 is the live run): the expanded lower ladder is GLM parent per perpetual goal, GLM director per LT subgoal, GLM parent per ST subgoal, DeepSeek kids. Today brief.py knows kid, parent, director (claude-code) and prime_director; the ladder roles table (L3.01) has rows (0 director pi glm), (1 parent pi glm), (0 parent pi glm), (0 kid pi deepseek). FILES: extensions/agi/bin/brief.py (director template for a pi-harness director: head, the perpetual goal and its LT subgoal it owns, the spawn primitive via dispatch.py --tier parent --role parent --ladder-tier 0 --target, the review and accept/demote duties, the comms rooms it must read: tier1-directors or tier0-parents via send.py, the rotation loop rotate.py loop --role), extensions/agi/bin/dispatch.py (--role director --ladder-tier 0 resolves the row and passes the assembled brief), extensions/agi/bin/adapters/pi_adapter.py if a director needs anything a parent does not, tests. Keep the head derivation shared with the claude-code director so the Michael line, mantle rules and decision method come from one place. VERIFY: red-first tests that brief.py assemble for role director tier 0 contains the head and the spawn primitive; a dry dispatch prints the resolved pi command with ~z-ai/glm-flash-latest; one real short-lived GLM director spawned against a tiny target that only reads the brief and reports back (cost cents), evidence in the experiment. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Do not commit, push, or run grid.py commit.
