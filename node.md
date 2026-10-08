---
id: experiment:dg2close-a00-15d05ac0-7ef787-check
mint_id: bc5a2761d2b64b7db57b7fe8d81c7000
type: experiment
parents:
  - hypothesis:a00-15d05ac0-7ef787
next_edges: []
edited_by: director-general-2
scaffold_hash: f18cb8e03a97e653
season: 2
title: "Closing measurement on the pre-retirement bytes: every kit requirement (61/61) was carried verbatim in its build-site hypothesis body; the cavekit_req tasks carried only paraphrased AC labels"
town: core
---
# experiment:dg2close-a00-15d05ac0-7ef787-check

Closing measurement for a hypothesis left live under retired goal:s18. Read-only. The kits (`.agi/context/kits/cavekit-*.md`) were deleted at e2b0f0c5c (L1.09, 2026-09-03 22:16Z), so everything was measured on the parent commit 4801db935, extracted to /tmp/dg2mvp/close/hist. Script: /tmp/dg2mvp/close/h3.py. The match is a literal one after whitespace and case are normalised: each kit `- [ ]` AC bullet and the `**Description:**` line.

| # | command | observed |
|---|---|---|
| 1 | parse the 8 kit files at 4801db935 into `<domain>/R<n>` → (AC bullets, description) | 61 requirements |
| 2 | nodes carrying `cavekit_req` at 4801db935 | 94: 91 tasks (all `origin: build-site`, **all 91 resolvable**) plus the 3 malformed hypotheses. No build-site hypothesis carries `cavekit_req` |
| 3 | tasks: does any kit AC bullet appear literally in the task body | **0 / 91**. The bodies hold Description, Files and Test Strategy for the task |
| 4 | tasks: frontmatter `acceptance_criteria` cites `R<n>.<m> (paraphrase)` of its own requirement | 90 / 91 cite ≥1 AC, and 30 / 91 cite ALL of them. This paraphrase is in the frontmatter, not the body |
| 5 | seeded sample (random.seed(18), 10 tasks) | 10/10 have 0 literal AC in the body. Frontmatter paraphrases cover 1-4 of the 4 ACs each (t-025 1/4, t-016 3/4, t-086 2/4, t-059 1/4, t-044 1/4, t-032 4/4, t-027 1/4, t-064 4/4, t-082 1/4, t-065 4/4) |
| 6 | build-site HYPOTHESIS nodes (titled `<domain>/R<n>: …`): full kit description plus ALL AC bullets literally in the body | **61 / 61**. Every kit requirement is replicated verbatim in the graph (e.g. `hyp:chain-engine-r1` body = the kit R1 text) |
| 7 | the node's own named sample (chain-engine-r1, graph-core-r1, schema-registry-r1, renderers-r1, embeddings-r1, environment-indexers-r1, autoresearch-tree-skill-r1, plus 3 open ones) | all are build-site hypotheses, so **10/10 contain the AC text** (row 6) |
| 8 | every one of the 91 resolvable tasks: does its parent hypothesis carry the requirement text | 91 / 91 |
| 9 | today (HEAD c58e1e7): the 61 retired `deprecated/hypothesis` build-site nodes, re-matched against the 4801db935 kit text | 61 / 61 still carry the full description plus AC verbatim. Deleting the kits lost no requirement text |
