---
id: hypothesis:l4-merge-kids-stays-in-the-parents-own-worktree
mint_id: 1163f303c81641dcbdc0f79d552d6cae
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-parent-cuts-five-and-merges-its-kids
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 2cdeefdb0c024373
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-20 (VERB HELD by the prime at merge-up 29): season.py:1453 resolves `git_common_root` and merges kid branches into the MAIN checkout's checked-out branch (season/s2) when run from a parent worktree, with no ownership check (:1466); brief.py:1449 tells every --branch parent to run it. CLAIM: `merge-kids` resolves the round branch from the parent's OWN worktree root (the cwd's worktree, never git_common_root), refuses unless the checked-out branch there is the parent's round branch (`loop/...-<agent>@sN`), checks that every merged kid branch's lease belongs to that parent's round, refuses a node conflict outside Agent Notes/verdict instead of resolving to ours, and is proven on a worktree fixture (a main checkout + a parent worktree + two kid branches: the merge lands on the round branch, the main checkout's branch is byte-identical before/after); until it lands brief.py's item 5 does NOT instruct a parent to run merge-kids (line stripped or gated behind a config flag that is off). TESTS: fixture as above; run from the main checkout -> refused; foreign-lease kid branch -> refused; body conflict -> refused with the file named. FALSIFIER: any merge-kids run lands a commit on the main checkout's branch. CEILING: 2 kids (season.py / brief.py disjoint). FILE SCOPE: extensions/agi/bin/season.py (merge-kids only) + extensions/agi/bin/brief.py (item 5 only) + test_season.py + test_brief*.py. LANE: sanctuary-helper (ids L4.200+). EXCLUDED: everything else."
thought_session: sanctuary-director-gen12
title: season.py merge-kids merges onto the parent's OWN round branch in its OWN worktree, never the main checkout's branch; HELD until proven
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-merge-kids-stays-in-the-parents-own-worktree

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-20 (VERB HELD by the prime at merge-up 29): season.py:1453 resolves `git_common_root` and merges kid branches into the MAIN checkout's checked-out branch (season/s2) when run from a parent worktree, with no ownership check (:1466); brief.py:1449 tells every --branch parent to run it. CLAIM: `merge-kids` resolves the round branch from the parent's OWN worktree root (the cwd's worktree, never git_common_root), refuses unless the checked-out branch there is the parent's round branch (`loop/...-<agent>@sN`), checks that every merged kid branch's lease belongs to that parent's round, refuses a node conflict outside Agent Notes/verdict instead of resolving to ours, and is proven on a worktree fixture (a main checkout + a parent worktree + two kid branches: the merge lands on the round branch, the main checkout's branch is byte-identical before/after); until it lands brief.py's item 5 does NOT instruct a parent to run merge-kids (line stripped or gated behind a config flag that is off). TESTS: fixture as above; run from the main checkout -> refused; foreign-lease kid branch -> refused; body conflict -> refused with the file named. FALSIFIER: any merge-kids run lands a commit on the main checkout's branch. CEILING: 2 kids (season.py / brief.py disjoint). FILE SCOPE: extensions/agi/bin/season.py (merge-kids only) + extensions/agi/bin/brief.py (item 5 only) + test_season.py + test_brief*.py. LANE: sanctuary-helper (ids L4.200+). EXCLUDED: everything else.
