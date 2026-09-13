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
