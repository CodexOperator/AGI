---
id: verdict:dg2mvp-g133
mint_id: b894ee4069e1418382dda120ccefca97
type: verdict
parents:
  - experiment:dg2mvp-g133-check
  - hypothesis:g133-one-resolve-old-sha-reads-pre-rewrite-ids-through-a-cell-named-map
next_edges: []
confidence: 0.92
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g133-check
scaffold_hash: 2ed25c8de00dfaf6
season: 2
title: "goal:g1.33 post-build (5f1e8092f2): proved 0.92 -- resolve_old_sha's map branch resolves a pre-rewrite id through the cell-named map (full id + 12-hex prefix), prints no map line, answers every miss silently; one map reader, cell-only path; home-path WARN never refuses; ceiling over, closed on the node"
town: core
verdict: proved
---
# verdict:dg2mvp-g133

## Verdict: proved (0.92)

Every CLAIM conjunct holds at HEAD and no falsifier fires.
- (1) resolve_old_sha resolves a pre-rewrite id (40-hex and 12-hex prefix) from the live cell-named map to its post-rewrite id (a commit in the repo), returns a git-known id as itself, None otherwise.
- (2) path from the cell only (0 literal map paths in bin/, F4 0 hits); absent cell, absent file, chmod-000 file, junk rows, ambiguous prefix, all-zero or non-commit new id each answer None silently.
- (3) `links.py sha` prints exactly the new id or `unknown commit id` (rc 1) / a named refusal (rc 2); no output line carried two 40-hex ids; the old id is never echoed.
- (4) write.py WARNs once (create and edit), rc 0, never refuses, never echoes the path.
- ONE resolver, ONE map reader. Tests: test_resolve_old_sha 17 passed, test_links 48 passed (1 skip, 1 xfail of another row), test_write 206 passed (1 xfail of another row; the test_g73320_* rows green).
Residue notes (not gaps): the map's line-2 pick resolves None because its new id is not in this clone (41809 of 79566 rows are old-unknown AND new-unknown here; 17414 resolve), by design; ceiling overrun and the unwired-readers bullet are already closed/demoted on the node (DH.DG3.44, DH.DG3.46).
