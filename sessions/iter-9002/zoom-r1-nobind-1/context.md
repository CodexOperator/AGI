# autoresearch-tree iteration 9002 — agent zoom-r1-nobind-1

## Zoom Level: 1 — Goals
Level 1 is the top of the zoom axis: goals and their skill-tree of general nodes (nodes/goal/*.md). Long-term goals (e.g. goal:g7) decompose into sub-goals (goal:g7.2, parents: [goal:g7]). No code lives at this level — it is what the project is trying to achieve, not how.

21 level-1 (goal) node(s) across the whole corpus (no --target given).

### Goals in scope
-   `goal:g1` — G1: Zero-operations loop: every mundane step is a command
    children: idea:engine-cli, idea:engine-driver-sh, idea:engine-find-root
-   `goal:g2` — G2: Adjustable zoom with contracts that survive the trip
    children: goal:g2.1, goal:g2.2, idea:engine-embeddings
-   `goal:g2.1` — G2.1: Level 3 first: code nodes that stitch back into a running tree
    parents: goal:g2
    children: hyp:level3-node-anatomy, idea:engine-agi-algos, idea:engine-level3
-   `goal:g2.2` — G2.2: IO maps as inherited contract slices
    parents: goal:g2
-   `goal:g3` — G3: Scoring that added motion cannot move
    children: goal:g3.1, idea:engine-benchmark, idea:engine-chain-engine
-   `goal:g3.1` — G3.1: `evidence_runs` must resolve to a real node
    parents: goal:g3
    children: idea:engine-evidence-gate, idea:engine-post-wire
-   `goal:g4` — G4: Right model at the right grain, several goals at once
    children: goal:g4.1, idea:engine-agi-bridge-index, idea:engine-dispatch
-   `goal:g4.1` — G4.1: Parallel kids share one working tree and collide
    parents: goal:g4
-   `goal:g5` — G5: Goals are a lifecycle the engine reads, not a human convention
    children: idea:engine-schema-registry, idea:engine-snapshot-build-site, idea:engine-snapshot-goals
-   `goal:g6` — G6: The closed loop: engine work starts in the graph
    children: goal:g6.1, goal:g6.2, idea:deprecate-the-gamed-mass
-   `goal:g6.1` — G6.1: agi-tree becomes the source of truth agi is assembled from
    parents: goal:g6
    children: idea:engine-decompose-engine
-   `goal:g6.2` — G6.2: Retire the padding and keep it recoverable
    parents: goal:g6
-   `goal:g7` — G7: Nothing the loop produces is ever silently lost
    children: goal:g7.1, goal:g7.2, goal:g7.3
-   `goal:g7.1` — G7.1: Referential integrity on every parent reference
    parents: goal:g7
-   `goal:g7.2` — G7.2: Duplicate node ids silently hide files on disk
    parents: goal:g7
-   `goal:g7.3` — G7.3: `evidence_runs` as a bare integer is still unverifiable
    parents: goal:g7
-   `goal:g8` — G8: Forkability: anyone grows their own tree
-   `goal:g9` — G9: Legibility: a human can see what the loop is doing
    children: goal:g9.1, goal:g9.2, goal:g9.3
-   `goal:g9.1` — G9.1: CLI dashboard, runnable as a Claude Code side terminal
    parents: goal:g9
    children: idea:engine-dashboard
-   `goal:g9.2` — G9.2: The same view in a browser
    parents: goal:g9
-   `goal:g9.3` — G9.3: Ride along as a kid
    parents: goal:g9

## Your Task
Pick one `goal` node above to extend, fork, or seed a new chain from.
Acceptable: spawn one child node (hyp from idea, exp from hyp, mvp from exp, outcome from mvp).
When done, signal completion:
```
python3 <plugin>/bin/cli.py done 9002 zoom-r1-nobind-1 \
  --verdict <verdict_state> --confidence <0.0-1.0> \
  --node-id <new_node_id> \
  --notes "<one-line>"
```

If stuck >2 attempts → write `pending` verdict and stop.
