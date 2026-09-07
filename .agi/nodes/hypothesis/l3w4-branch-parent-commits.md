---
id: hypothesis:l3w4-branch-parent-commits
mint_id: f1abeda9d181419a81b02e8baa542566
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-VIII
scaffold_hash: 2936d260caafe85b
season: 2
testable_claim: After the change, a parent that accepts its kid's node while resident in a worktree leaves its loop/<slug>@sN branch at one or more commits with a clean working tree, and season.py merge-up exits non-zero with a named message when handed a branch that is zero commits ahead of its recorded base_branch instead of reporting success. Both are proven by red-first tests that fail before the change and pass after.
title: The parent owns the commit inside its worktree
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-branch-parent-commits

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
WHY THIS EXISTS AS ITS OWN BRIEF. It is gap (1) of hypothesis:l3w4-parent-branch-merge-up, split out by Belam VIII after that brief returned probe-only for the FOURTH time at L3.33. The parent brief had grown to three independent gaps and a kid does one thing well; trap 0g says a brief whose claim states a defect gets proved by confirmation and fixed by nobody, so the claim above is written as the FIX's proof condition and this is a BUILD, not a probe. THE DEFECT, measured twice. A kid is contractually forbidden to commit and nothing else commits inside a worktree, so a loop branch reaches season.py merge-up at zero commits with a dirty working tree and merge-up REPORTS SUCCESS ON AN EMPTY BRANCH. At L3.32 two worktrees stood empty; at L3.33 all four did, and the prime hand-committed every one to complete the round. THE FIX. Give the commit to the PARENT at the moment it accepts its kid's node — it already owns acceptance, and the prime cannot scale to one commit per worktree at four to six parents. Add the second half too: merge-up must refuse a zero-commit branch loudly rather than report a green merge of nothing, because a false green here is indistinguishable from success and that is how L3.30's isolation failure hid. UNTIL THIS LANDS every --branch round needs a human at the end, which is the one thing blocking the owner's item 32 ask of seats that run their own loops.
