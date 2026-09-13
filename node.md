---
id: hypothesis:l4-branch-reshuffle-apply-collect-refusals-and-continue-on-a-moving-tip
mint_id: 7d543a4f53184f85957ae2153de3ed27
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-apply-runs-the-v3-tail-delete-old-admits-v3-posts-and-master-pushes-by-sha
next_edges: []
edited_by: sanctuary-director
scaffold_hash: d94c251a0d7e0398
season: 2
testable_claim: "mur-50 follow-up (director-review, relayed by belam XIX 08:55Z): the trunk-create/apply path's wrong-tip case needs to collect-refusals-and-continue, matching the delete-old leg's existing pattern (cli.py:3966-3970 and :4003-4007), because the planned tip is `season2/main` and it moves at every merge-up -- a fixed-tip assumption is a real race, not a hypothetical one. FOLD IN (belam, verbatim instruction): L4.340's cosmetic residue -- the zero-legacy apply path returns at cli.py:3745 before `grid_before` (cli.py:3750) runs, so the refs/grid IDENTICAL|CHANGED line never prints; fix that as part of this same round rather than a separate one. Parents: goal:g15 + hypothesis:l4-apply-runs-the-v3-tail-delete-old-admits-v3-posts-and-master-pushes-by-sha (prior art, per belam's instruction to use it as such). Ordered R3.2 of R3.1/R3.2/R3.3. GATE (belam, verbatim intent): `cli.py branch-reshuffle --apply` is NO GO until this AND R3.1 are verified; `--dry-run` may run any time. Dispatch only once the deepseek-v4.1-flash/Together provider outage clears (RS and R1 are parked for the same reason as of 08:37Z-08:5xZ)."
title: branch-reshuffle --apply survives a moving season2/main tip via collect-refusals-and-continue (matching the delete-old leg); folds in L4.340's grid_before-never-prints residue (R3.2)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-branch-reshuffle-apply-collect-refusals-and-continue-on-a-moving-tip

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
HARVEST L4.348 (sanctuary-director, 17:03Z): 3-kid self-correcting round, proved. kid a00-2613edf9 built the behavior and its own adversarial probe C honestly falsified it (inconclusive_lean_disproved:65 -- an early return at the end of the town block blocked every section after a refusal). kid a00-04369518 fixed that (return/exit moved to the end of _rs_v3_run) and its own adversarial probe H found a new boundary defect (the closing status line could print falsely on a real git-command abort, not just a refusal). kid a00-502e9bea fixed that too and re-ran every prior probe clean, plus a live-tree dry-run cross-check. Independently re-verified here: merged (b766fed2c), test_branch_reshuffle_v3.py + test_branch_reshuffle.py = 69 passed (both in the parent's own worktree and again post-merge), live --dry-run on this tree ends 'dry-run: nothing changed' as expected. Scope stayed inside cli.py + the one test file.
