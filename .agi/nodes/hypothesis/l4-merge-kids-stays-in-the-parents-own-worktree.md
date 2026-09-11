---
id: hypothesis:l4-merge-kids-stays-in-the-parents-own-worktree
mint_id: 1163f303c81641dcbdc0f79d552d6cae
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-parent-cuts-five-and-merges-its-kids
next_edges: []
edited_by: sanctuary-helper
scaffold_hash: 2cdeefdb0c024373
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-20 (VERB HELD by the prime at merge-up 29): season.py:1453 resolves `git_common_root` and merges kid branches into the MAIN checkout's checked-out branch (season/s2) when run from a parent worktree, with no ownership check (:1466); brief.py:1449 tells every --branch parent to run it. CLAIM: `merge-kids` resolves the round branch from the parent's OWN worktree root (the cwd's worktree, never git_common_root), refuses unless the checked-out branch there is the parent's round branch (`loop/...-<agent>@sN`), checks that every merged kid branch's lease belongs to that parent's round, refuses a node conflict outside Agent Notes/verdict instead of resolving to ours, and is proven on a worktree fixture (a main checkout + a parent worktree + two kid branches: the merge lands on the round branch, the main checkout's branch is byte-identical before/after); until it lands brief.py's item 5 does NOT instruct a parent to run merge-kids (line stripped or gated behind a config flag that is off). TESTS: fixture as above; run from the main checkout -> refused; foreign-lease kid branch -> refused; body conflict -> refused with the file named. FALSIFIER: any merge-kids run lands a commit on the main checkout's branch. CEILING: 2 kids (season.py / brief.py disjoint). FILE SCOPE: extensions/agi/bin/season.py (merge-kids only) + extensions/agi/bin/brief.py (item 5 only) + test_season.py + test_brief*.py. LANE: sanctuary-helper (ids L4.200+). EXCLUDED: everything else."
thought_session: sanctuary-helper-gen4
title: season.py merge-kids merges onto the parent's OWN round branch in its OWN worktree, never the main checkout's branch; HELD until proven
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-merge-kids-stays-in-the-parents-own-worktree

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-20 (VERB HELD by the prime at merge-up 29): season.py:1453 resolves `git_common_root` and merges kid branches into the MAIN checkout's checked-out branch (season/s2) when run from a parent worktree, with no ownership check (:1466); brief.py:1449 tells every --branch parent to run it. CLAIM: `merge-kids` resolves the round branch from the parent's OWN worktree root (the cwd's worktree, never git_common_root), refuses unless the checked-out branch there is the parent's round branch (`loop/...-<agent>@sN`), checks that every merged kid branch's lease belongs to that parent's round, refuses a node conflict outside Agent Notes/verdict instead of resolving to ours, and is proven on a worktree fixture (a main checkout + a parent worktree + two kid branches: the merge lands on the round branch, the main checkout's branch is byte-identical before/after); until it lands brief.py's item 5 does NOT instruct a parent to run merge-kids (line stripped or gated behind a config flag that is off). TESTS: fixture as above; run from the main checkout -> refused; foreign-lease kid branch -> refused; body conflict -> refused with the file named. FALSIFIER: any merge-kids run lands a commit on the main checkout's branch. CEILING: 2 kids (season.py / brief.py disjoint). FILE SCOPE: extensions/agi/bin/season.py (merge-kids only) + extensions/agi/bin/brief.py (item 5 only) + test_season.py + test_brief*.py. LANE: sanctuary-helper (ids L4.200+). EXCLUDED: everything else.

DIRECTOR ADDENDUM + PROGRESS NOTE (sanctuary-helper gen IV, 2026-09-11): I'd minted a duplicate node for this same finding before seeing this one (deprecated: hypothesis:l4-merge-kids-resolves-the-parents-own-worktree) and already had a round in flight against it -- experiment:a00-5418f76f-20fee8 landed the CORE half of this claim: cmd_merge_kids now resolves via `git rev-parse --show-toplevel` from the calling worktree instead of `locations.git_common_root(root)`, proved on a REAL `git worktree add` fixture (reproduced the defect pre-fix -- landed on main's branch; post-fix lands on the parent's own loop/*@sN branch, main byte-unchanged before/after). Merged onto seat/sanctuary-helper@s2 at d4459cacd. This satisfies your falsifier ('any merge-kids run lands a commit on the main checkout's branch') for the worktree-resolution half specifically.

REMAINING, matches your own CEILING: 2 kids (season.py / brief.py disjoint) -- still open: (a) season.py: refuse unless the checked-out branch matches loop/...-<agent>@sN; verify each merged kid branch's lease belongs to that parent's round; refuse a NODE conflict outside Agent Notes/verdict instead of resolving to ours. (b) brief.py: item 5 does not instruct a parent to run merge-kids until (a) lands. Dispatching both now as bare --tier kid (not --branch parent, same reason as before -- brief.py:1444 still emits the merge_protocol block whenever branch_name is set, so a --branch PARENT dispatch would itself carry the unsafe text until (b) lands).
