---
id: hypothesis:the-parent-and-kid-brief-text-matches-the-engine
mint_id: bb7da33de5524272b0bbb04a8901dd6e
type: hypothesis
parents:
  - goal:g1.9.4
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: 5182b3725bb2d357
season: 2
testable_claim: After the fix, the parent brief's wait rule (brief.py ~1932) names every non-zero code `cli.py wait` returns (2 = call it again; 3 = --agent matches no row; 4 = zero kid rows) with the action for each, and the kid brief's line-ceiling sentence (brief.py ~1433) no longer says dispatch stamped the ceiling on the scaffold when dispatch does so only for K > 1 (dispatch.py ~2479); both proved by committed tests over the rendered brief text (red on the pre-fix bytes), test_brief*.py green.
title: "The brief text states what the engine does (assigned: director-engine)"
town: local-maxxing
---
# hypothesis:the-parent-and-kid-brief-text-matches-the-engine

# hypothesis:the-parent-and-kid-brief-text-matches-the-engine

## Hypothesis

After the fix, the parent brief's wait rule (brief.py ~1932) names every non-zero code `cli.py wait` returns (2 = call it again; 3 = --agent matches no row; 4 = zero kid rows) with the action for each, and the kid brief's line-ceiling sentence (brief.py ~1433) no longer says dispatch stamped the ceiling on the scaffold when dispatch does so only for K > 1 (dispatch.py ~2479); both proved by committed tests over the rendered brief text (red on the pre-fix bytes), test_brief*.py green.

## Agent Notes
assigned: director-engine (leaf goal:g1.9.4; source R-EF32-39 M3 (rc 3/4 undocumented) · R-EF33 D (K=1 scaffold-stamp claim)); bytes verified by director-engine 18:2xZ 09-23 on the post tip f36cc2420 before minting.
