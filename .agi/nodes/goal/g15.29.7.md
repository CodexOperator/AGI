---
id: goal:g15.29.7
mint_id: 7be0483a516b47d4a0682dc859359b43
type: goal
parents:
  - goal:g15.29
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G15.29.7
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: efdeab16e1a009fe
season: 2
seeds:
  - hypothesis:the-pending-key-swap-completes-only-after-the-authority-publish
status: active
tags:
  - core
  - engine
  - residue-batch
  - leaf
title: "G15.29.7: HELD: THE PENDING KEY SWAP COMPLETES ONLY AFTER THE AUTHORITY PUBLISH (09-23 mur residue leaf; assigned director-engine)"
town: core
---
# goal:g15.29.7

# goal:g15.29.7 — HELD: THE PENDING KEY SWAP COMPLETES ONLY AFTER THE AUTHORITY PUBLISH

```
source    R-EF51 M1 (C3 gate bypass via _complete_pending_key_swap) · R-EF20 M1 (push: HELD counted as not-failed) M2 (no frozen-path test)
          bytes verified by director-engine 18:2xZ 09-23 on the post tip f36cc2420 before minting
rule      KEEP SPLITTING (owner 09-23 10:4xZ, goal:g5): one leaf, one small round; split again if it grows
round     hypothesis:the-pending-key-swap-completes-only-after-the-authority-publish (dispatch after the named rounds land)
writer    director-engine
```
