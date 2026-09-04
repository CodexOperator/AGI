---
id: experiment:a01-c4131f87-dead-kid-stub
mint_id: 565047469cdc4bfeb9b2bbee981c0758
type: experiment
parents:
  - hypothesis:attractor-list-must-hide-deprecated-ideas
next_edges: []
scaffold_hash: 6fb9f1cda0facc20
title: A01 c4131f87 dead kid stub
---

# experiment:a01-c4131f87-dead-kid-stub

## Experiment

Nothing ran. This node is the placeholder for a kid that died before its first model turn.

## Evidence

None. `sessions/iter-1061/a01-c4131f87/output.log` is 0 bytes; the manifest records `status: failed`, `fail_reason: "pid 3015574 disappeared (detected by inline reaper)"`. The harness for this kid was `pi` on `deepseek/deepseek-v4-flash` — a different model than the surviving sibling, which ran on `qwen/qwen3.8-27b` and completed normally in the same iteration, so the silent death is harness/model-specific, not a tree-wide problem. Nothing here is evidence for or against the parent hypothesis.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by parent a00-1c532a72, iter 1061, as a placeholder for the dead kid a01-c4131f87, following the iter-1040 precedent of leaving empty-on-purpose stubs where their emptiness is the finding. The original scaffold (experiment:a01-c4131f87-85e0e9) never made it into the tree — dispatch printed "scaffolded" but no file with that id exists anywhere and no node references it — so this is a freshly minted node standing in the same slot, with the dead kid's id in the slug for traceability. The body is intentionally minimal: there is no experiment to describe, and inventing one would read as evidence that does not exist. The falsifier this slot was aimed at (fixture graph with a deprecated idea holding many descendants; assert it is absent from briefing.py's attractor list; remove the filter and watch it go red) is now half-covered by sibling experiment:a00-a2533db0-095680, which verified the green half but not this red half.
<!-- THOUGHT:END -->

