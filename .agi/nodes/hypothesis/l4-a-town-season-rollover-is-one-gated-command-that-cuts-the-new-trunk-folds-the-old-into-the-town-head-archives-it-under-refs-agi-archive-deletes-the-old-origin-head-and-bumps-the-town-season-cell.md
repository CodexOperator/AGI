---
id: hypothesis:l4-a-town-season-rollover-is-one-gated-command-that-cuts-the-new-trunk-folds-the-old-into-the-town-head-archives-it-under-refs-agi-archive-deletes-the-old-origin-head-and-bumps-the-town-season-cell
mint_id: be9ad53cd63c45abbb0f0484dbf49f75
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 9c7d281e8105dd00
season: 2
testable_claim: "season.py rollover --town <town> (dry by default; --apply performs; --delete-old gates the origin delete) performs, in order and each step verified before the next: (1) cut <town>/season<m+1>/main from the old trunk tip; (2) fold <town>/season<m>/main into <town>/main by merge --no-ff (the town ladder head, add-only, as master holds season 1); (3) mirror the old trunk to refs/agi/archive/<town>/season<m>/main on origin and verify the ref sha == the old tip; (4) delete <town>/season<m>/main on origin only under --delete-old and only after (3) verified (the L5.01 content-containment gate, cli.py ~3292-3309, reused not re-written); (5) bump the town node season cell m -> m+1 with a season_history entry {season m closed, m+1 opened} so branches.py derive_names re-derives the trunk and post branches; (6) ls-remote --heads count before == after (+0: one head cut, one deleted). Dry run prints every step with its shas and performs nothing; a failed step stops and names itself, leaving no half state (the new trunk is cut last-to-first-safe: archive before delete, delete before bump). Falsifier: any step performs under dry; the delete runs before the archive ref verifies; the fold is a fast-forward or rewrites the town head; heads count drifts; the season cell bumps while the old head still exists on origin; the global season changes."
title: "SM.104 (owner 09-18 02:1xZ via the Prime, doc:l5-owner-decisions 9d09faa75): a town season rollover is ONE gated command -- cut the new trunk, fold the old trunk into the town head, archive it under refs/agi/archive, delete the old origin head, bump the town season cell, heads count +0"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-town-season-rollover-is-one-gated-command-that-cuts-the-new-trunk-folds-the-old-into-the-town-head-archives-it-under-refs-agi-archive-deletes-the-old-origin-head-and-bumps-the-town-season-cell

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.104 BRIEF (sanctuary-master, 09-18 02:3xZ; owner 02:1xZ verbatim via the Prime: a season rollover must DELETE the old season head from GitHub and FOLD it in through our standard storage mechanism; measured by the Prime: nothing does that today -- branches.py derives names only, old trunks stay frozen heads, the store is refs/agi/archive/<old-name> as L5.01 --delete-old wrote it). TEMPLATE-FIRST: extend the existing verb season.py rollover (today: the GLOBAL N+1 rollover, --dry-run) with --town <town>; reuse the --delete-old B2 content-containment gate in cli.py (~3292-3309) and the archive-ref writer L5.01 used (kid finds it by the refs/agi/archive string, never re-writes it); the town season cell write goes through write.py (town node season + season_history) never a hand edit; branches.py derive_names is the only name source. Steps + order + falsifiers: see testable_claim. CEILING 40 production lines (six steps ~6 each incl. the stop-and-name paths); overage disclosed. TESTS (one file, test_season_rollover_town.py, on a throwaway bare origin under /tmp): (1) dry run performs nothing (refs and node unchanged) and prints six steps with shas; (2) --apply without --delete-old: new trunk cut, fold merged --no-ff into <town>/main, archive ref == old tip, old head STILL on origin, season cell NOT bumped (bump gated on the delete) -- or bumped if the Prime rules the cell may lead; state which; (3) --apply --delete-old: old head gone, archive verified, cell bumped m -> m+1 with a history entry, heads count +0; (4) archive verify failure (ref mismatch injected) -> stops before the delete, names step 3; (5) global season unchanged throughout; (6) idempotent re-run refuses by name (trunk exists). FILE SCOPE: season.py, the shared gate/archive helpers only by import, one test file; towns.py only if the loader must read the bumped cell. FIRST LIVE RUN: core 2 -> 3 (mine, after this lands; hold the town:core edit until then). Delivery: batch + your mur review in one [merge-up] line; reds fixed in-loop.
