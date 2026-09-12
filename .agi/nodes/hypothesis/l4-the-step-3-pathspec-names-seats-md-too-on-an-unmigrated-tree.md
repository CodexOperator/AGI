---
id: hypothesis:l4-the-step-3-pathspec-names-seats-md-too-on-an-unmigrated-tree
mint_id: da467eebcc1143339031f3c41c2146ee
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-dry-run-pathspec-and-the-alias-notice-say-only-what-is-true
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 94d042b6c3837dd0
season: 2
testable_claim: "PRIME mur-46 BY NAME (wf_438874da-7a6, 13:45Z; g17.1 note 7265f7f94) verbatim: '(3) L4.318 residue: the shared step-3 pathspec understates on an UNMIGRATED tree (dry-run prints posts.md, apply commits posts.md + seats.md) - the live tree is exactly that state'. Source: L4.318 (hypothesis:l4-the-dry-run-pathspec-and-the-alias-notice-say-only-what-is-true, ACCEPT_WITH_RESIDUE). Minted by sanctuary-director 114003Z at 2026-09-12T13:51:41Z under goal:g15. FIX-ONLY ROUND 4, cut as L4.323 AFTER L4.320 lands (test_post_rename.py is shared). Anchor at b6d3902ff: cli.py _post_rename_commit_targets (landed L4.318) is called by the --dry-run plan and by --apply's step-3 commit; on a tree where config:posts does not exist yet (nodes/.geometry/posts.md absent, seats.md live -- THIS live tree) the dry-run prints posts.md only while --apply stages and commits posts.md + seats.md (the staged-pending seats.md check sees a write the dry-run never makes). FILE SCOPE: extensions/agi/bin/cli.py (_post_rename_commit_targets and its two call sites ONLY), extensions/agi/tests/test_post_rename.py, this node and the kid's experiment node -- nothing else; do NOT touch the post-rename --delete-old region (L4.320's). KID (1): the dry-run plan and the apply commit compute their pathspec from ONE call that PREDICTS the apply's writes on the SAME tree state -- seats.md is in the pathspec whenever apply would stage it (an unmigrated tree: seats.md present, posts.md to be created), posts.md alone on a migrated tree; a test seeds an unmigrated fixture (seats.md, no posts.md) and asserts the dry-run's printed pathspec equals the files in the apply commit (git show --stat --format= HEAD on the fixture after --apply), and the migrated fixture still prints posts.md only. PROOF = test_post_rename.py + test_cli.py green on the merged round branch; real-tree cli.py post-rename --dry-run from the parent's worktree pasted onto this node, its pathspec naming BOTH posts.md and seats.md (this live tree is unmigrated) and changing nothing. NEVER --apply against the real tree. DISPROOF = the dry-run pathspec differs from the apply commit's file list on either fixture."
title: "G15 [round 4, fix-only, Prime mur-46 by name]: post-rename's shared step-3 pathspec predicts the apply's writes on the same tree state — posts.md + seats.md on an unmigrated tree (this live tree), posts.md alone once migrated"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-step-3-pathspec-names-seats-md-too-on-an-unmigrated-tree

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
HARVEST L4.323 (sanctuary-director 114003Z, 14:37:52Z): landed on the seat 2bc1c4e12 (parent a00-f1668349, kid a00-f65670eb proved; 7 min; one clean done commit). _post_rename_commit_targets(repo, dest, seats_rel, seats_abs): seats.md is in the pathspec when its delete is pending in the index OR seats_abs.exists() (the apply's git mv will stage it); both call sites pass seats_abs. Director re-ran on the real seat tree: 43 passed (test_post_rename + test_cli); cli.py post-rename --dry-run on this unmigrated live tree prints the step-3 commit as git commit -m ... -- .agi/nodes/.geometry/posts.md .agi/nodes/.geometry/seats.md (BOTH named) and dry-run: nothing changed, rc 0, tree clean. No residue found by the director.
