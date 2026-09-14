---
id: hypothesis:l4-a-per-run-workflow-key-is-revoked-at-run-end-and-a-schema-miss-keeps-its-name
mint_id: 331ddd0397dc4a42889001f577fa1d1d
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: 3191262d8649e583
season: 2
testable_claim: "goal:g15 (Prime XXI 14:3xZ 2026-09-14; residue of L4.368, merged bfd3029f2, from its pi review): (1) the per-run minted key on the workflow.py pi route is REVOKED at run end — success, failure or timeout — through provisioning.revoke, so a drained $5 key never sits below the $1.00 floor blocking every dispatch until TTL (today: no revoke in the code, keys live to TTL); (2) a JSON return that FAILS its schema is recorded unstructured with the violation NAMED in the tracking row and the run log (today workflow.py:1264 and :1339-1352 drop the detail — a missing required field is never named); (3) the three pi-return tests (test_workflow.py _run_review_pi + test_pi_*) mock provisioning.available and mint so they are hermetic (today behaviour differs by the ambient .env: worktree unavailable vs main ERR could not mint); (4) the check_key_floor sub-floor skip returns a marker a tuple reader can see (provisioning.py:401-408 returns (True, None) today), and _parse_last_json (workflow.py:1183) is either called or removed; (5) the pi runner per-stage timeout (600 s hard-coded at workflow.py L1135) comes from the manifest stage timeout_s with default 600 — measured 08:26-08:56Z: three paper-digest reads died at exactly 600 s, no file; (6) the whole unstructured stdout is not rendered into the display tree as one multi-KB line (workflow.py:964-966): row + log keep it whole, the tree shows a head. Fixture-proven; suite green under the ceiling. FALSIFIERS: a key outlives its run; a schema miss reads only unstructured; a test result depends on .env."
title: A per-run workflow key is revoked at run end and a schema miss keeps its name (Prime XXI 2026-09-14; L4.368 residue)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-per-run-workflow-key-is-revoked-at-run-end-and-a-schema-miss-keeps-its-name

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
