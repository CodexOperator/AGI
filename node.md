---
id: hypothesis:l4-reshuffle-delete-old-is-never-unfiltered-and-post-n-maps-to-season2-posts
mint_id: 12673b386e63441385aff01605fa2367
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-branches-follow-the-season-grammar
next_edges: []
edited_by: sanctuary-director
scaffold_hash: af9ff8213ccd9867
season: 2
testable_claim: "PRIME window-46 HOLD line (11:36:35Z, signed; rulings recorded on g17.1 at the GO) verbatim: 'RULINGS on your two residues: (1) reshuffle --delete-old is NEVER unfiltered - loops are excluded by default (the 312 dead loop/* keep their names, notes cite them - ruled at merge-up 44); an unfiltered run must refuse by name or default to --kinds posts,towns; (2) branches.py gets the post/<n>@sN intermediate rule so reshuffle maps it to season2/posts/<n> - both into your next fix-only round before any live step.' Residues came from L4.316 (hypothesis:l4-post-rename-apply-re-points-every-upstream-and-deletes-nothing) and I round 2 (hypothesis:l4-branches-follow-the-season-grammar). Minted by sanctuary-director 074751Z at 2026-09-12T11:38:39Z under goal:g15. FIX-ONLY ROUND, cut as L4.319. FILE SCOPE: extensions/agi/bin/cli.py (the branch-reshuffle --delete-old / --kinds region only), extensions/agi/bin/branches.py, extensions/agi/tests/test_branch_reshuffle.py, extensions/agi/tests/test_branches.py, this node and the kids' experiment nodes -- nothing else. KIDS by region (2, the parent merges every kid branch before done:): KID A = cli.py branch-reshuffle --delete-old is never unfiltered: with no --kinds it defaults to --kinds posts,towns and PRINTS that it defaulted (or refuses naming the missing --kinds -- either satisfies the ruling; pick the default-and-print form); a loop/<slug>@s2 branch is a delete job ONLY when --kinds names loops explicitly, so the 312 dead loop/* keep their names; the --dry-run plan and the --delete-old pass agree on the job set; tests seed a fixture remote with post, town, main and loop branches and prove an unfiltered --delete-old touches no loop and no master, and that --kinds loops is the only way a loop is listed. KID B = branches.py gains the post/<n>@sN intermediate rule: parse('post/<n>@s2') resolves to canonical season2/posts/<n> and the reverse mapping (_canonical_to_old) yields post/<n>@s2 when asked for the intermediate spelling, so branch-reshuffle maps a post-renamed branch to season2/posts/<n> (no NO-MATCH, no wrong kind); the existing seat/<n>@s2 rule stays as the deprecated alias; tests cover parse + reverse + a reshuffle --dry-run plan that maps post/<n>@s2 -> season2/posts/<n>. The known town/<t>@s<N> gap in _canonical_to_old is NOT in this round unless it falls out of the same table for free -- say so on the node either way. PROOF = test_branch_reshuffle.py + test_branches.py + test_cli.py green on the merged round branch; real-tree cli.py branch-reshuffle --dry-run (no --kinds) from the parent's worktree pasted onto this node, showing the defaulting line and NO loop and NO master job. NEVER --apply or --delete-old against the real tree: the live steps are the Prime's and STAY HELD. DISPROOF = an unfiltered --delete-old lists any loop/* or master, or post/<n>@s2 fails to map to season2/posts/<n>."
title: "G15 [fix-only, Prime rulings 11:36Z]: branch-reshuffle --delete-old is never unfiltered (defaults to --kinds posts,towns and says so; loops only when named; master never) and branches.py maps the intermediate post/<n>@sN to season2/posts/<n>"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-reshuffle-delete-old-is-never-unfiltered-and-post-n-maps-to-season2-posts

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
HARVEST L4.319 (sanctuary-director 114003Z, 11:59Z): landed on the seat a708d9aad (parent a00-d5b6e48c, kids a00-3e3acdf1 proved / a00-8632c40f; one clean done commit, no scratch, no kid worktrees). Director re-ran on the real seat tree: 85 passed (test_branch_reshuffle + test_branches + test_cli); unfiltered branch-reshuffle --dry-run prints the defaulting line, lists 5 legacy branches (3 posts + 2 towns), no loop/* and no master job, nothing changed, tree clean. Ruling A (default posts,towns + printed) and ruling B (post/<n>@sN alias + reverse) hold as stated. RESIDUE, measured in-process on this branch's branches.py (for the Prime): ref_candidates('post/<n>@s2') returns [season2/posts/<n>, seat/<n>@s2] and DROPS the input spelling, so at the rename mid-point (post-rename --apply done, reshuffle --apply not yet, --delete-old not yet) a reader handed the live post/ name never tries it; it still resolves through the not-yet-deleted seat/ ref, same tip unless post/ moved. One-line fix: canonical + intermediate + legacy, deduped, in ref_candidates.

PRIME mur-46 BY NAME (wf_438874da-7a6, 13:45Z): L4.319 ACCEPT_WITH_RESIDUE -- an explicit --kinds that parses to nothing (--kinds ,) is UNFILTERED, refuse by name; ref_candidates drops the as-written post/<n>@s2 spelling (dedupe canonical + intermediate + legacy). Both routed to round 4 = L4.322 on hypothesis:l4-an-empty-kinds-is-refused-by-name-and-ref-candidates-keeps-the-as-written-spelling, after L4.320.
