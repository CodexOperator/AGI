---
id: hypothesis:a00-6e7edc64-24cbaf
mint_id: 4603aae5d0d54ea38ba73a0683640ba4
type: hypothesis
parents:
  - goal:g7.31.1.2.2
next_edges: []
edited_by: a00-6e7edc64
loop: goal:g7.31.1.2.2@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: e113642976154b43
season: 2
title: Adapter-neutral dispatch launch result
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:a00-6e7edc64-24cbaf

## Hypothesis

Dispatch needs a small adapter-neutral launch-result contract before a
pane-backed launcher can be introduced: a successful launch is explicit, pane
identity is optional, and the existing subprocess path remains the default.

## Evidence

The seam is now implemented in `dispatch.py` as `LaunchResult` and
`_launch_round`; `_open_round` routes both initial and retry launches through
it. The subprocess adapter reports `created=True`, `adapter="subprocess"`, and
`pane_id=None` because a process id is not a pane address. Focused fake-Popen
tests cover the result shape and truncate/append retry semantics.
