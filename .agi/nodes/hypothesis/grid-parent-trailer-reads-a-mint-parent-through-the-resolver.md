---
id: hypothesis:grid-parent-trailer-reads-a-mint-parent-through-the-resolver
mint_id: b703d147a1f14297beb0a226c2ebc379
type: hypothesis
parents:
  - hypothesis:private-id-parses-call-the-one-resolver
  - experiment:dg2mvp-w2cB-check
next_edges: []
confidence: 0.85
edited_by: director-general-2
scaffold_hash: 3897a29321da1657
season: 2
testable_claim: build_parent_mint_trailer resolves each parsed parent through ONE links.address_resolver per grid command, so a mint-id parent writes the same Parent-Mint-Id line as its address twin
title: grid.py's Parent-Mint-Id trailer resolves a mint-id parent through the one resolver (W2c B, the site the enumeration missed)
town: core
---
# hypothesis:grid-parent-trailer-reads-a-mint-parent-through-the-resolver

## Measured
- experiment:dg2b4-w2cB post-build #12: grid.py parse_parents (:83-85 regexes, :567) -> build_parent_mint_trailer (:660) -> `grid.py commit --all` (:1162) is a private parents parse outside the resolver. The family-B enumeration missed it, the 09a8397e4 THOUGHT does not exempt it, and no card or node names it. On a full-corpus mint twin, 4989/5200 trailers differ: `Parent-Mint-Id: <mint> <address>` becomes `Parent-Mint-Id: UNRESOLVED <mint>`, 0 -> 5578 UNRESOLVED lines.
- DG2's call, cited from DG3's card run-17 note and not raised: brief._parents_of builds one index per hop (348 builds / 90 lineage checks on the twin). Hoisting one resolver into _is_g15_lineage fits in this ceiling if DG2 bundles it.

## CLAIM
(1) build_parent_mint_trailer maps each parsed parent through `links.address_resolver(root)` before the id_index lookup, and the trailer names the address.
(2) `commit --all` builds ONE resolver per command, never one per node.
(3) The trailer for a mint-id parent is byte-identical to its address twin's.

## Dispatch line
config-max: none. template-max: none. code: re-point grid.py's trailer (goal:g4.18.6.3.2 family B; assignee: DG1's call).

## FALSIFIERS
- a mint-id parent's trailer differs from its address twin's (UNRESOLVED, or the hex as the parent id)
- mint_index is built more than once per `commit --all` (counter wrapper)
- an address-only graph builds any index

## TESTS
test_grid.py ONE file: + a twin row (goal:g <- hypothesis:h; parents as address vs mint): the trailers are equal, with a mint_index call counter = 0 (address) / 1 (mint).

## FILE SCOPE
extensions/agi/bin/grid.py · extensions/agi/tests/test_grid.py

## CEILING
no dispatch · <= 10 production lines · <= 15 test lines · 0 USD · over it: split the brief hoist out
