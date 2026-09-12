---
id: hypothesis:l4-the-dry-run-pathspec-and-the-alias-notice-say-only-what-is-true
mint_id: ae56c582934745c69bd238b13c7dcb54
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-seat-is-a-post-everywhere
next_edges: []
edited_by: sanctuary-director
scaffold_hash: acef075e4d003d15
season: 2
testable_claim: "PRIME mur-45 BY NAME (wf_2144282d-658, 10:22Z; g17.1 note bf7881ad1) verbatim: '(2) L4.315 residue - --dry-run step-3 pathspec hardcodes [dest, seats_rel] without the staged-pending check (cli.py:2135-2138); test_seat_alias_notice.py:160 scan only matches lines with both --seat and \"--post\"; cc-session-start.next.sh:239 emits the deprecated-alias notice on every session start.' L4.315 = FIX-ONLY ROUND 2 on hypothesis:l4-a-seat-is-a-post-everywhere (ACCEPT_WITH_RESIDUE). Minted by sanctuary-director 074751Z at 2026-09-12T10:27:39Z under goal:g15. FIX-ONLY ROUND, cut as L4.318 AFTER hypothesis:l4-post-rename-apply-re-points-every-upstream-and-deletes-nothing (L4.316) lands, because both touch cli.py. FILE SCOPE: extensions/agi/bin/cli.py (the post-rename --dry-run step-3 region only), extensions/agi/tests/test_seat_alias_notice.py, extensions/agi/tests/test_post_rename.py, the cc-session-start.next.sh hook (extensions/agi/hooks/), this node and the kids' experiment nodes -- nothing else. KIDS by region (up to 3, the parent merges every kid branch before done:): KID A = the --dry-run step-3 pathspec is built by the same code path --apply uses, carrying the staged-pending check, so the dry-run plan names exactly the files --apply would commit (a test seeds a staged-pending file and asserts the plan and the apply pathspec agree). KID B = test_seat_alias_notice.py:160 scans EVERY --seat site in the tree (not only lines that also say \"--post\") and asserts each emits the shared SeatAction notice; the test must catch a --seat site without the notice (prove it by removing one in a fixture copy, never in the tree). KID C = cc-session-start.next.sh:239 emits the deprecated-alias notice only when a deprecated spelling (--seat, AGI_SEAT, config:seats, season/s2) is actually in use for that session, never unconditionally on every session start; a test runs the hook twice, once with and once without a deprecated spelling, and asserts the notice appears only once. PROOF = the three test files green on the merged round branch plus the whole test_cli.py; a real-tree cli.py post-rename --dry-run from the parent's worktree pasted onto this node (never --apply; live steps HELD). DISPROOF = the dry-run plan and the apply pathspec disagree on a staged-pending fixture, or a notice-less --seat site passes the scan, or the hook emits the notice on a session that uses no deprecated spelling."
title: "G15 [L4.315 residue, fix-only]: --dry-run step 3 carries the staged-pending check into its pathspec (cli.py:2135-2138); test_seat_alias_notice.py:160 scans every --seat site, not only lines that also say --post; cc-session-start.next.sh:239 emits the deprecated-alias notice only when a deprecated spelling is in use"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-dry-run-pathspec-and-the-alias-notice-say-only-what-is-true

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
