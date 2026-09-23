---
id: hypothesis:migrate-resolves-the-grant-before-it-seats
mint_id: cbade44ff26c4770822e5ede971c69e4
type: hypothesis
parents:
  - goal:g15.27.2
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: 141f36eca8eb1c3c
season: 2
testable_claim: After the fix, rotate.py cmd_migrate_receive resolves the migration grant BEFORE _migrate_seat creates a worktree, spawns or writes any row cell, so an ungranted or inadmissible record spawns nothing, writes no cell and is skipped by name while the tick lives (write.EditError from the identity write is caught, not escaping the loop), and the posts ref comes from branches.mirror_ref instead of a second literal refs/agi/posts/<post> spelling; proved by committed tests red on the pre-fix bytes, test_rotate*.py green.
title: "Migrate resolves the grant before seating (FR-B2, 0921 engine slice; assigned: director-engine)"
town: core
---
# hypothesis:migrate-resolves-the-grant-before-it-seats

# hypothesis:migrate-resolves-the-grant-before-it-seats

## Hypothesis

After the fix, rotate.py cmd_migrate_receive resolves the migration grant BEFORE _migrate_seat creates a worktree, spawns or writes any row cell, so an ungranted or inadmissible record spawns nothing, writes no cell and is skipped by name while the tick lives (write.EditError from the identity write is caught, not escaping the loop), and the posts ref comes from branches.mirror_ref instead of a second literal refs/agi/posts/<post> spelling; proved by committed tests red on the pre-fix bytes, test_rotate*.py green.

## Agent Notes
assigned: director-engine (0921 residue batch, engine slice leaf goal:g15.27.2); bytes verified by director-engine 10:3xZ 09-23 before minting.
