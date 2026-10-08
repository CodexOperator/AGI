---
id: hypothesis:the-agent-named-clis-join-the-choice-surface
mint_id: dba782e3f9f14c62b09503810de4bca8
type: hypothesis
parents:
  - goal:g1.25.3
next_edges: []
confidence: 0.8
edited_by: director-engine
scaffold_hash: 8599f6527813bc45
season: 2
testable_claim: "After the round, command:commands covers 19 more engine CLIs -- brief, level3, season, heal, zoom, locations, commands, stitch, sensei, paths, post_wire, node_writer, metrics, unify, hierarchy, handoff, evidence_gate, benchmark, anonymize: every verb declared (typed args, placement data, side_effects, proposable) or excluded by name with a reason, destructive / live-seat / owner-ops verbs never proposable; the coverage and drift tests include them and stay green; propose still imports and executes nothing; the manifest stays deterministic with no absolute path or box value."
title: "the agent-named CLIs join the choice surface: 19 more engine CLIs declared or excluded by name (assigned: director-engine)"
town: local-maxxing
---
# hypothesis:the-agent-named-clis-join-the-choice-surface

# hypothesis:the-agent-named-clis-join-the-choice-surface

## Hypothesis

```
set        brief.py level3.py season.py heal.py zoom.py locations.py commands.py stitch.py sensei.py paths.py post_wire.py node_writer.py
           metrics.py unify.py hierarchy.py handoff.py evidence_gate.py benchmark.py anonymize.py
proves     the coverage test's CLI list grows by these 19 and stays green: every verb declared with typed args + placement data + side_effects
           + proposable, or excluded by name with a reason (destructive / live-seat / owner-ops verbs never proposable); the drift test covers
           them; propose still imports and executes nothing; the manifest stays deterministic with no absolute path or box value
```

## Agent Notes
assigned: director-engine (goal:g1.25, the owner's cli-maxxing; survey batch 2 of 3); measured before minting.
