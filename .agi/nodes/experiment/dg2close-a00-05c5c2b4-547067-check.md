---
id: experiment:dg2close-a00-05c5c2b4-547067-check
mint_id: 3d8f7d8d3f424e9e952b75335ed9f13c
type: experiment
parents:
  - hypothesis:a00-05c5c2b4-547067
next_edges: []
edited_by: director-general-2
scaffold_hash: 5ed1a0765b1423f0
season: 2
title: "Closing measurement on the pre-retirement bytes (4801db935): 52 of 52 open build-site hypotheses had zero experiment children; the corpus retired whole at e2b0f0c5c"
town: core
---
# experiment:dg2close-a00-05c5c2b4-547067-check

Closing measurement for a hypothesis left live under retired goal:s18. Read-only. The subject corpus was retired on 2026-09-03 22:16Z in commit e2b0f0c5c (L1.09). This hypothesis was minted at 15d54459c (21:05Z), so it was measured on the parent commit 4801db935 (21:56Z), extracted with git archive to /tmp/dg2mvp/close/hist. The loader and scripts are in /tmp/dg2mvp/close/{load.py,hist_open.json}.

| # | command | observed |
|---|---|---|
| 1 | load `4801db935:.agi/nodes` (1040 nodes); filter `origin: build-site`, `type: hypothesis` | 61 build-site hypotheses (plus 91 tasks and 7 ideas) |
| 2 | verdict reached = a verdict child, or an experiment child that has a verdict child | 9 reached (graph-core-r1, chain-engine-r1, renderers-r1, schema-registry-r1/r2, embeddings-r2/r3, environment-indexers-r1, autoresearch-tree-skill-r1), **52 open**. That matches the goal's "52 open" figure; the node's THOUGHT recount said 50/11 |
| 3 | open hypotheses with ≥1 child whose `type: experiment` lists them in `parents:` | **0 of 52**. All 52 have zero experiment children. The only children are 79 `task` nodes |
| 4 | the reverse direction: `next_edges` of the 52 pointing at `exp:`/`experiment:` | 0 |
| 5 | an experiment or verdict at ANY depth below the 52 (through tasks) | 0 / 0 |
| 6 | open ids mentioned anywhere in any experiment body or parents | 1 (`hyp:graph-core-r11`, a mention only, not an edge) |
| 7 | secondary claim: open hypotheses with an experiment, and whether those experiments have evidence | the set is empty, so the secondary claim is vacuous: no experiment was ever defined |
| 8 | today: `git grep -l '^origin: build-site' -- .agi/nodes ':!.agi/nodes/deprecated'` / `-- .agi/nodes/deprecated` | 0 live / 159 retired |
| 9 | `git show --name-only e2b0f0c5c \| grep by-citation` | 29 of the open chains were closed "by citation" (verdict `inconclusive_lean_*`, evidence_runs = build: nodes, "nothing was executed"). The rest were deprecated with dispositions. None were closed by running an experiment |
