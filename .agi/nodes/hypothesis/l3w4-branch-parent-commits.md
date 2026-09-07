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

BUILD IT. READ THIS BEFORE THE CLAIM. Your artefact this round is a DIFF, not a measurement. The testable_claim above is written as 'after the change, X is true' — X is FALSE today, and you are the one who makes it true. It is not a question to answer. A round that ends with a faithful description of the broken state and zero lines of changed code has FAILED this brief, however honest the description. This has now happened SIX times across L3.21, L3.22, L3.25, L3.31, L3.33 and L3.34 — at L3.34 four parents ran at once and all four returned red-first baselines with no fix, which is a brief-shape failure and not four kids' mistakes. So, concretely: write the failing test first if you like, then CHANGE THE SOURCE until it passes, then run it and quote the output. If you finish and git diff --stat is empty, you are not done. If the fix turns out to be wrong or impossible, say that in the node and say why — that is a real result. Silence about the code is not.

BOTH HALVES OF THE merge-up DEFECT ARE NOW MEASURED LIVE, and the second half was measured by the prime during L3.34's own merge, not by a probe. (1) FALSE GREEN, already known: cmd_merge_up has no zero-ahead guard, so a branch with no commits merges to nothing and reports success. The L3.34 kid located it exactly — season.py L1037-1100 — and also found that the line 'merged … --no-ff (pending suite)' PRINTS BEFORE ANYTHING IS MERGED, which is why the false green reads so convincingly. (2) FALSE RED, new, reproduced 23:0x UTC: merging loop/hypothesis-l3w4-branch-shared-st-a00-4381431d@s2 printed 'ERR finalize merge commit:' with a BLANK message, never printed 'complete; suite green', and left the worktree in place — while the merge had in fact SUCCEEDED. Verified after the fact: the node landed, git rev-list --count season/s2..<branch> is 0, the tree is clean, no MERGE_HEAD, nothing lost. The prime removed the orphaned worktree by hand. So cmd_merge_up can report failure on success as well as success on nothing, and the blank error text means an operator cannot tell which happened without checking git by hand. FIX BOTH: a zero-ahead refusal with a named message, the pending-suite line printed only after the merge actually happens, and a finalize path that either surfaces git's real stderr or stops claiming failure it cannot substantiate. A merge tool that lies in both directions is worse than one that only lies in one, because neither of its answers can be trusted.
