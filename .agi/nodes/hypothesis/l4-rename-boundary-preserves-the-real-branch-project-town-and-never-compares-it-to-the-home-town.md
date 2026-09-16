---
id: hypothesis:l4-rename-boundary-preserves-the-real-branch-project-town-and-never-compares-it-to-the-home-town
mint_id: d6d2f0b1e2a04eb4a1ba2c7637a6bef0
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 7d783a437ccb62b0
season: 2
testable_claim: "SM.62 (SM review of SM.59 18:2xZ; OWNER ruling 18:12Z relayed by the director, to be banked verbatim in doc:l4-owner-decisions by the Prime): every perpetual agent post is SANCTUARY town by definition -- the town of agents -- separate from the PROJECT town its branch builds on (core/, web-app-suite/, ...). SM.59 conjunct 2 compared the two as ONE axis (towns.row_town vs the branch's town segment in rotate._town_post_branch) and so refuses the universal state. MEASURED on MAIN 7ae85886c: every real post branch is core/season2/posts/<post>/main (for-each-ref: sanctuary-director, sanctuary-helper, sensei-director) while the [config] town_cell overrides resolve sensei-director/sanctuary-master/master-sensei to sanctuary -- on the SM.59 bytes `rename-post sensei-director director-sanctuary` raises RenameTownRefusal 'is in town sanctuary (row cell), the real branch core/season2/posts/sensei-director/main carries town core' (exit 4), the very rename the owner ordered. CLAIM: (1) the rename boundary never compares the row town cell to the branch's project-town segment -- the REAL branch's (project town, season) tuple read from local refs is preserved verbatim into the new spelling (SM.59 kid2's _rename_post_segment, kept); (2) a post with NO real ref has NO branch surface: the `branch` and `branch (origin)` rows are emitted skipped-by-name ('no real branch for <post>: nothing to rename'), never a spelling derived from the row town; (3) the only town refusals that remain are disagreeing real branches for one post (kept) and a new-name row whose HOME town (towns.row_town) differs from the old row's (kept); (4) towns.row_town is read for (3) and nothing else on the rename path -- the derived-spelling fallback and the t_town != town refusal are DELETED, not bypassed. FALSIFIERS: a dry-run rename of a sanctuary-home post on a core branch that refuses or re-spells the town; a no-ref post whose surfaces carry a derived branch; a rename that changes the (town, season) tuple; a surviving row-town-vs-branch comparison. TESTS (<=4, the real-git fixture SM.59 left in test_rename_post.py): sanctuary-home post on a core branch -> proceeds, new branch core/season2/posts/<new>/main; no-ref post -> branch surfaces skipped by name, dry-run exit 0; two disagreeing refs -> refusal unchanged; new-name row in a different home town -> refusal unchanged. FILE SCOPE: rotate.py (_town_post_branch, _rename_surfaces, the RenameTownRefusal messages), test_rename_post.py; test_town_rows_readers.py only if an SM.59 assertion encodes the deleted comparison. CEILING: <=30 production lines NET (expected negative), ONE kid, re-brief SM past 2x. OUT OF SCOPE: the [config] town_cell overrides values, any row cell, a project-town cell -- Prime + master-sensei ([rule] to belam 18:2xZ)."
title: L4 rename boundary preserves the real branch project town and never compares it to the home town
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-rename-boundary-preserves-the-real-branch-project-town-and-never-compares-it-to-the-home-town

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.62 harvest reviewed BY NAME by sanctuary-master gen 4 18:5xZ (post branch 5aaa654fc/1969598f9, 1 kid, rotate.py net +5 of 30, tests reshaped +/-): ACCEPT :85 at the bytes -- _town_post_branch no longer takes a town, derives nothing from the row cell, prints the reason and returns None for no-ref/gitless (both branch surfaces skipped by name), keeps the disagreeing-refs refusal; the t_town != town refusal is deleted, not bypassed; the legacy town-less arm swaps the /posts/ segment only. First-hand by the director on its own row: rename-post sensei-director director-sanctuary --dry-run exits 0 (was refused under SM.59) -- the ordered rename is unblocked once this lands on MAIN. Merge-time failure outside the round's scope: test_branch_spelling_grep.py x2, cause = the DOCSTRING at rotate.py :3484 spells `season2/posts` (the only occurrence in the file); fix redirected to a docstring reword, NOT a re-pin (the pinned inventory exists to refuse hand-spelled literals). Prime's config half landed independently at 0bba784ee (overrides -> sanctuary; branch prefix the only project axis, 496f4b99e).
