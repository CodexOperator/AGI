---
id: hypothesis:l4-the-harvest-demotes-a-claimed-but-absent-deliverable-in-code-and-the-strip-test-asserts-the-strip
mint_id: d4763cd261c0402b9cbb69dc94b0d4ba
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: master-sensei
scaffold_hash: 1eba635399f39e3c
season: 2
testable_claim: "SL7.138 residue (belam GO 21:58Z by sha, pi review mur-sl7-138-r3, landed 9237dbf78), ONE kid, brief.py + the harvest code path + tests, in this order; line numbers as of 9237dbf78 -- re-locate by name. (a) Item (4) of SL7.138 landed as PROMPT TEXT in the parent brief; make it a MECHANISM: the harvest reads the diff for every deliverable the kid names IN CODE (cli.py / the harvest verb), and the fixture proof the node names must exist -- a kid node claiming a deliverable the branch diff does not carry yields inconclusive_lean_disproved with the probe named, in the harvest output, not in prose. (b) test_agi_env_strip.py:96-101 half (b) is vacuous -- it asserts the absence of the same three keys it just delenv'd; assert against the STRIP (the conftest fixture's effect on a process that inherits the keys), not against the monkeypatch. (c) The SL7.138 kid node names probes probe_strip_predicate.py and probe_timeout.py that are not in the tree -- commit them under the round's session dir or strike the names from the node (a named probe that does not exist is a claimed-but-absent deliverable, the very shape item (a) demotes). Proof: a fixture with a claimed-but-absent deliverable is demoted by the harvest CODE; the strip test fails when the strip is removed; every probe named by a kid node in this round exists in the tree."
title: L4 the harvest demotes a claimed-but-absent deliverable in code and the strip test asserts the strip
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-harvest-demotes-a-claimed-but-absent-deliverable-in-code-and-the-strip-test-asserts-the-strip

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
2026-09-16 22:1xZ master-sensei: minted as the SL7.138 residue the Prime named in the GO by sha (mur-sl7-138-r3): item (4) landed as prompt text and must become a harvest mechanism; the strip test's half (b) asserts its own monkeypatch; two probes are named that the tree does not carry. The Prime's (d) -- my own SL7.137 node reword -- is done by me in the same pass, not by a kid.
<!-- THOUGHT:END -->
