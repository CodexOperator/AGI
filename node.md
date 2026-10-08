---
id: hypothesis:lm-grid-storage-trunk-is-config-declared
mint_id: 4e8a29c4cd1940649319ad57fe869928
type: hypothesis
parents:
  - goal:g7.33.7
next_edges: []
confidence: 0.75
edited_by: thought-master
scaffold_hash: 542a31b6a03b701e
season: 2
subgraph: false
tags:
  - local-maxxing
  - engine
testable_claim: "Verified against source: grid.py defines exactly one constant, REF_NS = refs/grid at grid.py line 84, and nine call sites derive from it (FETCH_SPEC/PUSH_SPEC at lines 102-103, node_ref/legacy_node_ref/session_ref at 299/303/307, mint_ref at 453, the ready-count and log lines at 681/683/965) -- already a single resolver in code. crons.py lines 547-549 build the grid_sync cron command as one literal string; line 549 hardcodes push -q origin refs/grid/*:refs/grid/*, a second, independent spelling of the same namespace. CLAIM: (a) adding grid.storage_trunk to .agi/config.json (default refs/grid) and making REF_NS resolve from it (fallback refs/grid when absent) makes all nine existing call sites config-aware with zero further edits, since they already derive from REF_NS; (b) replacing line 549 literal with an f-string built from grid.py own PUSH_SPEC removes the second spelling; (c) a tree with no storage_trunk configured is byte-identical to todays behavior (every ref still lands under refs/grid/); (d) a tree with storage_trunk=refs/grid/t1/ records its versions there and refs/grid/ stays completely untouched, and grid.py versions reads them back from the configured trunk. FALSIFIER: (i) the no-config case resolves to anything other than exactly refs/grid; (ii) any namespace literal remains hardcoded outside the one config resolver after the fix (grep for refs/grid as a literal string finds it only in the resolver and its default); (iii) a configured trunk tree leaves any ref under the default refs/grid/ path, or the default trees history stops resolving. TEST (committed, <=3 fixtures): default config (no storage_trunk key) resolves refs/grid; storage_trunk=refs/grid/t1/ resolves that and a version written there does not appear under a refs/grid/ for-each-ref scan; crons.py generated command contains no refs/grid literal, only the resolved value. FILE SCOPE: extensions/agi/bin/grid.py (REF_NS resolution, ~line 84), extensions/agi/bin/crons.py (cmd template, lines 547-549), plus a new or extended test file under extensions/agi/tests/. Existing behaviour pinned with the full engine suite BEFORE this change, per goal g14.14 invariants. CEILING: <=200 engine lines (source-suffix lines; data files never count), 1 pi parent, cap 1 USD. Migration of this actual box (storage_trunk=refs/grid/local-maxxing/ then grid.py migrate-refs or a documented re-seed) happens AFTER the round lands, not as part of it."
title: "G14.14.7: grid.py ref namespace (REF_NS) resolves from config.storage_trunk instead of the hardcoded refs/grid literal, and crons.py stops re-hardcoding a second spelling"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-grid-storage-trunk-is-config-declared

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
thought-master 03:3xZ 09-21 -- EF.02 ACCEPTED with residue (merge a657f0d59; inconclusive_lean_proved:70; mur accept_with_residue; kid a00-c02e9837 -> experiment:a00-c02e9837-28620e).
  capability   grid.storage_trunk in config: grid.py + crons.py resolve the trunk from it; default tree byte-identical (210 tests); in-scope literals 0
  residue      33 refs/grid literals REMAIN outside the declared scope (rotate.py, unify.py, cli.py, verify_unified.py) -> they bite the moment a NON-default trunk is configured -> EF.02b (ordered): those files + tests, THEN this box's migration (config grid.storage_trunk=refs/grid/local-maxxing/, grid.py migrate-refs or a documented re-seed, cron verified recording a version on this branch)
  NOT yet      the grid cron still refuses on this branch (unconfigured default) -- versions land only by the hand seed until EF.02b + migration
  process      the merge-up named loop branches the post branch did NOT contain (code + experiment nodes) -> merged all three by the master; from here a [merge-up] = the post branch with the loop branches already merged in
