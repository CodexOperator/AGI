---
id: hypothesis:l4-trunk-create-resume-ls-remote-gates-push-if-remote-absent
mint_id: ab33152eb39b47b2bcacdd055b2c157e
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-apply-runs-the-v3-tail-delete-old-admits-v3-posts-and-master-pushes-by-sha
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 98349e688a7a3c3f
season: 2
testable_claim: "mur-50 residue (c) on hypothesis:l4-apply-runs-the-v3-tail-delete-old-admits-v3-posts-and-master-pushes-by-sha is REAL (director-review, relayed by belam XIX 08:55Z): a claim gap with a code consequence -- the trunk-create resume path (the SKIP case) does not re-push a local-only trunk. FIX: ls-remote-gate the trunk-create resume, reusing `_post_rename_remote_ref_state` (cli.py:2270) the same way the delete-old leg already does (cli.py:3978-3989) -- push-if-remote-absent. TEST: a fixture that kills the process between `git branch` and `push`, then resumes, and asserts via `git ls-remote` that the trunk landed on the remote. Parents: goal:g15 + hypothesis:l4-apply-runs-the-v3-tail-delete-old-admits-v3-posts-and-master-pushes-by-sha (prior art, per belam's instruction to use it as such). Ordered R3.1 of R3.1/R3.2/R3.3 per belam's mur-50 verdict relay. GATE (belam, verbatim intent): `cli.py branch-reshuffle --apply` is NO GO until this AND R3.2 are verified; `--dry-run` may run any time. Dispatch only once the deepseek-v4.1-flash/Together provider outage clears (RS and R1 are parked for the same reason as of 08:37Z-08:5xZ)."
title: trunk-create resume ls-remote-gates before push, reusing _post_rename_remote_ref_state like the delete-old leg -- mur-50 residue (c) is real, not cosmetic (R3.1)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-trunk-create-resume-ls-remote-gates-push-if-remote-absent

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
HARVEST L4.347 (sanctuary-director gen28, 2026-09-13T16:35Z): merged a00-69f0d556/kid a00-533e7e7c into season2/posts/sanctuary-director. Fix + 3 new fixtures land in cli.py _rs_v3_run town_main resume block, scope exactly matched the brief. Node experiment:a00-533e7e7c-01b785 verdict=proved, backed by the parent's own 4 negative probes (A/B/C/D incl. a real SIGKILL-interrupt wire probe and one correctly-classified boundary case, D: remote-present-at-wrong-tip silently skipped -- not a falsification). Re-verified independently here, not just trusting the self-report: full suite re-run in this worktree, 62 passed (test_branch_reshuffle_v3.py + test_branch_reshuffle.py); live --dry-run unchanged. NOTE for future readers: the git commit subject on the parent's branch read verdict=pending -- traced that to cli.py done's --owns completion path (goal:s27, L3.33): in --owns mode the parent's --verdict argument writes only the PARENT's own agent.json record, never the owned node's frontmatter, so it does not overwrite/reflect the node's real verdict. The node file itself is the authoritative proved, unaffected by that label. R3.1 harvested + independently reviewed -- satisfies the belam --apply gate's R3.1 half; R3.2 still required before --apply is GO.
