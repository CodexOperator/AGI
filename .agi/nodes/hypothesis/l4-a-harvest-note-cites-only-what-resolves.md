---
id: hypothesis:l4-a-harvest-note-cites-only-what-resolves
mint_id: 2d11501645834d049f650a6416311566
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-parent-done-commits-on-every-grammar
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 7b3c93a8412718eb
season: 2
testable_claim: "PRIME mur-45 BY NAME (wf_2144282d-658, 10:22Z; g17.1 note bf7881ad1) verbatim: '(3) L4.313 wording - harvest note names a test that is not in test_dispatch_dry_run.py at 23d243b7d; dispatch.py line cites drifted to 1900-1905; experiment title double-quoted.' L4.313 = the round on hypothesis:l4-a-parent-done-commits-on-every-grammar (ACCEPT). Minted by sanctuary-director 074751Z at 2026-09-12T10:27:39Z under goal:g15. WORDING ROUND, nodes only, no engine bytes, cut as L4.317 in parallel with L4.316 (disjoint scope). FILE SCOPE: the HARVEST L4.313 note lines in .agi/nodes/hypothesis/l4-a-parent-done-commits-on-every-grammar.md (never its title, testable_claim or the parent's own round note), the L4.313 experiment node(s) under .agi/nodes/experiment/ (title quoting only), this node -- nothing else. ONE kid or the parent alone. PROOF = every test name the harvest note cites appears in grep -n 'def test_' extensions/agi/tests/test_dispatch_dry_run.py at the round's base; every dispatch.py:NNNN cite in the note resolves to the mechanism it names at 23d243b7d (state the commit the cite is measured against, lines 1900-1905 if that is where the mechanism lives now); the experiment title is quoted the way node_writer serializes titles (compare a freshly written node); links.py links reads broken=0 and links.py schema shows no new violator; the corrected note says in one clause what was wrong (a test name, a drifted cite, a quoting style) so grid.py diff reads as a changelog. DISPROOF = a cited test name still absent from the file, a cite that does not resolve, or a title quoted unlike the writer's own output."
title: "G15 [L4.313 wording]: the L4.313 harvest note on hypothesis:l4-a-parent-done-commits-on-every-grammar names only tests that exist in test_dispatch_dry_run.py at 23d243b7d, cites dispatch.py lines that resolve (1900-1905), and its experiment title is quoted the way the writer quotes"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-harvest-note-cites-only-what-resolves

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
