---
id: hypothesis:l4-spawn-cds-into-the-row-worktree-cell-when-set
mint_id: 399312d9cd9a4636bbbd15dd6b4e4465
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 0f132d5b1f05fed5
season: 2
testable_claim: "cmd_spawn currently launches the successor in the spawner process cwd and ignores the row worktree cell (Prime gen 21, measured 2026-09-16 06:35-06:39Z: three worktree posts came up in MAIN instead). Claim: cmd_spawn should cd into the row worktree cell when that cell is set, before launching the harness process."
title: L4 spawn cds into the row worktree cell when set
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-spawn-cds-into-the-row-worktree-cell-when-set

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
