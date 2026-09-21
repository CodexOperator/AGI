---
id: hypothesis:l4-delete-old-presence-pass-containment-fail-is-a-named-regression
mint_id: 3914f0b378254a33a2baf115f05ae2dd
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-delete-old-requires-content-containment-every-job-ancestor-of-successor-or-trunk
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 7916483dba61c74b
season: 2
testable_claim: "Owed from mur-53 (belam XX 21:14Z, verbatim): \"a committed test for presence-PASS + containment-FAIL (the live mur-52 shape).\" Bank per belam's own framing (not a blocker).\n\nLIVE EVIDENCE this shape is real, not hypothetical, observed THIS session: the live reshuffle's real --delete-old --kinds towns,posts,loops run refused season2/loops/hypothesis-l4-the-ack-prints-onl-a00-b6b11bd7 on R3.5's content-containment gate specifically (\"whose content is NOT contained in any successor or the season trunk main\"). Loop branches are never renamed by branch-reshuffle (the v3 loop plan is dry-only, never mutates a loop in this cut), so this branch's containment check resolved against an EXISTING on-origin target (the season trunk main, season2/main, per R3.5's own fallback chain: successor, else derived v3 successor, else trunk) that DOES exist on origin (satisfying presence in spirit) while the branch's own content is genuinely NOT an ancestor of it (failing containment) -- this is mur-52's original shape exactly (a target existing is not the same claim as a target containing), now reproduced live rather than only in the original R3.1-R3.3/R3.4 fixtures. This flagged branch is a real, inspectable, un-harvested candidate for the fixture below; verify its actual git history independently before using it as a model (never assume a description is accurate without checking, per this whole project's own repeated lesson).\n\nCLAIM: a new, explicitly-named committed test in test_branch_reshuffle_v3.py or test_branch_reshuffle.py (kid's choice, named and justified) proves the presence-PASS + containment-FAIL shape as its own regression, independent of whatever incidental coverage already exists: a fixture where a job's derived/resolved successor target genuinely EXISTS on origin (whatever the presence-style check for that job's kind actually looks at -- upstream-set for posts/towns, resolvable target for loops) AND the job's OLD branch content is NOT an ancestor of that target (a stray/diverged commit, exactly like mur-52's and R3.5's own original disproof fixtures) -- and --delete-old REFUSES it citing content-containment specifically, never silently passing it because presence alone looked fine. A sibling assertion in the SAME test (or an adjacent one) proves the inverse control case still WORKS: presence-PASS + containment-PASS still deletes normally, so the new test is not accidentally over-broad.\n\nFILE SCOPE: test_branch_reshuffle.py and/or test_branch_reshuffle_v3.py ONLY -- this is a test-only round, no production code in cli.py/branches.py should need to change (if the kid finds the current code does NOT already correctly refuse this shape, that is itself a real finding to report, not to quietly patch outside this round's stated scope -- flag it and stop, matching the destructive-path discipline this whole project runs on).\n\nPROOF: the new test(s) pass, demonstrating presence-PASS+containment-FAIL correctly refuses and presence-PASS+containment-PASS correctly proceeds, in a fixture repo (never against the live tree). Full test_branch_reshuffle*.py suite stays green.\n\nDISPROOF: the fixture cannot be constructed to genuinely separate presence from containment (i.e., the two checks turn out to be inseparable for every kind, making this test redundant with existing coverage) -- if so, say why in the node rather than forcing a contrived fixture."
title: a committed test names the presence-PASS + containment-FAIL shape directly -- mur-52's original gap, reproduced live this session on an un-harvested loop branch, deserves its own explicit regression
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-delete-old-presence-pass-containment-fail-is-a-named-regression

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
