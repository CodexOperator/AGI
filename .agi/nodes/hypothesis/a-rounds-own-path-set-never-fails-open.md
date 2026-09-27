---
id: hypothesis:a-rounds-own-path-set-never-fails-open
mint_id: 885ebe132f374f549e04b8e2d15e9b05
type: hypothesis
parents:
  - goal:g1.26
next_edges: []
edited_by: belam
scaffold_hash: 4f0c04007360227f
season: 2
testable_claim: an absent agent_id refuses by name; --owns is bound to dispatch-time ids; a test fails on 6c403aeb4b
title: "A round own-path set never fails open and has no unguarded kid route (assigned: director-engine)"
town: core
---
# hypothesis:a-rounds-own-path-set-never-fails-open

# hypothesis: A round own-path set never fails open and has no unguarded kid route (assigned: director-engine)

## Why this exists
**Parent `goal:g1`** (PASS residues; g15 -> g20 -> g1). A real code defect confirmed by the PASS 10 merge-up review (BASE 9e16b8ed90 -> TIP 6c403aeb4b, merged 2129f70bb).

## Measured
cli.py:2293 the --node-id seed guard fails OPEN when agent_id is absent; cli.py:2288 --owns is a third kid-supplied route into the own-path set, unguarded (the agent-id-in-basename fix cannot cover it: 689e62f96 carries 4 kid files in one parent commit) (PASS 10 c8)

## Testable claim
an absent agent_id refuses by name; --owns is bound to dispatch-time ids; a test fails on 6c403aeb4b

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
2026-09-27 04:2xZ belam: re-parented goal:g1 -> goal:g1.26 (the PASS 10 leaf), owner 04:1xZ: subgoals like directors (skill agi-goal §5); id and body unchanged.
<!-- THOUGHT:END -->
