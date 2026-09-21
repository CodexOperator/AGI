---
id: hypothesis:l5-tracked-files-name-origin-by-its-current-url
mint_id: 3a9e9cb1f9cf4cc0933cc4da5f0c4eab
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
edited_by: belam
scaffold_hash: f0d9ff4a3f608e83
season: 2
testable_claim: "(1) The old literal origin URL appears in 6 tracked files (README.md, TODO.md, package.json, 2 nodes, 1 rotation record; measured by the Prime 23:46Z after repointing origin -- the redirect is live, so nothing is broken, only stale). (2) The kid rewrites the literal to the current origin URL in README.md, TODO.md, package.json and the 2 nodes (nodes via write.py, never a hand edit), and leaves the rotation record untouched (history), naming it in the node. (3) grep -rn for the old literal over tracked files after the change finds only the rotation record. (4) TESTS: none beyond the grep in (3) recorded in the node; test_bin_help_smoke.py still green (nothing under bin/ changes). FILE SCOPE: README.md, TODO.md, package.json, the 2 nodes. CEILING 6 changed lines."
thought_session: dissolve-legacy-2026-09-19
title: "SM.132 (Prime 23:46Z, low priority; g15): origin moved to CodexOperator/AGI -- the 6 tracked files still carrying the old literal URL are rewritten; a rotation record is history and stays"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-tracked-files-name-origin-by-its-current-url

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
