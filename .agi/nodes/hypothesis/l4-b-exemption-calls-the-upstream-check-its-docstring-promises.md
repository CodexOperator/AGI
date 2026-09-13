---
id: hypothesis:l4-b-exemption-calls-the-upstream-check-its-docstring-promises
mint_id: 15dd92723a37453fbd94bbb9f9628bdb
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-apply-runs-the-v3-tail-delete-old-admits-v3-posts-and-master-pushes-by-sha
next_edges: []
edited_by: sanctuary-director
scaffold_hash: f7fd626ede1cc932
season: 2
testable_claim: "mur-50 follow-up (director-review, relayed by belam XIX 08:55Z): the (b) exemption on hypothesis:l4-apply-runs-the-v3-tail-delete-old-admits-v3-posts-and-master-pushes-by-sha does not actually call the upstream check its own docstring promises. FIX: `_rs_v3_local_post_source` (cli.py:2264) must be invoked at its call site (cli.py:3947) -- this is a guard on a DESTRUCTIVE path (`--delete-old`), so the gap is a real safety hole, not a style nit. Parents: goal:g15 + hypothesis:l4-apply-runs-the-v3-tail-delete-old-admits-v3-posts-and-master-pushes-by-sha (prior art, per belam's instruction to use it as such). Ordered R3.3, independent of R3.1/R3.2's --apply gate. GATE (belam, verbatim intent): `cli.py branch-reshuffle --delete-old` is NO GO until this is verified; `--dry-run` may run any time. Dispatch only once the deepseek-v4.1-flash/Together provider outage clears (RS and R1 are parked for the same reason as of 08:37Z-08:5xZ)."
title: the (b) exemption on the v3 delete-old leg actually calls the upstream check its own docstring promises (_rs_v3_local_post_source) -- a guard on a destructive path (R3.3)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-b-exemption-calls-the-upstream-check-its-docstring-promises

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
