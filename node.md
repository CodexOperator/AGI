---
id: hypothesis:a-path-shaped-bin-resolves-in-the-spawns-cwd
mint_id: 2e0438c0a7ab49118881856d04ba904f
type: hypothesis
parents:
  - goal:g1.26
next_edges: []
edited_by: belam
scaffold_hash: a689b82fb32c9e9f
season: 2
testable_claim: a relative bin valid in the spawn cwd resolves; an invalid one refuses by name; the build node is versioned with the payload
title: "A path-shaped bin is judged in the spawn cwd, not the resolver cwd (assigned: director-engine)"
town: core
---
# hypothesis:a-path-shaped-bin-resolves-in-the-spawns-cwd

# hypothesis: A path-shaped bin is judged in the spawn cwd, not the resolver cwd (assigned: director-engine)

## Why this exists
**Parent `goal:g1`** (PASS residues; g15 -> g20 -> g1). A real code defect confirmed by the PASS 10 merge-up review (BASE 9e16b8ed90 -> TIP 6c403aeb4b, merged 2129f70bb).

## Measured
adapters/__init__.py:117 judges a path-shaped bin with os.path.exists in the RESOLVER process cwd while Popen runs in another cwd -> over-refusal of a valid relative bin, untested; build:bin-adapters-init not re-versioned with its payload (PASS 10 c5)

## Testable claim
a relative bin valid in the spawn cwd resolves; an invalid one refuses by name; the build node is versioned with the payload

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
2026-09-27 04:2xZ belam: re-parented goal:g1 -> goal:g1.26 (the PASS 10 leaf), owner 04:1xZ: subgoals like directors (skill agi-goal §5); id and body unchanged.
<!-- THOUGHT:END -->
