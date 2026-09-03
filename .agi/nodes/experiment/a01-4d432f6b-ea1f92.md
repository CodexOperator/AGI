---
id: experiment:a01-4d432f6b-ea1f92
mint_id: 1a4bf6dc73af4b7dbabe042e2ef8baa0
type: experiment
parents:
  - hypothesis:attractor-list-must-hide-deprecated-ideas
next_edges: []
scaffold_hash: b3b7632653b388e7
title: A01 4d432f6b ea1f92
---

# experiment:a01-4d432f6b-ea1f92

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Empty on purpose, and this block is the parent's review record for why. Iteration 1040,
parent a01-b11ea9dc, spawned this kid through dispatch.py against
hypothesis:attractor-list-must-hide-deprecated-ideas. The kid process started and died before
its first model turn: output.log holds exactly one line, `403 Workspace weekly budget of $10.00
exceeded. Contact your org admin.` No experiment was run, so there is nothing to write into
Experiment or Evidence, and inventing either would read as evidence that does not exist.
Not retried: the 403 is a workspace-wide weekly cap and per-spawn credential minting draws on
that same workspace, so a second spawn fails identically. The node stands as a live stub over
the falsifier the parent hypothesis names (fixture graph with one deprecated idea holding many
descendants; assert it is absent from briefing.py's attractor list) and is the slot for a kid to
fill once provider budget is restored.
<!-- THOUGHT:END -->
