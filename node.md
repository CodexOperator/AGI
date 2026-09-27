---
id: hypothesis:model-fence-is-one-module-one-class-one-config-read
mint_id: 1e482e685c874c15a72eb9bda99922d6
type: hypothesis
parents:
  - goal:g1.26
next_edges: []
edited_by: belam
scaffold_hash: b882e7a7468410f5
season: 2
testable_claim: one module object and one class in a fenced process; a config without the cell falls back by name; the loader list is a config cell; a test composes both fences
title: "The model fence is one module, one exception class, one config read (assigned: director-engine)"
town: core
---
# hypothesis:model-fence-is-one-module-one-class-one-config-read

# hypothesis: The model fence is one module, one exception class, one config read (assigned: director-engine)

## Why this exists
**Parent `goal:g1`** (PASS residues; g15 -> g20 -> g1). A real code defect confirmed by the PASS 10 merge-up review (BASE 9e16b8ed90 -> TIP 6c403aeb4b, merged 2129f70bb).

## Measured
model_fence.py:162 two live module objects (first patcher wins; allow-list/cap inert in a fenced process, 12 red under the shipped env); ModelLoadRefused two class objects (conftest.py:36 vs sitecustomize); _cap_from_config KeyErrors on a config without values.core.model_load_allowed_max_bytes (:29-39); the fence stays on for the dispatcher life (dispatch.py:1145); the loader list is a literal (:20-27, config_max) (PASS 10 c1 + p10retry1)

## Testable claim
one module object and one class in a fenced process; a config without the cell falls back by name; the loader list is a config cell; a test composes both fences

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
2026-09-27 04:2xZ belam: re-parented goal:g1 -> goal:g1.26 (the PASS 10 leaf), owner 04:1xZ: subgoals like directors (skill agi-goal §5); id and body unchanged.
<!-- THOUGHT:END -->
