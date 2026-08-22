# agi-tree INJECTION CONTEXT
_generated 2026-08-22T05:27:03+00:00_

## graph snapshot
- nodes: 643
- edges: 543
- by type: app-purpose=2, app_purpose=14, bigger-outcome=2, bigger_outcome=15, experiment=105, goal=43, hypothesis=101, idea=43, level3=74, mvp=20, node=3, outcome=18, task=90, verdict=113
- **scored on `outcome_coverage`** (`metric_primary`) — this is the target
- outcome_coverage: 0.198 (mvps per hypothesis; goal-attributable)

## chain diagnostics (descriptive — not targets)
- chain count: 26
- longest chain: 10 hops (via next edges)
Hop counts describe the graph's shape; they do not score the work. A
rising longest chain against a flat `outcome_coverage` means hops are
being padded — agents once drove this stat to 9 chains x 2000 hops carrying
no signal (TODO.md H3), and that structure is what made chain-finding
non-terminating (H0c). Read these numbers, never optimise them.

## attractive ideas (descendant count, top 10)
- idea:domain-graph-core :: 56 descendants
- idea:domain-environment-indexers :: 38 descendants
- idea:domain-schema-registry :: 38 descendants
- idea:domain-chain-engine :: 37 descendants
- idea:domain-embeddings :: 37 descendants
- idea:domain-autoresearch-tree-skill :: 36 descendants
- idea:domain-renderers :: 29 descendants
- idea:engine-graph-core :: 18 descendants
- idea:domain-chain-bootstrap :: 15 descendants
- idea:engine-schema-registry :: 14 descendants

## big-vs-small decision
Each iteration MUST first answer: **explore a big idea or small idea?**
- big = fresh chain, broad concept (default 30%)
- small = extend existing chain mid-way (default 70%)

## verdict taxonomy
`proved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N | pending`

## chain rules
- **chain length is never a target.** Extend a chain only when the next
  node adds evidence or moves a goal; a short chain that closes a goal
  beats a long one that closes nothing.
- attraction is the descendant list above (goal-attributable), not hop count
- mid-chain join is always allowed; so is starting fresh (see big-vs-small)
- forks welcome — same idea may spawn multiple hypotheses
- new ideas spawn from any node type (idea/hypothesis/experiment/verdict)
- `proved`/`disproved` require `evidence_runs >= 1`; unevidenced verdicts
  are auto-demoted to `inconclusive_lean_*` by the evidence gate

## next-step suggestions
- pending tasks: 90 (see nodes/task/)

