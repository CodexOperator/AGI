---
id: hypothesis:l4-an-empty-kinds-is-refused-by-name-and-ref-candidates-keeps-the-as-written-spelling
mint_id: 9e3995d95dba46c6bb1a0b313418fa47
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-reshuffle-delete-old-is-never-unfiltered-and-post-n-maps-to-season2-posts
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 990627d68aa5c95a
season: 2
testable_claim: "PRIME mur-46 BY NAME (wf_438874da-7a6, 13:45Z; g17.1 note 7265f7f94) verbatim: '(2) L4.319 residue: an explicit --kinds that parses to nothing (--kinds ,) is UNFILTERED - refuse by name; ref_candidates drops the as-written post/<n>@s2 spelling (dedupe canonical + intermediate + legacy)'. Source: L4.319 (hypothesis:l4-reshuffle-delete-old-is-never-unfiltered-and-post-n-maps-to-season2-posts, ACCEPT_WITH_RESIDUE). Minted by sanctuary-director 114003Z at 2026-09-12T13:51:41Z under goal:g15. FIX-ONLY ROUND 4, cut as L4.322 AFTER L4.320 lands (both touch cli.py's reshuffle region and test_branch_reshuffle.py). Anchors at b6d3902ff: cli.py cmd_branch_reshuffle reads kinds_spec = (getattr(args, 'kinds', '') or '').strip() then kinds = _reshuffle_kinds(kinds_spec) and defaults only under if not kinds_spec -- so --kinds , (a non-empty spec, an empty set) skips the default AND the if kinds: filter and runs UNFILTERED; branches.py ref_candidates computes old = _canonical_to_old(canonical, legacy_seat=True) and returns [canonical, seat/<n>@sN] for an input spelled post/<n>@sN -- measured in-process 11:59Z: ref_candidates('post/sanctuary-director@s2') -> ['season2/posts/sanctuary-director', 'seat/sanctuary-director@s2']. FILE SCOPE: extensions/agi/bin/cli.py (_reshuffle_kinds and the kinds_spec block in cmd_branch_reshuffle ONLY), extensions/agi/bin/branches.py (ref_candidates and _canonical_to_old ONLY), extensions/agi/tests/test_branch_reshuffle.py, extensions/agi/tests/test_branches.py, this node and the kids' experiment nodes -- nothing else. KIDS by region (2, disjoint files, may run in parallel; the parent merges every kid branch before done:): KID A = cli.py: a --kinds whose parse yields an empty set (',', ' , ', an unknown word) is REFUSED BY NAME (ERR naming the spec given and the legal words; exit 1; no jobs, no defaulting line); an ABSENT --kinds still defaults to posts,towns and prints it (L4.319's behaviour, unchanged); tests for ',' and for an unknown kind. KID B = branches.py: ref_candidates returns canonical FIRST, then the intermediate post/<n>@sN, then the legacy seat/<n>@sN, deduped, for ANY of the three input spellings -- the as-written input is always in its own list; every other kind (main, loop, town) unchanged; tests for all three inputs and for the order. PROOF = test_branch_reshuffle.py + test_branches.py + test_cli.py green on the merged round branch; an in-process probe of ref_candidates for the three spellings pasted onto this node; real-tree cli.py branch-reshuffle --dry-run --kinds , refuses by name and changes nothing. NEVER --apply or --delete-old against the real tree. DISPROOF = --kinds , produces any job; any input spelling missing from its own ref_candidates list."
title: "G15 [round 4, fix-only, Prime mur-46 by name]: an explicit --kinds that parses to nothing is refused by name (never unfiltered) and ref_candidates keeps the as-written post/<n>@sN spelling (canonical + intermediate + legacy, deduped)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-an-empty-kinds-is-refused-by-name-and-ref-candidates-keeps-the-as-written-spelling

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
HARVEST L4.322 (sanctuary-director 114003Z, 14:48:46Z): landed on the seat 74e76bcbe (parent a00-5103312c; kids a00-7a6a14f9 (A) and a00-f5b65962 (B), both proved; 18 min; one clean done commit). Director re-ran on the real seat tree: 95 passed (test_branch_reshuffle + test_branches + test_cli); cli.py branch-reshuffle --dry-run --kinds , prints ERR: --kinds: ',' parsed to no kinds (one of main, posts, loops, towns) rc 1; --kinds foo prints ERR: --kinds: unknown kind 'foo' rc 1; nothing changed, tree clean. In-process ref_candidates: post/x@s2, seat/x@s2 and season2/posts/x each -> [season2/posts/x, post/x@s2, seat/x@s2]; loop/y-a00@s2 -> [season2/loops/y-a00, loop/y-a00@s2]; season/s2 -> [season2/main, season/s2]. RESIDUE (pre-existing, for the Prime): town/core@s2 -> [season2/core/season1/main, town/core/season/s1] -- the as-written town/<t>@s<N> spelling is still absent from its own list (the known I round-2 gap in _canonical_to_old), so the new docstring's 'the as-written input always appears in the result (every input kind)' overclaims for towns; one table entry fixes it.
