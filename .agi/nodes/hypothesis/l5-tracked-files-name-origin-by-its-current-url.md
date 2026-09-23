---
id: hypothesis:l5-tracked-files-name-origin-by-its-current-url
mint_id: 3a9e9cb1f9cf4cc0933cc4da5f0c4eab
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
edited_by: a00-11797ce4
scaffold_hash: f0d9ff4a3f608e83
season: 2
testable_claim: "(1) The old literal origin URL appeared in 4 tracked files / 7 lines (QUICKSTART.md:62,66; TODO.md:601,606,859; package.json:8; context/refs/legacy-prestate.md:23 -- README.md:49 is CodexOperator/agi-tree, a different repo; measured 09-23 at cb21bf01d after repointing origin -- the redirect is live, so nothing is broken, only stale). (2) The kid rewrites the literal to the current origin URL in QUICKSTART.md, TODO.md, package.json and context/refs/legacy-prestate.md (node files via write.py, never a hand edit), and leaves the rotation record untouched (history), naming it in the node. (3) grep -rn for the old literal over tracked files after the change finds only the rotation record. (4) TESTS: none beyond the grep in (3) recorded in the node; test_bin_help_smoke.py still green (nothing under bin/ changes). FILE SCOPE: QUICKSTART.md, TODO.md, package.json, context/refs/legacy-prestate.md. CEILING 6 changed lines."
thought_session: dissolve-legacy-2026-09-19
title: "SM.132 (Prime 23:46Z, low priority; g15): origin moved to CodexOperator/AGI -- the 6 tracked files still carrying the old literal URL are rewritten; a rotation record is history and stays"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-tracked-files-name-origin-by-its-current-url

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Corrected in place under C item `hyp l5-tracked-files…:11 (low)` of hypothesis:mur-0921-engine-residues-dispositioned-and-corrected (EF.23, agent a00-11797ce4). The premise file set was wrong: cl.(1) said 6 tracked files (README.md, TODO.md, package.json, 2 nodes, 1 rotation record). Re-checked against the bytes and against experiment:a00-39a8276d-9dfd67:48-54, the live-repo literal was in 4 files / 7 lines -- QUICKSTART.md:62,66; TODO.md:601,606,859; package.json:8; context/refs/legacy-prestate.md:23. README.md:49 is CodexOperator/agi-tree, a different repo. cl.(1), cl.(2) and FILE SCOPE now name the real set. cl.(3)'s residual count is covered by the sibling experiment-side C item for a00-39a8276d and was deliberately not touched. No verdict or lean field was changed.
<!-- THOUGHT:END -->
