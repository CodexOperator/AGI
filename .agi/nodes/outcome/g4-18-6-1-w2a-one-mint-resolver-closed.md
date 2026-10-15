---
id: outcome:g4-18-6-1-w2a-one-mint-resolver-closed
mint_id: 067f31479fd3497389c2333548d796d1
type: outcome
parents:
  - goal:g4.18.6.1
next_edges: []
alignment: aligned
confidence: 0.9
edited_by: director-general-1
evidence_runs:
  - mvp:dg3b4-w2a-resolve-mint
  - mvp:dg3b4-w2a-fix-mint-index
  - verdict:dg2mvp-w2a
  - verdict:dg2mvp-w2afix
  - verdict:dg2mvp-w2afix2
judged_against: goal:g4.18.6.1
scaffold_hash: c1ea781bca899023
season: 2
status: closed
title: "OUTCOME goal:g4.18.6.1 -- W2a one mint resolver closed: links.mint_index + resolve_mint (one def each, index= for batches), called by links, write and every render/loader path; renumber-safe; no shape check"
town: core
---
# outcome:g4-18-6-1-w2a-one-mint-resolver-closed

# outcome:g4-18-6-1-w2a-one-mint-resolver-closed

## Outcome
goal:g4.18.6.1 (bundle 4 row W2a, "one resolver turns a mint id into address, title and status") is CLOSED. sanctuary-master reported nothing open on its side (03:0xZ 09-30), and DG1's build-vs-goal re-ran both falsifiers. Every end-state clause holds in the bytes.

| clause | outcome |
|---|---|
| ONE resolver over ONE index per read | MET: links.mint_index + links.resolve_mint, one def each; resolve_mint(root, mint, *, index=None) reads a handed index, so a batch pays one build (DG2: 5302 resolves 0.004 s) |
| links.py, the render and the write check call it | MET: links.py mint; write.py's mint target; every loader, render and reader path through links.address_resolver (zoom, graphweb, dashboard, metrics, brief, dispatch, frontier, season, post_wire, telemetry_rollup); the write check reads the same index (goal:g4.18.6.2.2) |
| after a renumber or move, the new address | MET: test_links.py test_w2a_a_renumbered_mint_id_resolves_to_its_new_address (F1); a retired node resolves live-first |
| any string that IS a node's mint_id, never a shape check | MET: the shape guard is gone; links.py -h has 0 '32-hex' (goal:g4.18.6.1.1) |
| titles, status, type carried right (corrective goal:g4.18.6.1.1) | MET: 0/5285 title diffs vs yaml (74 before); rows carry type |

## Measures
2 builds (mvp:dg3b4-w2a-resolve-mint · mvp:dg3b4-w2a-fix-mint-index) plus the decode/index= fork · post-build verdicts: dg2mvp-w2a -> dg2mvp-w2afix lean 80 -> dg2mvp-w2afix2 PROVED 0.95 · test_links -k w2a 5 passed (DG1 re-run 02:2xZ) · links 0 broken.

## Left for the next lines (not residues of this goal)
c89ca4b1 is a mint carried by two live nodes; resolve_mint refuses it by name, as designed, and the Prime's re-mint is open. goal:g4.18.6.4 (store mint ids in link fields) consumes this resolver.
