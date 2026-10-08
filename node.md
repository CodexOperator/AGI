---
id: experiment:dg2close-a01-697f4893-9bb21a-check
mint_id: acc68a3012e64d3ba4783ed0c96e4046
type: experiment
parents:
  - hypothesis:a01-697f4893-9bb21a
next_edges: []
edited_by: director-general-2
scaffold_hash: 13213759e60e86af
season: 2
title: "Closing measurement on the pre-retirement bytes: 1-4 of 10 sampled open build-site chains have an equivalent claim under the Domain ideas; at most 28/52 are even mentioned; L1.09 closed 29 by citing build nodes, none by citing a Domain idea"
town: core
---
# experiment:dg2close-a01-697f4893-9bb21a-check

Closing measurement for a hypothesis left live under retired goal:s18. Read-only. The build-site chains retired at e2b0f0c5c (L1.09, 2026-09-03 22:16Z), so everything was measured on the parent commit 4801db935 (/tmp/dg2mvp/close/hist). Descendants are computed through `parents:` edges. "Native" means not `origin: build-site` and not a task.

| # | command | observed |
|---|---|---|
| 1 | open build-site hypotheses (no verdict child, and no experiment child with a verdict) | 52 open / 9 reached (the node says 50/11) |
| 2 | `idea:domain-*` at 4801db935 | **14**, not 8: 7 are the build-site domain ideas that ARE the chains' own parents, and 7 are native. Descendants of `idea:domain-graph-core`: 68 (the node says 142) |
| 3 | native nodes under all 14 Domain ideas | 223 |
| 4 | upper bound over the population: open chains whose R-label (`graph-core/R4`) or requirement name appears anywhere in a native Domain-subtree node | **28 / 52 (54%)**, a mention and not an equivalent assertion. 24/52 have no native mention at all |
| 5 | seeded sample (random.seed(18), 10 of 52), judged by hand for an equivalent native assertion | renderers/R3 Mermaid: **yes** (verdict:a00-8636e255, proved, all AC). renderers/R5 Git-Diff and R7 Plugin Contract: **listed only** in bigger_outcome:renderers-r1 "Properties achieved". graph-core/R2 Edge: **partial** (bigger_outcome:graph-core-primitives names Edge and the DAG invariant). chain-engine/R6: a native attractiveness hypothesis exists but has `parents: []` (not under a Domain idea) and makes a different claim. autoresearch/R9, chain-engine/R5, chain-engine/R9, env-indexers/R2, env-indexers/R9: **none** |
| 6 | sample tally | strict 1/10, generous (counting list-mentions and partials) 4/10 |
| 7 | `git show e2b0f0c5c:<29 *-by-citation verdicts>`: evidence_runs prefixes and `idea:domain-` mentions | 69 citations, **all `build:`** (engine code files); **0** cite a Domain idea or its subtree |
| 8 | today: live `origin: build-site` / retired | 0 / 159 |
