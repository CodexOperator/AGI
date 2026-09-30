---
id: experiment:dg2close-a01-1f2762d5-1d90c0-check
mint_id: d1d797fca4cb497d81fc31a7892f64a4
type: experiment
parents:
  - hypothesis:a01-1f2762d5-1d90c0
next_edges: []
edited_by: director-general-2
scaffold_hash: e4dd62c7e9991444
season: 2
title: "Closing measurement at HEAD: removing the 3 free-text cavekit_req fields and inlining them changes nothing measurable (graph load, find_chains, links, schema all byte-identical before/after on a /tmp copy); the 3 values are still live, never fixed"
town: core
---
# experiment:dg2close-a01-1f2762d5-1d90c0-check

Closing measurement for a hypothesis left live under retired goal:s18. Read-only. HEAD c58e1e7 `.agi/nodes` was extracted with git archive twice, into /tmp/dg2mvp/close/a01-1f2762d5-1d90c0/{before,after}. The code was an f4eb68f /tmp tree (no engine file differed in scope). In `after`, the claim's fix was applied: the `cavekit_req:` line was deleted from the 3 nodes and `<!-- cavekit:inlined -->` plus the value was appended to each body. The live repo was not touched.

| # | command | observed |
|---|---|---|
| 1 | `git -C agi grep -n '^cavekit_req:' -- .agi/nodes ':!.agi/nodes/deprecated'` | exactly the 3 malformed values, **still live today**: `a00-ddbe3410-3cc776` `bootstrap/chain-block`, `a00-ddbe3410-iterative-traversal` `chain-engine/iterative-fix`, `a00-ddbe3410-structural-repair` `structural-bias/synthetic-repair`. The other 91 carriers are retired. (goal:s18's retirement THOUGHT calls the 3 live ones "graph-core/R1, R2" legacy labels, which is not what the bytes hold) |
| 2 | `git grep -n cavekit_req -- extensions skills src` (non-test) | readers: `snapshot-build-site.py` only, on kit-derived task dicts parsed from `context/plans/build-site.md` (absent, so its L18 guard makes it a no-op), plus a `node_writer.py` task scaffold string. **No reader of hypothesis frontmatter** |
| 3 | `git grep -n cavekit -- extensions/agi/tests` | 0 hits: no test depends on the field |
| 4 | `[hypothesis].md` schema `required:` | `[id, type, mint_id, title, testable_claim]`: cavekit_req is not required (only `[task].md` requires it) |
| 5 | probe.py: `load_directory` on before/after | 5310 nodes each, 0 loader warnings; the (id, type, parents, children) signature is identical (`f6e860d323c6d8af`) and the edge sets are identical |
| 6 | probe.py: `find_chains(g, <nodes dir>)` and `find_chains_from_node(g, idea:domain-chain-bootstrap)` | before = after = 0 chains (sha `4f53cda18c2baa0c`). This is unchanged but vacuous: find_chains yields 0 chains on the HEAD corpus as a whole |
| 7 | `links.py links --broken --root <copy>` on both | 311 BROKEN lines each (payload refs that point outside the node-only copy), **diff identical**; 0 mention ddbe3410 |
| 8 | `links.py schema --root <copy>` on both | output byte-identical (md5 `0bcec1fe…`); 0 schema violations name ddbe3410 |
| 9 | `level3.py` | not run: it scans engine CODE files via `git ls-files` and reads no hypothesis frontmatter (row 2), so the conjunct is trivially unaffected. The full pytest suite was not re-run (one-file rule); row 3 shows no test reads the field |
