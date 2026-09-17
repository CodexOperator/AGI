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

17:0xZ 09-17 (belam gen 28) HEAD 1 REMOTE HALF DONE: origin refs/heads == the 13 target names at 17:05Z (git ls-remote --heads origin): master, season1/main, season2/main, core/{main,season2/main}, sanctuary/{main,season2/main}, streaming-suite/{main,season1/main}, web-app-suite/{main,season1/main}, local-maxxing/{main,season1/main}. Stamp 12/12 green at 8115235d9 (suite 5405/0/16, baseline 3201/217/3418; L5.05 proved live: the 15 L4 moves counted as moves). Prime acts, each measured: (1) core/main + core/season2/main fast-forwarded fbdaf9f91 -> 8115235d9 (ancestor-proven, no force; the tool refused a create over an existing tip); (2) local-maxxing pair created from season2/main (the town had no branch; the planner named a nonexistent source season2/local-maxxing/season1/main -- planner gap, HEAD 3 line); (3) sanctuary pair created by --apply; (4) post mirrors refreshed + the 3 unmerged branches archived under refs/agi/archive/* (collaborator-branch, copilot-add-open-source-license, season2-sensei-genless-templates; each 1 commit, bytes kept) then deleted by hand on the owner word -- the containment gate refuses unmerged content by design; (5) --delete-old removed 9 under lease (3 core/season2/posts/*/main, 3 season2/posts twins, 3 season2/loops); (6) sessions/verified.stamp has NO engine writer (only fixtures write it) -- written by the Prime with the measured proof, gap -> HEAD 3 line; (7) post branches re-pointed: fetch refspec +refs/agi/*:refs/agi/*, push.default upstream, branch.<post>.merge refs/agi/posts/<post> -- a plain git push from a post worktree lands on its mirror (dry-run proven), never refs/heads; (8) loop-prune --apply: local branches 678 -> 135 (543 merged loops deleted; 8 unmerged kept by name); the 109 dead kid worktrees REMAIN -- the reaper sweep refuses them (dirty / session dir not home / unmerged), HEAD 3 line. Models: parents + kids -> deepseek/deepseek-v4.1-flash (55699759b, owner 16:5xZ). NEXT: HEAD 2 (L5.02 boundary apply -> the two rotations).

21:2xZ 09-17 (belam gen 28, rotating): HEAD 2 half-DONE. The point rotated gen 34->35 at 17:28Z; L5.02 landed 16e08ffa6; its 19:08Z boundary rotation APPLIED the rename (48/54 surfaces; record sanctuary-director.20260917T190833Z: join unresolved after 613s) but never spawned -- ROOT CAUSE measured by the predecessor: _apply_staged resolves session-file surfaces MAIN-rooted while spawn_window resolves the prompt file CWD-relative, so MAIN stale card renamed + worktree brief not found -> exit 1 before any window (node minted: ...-resolves-session-files-against-the-wrong-root, HEAD 3 priority). Prime recovery 19:33-19:34Z: row renamed sanctuary-director -> director-belam (town sanctuary), stuck gen-35 session reaped by named pid (chain proven), rotate.py spawn seated director-belam @429 (Sonnet 5 max); it signs VERIFIED under the new name and runs HEAD 3 (L5.10 landed 7561fddf9). Standing gap closed: a director had NO durable role doc (the card was the whole brief) -> extensions/agi/briefs/director-belam-duties.md, pointer pinned as the card first line. Remaining HEAD 2: worktree dir + branch spelling (post-sanctuary-director, core/season2/posts/sanctuary-director/main) = HEAD 3 line; sensei-director -> director-sanctuary rotation WAITS for the root-resolution fix to land (same failure shape otherwise), then re-stage + rotate. Owner rulings this hour: cap 8 parents (b8114fe85), agent_timeout_mins 75 (74416e1de), models v4.1 flash (55699759b), quiet rows (f54c02af0), hourly wake repair (dc1ead9b1). Prime chain stays belam-S1-L4-<n> numerals (the successor name is derived from the window; the loop label lives here).

21:3xZ 09-17 (belam gen 29, seated 21:21Z wake 0): L5.07 LANDED 68a711d91 (verification.py writes verified.stamp on a no-FAIL level and retracts it on red; 6 tests; 3 experiments; GO-by-SHA 0196076a5, mur-l5-07 accept_with_residue x2). Verify on MAIN: links 0, goals byte-identical, active 3214->3219, guard silent. RULING: three g15 residues queued not dispatched -- whole-level predicate, retraction scope, and the Prime-found green-side mirror: a worktree green run writes the SHARED MAIN stamp and cli.py:5336 tests existence only, so the gate must read ran_on and refuse a stamp whose sha is not HEAD. bin-suite-fresh owed on MAIN (rotate.py, verification.py) = one Prime suite window when the wave quiets. Account read 21:24Z: 48.89 of 65 (owner top-up 25 -> 65).

21:5xZ 09-17 (belam gen 29): L5.12 LANDED 85a529480 (overdue alarm re-fires every comms.overdue_repeat_min, default 30; heal.py, 205 test lines) and L5.06 LANDED 339789e57 (reshuffle dry-run and apply agree on an existing town tip; cli.py both arms). Verify: links 0, goals byte-identical, active 3219->3226, guard silent; two g15 residues queued (dead-pid vs stale repeat stamp needs a committed test; the v2 master leg carries the same no-origin APPLY lie at cli.py:5296). RED FOUND: the Prime suite window at 8249b02c1 read 5416/2/16 -- test_workflow.py pinned the ~deepseek/deepseek-v4-flash-latest alias while 55699759b (owner 16:5xZ, both tiers to deepseek/deepseek-v4.1-flash) landed AFTER the 8115235d9 stamp, so MAIN was red from 17:08Z unseen (trap 0al: a config cell the suite pins is code -- run the suite after the edit). Prime test-only fix f6a82dcc7: both asserts read the live harnesses.pi.models.kid cell. L5.07 proved live: the red run wrote no verified.stamp. Second suite window opens on 339789e57 for the green stamp.
