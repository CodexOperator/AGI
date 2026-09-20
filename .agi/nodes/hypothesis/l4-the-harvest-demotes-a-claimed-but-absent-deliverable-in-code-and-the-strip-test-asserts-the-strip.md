---
id: hypothesis:l4-the-harvest-demotes-a-claimed-but-absent-deliverable-in-code-and-the-strip-test-asserts-the-strip
mint_id: d4763cd261c0402b9cbb69dc94b0d4ba
type: hypothesis
parents:
  - goal:g6.14
next_edges: []
edited_by: belam
scaffold_hash: 1eba635399f39e3c
season: 2
testable_claim: "SL7.138 residue (belam GO 21:58Z by sha, pi review mur-sl7-138-r3, landed 9237dbf78), ONE kid, brief.py + the harvest code path + tests, in this order; line numbers as of 9237dbf78 -- re-locate by name. (a) Item (4) of SL7.138 landed as PROMPT TEXT in the parent brief; make it a MECHANISM: the harvest reads the diff for every deliverable the kid names IN CODE (cli.py / the harvest verb), and the fixture proof the node names must exist -- a kid node claiming a deliverable the branch diff does not carry yields inconclusive_lean_disproved with the probe named, in the harvest output, not in prose. (b) test_agi_env_strip.py:96-101 half (b) is vacuous -- it asserts the absence of the same three keys it just delenv'd; assert against the STRIP (the conftest fixture's effect on a process that inherits the keys), not against the monkeypatch. (c) The SL7.138 kid node names probes probe_strip_predicate.py and probe_timeout.py that are not in the tree -- commit them under the round's session dir or strike the names from the node (a named probe that does not exist is a claimed-but-absent deliverable, the very shape item (a) demotes). Proof: a fixture with a claimed-but-absent deliverable is demoted by the harvest CODE; the strip test fails when the strip is removed; every probe named by a kid node in this round exists in the tree."
thought_session: dissolve-legacy-2026-09-19
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

## Agent Notes
DEFERRED to the NEXT loop by owner order 2026-09-17 00:4xZ (via belam gen 27; ack 00:46Z; FULL PAUSE 00:5xZ): SL7.139 loop tip 62c27623d on season2/loops/hypothesis-l4-the-harvest-demote-a00-5b6321f6 (kid experiment:a00-64495393-5457b7 re-verdicted inconclusive_lean_proved:60, note names r1 base / r2 tree), temp-tree gate 0c9acd913 GREEN on 90b91cd20, both GO conditions met (SL7.140 minted 90b91cd20). NOT landed -- the chain stopped at LOCKS-AT-MERGE before the order; MAIN untouched; window closed 00:4xZ. Merge = sanctuary-master then: re-gate on the actual HEAD, ONE --no-ff 62c27623d, numbers line, stamp in two calls.

SM gen 6 LANDED on MAIN at fe8703725 (--no-ff loop tip 62c27623d, GO by SHA belam 07:26Z): re-gated clean on 32e5a8939, 57 green in a throwaway detached tree (test_cli + test_agi_env_strip); kid experiment:a00-64495393-5457b7 :60 as master-sensei re-verdicted, 80/40 = 2.0x disclosed. Stamp folds into the next suite. SL7.140 (the deliverable check diffs against the round base in the kid worktree) is the follow-on round, dispatched into the first slot after PAIR 1.
