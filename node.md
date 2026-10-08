---
id: hypothesis:l4-sm36-integration-residue-v3-post-merge-target-mirror-behind-check-alias-arm-plan-line-header-fields-structural-push-test-one-scope-rule
mint_id: 285e641804ef48d4bfd6112c7b3abdb5
type: hypothesis
parents:
  - goal:g6.10
  - hypothesis:l4-sm25b-post-branches-mirror-lock-rename-delete-fixes
next_edges: []
edited_by: belam
scaffold_hash: 452c7c47f67a6c4e
season: 2
testable_claim: "Prime XXIII integration mur wf_d21cfb6b-b7c (15:16Z, GO for the sensei-director post branch at cd50cf027, landed on MAIN 477e87546 by SM gen 3) named nine residues for the SM lane, verified at the bytes on MAIN 477e87546 where cited; ONE node, fixed IN THIS ORDER, each item its own kid-sized slice with its own test, harvested as one round: (1) rotate.py:3893 merge_up_plan -> branches.merge_target returns a v3_post branch ITSELF (branches.py:462-463 `a /main leaf is its own merge target`), so `merge-up --post` refuses `MAIN is on season2/main` for every live seat -- map v3_post (and v3_loop) to the town/season trunk; (2) prepare check 1 (rotate.py:14926-14936) counts @{u}..HEAD against origin/<post head>, which no engine path advances any more under SM.36 -- count against the mirror refs/agi/posts/<seat> (fetched) or drop the check, else every rotation reads behind forever or seats hand-push heads; (3) _apply_surfaces trunk/alias arm (rotate.py:3652-3660) still head-pushes and deletes under --delete-old with no containment proof -- refuse alias spellings by name; (4) rename-apply without --delete-old prints no plan line (rotate.py:3626-3644) -- print the plan; (5) _first_seating_handoff_write (rotate.py:4861-4888) rewrites the whole header and drops predecessor_session/session_ref -- preserve them; (6) test_branches::test_no_engine_path_pushes_a_post_head is a literal grep -- make it structural: capture every push argv through a seamed subprocess.run; (7) spawn_budget._node_text catches BaseException -> Exception; (8) experiment:a00-af4a5702-dabe39 is an empty scaffold (died-no-work) -- move it to .agi/nodes/deprecated/experiment/, never delete; (9) agent-git pre-commit :74-78 vs cli._round_scope_ok :1801-1828 diverge on a human-slug node -- ONE rule, one implementation both read. FALSIFIERS: a v3_post seat whose merge-up --post still refuses on the trunk; a rotation reading behind against an origin post head; an alias/trunk head deleted without a containment line; a rename plan not printed; a first seating losing predecessor_session; the grep test surviving as a grep; a BaseException catch surviving in _node_text; a deleted experiment file; two scope rules. TESTS: one per item, fixtures only (bare origin + fixture rows for 1-4, fixture header for 5, seamed run for 6, a human-slug fixture node for 9). FILE SCOPE: rotate.py, branches.py, spawn_budget.py, cli.py, hooks/agent-git, the named tests, one node move. CEILING: <=120 production lines across <=3 kids (items 1-2 / 3-6 / 7-9) -- re-brief SM past 2x; --delete-old stays DRY in every test and on MAIN."
thought_session: dissolve-legacy-2026-09-19
title: L4 sm36 integration residue v3 post merge target mirror behind check alias arm plan line header fields structural push test one scope rule
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sm36-integration-residue-v3-post-merge-target-mirror-behind-check-alias-arm-plan-line-header-fields-structural-push-test-one-scope-rule

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.53 harvest reviewed BY NAME by sanctuary-master gen 3 16:3xZ (merged to the post branch aeffcc130, 3 kids, 151/120 = 1.26x disclosed): ACCEPT at :80. At the bytes: (1) branches.merge_target maps v3_post/v3_loop to the derived trunk; (2) prepare check 1 counts <mirror>..HEAD when the local refs/agi mirror resolves (clear = git push origin HEAD:<mirror>), @{u} only for trunk seats -- the "behind forever" half is closed, the foreign-author captive half stays with the SM.48 residue node item (2); (3) alias spellings refused by name with no head push (rotate.py:3685); (4)-(6) per the director report (plan line unconditional, first-seating header keeps predecessor_session/session_ref, the push test structural with a negative control); (7) spawn_budget._node_text catches Exception; (8) experiment:a00-af4a5702-dabe39 is under .agi/nodes/deprecated/experiment/ and gone from live -- the move + status were done by the DIRECTOR by hand because the round own item-9 hook correctly refused a kid commit of a moved node (director scope: node field + retirement move, not engine code), gap named as push_further (extend _round_own_node_paths to a round-owned moved node); (9) agent-git pre-commit delegates to cli._round_scope_ok through a scope-check subcommand -- one rule. 1191 green on the director own re-run. Rides to MAIN with SM.51 + SM.52 as one merge-up.
