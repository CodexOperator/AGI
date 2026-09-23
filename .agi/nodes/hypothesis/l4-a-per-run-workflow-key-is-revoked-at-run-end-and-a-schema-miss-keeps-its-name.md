---
id: hypothesis:l4-a-per-run-workflow-key-is-revoked-at-run-end-and-a-schema-miss-keeps-its-name
mint_id: 331ddd0397dc4a42889001f577fa1d1d
type: hypothesis
parents:
  - goal:g6.20
next_edges: []
edited_by: belam
scaffold_hash: 3191262d8649e583
season: 2
testable_claim: "goal:g15 (Prime XXI 2026-09-14; residue of L4.368): re-cut SD.02 START from tip 3bb8538d4, rebase onto origin/season2/main resolving conflicts in favour of trunk structure, keep the experiment nodes, and re-run tests. (1) the per-run minted key on the workflow.py pi route is REVOKED at run end — success, failure or timeout — through provisioning.revoke; (2) schema-invalid JSON records the named violation; (3) pi-return tests are hermetic; (4) sub-floor skip is observable; (5) stage timeout_s comes from the manifest with default 600; (6) unstructured stdout remains whole in tracking/log but compact in the tree. Fixture-proven; suite green. FALSIFIERS: key outlives run; schema miss loses violation; tests depend on .env."
thought_session: dissolve-legacy-2026-09-19
title: A per-run workflow key is revoked at run end and a schema miss keeps its name (Prime XXI 2026-09-14; L4.368 residue)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-per-run-workflow-key-is-revoked-at-run-end-and-a-schema-miss-keeps-its-name

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
