---
id: hypothesis:lm-dispatch-stale-base-measures-a-town-post-against-core-main
mint_id: 5a2fa8f379e3498a98b68008da6338fe
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
ceiling: "dispatch.py _current_town_branch only (8 code lines plus comments), two tests, no ladder edit, no other file; 0 USD. DEVIATION: hand-written by the thought-master under the owner 01:0xZ in-branch fix authority and the 01:1xZ \"urgent fix\" line, not by a kid -- one-token tuple change plus a guarded self-rule, tests red then green, reported to the SM."
edited_by: belam
falsifier: after the change a dispatch from local-maxxing/season1/posts/director-thought/main still prints integration season2/main, OR one from local-maxxing/season1/main does, OR any existing test_dispatch.py stale-base / town-branch test regresses, OR core-side behaviour changes (core/season2/main resolves to anything but None; season/s2 resolves to anything but season/s2).
link_ref: extensions/agi/bin/dispatch.py
location: source_root
scaffold_hash: 05b36d0f3d6724a2
season: 2
testable_claim: "dispatch.py _current_town_branch names only the kinds post and loop when it hands a spawner branch to branches.merge_target; the v3 town-first spellings every live seat carries (local-maxxing/season1/posts/director-thought/main = v3_post) fall through to the ladder exact-equality lookup, match no town_branches row (the ladder has none for local-maxxing) and return None, so the stale-base gate measures a thought-town director against season2/main and refuses until it merges origin/season2/main into its post branch -- which it did before every dispatch (14 such merges on refs/agi/posts/director-thought 09-18/19; owner 01:1xZ 09-19 in my pane: \"Your director is merging into prim branch I think ... Needs urgent fix ... needs updating his brief\"). My own trunk dispatch (TMM.01, 01:13Z) hit the same gate: integration season2/main, behind 6. CLAIM: naming v3_post and v3_loop in that tuple resolves the post to its own town trunk (merge_target already does: local-maxxing/season1/main), and a v3 town trunk whose town has NO ladder row integrates against itself on origin, while a town WITH a row (core: season/s2) is byte-for-byte unchanged."
tests: "red-first, both failed before the patch: test_dispatch.py::test_v3_post_branch_resolves_its_own_town_trunk (post + v3 loop spellings -> local-maxxing/season1/main) and ::test_v3_town_trunk_without_ladder_row_integrates_against_itself (trunk -> itself; core/season2/main -> None unchanged); then the 13 related tests (-k town_branch or v3 or stale_base) and the whole test_dispatch.py."
thought_session: dissolve-legacy-2026-09-19
title: Lm dispatch stale base measures a town post against core main
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-dispatch-stale-base-measures-a-town-post-against-core-main

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
RED CLOSED 05:4xZ 09-19 (Prime [red] 05:42Z, MAIN suite #6 at c132a67b4: test_branch_spelling_grep x2 deterministic): b6c121ffa's two comments hand-spelled a season branch (dispatch.py:648 'season2/main', :661 'season/s2') outside the L4.332-pinned inventory. Fixed by sanctuary-master directly on core (comment rewords only, 2 lines, no pin change, no code path touched; owner 01:0xZ full authority in-branch + the Prime's own fix line): 'core's main' and 'the row's own season branch'. test_branch_spelling_grep + test_dispatch.py 134 green. TM syncs by the standing order.
