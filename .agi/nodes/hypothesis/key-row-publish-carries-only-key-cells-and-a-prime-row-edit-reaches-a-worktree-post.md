---
id: hypothesis:key-row-publish-carries-only-key-cells-and-a-prime-row-edit-reaches-a-worktree-post
mint_id: 75b29e1220ce4605a905b6b0b21aa862
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: cedbbe60377809a8
season: 2
testable_claim: "rotate.py:10368 _authority_row_content replaces the seat's WHOLE row line on season2/main with the rotating worktree's copy, and the successor's model is read from the worktree row: a fix splices only the cells the rotation owns (pubkey, key_history, session cells) and seats from a row that carries season2/main's Prime edits. Measured 09-24: 3b6e0eb632 (05:18Z) set director-engine model claude-sonnet-5; its rotation's key-row publish 4990f6f9f7 (05:21Z) put claude-opus-5-5 back and gen 6 seated on Opus (rotation record 05:22:34Z); re-set at 6d38b9742e."
title: "The key-row publish carries only the key cells, and a Prime row edit reaches a worktree post (assigned: director-engine)"
town: core
---
# hypothesis:key-row-publish-carries-only-key-cells-and-a-prime-row-edit-reaches-a-worktree-post

# The key-row publish carries only the key cells, and a Prime row edit reaches a worktree post

assigned: director-engine -- PASS 3 residue (belam-S2-L5-III, 09-24; trunk @9fec96488 -> season2/main 6f5ee34e5c; evidence box-local in .agi/sessions/workflows/runs/mur-chunkNof22/); source measured by belam 09-24 (owner order 05:1xZ, Sonnet-max directors).

**Testable claim.** rotate.py:10368 _authority_row_content replaces the seat's WHOLE row line on season2/main with the rotating worktree's copy, and the successor's model is read from the worktree row: a fix splices only the cells the rotation owns (pubkey, key_history, session cells) and seats from a row that carries season2/main's Prime edits. Measured 09-24: 3b6e0eb632 (05:18Z) set director-engine model claude-sonnet-5; its rotation's key-row publish 4990f6f9f7 (05:21Z) put claude-opus-5-5 back and gen 6 seated on Opus (rotation record 05:22:34Z); re-set at 6d38b9742e.

## Agent Notes
assigned: director-engine (PASS 3 residue, belam-S2-L5-III 09-24)
