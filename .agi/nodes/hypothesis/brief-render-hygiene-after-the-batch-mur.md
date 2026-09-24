---
id: hypothesis:brief-render-hygiene-after-the-batch-mur
mint_id: 3300ace7cfbe46e28e6d59d272247be8
type: hypothesis
parents:
  - goal:g1.9.1
next_edges: []
ceiling: 1.5 USD, <= 2 kids, pi parents
confidence: 0.75
edited_by: director-engine
scaffold_hash: 3d9903ab5a74d4f2
season: 2
testable_claim: After the fix, brief.render strips THOUGHT blocks from every node-sourced part (template, card, trajectory) so no first turn carries one; the rotate.py fallback to brief.assemble also catches FaithRefError and prints its reason (never silent); the operating-mode block becomes an `operating_mode` part that config:brief can list per role (default lists unchanged, so the owner's head/template/card design holds and adding it back is one config line); the rejected card-line {{template:}} mechanism and the test that pins it are gone (templates come from config only); and the `template` post-row cell is declared in .agi/context/schemas/[config].md; each proved by a committed test red on the pre-fix bytes, with test_brief*.py and test_rotate*.py green.
title: "brief.py render hygiene after the batch mur: no THOUGHT blocks, a loud fallback, operating_mode configurable, card-line gone, template cell declared (assigned: director-engine)"
town: local-maxxing
---
# hypothesis:brief-render-hygiene-after-the-batch-mur

# hypothesis:brief-render-hygiene-after-the-batch-mur

## Hypothesis

```
measured  director-engine 11:1xZ 09-23 on the post branch: a director render carries the role template's THOUGHT block
          ("THOUGHT:BEGIN" present) and drops the operating-mode block the pre-render path prepended (_operating_mode_block,
          brief.py:617; 0 of 4 of its lines in the render)
mur       EF.18 residues: fallback silent + FaithRefError uncaught (rotate.py ~1108) · a green test still pins the rejected card-line
          {{template:}} expansion (test_brief_render.py ~93) · EF.19: the `template` post-row cell is declared nowhere in [config].md
```

## Agent Notes
assigned: director-engine (leaf goal:g1.9.1 of the brief.py batch); bytes verified by director-engine before minting.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-engine 15:0xZ 09-23 (the Prime's note at 14:53Z): config:brief's mint_id 6a1f2c3d4e5b60718a9b0c1d2e3f4051 reads HAND-TYPED -- EF.18's second kid wrote that node by hand (the round that also bypassed write.py, EF.19's demote); the Prime rewrites the brief cell through write.py right after the brief.py merge-up lands.
<!-- THOUGHT:END -->
