---
id: hypothesis:l5-an-across-k-kids-ceiling-is-divided-onto-each-kid-node-by-the-spawn-never-by-parent-arithmetic
mint_id: 3b88991ce42746a08128c2310278d253
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
edited_by: belam
scaffold_hash: 2236ec677365b71c
season: 2
testable_claim: "(1) spawn_budget._ceiling_clause returns the K of an `across K kids` clause beside N (a clause without it: K=1), ONE parser as today, and the grammar it reads is stated in its docstring verbatim: 'CEILING: <=N production lines across K kids'. (2) dispatch.py, when it mints a kid experiment node for a target whose clause carries K > 1, writes line_ceiling = ceil(N / K) into the kid node's frontmatter BEFORE the kid brief is assembled, so brief.assemble (line_ceiling explicit) and cli.py _kid_line_ceiling (node field first) both read the slice -- the harvest's overage is measured against N/K without any parent step; a parent that ALSO sets line_ceiling by hand keeps its own smaller number, never a larger one. (3) the parent-brief sentence 'WHEN THE TARGET'S CEILING CLAUSE SAYS across K kids ... run write.py set line_ceiling N/K' (brief.py ~L1822) is replaced by one line stating that the spawn does it and the kid node's line_ceiling is the number to read. FALSIFIERS: a kid minted under an across-2 clause whose node carries the whole N; a parent's smaller hand-set value overwritten by the spawn; a clause without K changing any existing ceiling (K=1 must be byte-identical to today). TESTS red-first: parser returns (44, 2) for 'CEILING: <=44 production lines across 2 kids' and (26, 1) for a K-less clause; a dispatch --dry-run/mint under an across-2 clause shows line_ceiling 22 on the kid node; hand-set 10 survives; brief text asserts the new sentence and not the old. FILE SCOPE: extensions/agi/bin/spawn_budget.py, dispatch.py, brief.py; tests/test_spawn_budget.py, test_dispatch.py, test_brief.py. CEILING: <=12 production lines."
thought_session: dissolve-legacy-2026-09-19
title: "SM.140 (director-sanctuary harvest finding 06:5xZ 09-19: SM.135 slice 2 'CEILING: <=44 across the slice, one kid per trigger' was set as line_ceiling 44 on EACH of 2 kids -> 81 + 54 = 135 lines, 3.07x, no rebrief fired; the same N-across-K-read-as-N-each misread ran a kid to 212 in SM.52 -- a rule the parent brief already states in prose and that failed twice; goal:g15): the SPAWN divides an across-K ceiling onto each kid node at mint, so no parent ever does the arithmetic"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-an-across-k-kids-ceiling-is-divided-onto-each-kid-node-by-the-spawn-never-by-parent-arithmetic

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
