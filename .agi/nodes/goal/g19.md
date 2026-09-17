---
id: goal:g19
mint_id: 8f65a4a17e274fe0b252e0d7401e1981
type: goal
parents:
  - vision:self-perpetuating
  - goal:g15
next_edges: []
confidence: 0.8
edited_by: belam
goal_id: G19
goal_kind: long-term
heading_level: 2
origin: goals-doc
scaffold_hash: c2f006e8256e7086
season: 2
seeds: []
status: active
tags:
  - goal
  - l5
  - tidy-pass
title: "G19: L5 the tidy pass — branch deletes, post session-name updates, then every straggling bugfix; Prime + one director"
town: core
---
<!-- BODY:BEGIN -->
# goal:g19

## Agent Notes
OWNER 2026-09-17 13:3xZ (verbatim in doc:l5-owner-decisions): "a small one. To just take care of any leftover straggling bug fixes and first and foremost the first thing it needs to do is take care of collapsing all these branches and take care of renaming the sessions properly" -- "first thing should be branch deletes, and the next thing should be post session name updates, and then everything else" -- "we're strictly just going to have you running a single director running several parents at a time" -- "your director should be named director-belam, not anything else". Plan: doc:l5-plan. Formation: Prime + ONE director (sanctuary-director -> director-belam) + <=4 parents; every other post idle; no livestream; the thought-town relocation is NOT in L5 (scope creep).

## Done-state (each claim measured on season2/main before L5 closes)
1. `git ls-remote --heads origin` == exactly the 13 names in doc:l5-plan §1 HEAD 1; the 12 named refs are gone; the 3 live post branches are on refs/agi/posts/<post> with the worktree upstreams re-pointed; no local branch merged into season2/main remains; no dead kid worktree under .agi/worktrees/a00-* remains; `verification.py` stamp fresh on the resulting tree.
2. `tmux list-windows -t agi-rc` shows director-belam and director-sanctuary (never sanctuary-director / sensei-director); `send.py whois` + `send.py send director-belam` resolve; both `.rename.json` files consumed; `rotate` applies a staged rename at the boundary under a fixture test that fails if `_apply_staged` is uncalled.
3. Every item in doc:l5-plan §1 HEAD 3's list is either landed (hypothesis with an experiment node, verdict, merge-up by SHA) or retired with a note naming the landed bytes that closed it; no residue prose.
4. COMPLETE.md carries the L5 section as a whole replacement; active node count never dropped (3187/217/3404 at open).

Numbers at open (13:3xZ 09-17): nodes 3187/217/3404 (SM.101 minted 12:09Z) · origin refs/heads 21 · local branches 678 (646 merged) · kid worktrees 109 · stamp baseline STALE (3198 active at 66ef15961; 3186 after the retire pass) · account $18.12/$25 at 06:36Z.

16:3xZ 09-17 (belam gen 28): HEAD 1 code half LANDED -- L5.01 (branch-reshuffle second-pass planner + loop-prune over 3 grammars; 3 kids) at 616d270b6, suite 5399/0/16, links 0, goals byte-identical. L5.01-live step 0 done 16:0xZ: origin refs/agi/* back-filled (posts/sanctuary-helper + 3 loops) through branches.mirror_and_prove -- full-mirror state, the planner plans exactly 12 deletes. L5.03 (verified dm auto-posts into the chat; STALE-ROW tag on a working-tree row) landed 0234ecb50 + 011ac1170 (Prime test-only fix, 4 asserts suffix-tolerant). BLOCKER for --delete-old: the never-lower stamp cannot follow a deprecation MOVE (15 L4 retirements; active 3198 -> 3197 by path manifest) -> L5.05 (node-count guard counts a move as a move) dispatched in parallel with L5.04 (auto-post never consumes what it cannot deliver). Owner 14:1xZ: idle posts quiet (17 rows), stranded-wake repair hourly (comms.wake_repair_every_s 3600, dc1ead9b1). Next: L5.04 + L5.05 land -> one suite + stamp -> L5.01-live (dry-run -> apply -> delete-old -> ls-remote == 13 -> loop-prune) -> HEAD 2.
