---
id: exp:id-fanout-budget
mint_id: 15df46d4b87f40d3b5b40080e19c3546
type: experiment
parents:
  - hyp:zoom-encoded-node-ids
confidence: 0.92
edited_by: season.py
season: 1
tags:
  - g2.5
thought_session: season
title: "Fan-out budget: does any node in the corpus exceed 36/62 children?"
---
**Method.** Walked `/home/ubuntu/work/agi-tree/nodes/**/*.md` (a plain
`glob`, explicitly unioned with a dotfile glob because Python's `**/*.md`
silently skips names starting with `.` — this corpus has exactly one such
file, `nodes/level3/.gitignore.md`, which would otherwise have
undercounted its own census parent's fan-out by 1). For every file, parsed
the YAML frontmatter block between the first two `---` lines with a
regex-based reader (no external YAML dependency), extracting `id:`,
`type:`, and `parents:` (both block-list `- foo` and inline `[a, b]`
forms). Built `children_of[parent_id] = [child_id, ...]` by iterating every
node's `parents:` list and appending that node's id under **each** parent
named — a node with 2 parents is counted as a child of both, which inflates
fan-out for both parents. This is the honest reading per the brief: either
parent would independently have to mint a sibling character for that
child, so undercounting by picking "the" parent would hide real budget
pressure. Fan-out = number of children a given id has, counted this way.
Script: `/tmp/fanout.py` (scratch, not committed, reproducible from this
method description alone).

**Corpus census.** 828 `.md` files under `nodes/`, all 828 had a parseable
frontmatter block, all 828 had an `id:` field. Type counts: experiment 113,
verdict 121, hypothesis 103 (+1 file with no readable `type:` field, 3
total), goal 62, idea 71, task 91, mvp 26, outcome 20, level3 181,
app-purpose/app_purpose 17, bigger-outcome/bigger_outcome 20. 811 distinct
ids among 828 files — 17 ids each appear on two separate files on disk
(`app-purpose:graph-core`, `bigger_outcome:cli-invocation-r1`,
`bigger-outcome:graph-core-r1`, `bigger_outcome:session-management-r1`,
`exp:cli-invocation-r1`, `exp:graph-core-r1`, `exp:schema-registry-r2`,
`mvp:graph-core-r1`, `outcome:cli-invocation-r1`, `outcome:graph-core-r1`,
`task:t-090`, `verdict:cli-invocation-r1`, `verdict:graph-core-r1`,
`verdict:idea_domain-cli-invocation`, `verdict:schema-registry-r2`,
`verdict:session-management-r1`, `verdict:verdict_session-management-r1`).
This is exactly the duplicate-id fossil G2.5 names as motivation (the
loader "kept X, hidden Y" bug, G7.2) — not something this experiment fixes.
My raw scan counts every file regardless, so fan-out numbers below are an
upper bound relative to whatever any single live loader actually sees. 20
distinct strings in `parents:` fields do not resolve to any real id in the
corpus (7 are literal blank entries, the rest are ids like
`hypothesis:embeddings-r1` that no longer exist as files) — these do not
inflate any real node's fan-out count since they only exist as references,
not as counted children of an "in-corpus" id. 106 nodes declare zero
parents (root goals `goal:g1`..`goal:g10`, `goal:s1`..`goal:s10`; census
roots under `idea:domain-*`/`idea:engine-*`; and a handful of orphan
fossils including `build:src-init`).

**Full fan-out distribution, all node types.**
- Distinct ids with >=1 child: 333
- Max fan-out: **20** — `idea:engine-graph-core`
- Median: 1, Mean: 2.35
- Parents exceeding 36: **0**
- Parents exceeding 62: **0**

Histogram (children-count -> number of parents with that count):
```
1:195  2:59  3:26  4:13  5:3  6:16  7:3  8:4  9:2  10:5
11:1  13:1  14:1  15:1  16:1  19:1  20:1
```

Top 10 parents by child count:
```
idea:engine-graph-core                  20
idea:engine-context-refs                19
idea:domain-graph-core                  16
idea:engine-tests-graph-core            15
idea:engine-schema-registry             14
idea:engine-tests                       13
idea:domain-chain-engine                11
goal:g6                                 10
goal:g7                                 10
idea:domain-autoresearch-tree-skill     10   (tied: idea:domain-environment-indexers, idea:engine-chain-engine, also 10)
```

**Level-3 specific, restricted to `type: level3` children grouped by their
census parent.** 181 level3 nodes on disk (GOALS.md's own text cites 178 —
the corpus grew by 3 since that count was written; not a discrepancy in
method). 1 level3 node (`build:src-init`) declares no parent and is
excluded from the census-parent tally.
- Distinct census parents: 58
- Max fan-out: **20** — `idea:engine-graph-core` (same node as the
  corpus-wide worst offender: essentially all of its 20 children are
  level3 nodes)
- Median: 1.0, Mean: 3.12
- Census parents exceeding 36: **0**
- Census parents exceeding 62: **0**

All 58 census parents by level3-child count:
```
idea:engine-graph-core                  20
idea:engine-context-refs                19
idea:engine-tests-graph-core            15
idea:engine-schema-registry             14
idea:engine-tests                       13
idea:engine-chain-engine                10
idea:engine-tests-schema-registry        9
idea:engine-context-kits                 6
idea:engine-agi-algos                    6
idea:engine-tests-renderers              6
idea:engine-renderers                    5
idea:engine-embeddings                   4
idea:engine-tests-embeddings             4
idea:engine-context-impl                 3
idea:engine-tests-chain-engine           3
goal:g8.2                                2
idea:engine-gitignore                    1
idea:engine-handoff                      1
idea:engine-readme                       1
idea:engine-todo                         1
idea:engine-autoresearch-config          1
idea:engine-autoresearch-ideas           1
idea:engine-autoresearch-md              1
idea:engine-autoresearch-sh              1
idea:engine-benchmark                    1
idea:engine-cli                          1
idea:engine-dashboard                    1
idea:engine-decompose-engine-goalmap     1
idea:engine-decompose-engine             1
idea:engine-dispatch                     1
idea:engine-evidence-gate                1
idea:engine-grid                         1
idea:engine-heal                         1
idea:engine-level3                       1
idea:engine-metrics                      1
idea:engine-payload-boundary             1
idea:engine-post-wire                    1
idea:engine-render-context               1
idea:engine-snapshot-build-site          1
idea:engine-snapshot-goals               1
idea:engine-stitch                       1
goal:g6.3                                1
idea:engine-zoom                         1
idea:engine-conftest                     1
idea:engine-context-plans                1
idea:engine-driver-sh                    1
idea:engine-agi-bridge-readme            1
idea:engine-agi-bridge-index             1
idea:engine-cc-session-start             1
idea:engine-agent-prompt                 1
idea:engine-find-root                    1
idea:engine-package-json                 1
idea:engine-run-loop-sh                  1
idea:engine-schema-sql                   1
idea:engine-migrate-to-sqlite            1
idea:engine-skill-doc                    1
goal:g8.1                                1
idea:engine-start-sh                     1
```

**Current id-length distribution (for comparison against 36-char UUIDs).**
Min 7 chars (`goal:g1`, `goal:g2`, ... all single-digit `goal:g<N>` and
`goal:s<N>` ids), median 27, mean 26.7, max 88 chars (three tied:
`level3:context-refs-zoom-roundtrip-ground-truth-subject-a-t005-trial-{1,2,3}-reconstruction.md`).
So the current scheme already spans 7-88 characters depending on node
type/depth — a flat 36-char UUID would be shorter than today's worst-case
level3 ids but far longer than today's typical goal/idea ids, and would
lose the "truncate = ancestor" property those short ids don't have either.

**Reproducibility.** Re-running requires only: glob `nodes/**/*.md` plus
the dotfile variant, parse `id`/`type`/`parents` from frontmatter, build
the multi-parent-inclusive `children_of` map, and tabulate. No graph
traversal library, no engine code, and no state beyond the files on disk
was used.