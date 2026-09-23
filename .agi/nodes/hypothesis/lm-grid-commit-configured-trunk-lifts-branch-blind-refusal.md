---
id: hypothesis:lm-grid-commit-configured-trunk-lifts-branch-blind-refusal
mint_id: fb3689931ac1439f96a572e9e3245f29
type: hypothesis
parents:
  - goal:g7.33.7
next_edges: []
confidence: 0.8
edited_by: thought-master
scaffold_hash: 92157eabbd10a68e
season: 2
subgraph: false
tags:
  - local-maxxing
  - engine
testable_claim: "Found LIVE, not theoretical: the 06:55Z grid_sync cron tick still refused with node refs are branch-blind ... pass --allow-branch even though grid.storage_trunk=refs/grid/local-maxxing is now configured on the trunk (EF.08 cutover, confirmed done). Verified against source: cmd_commit (grid.py line 883) guards at lines 918-938 with exactly if not session and not allow_branch: -- resolve the checked-out branch, refuse with sys.exit(2) unless it is a legal season branch. The condition checks ONLY session and allow_branch; it has no awareness of ref_ns_for(root) or whether a non-default trunk is configured. CLAIM: the guard becomes if not session and not allow_branch and ref_ns_for(root) == DEFAULT_REF_NS: -- a configured NON-DEFAULT storage_trunk lifts the branch-blind refusal (the refs already live in a project-specific, non-shared-default namespace, which is the concern the guard exists to police against); --allow-branch remains the explicit override for an unconfigured (DEFAULT_REF_NS) tree, unchanged; an unconfigured tree on a non-season branch still refuses exactly as today. FALSIFIER: (a) a configured non-default trunk on a non-season branch still refuses without --allow-branch (the fix did not fire); (b) an UNCONFIGURED tree (default refs/grid) on a non-season branch stops refusing without --allow-branch (a real regression -- the guard is now too permissive); (c) --allow-branch stops working as an override on an unconfigured tree; (d) a session commit (D3 drafts, already ungated) changes behavior. TEST (committed, <=3 fixtures): a scratch repo with storage_trunk configured, on a non-season branch, commit --all with no --allow-branch succeeds; the same scratch repo unconfigured (default trunk) on the same branch still refuses with exit 2 naming --allow-branch; --allow-branch still overrides the unconfigured-refusing case. Live proof after merge: the next real grid_sync cron tick on this actual branch (local-maxxing/season2/posts/director-engine/main or wherever the cron runs) commits without --allow-branch in its own crontab line, checked via the cron log thought-master already reads. FILE SCOPE: extensions/agi/bin/grid.py (cmd_commit guard, lines ~918-938), extensions/agi/tests/test_grid.py. CEILING: <=200 engine lines (source-suffix lines; data files never count) -- thought-master called this tiny and the fix is a one-line condition change, so this should land far under. Cap 1 USD pi parent."
title: "G14.14.7 follow-up (EF.09, thought-master TME.15, found live at the 06:55Z cron tick): grid.py commit lifts the branch-blind refusal when a non-default storage_trunk is configured"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-grid-commit-configured-trunk-lifts-branch-blind-refusal

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
thought-master 07:3xZ 09-21 -- EF.09 ACCEPTED (merge 2da449a74; proved; kid a00-7f5cd566 -> experiment:a00-7f5cd566-2736c0; 223 tests by the director; engine suite on the merged trunk 5867 passed / 0 failed). LIVE PROOF (the thing every grid round since 01:5xZ was for): the first grid_sync cron tick after the merge logged 'grid: 71 new version(s), 1 error (missing mint_id), 286 with payload, 18 payloads unresolved, 0 demoted' on local-maxxing/season2/main with NO --allow-branch; refs/grid/local-maxxing/node 3773 -> 3812; doc:lm-town-trajectory at v2, goal:g14 at v2. The owner's rule (a trajectory change = a node version, recorded by the crons) is cron-backed from this tick.
