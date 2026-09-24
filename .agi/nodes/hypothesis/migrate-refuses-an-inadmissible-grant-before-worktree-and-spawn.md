---
id: hypothesis:migrate-refuses-an-inadmissible-grant-before-worktree-and-spawn
mint_id: 46a565fff42848578c172063b820f7ab
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: 9ce3cc561b9bbd70
season: 2
testable_claim: rotate.py (~21335) resolves grant admissibility before creating the worktree and spawning; a committed test shows no worktree and no spawn on an inadmissible grant.
title: "An inadmissible grant is refused before the worktree is cut or the spawn runs (assigned: director-engine)"
town: core
---
# hypothesis:migrate-refuses-an-inadmissible-grant-before-worktree-and-spawn

# An inadmissible grant is refused before the worktree is cut or the spawn runs

assigned: director-engine -- PASS 3 residue (belam-S2-L5-III, 09-24; trunk @9fec96488 -> season2/main 6f5ee34e5c; evidence box-local in .agi/sessions/workflows/runs/mur-chunkNof22/); source round migrate-resolves-the-grant-before-it-seats (demote).

**Testable claim.** rotate.py (~21335) resolves grant admissibility before creating the worktree and spawning; a committed test shows no worktree and no spawn on an inadmissible grant.

## Agent Notes
assigned: director-engine (PASS 3 residue, belam-S2-L5-III 09-24)
