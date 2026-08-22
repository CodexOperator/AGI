# autoresearch-tree iteration 9001 — agent zoom-r1-measure-t1

## Zoom Level: 1 — Goals
Level 1 is the top of the zoom axis: goals and their skill-tree of general nodes (nodes/goal/*.md). Long-term goals (e.g. goal:g7) decompose into sub-goals (goal:g7.2, parents: [goal:g7]). No code lives at this level — it is what the project is trying to achieve, not how.

Target node: **goal:g2**
3 level-1 (goal) node(s) within 2 hops of target `goal:g2`.

### Goals in scope
- → `goal:g2` — G2: Adjustable zoom with contracts that survive the trip (layer=0)
    children: goal:g2.1, goal:g2.2, idea:engine-embeddings
-   `goal:g2.1` — G2.1: Level 3 first: code nodes that stitch back into a running tree (layer=1)
    parents: goal:g2
    children: hyp:level3-node-anatomy, idea:engine-agi-algos, idea:engine-level3
-   `goal:g2.2` — G2.2: IO maps as inherited contract slices (layer=1)
    parents: goal:g2

## Your Task
Extend or fork from `goal:g2`. Stay tight — don't wander to other chains.
Acceptable: spawn one child node (hyp from idea, exp from hyp, mvp from exp, outcome from mvp).
When done, signal completion:
```
python3 <plugin>/bin/cli.py done 9001 zoom-r1-measure-t1 \
  --verdict <verdict_state> --confidence <0.0-1.0> \
  --node-id <new_node_id> --parent goal:g2 \
  --notes "<one-line>"
```

If stuck >2 attempts → write `pending` verdict and stop.