## ASCII view (≤200 lines)
```
# graph: 643 nodes
# types: app-purpose=2, app_purpose=14, bigger-outcome=2, bigger_outcome=15, experiment=105, goal=43, hypothesis=101, idea=43, level3=74, mvp=20, node=3, outcome=18, task=90, verdict=113
#
        app-purpose:autoresearch-tree-skill :: app_purpose
              app-purpose:chain-engine :: app-purpose
        app-purpose:cli-invocation :: app_purpose
              app-purpose:embeddings :: app_purpose
        app-purpose:environment-indexers :: app_purpose
            app-purpose:exporters :: app_purpose
              app-purpose:graph-core :: app-purpose
              app-purpose:renderers :: app_purpose
              app-purpose:schema-registry :: app_purpose
          app-purpose:session-management :: app_purpose
          app-purpose:session-management-r1 :: app_purpose
              app_purpose:a00-1467544f-aaaa25 :: app_purpose
                app_purpose:a00-ddbe3410-app001-chain-bo :: app_purpose
              app_purpose:a00-ddbe3410-app002-structur :: app_purpose
              app_purpose:a00-ddbe3410-app003-iterativ :: app_purpose
        app_purpose:vector-embedding-isomorphism :: app_purpose
        bigger-outcome:autoresearch-tree-skill-r :: bigger_outcome [spawns->app-purpose:autoresearch-tree-skill]
            bigger-outcome:chain-engine-r1 :: bigger-outcome [spawns->app-purpose:chain-engine]
      bigger-outcome:cli-invocation-r1 :: bigger_outcome [spawns->app-purpose:cli-invocation]
            bigger-outcome:embeddings-r2 :: bigger_outcome [spawns->app-purpose:embeddings]
            bigger-outcome:embeddings-r3 :: bigger_outcome
        bigger-outcome:environment-indexers-r1 :: bigger_outcome [spawns->app-purpose:environment-indexers]
          bigger-outcome:exporters-r1 :: bigger_outcome [spawns->app-purpose:exporters]
            bigger-outcome:graph-core-r1 :: bigger-outcome [spawns->app-purpose:graph-core]
            bigger-outcome:renderers-r1 :: bigger_outcome [spawns->app-purpose:renderers]
            bigger-outcome:schema-registry-r1 :: bigger_outcome [spawns->app-purpose:schema-registry]
            bigger-outcome:schema-registry-r2 :: bigger_outcome
        bigger-outcome:session-management-r1 :: bigger_outcome [spawns->app-purpose:session-management, spawns->app-purpose:session-management-r1]
            bigger_outcome:a00-1467544f-aaaa25 :: bigger_outcome [spawns->app_purpose:a00-1467544f-aaaa25]
      bigger_outcome:a00-324837df-2546ce :: bigger_outcome [spawns->app_purpose:vector-embedding-isomorphism]
              bigger_outcome:a00-ddbe3410-bo001-chain- :: bigger_outcome [spawns->app_purpose:a00-ddbe3410-app001-chain-bootstrap]
            bigger_outcome:a00-ddbe3410-bo002-struct :: bigger_outcome [spawns->app_purpose:a00-ddbe3410-app002-structural-repair]
            bigger_outcome:a00-ddbe3410-bo003-iterat :: bigger_outcome [spawns->app_purpose:a00-ddbe3410-app003-iterative-traversal]
    exp:a00-1467544f-aaaa25 :: experiment [spawns->verdict:a00-1467544f-aaaa25]
exp:a00-1467544f-chain-600hop :: experiment [spawns->verdict:a00-1467544f-chain-600hop]
exp:a00-324837df-2546ce :: experiment
  exp:a00-8636e255-bf1a6c :: experiment [spawns->verdict:a00-8636e255-bf1a6c]
  exp:a00-b4570cd1-context-injection-fix :: experiment [spawns->verdict:a00-b4570cd1-0b9427]
  exp:a00-c2ec59b7-b391d9 :: experiment [spawns->verdict:a00-c2ec59b7-b391d9]
    exp:autoresearch-tree-skill-r1 :: experiment [spawns->mvp:autoresearch-tree-skill-r1, spawns->verdict:autoresearch-tree-skill-r1]
      exp:autoresearch-tree-skill-r1-extend :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend]
        exp:autoresearch-tree-skill-r1-extend2 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend2]
        exp:autoresearch-tree-skill-r1-extend3 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend3]
exp:autoresearch-tree-skill-r1-r1-extend :: experiment
exp:autoresearch-tree-skill-r1-r1-extend :: experiment
exp:autoresearch-tree-skill-r1-r1-extend :: experiment
exp:autoresearch-tree-skill-r1:extend8 :: experiment
    exp:chain-engine-r1 :: experiment [spawns->verdict:chain-engine-r1]
    exp:chain-engine-r1-extend :: experiment [spawns->verdict:chain-engine-r1-extend]
        exp:chain-engine-r1-extend2 :: experiment [spawns->verdict:chain-engine-r1-extend2]
          exp:chain-engine-r1-extend3 :: experiment [spawns->verdict:chain-engine-r1-extend3]
exp:chain-engine-r1-r1-extend1 :: experiment
exp:chain-engine-r1-r1-extend2 :: experiment
exp:chain-engine-r1-r1-extend3 :: experiment
  exp:cli-invocation-r1 :: experiment
exp:cli-invocation-r1-extend1 :: experiment
exp:cli-invocation-r1-extend2 :: experiment
exp:cli-invocation-r1-extend3 :: experiment
exp:cli-invocation-r1-r1-extend1 :: experiment
exp:cli-invocation-r1-r1-extend2 :: experiment
exp:cli-invocation-r1-r1-extend3 :: experiment
    exp:dashboard-cli-r1 :: experiment
exp:embeddings-r1-extend1 :: experiment
exp:embeddings-r1-extend2 :: experiment
exp:embeddings-r1-extend3 :: experiment
exp:embeddings-r1-r1-extend1 :: experiment
exp:embeddings-r1-r1-extend2 :: experiment
exp:embeddings-r1-r1-extend3 :: experiment
    exp:embeddings-r2 :: experiment [spawns->verdict:embeddings-r2]
    exp:embeddings-r2-extend :: experiment [spawns->verdict:embeddings-r2-extend]
        exp:embeddings-r2-extend2 :: experiment [spawns->verdict:embeddings-r2-extend2]
          exp:embeddings-r2-extend3 :: experiment [spawns->verdict:embeddings-r2-extend3]
    exp:embeddings-r3 :: experiment [spawns->verdict:embeddings-r3]
    exp:embeddings-r3-extend :: experiment [spawns->verdict:embeddings-r3-extend]
        exp:embeddings-r3-extend2 :: experiment [spawns->verdict:embeddings-r3-extend2]
          exp:embeddings-r3-extend3 :: experiment [spawns->verdict:embeddings-r3-extend3]
      exp:engine-census-r1 :: experiment
    exp:environment-indexers-r1 :: experiment [spawns->mvp:environment-indexers-r1, spawns->verdict:environment-indexers-r1]
    exp:environment-indexers-r1-extend :: experiment [spawns->verdict:environment-indexers-r1-extend]
        exp:environment-indexers-r1-extend2 :: experiment [spawns->verdict:environment-indexers-r1-chain-extension, spawns->verdict:environment-indexers-r1-extend2]
          exp:environment-indexers-r1-extend3 :: experiment [spawns->verdict:environment-indexers-r1-extend3]
exp:environment-indexers-r1-r1-extend1 :: experiment
exp:environment-indexers-r1-r1-extend2 :: experiment
exp:environment-indexers-r1-r1-extend3 :: experiment
    exp:evidence-gate-resolution-r1 :: experiment
  exp:exp-a00-407fa689-verdict-pareto :: experiment
    exp:exp-a00-407fa689-verdict-repair :: experiment
  exp:exporters-r1 :: experiment [spawns->verdict:exporters-r1]
    exp:exporters-r1-extend :: experiment [spawns->verdict:exporters-r1-extend]
    exp:exporters-r1-extend2 :: experiment [spawns->verdict:exporters-r1-extend2]
        exp:exporters-r1-extend3 :: experiment [spawns->verdict:exporters-r1-extend3]
exp:exporters-r1-r1-extend1 :: experiment
exp:exporters-r1-r1-extend2 :: experiment
exp:exporters-r1-r1-extend3 :: experiment
    exp:graph-core-r1 :: experiment [spawns->verdict:graph-core-r1]
    exp:graph-core-r1-extend :: experiment [spawns->verdict:graph-core-r1-extend]
        exp:graph-core-r1-extend2 :: experiment [spawns->verdict:graph-core-r1-extend2]
          exp:graph-core-r1-extend3 :: experiment [spawns->verdict:graph-core-r1-extend3]
exp:graph-core-r1-r1-extend1 :: experiment
exp:graph-core-r1-r1-extend2 :: experiment
exp:graph-core-r1-r1-extend3 :: experiment
    exp:integrity-detection-r1 :: experiment
      exp:level3-scan-r1 :: experiment
    exp:renderers-r1 :: experiment [spawns->verdict:renderers-r1]
    exp:renderers-r1-extend :: experiment [spawns->verdict:renderers-r1-extend]
        exp:renderers-r1-extend2 :: experiment [spawns->verdict:renderers-r1-extend2]
          exp:renderers-r1-extend3 :: experiment [spawns->verdict:renderers-r1-extend3]
exp:renderers-r1-r1-extend1 :: experiment
exp:renderers-r1-r1-extend2 :: experiment
exp:renderers-r1-r1-extend3 :: experiment
    exp:schema-registry-r1 :: experiment [spawns->verdict:schema-registry-r1]
        exp:schema-registry-r1-extend :: experiment [spawns->verdict:schema-registry-r1-extend]
exp:schema-registry-r1-extend1 :: experiment
exp:schema-registry-r1-extend2 :: experiment
exp:schema-registry-r1-extend3 :: experiment
exp:schema-registry-r1-r1-extend1 :: experiment
exp:schema-registry-r1-r1-extend2 :: experiment
exp:schema-registry-r1-r1-extend3 :: experiment
    exp:schema-registry-r2 :: experiment [spawns->verdict:schema-registry-r2]
exp:schema-registry-r2-bracket-conventio :: experiment [spawns->verdict:schema-registry-r2-bracket-convention-extend3]
    exp:schema-registry-r2-extend :: experiment [spawns->verdict:schema-registry-r2-extend]
        exp:schema-registry-r2-extend2 :: experiment [spawns->verdict:schema-registry-r2-extend2]
          exp:schema-registry-r2-extend3 :: experiment
  exp:session-management-r1 :: experiment
  exp:session-management-r1-extend1 :: experiment [spawns->verdict:session-management-r1-extend1]
    exp:session-management-r1-extend2 :: experiment [spawns->verdict:session-management-r1-extend2]
      exp:session-management-r1-extend3 :: experiment [spawns->verdict:session-management-r1-extend3]
exp:session-management-r1-r1-extend1 :: experiment
exp:session-management-r1-r1-extend2 :: experiment
exp:session-management-r1-r1-extend3 :: experiment
    exp:stitch-roundtrip-r1 :: experiment
    exp:topological-queries-r1 :: experiment [spawns->verdict:topological-queries-r1]
  exp:zoom-numeric-axis-r1 :: experiment
      experiment:a00-ddbe3410-exp001-graph-cor :: experiment [spawns->verdict:a00-ddbe3410-verdict001-graph-core-r1-t001]
    experiment:a00-ddbe3410-exp002-structura :: experiment [spawns->verdict:a00-ddbe3410-verdict002-structural-repair]
    experiment:a00-ddbe3410-exp003-iterative :: experiment [spawns->verdict:a00-ddbe3410-verdict003-iterative-traversal]
  experiment:exp-a00-4125fa6d-005488 :: experiment [spawns->verdict:verdict-a00-4125fa6d-005488]
  experiment:exp:a00-204c9d9e-1d958f :: experiment [spawns->verdict:verdict:a00-204c9d9e-1d958f]
goal:g1 :: goal [spawns->goal:g1.1, spawns->goal:g1.2, spawns->idea:engine-cli (+2)]
  goal:g1.1 :: goal
  goal:g1.2 :: goal
goal:g2 :: goal [spawns->exp:zoom-numeric-axis-r1, spawns->goal:g2.1, spawns->goal:g2.2 (+4)]
  goal:g2.1 :: goal [spawns->hyp:level3-node-anatomy, spawns->idea:engine-agi-algos, spawns->idea:engine-level3]
  goal:g2.2 :: goal
  goal:g2.3 :: goal
  goal:g2.4 :: goal
goal:g3 :: goal [spawns->goal:g3.1, spawns->idea:engine-benchmark, spawns->idea:engine-chain-engine (+1)]
  goal:g3.1 :: goal [spawns->exp:evidence-gate-resolution-r1, spawns->idea:engine-evidence-gate, spawns->idea:engine-post-wire]
goal:g4 :: goal [spawns->goal:g4.1, spawns->goal:g4.2, spawns->goal:g4.3 (+3)]
  goal:g4.1 :: goal
  goal:g4.2 :: goal
  goal:g4.3 :: goal
goal:g5 :: goal [spawns->idea:engine-schema-registry, spawns->idea:engine-snapshot-build-site, spawns->idea:engine-snapshot-goals]
goal:g6 :: goal [spawns->goal:g6.1, spawns->goal:g6.2, spawns->goal:g6.3 (+4)]
  goal:g6.1 :: goal [spawns->exp:stitch-roundtrip-r1, spawns->idea:engine-decompose-engine, spawns->idea:engine-stitch]
  goal:g6.2 :: goal
  goal:g6.3 :: goal
  goal:g6.4 :: goal
  goal:g6.5 :: goal
goal:g7 :: goal [spawns->goal:g7.1, spawns->goal:g7.2, spawns->goal:g7.3 (+7)]
  goal:g7.1 :: goal [spawns->exp:integrity-detection-r1]
  goal:g7.2 :: goal
  goal:g7.3 :: goal
  goal:g7.4 :: goal
  goal:g7.5 :: goal
  goal:g7.6 :: goal
  goal:g7.7 :: goal
goal:g8 :: goal [spawns->goal:g8.1, spawns->goal:g8.2]
  goal:g8.1 :: goal
  goal:g8.2 :: goal
goal:g9 :: goal [spawns->goal:g9.1, spawns->goal:g9.2, spawns->goal:g9.3 (+5)]
  goal:g9.1 :: goal [spawns->exp:dashboard-cli-r1, spawns->idea:engine-dashboard]
  goal:g9.2 :: goal
  goal:g9.3 :: goal
  goal:g9.4 :: goal
  goal:g9.5 :: goal
goal:s1 :: goal
goal:s2 :: goal
goal:s3 :: goal
goal:s4 :: goal
goal:s5 :: goal
  hyp:a00-1467544f-aaaa25 :: hypothesis [spawns->exp:a00-1467544f-aaaa25]
  hyp:a01-7031af17-449ecb :: hypothesis [spawns->mvp:a01-7031af17-449ecb-r11, spawns->verdict:a01-7031af17-449ecb-r11]
  hyp:autoresearch-tree-skill-r1 :: hypothesis [spawns->exp:autoresearch-tree-skill-r1, spawns->task:t-076, spawns->task:t-088 (+1)]
  hyp:autoresearch-tree-skill-r2 :: hypothesis [spawns->task:t-077]
  hyp:autoresearch-tree-skill-r3 :: hypothesis [spawns->task:t-078]
  hyp:autoresearch-tree-skill-r4 :: hypothesis [spawns->task:t-079, spawns->task:t-080]
  hyp:autoresearch-tree-skill-r5 :: hypothesis [spawns->task:t-081]
  hyp:autoresearch-tree-skill-r6 :: hypothesis [spawns->task:t-082, spawns->task:t-083, spawns->task:t-084]
  hyp:autoresearch-tree-skill-r7 :: hypothesis [spawns->task:t-085, spawns->task:t-086]
  hyp:autoresearch-tree-skill-r8 :: hypothesis [spawns->task:t-087]
  hyp:autoresearch-tree-skill-r9 :: hypothesis [spawns->task:t-089]
  hyp:chain-engine-r1 :: hypothesis [spawns->exp:chain-engine-r1, spawns->exp:chain-engine-r1-extend, spawns->task:t-047]
... [truncated, 450 more nodes]
----
Types: app-purpose=2, app_purpose=14, bigger-outcome=2, bigger_outcome=15, experiment=105, goal=43, hypothesis=101, idea=43, level3=74, mvp=20, node=3, outcome=18, task=90, verdict=113
Edges: spawns=543
```
