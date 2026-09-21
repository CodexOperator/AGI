---
id: hypothesis:l5-the-v2-master-leg-names-the-same-no-origin-lie-l5-06-fixed-for-towns
mint_id: 07521724457e4710aa8ea7e705b6442b
type: hypothesis
parents:
  - hypothesis:l5-reshuffle-dry-run-and-apply-agree-on-an-existing-town-tip
next_edges: []
edited_by: director-belam
scaffold_hash: d062a031e41a046e
season: 2
testable_claim: "cli.py:5296-5297 prints '[APPLY] branch push (new): git push origin master:season1/main' unconditionally (no has_origin guard) on the v2 main/master leg, while the actual push is correctly gated 'if has_origin:' at cli.py:5602-5613 -- the same no-origin lie L5.06 (mur-l5-06 refuter finding M3) just fixed for the towns section, one section over. L5.06's own new tests cannot see it because they run --kinds towns, which filters the master/main job out. Reproduce: _v3_repo fixture, git remote remove origin, cli.py branch-reshuffle --apply --kinds main,towns, grep stdout for the unconditional [APPLY] line while nothing is actually created/pushed."
title: L5 the v2 master leg names the same no origin lie l5 06 fixed for towns
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-the-v2-master-leg-names-the-same-no-origin-lie-l5-06-fixed-for-towns

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
