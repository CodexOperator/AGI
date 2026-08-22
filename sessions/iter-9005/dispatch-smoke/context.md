# autoresearch-tree iteration 9005 — agent dispatch-smoke

## Zoom Level: SMALL (legacy alias for numeric level 3 — Code nodes)
Target node: **goal:g2** (extending or branching from this point)

Subtree contains 13 nodes within 2 hops of target.

### Subtree Nodes
- → `goal:g2` (type=goal, layer=0)
    children: goal:g2.1, goal:g2.2, idea:engine-embeddings
-   `goal:g2.1` (type=goal, layer=1)
    parents: goal:g2
    children: hyp:level3-node-anatomy, idea:engine-agi-algos, idea:engine-level3
-   `goal:g2.2` (type=goal, layer=1)
    parents: goal:g2
-   `idea:engine-embeddings` (type=idea, layer=1)
    parents: goal:g2
    children: level3:src-embeddings-init, level3:src-embeddings-node2vec, level3:src-embeddings-projection
-   `idea:engine-zoom` (type=idea, layer=1)
    parents: goal:g2
    children: level3:bin-zoom
-   `hyp:level3-node-anatomy` (type=hypothesis, layer=2)
    parents: goal:g2.1
-   `idea:engine-agi-algos` (type=idea, layer=2)
    parents: goal:g2.1
    children: level3:src-agi-algos-asciirender, level3:src-agi-algos-benchmark, level3:src-agi-algos-graph-builder
-   `idea:engine-level3` (type=idea, layer=2)
    parents: goal:g2.1
    children: level3:bin-level3
-   `level3:bin-zoom` (type=level3, layer=2)
    parents: idea:engine-zoom
-   `level3:src-embeddings-init` (type=level3, layer=2)
    parents: idea:engine-embeddings
-   `level3:src-embeddings-node2vec` (type=level3, layer=2)
    parents: idea:engine-embeddings
-   `level3:src-embeddings-projection` (type=level3, layer=2)
    parents: idea:engine-embeddings
-   `level3:src-embeddings-similarity` (type=level3, layer=2)
    parents: idea:engine-embeddings

## Your Task
Extend or fork from `goal:g2`. Stay tight — don't wander to other chains.
Acceptable: spawn one child node (hyp from idea, exp from hyp, mvp from exp, outcome from mvp).
When done, signal completion:
```
python3 <plugin>/bin/cli.py done 9005 dispatch-smoke \
  --verdict <verdict_state> --confidence <0.0-1.0> \
  --node-id <new_node_id> --parent goal:g2 \
  --notes "<one-line>"
```

If stuck >2 attempts → write `pending` verdict and stop.
