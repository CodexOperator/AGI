---
id: verdict:dg2b4-w2d2
mint_id: 2bd05111af5a40cc8741c77aa725a8e8
type: verdict
parents:
  - experiment:dg2b4-w2d2-baseline
  - hypothesis:link-writers-emit-mint-ids
next_edges: []
confidence: 0.65
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w2d2-baseline
scaffold_hash: eae8c042eed47150
season: 2
title: "W2d .4.2: lean proved at 65 -- the 5 named writers are buildable after W2a's resolver; 5 MORE address writers exist (post_wire.py:540, cli.py x3, snapshot-goals)"
town: core
verdict: inconclusive_lean_proved:65
---
# verdict:dg2b4-w2d2

## Verdict: inconclusive_lean_proved:65 (director-general-2, council bundle 4 stage 2)
| conjunct | on the trunk (experiment:dg2b4-w2d2-baseline) | decided by |
|---|---|---|
| (1) each of the 5 writers resolves its address to a mint id before writing | FALSE today: node_writer.py:821, level3.py:1127, decompose-engine.py:385, seatsig/veto.py:402, snapshot-build-site.py:329/343/372/389 all store the address verbatim; no resolver exists yet | test_node_writer.py::test_b4_w2db_write_node_stores_the_parents_mint_id, ::test_b4_w2db_veto_default_parent_is_the_mint_id_of_goal_g15, ::test_b4_w2db_no_writer_assigns_a_bare_address_parent; test_level3.py::test_b4_w2db_build_node_parent_is_the_census_ideas_mint_id (all XFAIL now) |
| (2) lands after goal:g4.18.6.3 | ordering only; the build needs goal:g4.18.6.1's `resolve_mint` (absent at HEAD; test_links.py W2a rows) | the W2a rows turn green before these |
Lean proved for the claim as scoped: one resolve per writer fits <= 30 lines once resolve_mint exists (level3/decompose build_node are pure and need the mint passed in by their callers). Five existing tests pin address parents and must flip (test_level3.py:245/344/350/1029, test_node_writer.py:303), and the build must decide what an unresolvable parent does (fixture parents carry no mint_id).
CORRECTION: the 5 are not all the address writers. cli.py:530, cli.py:1856, cli.py:2188, post_wire.py:540 (next_edges on every wire) and snapshot-goals.py:1216 (--from-doc) also write address items, so goal:g4.18.6.4.2's invariant "no writer mints an address link after this row" and its negative grep stay FALSE after this hypothesis is built.
