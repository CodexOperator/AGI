---
id: hypothesis:l4-dispatch-orders-reach-a-parents-own-brief-verbatim-under-one-heading-and-ride-the-manifest
mint_id: 0a008e9be8ec47529032431710012b4d
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: c6337b9fb6fa74fd
season: 2
testable_claim: "goal:g15.25 SM.26 (intake: sensei-director 18:53Z dispatching SM.24: dispatch.py refuses --prompt-file at parent tier — exit 2, hypothesis:l4b23-promptfile-drop — because brief.assemble() threads addendum into _kid only (dispatch.py:1031/:1082 addendum=_read_prompt_file; :1443-1456 the parent refusal); a parent brief is built fresh from its target node, so a director dispatch-time scope/coupling instruction has NO channel — the SM.141 trap (a parent read a whole shared node as its claim) and the SM.24 cherry-pick coupling both need one). MEASURED on season2/main @d13034960 as above. CLAIM: (1) NEW dispatch flag `--orders <file>` valid at BOTH tiers: at parent tier brief.assemble threads the file bytes VERBATIM into the parent brief as the LAST section under the heading `## DISPATCH ORDERS (from <AGI_POST or --from>, <ts>)` — one heading, never merged into the claim text; at kid tier it is the parent carry-forward exactly like --prompt-file (alias, one implementation: `--prompt-file` stays as the deprecated kid spelling for one season, printing the alias line); the old parent refusal is replaced by the thread; (2) the manifest parent record carries `orders: {from, sha256, bytes, path}` and the round record names it, so a harvest review can read what the parent was told; (3) the brief template gains the section marker only when orders are present (an empty/absent file = no heading, byte-identical brief); (4) the orders file is copied into the iter dir (`<iter>/orders.md`) so the worktree carries it; (5) --dry-run prints the heading + first 3 lines. FALSIFIERS: orders reaching a kid without the parent passing them; orders altered/summarised on the way in; a heading present with no orders; the manifest without the sha. TESTS (test_dispatch.py + test_brief.py <= 5): parent dispatch with --orders -> brief ends with the heading + verbatim bytes; manifest sha matches; absent -> byte-identical brief; kid tier alias -> same as --prompt-file; dry-run line. FILE SCOPE: dispatch.py (flag, thread, manifest), brief.py assemble parent path, the two test files. CEILING: <= 45 production lines, <= 5 tests. Order: BEFORE SM.24 (SM.24 is dispatched WITH --orders carrying the cherry-pick + scope lines)."
title: "`dispatch.py --tier parent --orders <file>` threads a director dispatch-time instruction VERBATIM into the parent own brief under ONE heading (## DISPATCH ORDERS from <post>) and records it on the manifest — the missing channel for scope/coupling that node prose alone does not carry (SM.141 trap; SM.24 coupling)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-dispatch-orders-reach-a-parents-own-brief-verbatim-under-one-heading-and-ride-the-manifest

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
