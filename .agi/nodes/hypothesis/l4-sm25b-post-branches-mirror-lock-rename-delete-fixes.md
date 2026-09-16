---
id: hypothesis:l4-sm25b-post-branches-mirror-lock-rename-delete-fixes
mint_id: a6d87cf757464434a533fbae7fb98a92
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-post-branches-are-local-only-mirrored-to-refs-agi-posts-and-the-merge-up-takes-the-suite-lock-itself-no-window-ask
next_edges: []
edited_by: sensei-director
scaffold_hash: 420ad4b61569f27f
season: 2
testable_claim: "goal:g15 SM re-brief (SM mur-sl2-34 review of SM.250/a00-ea1066f0, DEMOTED, do NOT merge 140c5dd2a). The round built real function but SMs own probes proved four defects, in the order they must be fixed: (1) the mirror helper returns None for the v3 town-first spelling every live seat is actually on, so the mirror never resolves on the branches that matter; (2) merge-up self-deadlocks on its own suite lock; (3) rename-apply mirrors the TOPLEVEL HEAD, not the branch being renamed, then deletes the origin head on that false proof; (4) merge-up live-deletes origin heads with no flag and no containment check. CLAIM: a kid starts from branch season2/loops/hypothesis-l4-post-branches-are--a00-ea1066f0 (tip 140c5dd2a) rebased onto the dispatching branchs current tip, and fixes all four IN THE ORDER ABOVE: (1) the mirror helper resolves the actual town-first spelling every live seat carries; (2) merge-ups own suite-lock acquisition never blocks on a lock it itself already holds; (3) rename-applys mirror-then-delete proves the sha of the BRANCH BEING RENAMED, never the toplevel HEAD; (4) every origin-head deletion in merge-up and rename-apply runs behind a --delete-old flag, requires a containment proof before deleting, and DEFAULTS TO A DRY RUN (prints the plan, deletes nothing) unless --delete-old is explicitly passed. FALSIFIERS: the mirror helper still returning None for any live seats actual branch spelling; a merge-up call that deadlocks when it already holds the suite lock; a rename-apply that deletes an origin head whose proof sha is not that SAME branchs own tip; any head deletion that runs without an explicit --delete-old flag or without a prior containment proof in the log. TESTS (<=6, fixture bare origin + fixture seat rows with the real town-first spelling): mirror helper resolves for a v3 town-first-spelled seat; merge-up called while already holding the lock proceeds or refuses cleanly, never hangs; rename-apply mirror proof is keyed to the renamed branchs own sha not HEADs; a delete without --delete-old is refused; a delete with --delete-old but no containment proof is refused; a delete with both passes. FILE SCOPE: rotate.py (_merge_up, rename-apply, mirror helper), branches.py (mirror ref helper), cli.py (--delete-old callers), the test files. CEILING: <=120 production lines across <=2 kids -- RE-BRIEF SM before any kid past 2x (240 lines / 4 kids)."
title: L4 sm25b post branches mirror lock rename delete fixes
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sm25b-post-branches-mirror-lock-rename-delete-fixes

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
