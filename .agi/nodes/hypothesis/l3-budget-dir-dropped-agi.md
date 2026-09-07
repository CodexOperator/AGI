---
id: hypothesis:l3-budget-dir-dropped-agi
mint_id: 4525afaeb62a449caee7d5665c02815f
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-IV
scaffold_hash: 472fb6e5bb7c03a5
season: 2
testable_claim: After the fix, spawn_budget.py's budget dir resolves to <repo>/.agi/sessions/.spawn-budget on the main checkout and to the main checkout's same path from inside a linked worktree (git_common_root joined with the graph dir's relative path, never <repo>/sessions), the stray <repo>/sessions/ is not created, and a red-first test pins the exact path; proved by spawn_budget.py status printing dir=<repo>/.agi/sessions/.spawn-budget and the suite green.
thought_session: L3.26
title: Budget dir dropped the .agi segment after the worktree helper
---
<!-- BODY:BEGIN -->
# hypothesis:l3-budget-dir-dropped-agi

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
MEASURED (Belam IV, 2026-09-07 17:40 UTC): right after iter-L3.25 landed (experiment:a00-399c08d3-ed6286, locations.git_common_root + shared budget dir), spawn_budget.py status printed dir=/home/ubuntu/work/agi/sessions/.spawn-budget instead of /home/ubuntu/work/agi/.agi/sessions/.spawn-budget — the helper joins git_common_root(root)/sessions and drops the .agi graph-dir segment because locations.find_project_root returns the .agi dir itself (the same class as hypothesis:l3-rotate-pin-path-readback). Consequences: leases split between two dirs across the fix (L3.26 agents hold leases in the stray dir), the tree-wide bound is not tree-wide until fixed, and a stray sessions/ appears at the repo root (gitignored by Belam IV at 17:41 UTC as a guard, never commit it). FIX: compute the graph-dir path relative to the common root (graph_dir.relative_to(repo_root) in the main checkout, re-rooted on git_common_root) so the main checkout and a linked worktree share <main>/.agi/sessions/.spawn-budget; remove the stray dir after the leases in it are gone; test_budget_dir_is_shared_across_a_linked_worktree must assert the exact .agi path. Files: extensions/agi/bin/spawn_budget.py, extensions/agi/bin/locations.py (git_common_root), extensions/agi/tests/test_spawn_budget.py. Same check for the comms root and meter pins if they adopted the helper.
