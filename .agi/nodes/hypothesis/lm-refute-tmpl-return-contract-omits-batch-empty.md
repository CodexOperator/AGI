---
id: hypothesis:lm-refute-tmpl-return-contract-omits-batch-empty
mint_id: 8212759069334c518d03603e9da81ab0
type: hypothesis
parents:
  - goal:g15
next_edges: []
ceiling: <= 1 USD OpenRouter; 0 compute; <=20 production lines; runs <=10 min
edited_by: director-thought
falsifier: REFUTE_SCHEMA required list and the RETURN CONTRACT stated key list still disagree after the edit, OR the fix changes any OTHER stage (review/verify/why/brainstorm) or the manifest research-review.json, OR no test is added proving the two lists now agree.
scaffold_hash: 1d8b8df27858c9e0
season: 2
testable_claim: "extensions/agi/workflows/agi-research-review.js REFUTE_TMPL (around line 32) instructs the model to set batch_empty, then states the top-level keys are exactly six and forbids adding others, omitting batch_empty from that list -- self-contradictory against its own REFUTE_SCHEMA (line 33) which requires seven keys including batch_empty. Fix: add batch_empty to the RETURN CONTRACT top-level-keys sentence so the instruction and the schema agree. Claim: after the fix, a fresh read of REFUTE_TMPL names exactly the 7 keys REFUTE_SCHEMA requires, and a schema-only unit test (render the template, assert batch_empty appears in the stated key list) passes."
tests: ONE pi parent + ONE kid, API-only (text edit, no compute); 0 USD compute, <=1 USD OpenRouter; runs <=10 min; FILE SCOPE extensions/agi/workflows/agi-research-review.js ONLY -- do not touch research-review.json or any other stage; add one small test asserting REFUTE_TMPLs stated top-level-key list includes batch_empty and matches REFUTE_SCHEMAs required list; land on the director post branch, push to refs/agi/posts/director-thought; mur by name.
title: agi-research-review.js REFUTE_TMPL RETURN CONTRACT omits batch_empty from its own top-level-keys list while REFUTE_SCHEMA requires it and the same template tells the model to set it -- a contract-obeying model fails the stage on the claude-code surface
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-refute-tmpl-return-contract-omits-batch-empty

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
