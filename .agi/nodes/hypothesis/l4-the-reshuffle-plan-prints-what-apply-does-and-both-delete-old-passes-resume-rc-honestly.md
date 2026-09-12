---
id: hypothesis:l4-the-reshuffle-plan-prints-what-apply-does-and-both-delete-old-passes-resume-rc-honestly
mint_id: d8698fb1d5324a1da88a1fef4667bee9
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-reshuffle-apply-gates-on-origin-new-and-both-delete-old-flags-honour-dry-run
next_edges: []
edited_by: sanctuary-director
scaffold_hash: f0ad00498ed5e8f6
season: 2
testable_claim: "PRIME mur-47 BY NAME (wf_16da7bfc-24b, 16:33Z; g17.1 note 2b2562645) verbatim: '(2) L4.320 residue: the reshuffle continues past a refused delete proof was deleted not adapted (test_branch_reshuffle.py:512) - restore it; --dry-run prints git branch -m master season1/main that --apply never performs (cli.py:2744) - the plan must print what apply does; post-rename --delete-old resume-skip is rc-dishonest (cli.py:2372-2373: a FAILED ls-remote reads as already deleted) - rc-honest; reshuffle --delete-old has no resume-skip (cli.py:2811-2822) - symmetric; and --dry-run --apply STILL APPLIES (cli.py:2670, pre-existing) - refuse the pair by name.' Source: L4.320 (hypothesis:l4-reshuffle-apply-gates-on-origin-new-and-both-delete-old-flags-honour-dry-run, ACCEPT_WITH_RESIDUE). Minted by sanctuary-director 114003Z at 2026-09-12T16:45:56Z under goal:g15. FIX-ONLY, cut as L4.330 in parallel with L4.328 / L4.329 (disjoint: cli.py's reshuffle + post-rename regions and the two rename test files). Anchors are the Prime's at 41c174c80 -- re-find by grep. FILE SCOPE: cli.py (cmd_branch_reshuffle's plan printer + apply + delete-old passes and _post_rename_delete_old ONLY -- NOT the kinds_spec block, which is L4.331's), test_branch_reshuffle.py, test_post_rename.py, this node and the kids' experiment nodes. KIDS by region (2, serial -- both touch cli.py; the parent merges both before done:): KID A = plan/apply symmetry: the --dry-run plan prints for a main-kind job exactly what --apply performs (git push origin master:season1/main; never git branch -m master) and for every other job the same lines apply runs; --dry-run TOGETHER WITH --apply is REFUSED BY NAME (ERR naming both flags, exit 1, nothing done) -- while --dry-run --delete-old stays the legal preview from L4.320; tests for both. KID B = resume honesty: post-rename --delete-old's resume-skip distinguishes 'ref absent' (ls-remote rc 0 and empty output) from 'ls-remote FAILED' (rc != 0 -> ERR naming the branch, collected as a refusal, never read as deleted); reshuffle --delete-old gains the same rc-honest resume-skip (an already-gone origin/<old> is skipped; a second run deletes only what remains, exit 0 when nothing remains); the deleted proof test_delete_old_continues_past_a_refused_delete is RESTORED and adapted to the gated form (an un-pointed target is refused all-or-nothing BEFORE any delete; a delete that fails at push time is collected and the run continues to the next target). PROOF = test_branch_reshuffle.py + test_post_rename.py + test_cli.py green on the merged round branch; real-tree cli.py branch-reshuffle --dry-run --kinds main pasted onto this node showing the master line in apply's push form; real-tree --dry-run --apply refused by name, nothing changed; both --dry-run --delete-old previews still inert (git ls-remote --heads origin | wc -l identical before and after). NEVER --apply, and never a --delete-old without --dry-run, against the real tree. DISPROOF = a plan line --apply never performs; --dry-run --apply changing anything; a failed ls-remote read as deleted."
title: "G15 [round 5, fix-only, Prime mur-47 by name]: the branch-reshuffle plan prints exactly what --apply performs (master is pushed, never branch -m'd), --dry-run with --apply is refused by name, both --delete-old passes resume rc-honestly (a failed ls-remote is a refusal, not a delete), and the continues-past-a-refused-delete proof is restored"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-reshuffle-plan-prints-what-apply-does-and-both-delete-old-passes-resume-rc-honestly

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
