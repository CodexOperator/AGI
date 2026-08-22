# autoresearch-tree iteration 9001 — agent zoom-r1-measure-t2

## Zoom Level: 2 — Sub-systems
Level 2 is sub-systems and their relationships: one census node per engine module/entry-point (nodes/idea/engine-*.md), each carrying a unit_path pointing at the real file it describes and a parent goal that motivates it. This is the layer between 'what we want' (level 1) and 'the file that does it' (level 3). Non-census idea nodes (research chains, domain groupings) are deliberately excluded — they are not sub-systems.

Target node: **goal:g2**
4 level-2 (idea) node(s) within 2 hops of target `goal:g2`.

### Sub-systems in scope
-   `idea:engine-embeddings` — Engine surface: extensions/agi/src/embeddings (layer=1)
    file: extensions/agi/src/embeddings
    parents: goal:g2
    children: level3:src-embeddings-init, level3:src-embeddings-node2vec, level3:src-embeddings-projection
-   `idea:engine-zoom` — Engine surface: extensions/agi/bin/zoom.py (layer=1)
    file: extensions/agi/bin/zoom.py
    parents: goal:g2
    children: level3:bin-zoom
-   `idea:engine-agi-algos` — Engine surface: extensions/agi/src/agi_algos (layer=2)
    file: extensions/agi/src/agi_algos
    parents: goal:g2.1
    children: level3:src-agi-algos-asciirender, level3:src-agi-algos-benchmark, level3:src-agi-algos-graph-builder
-   `idea:engine-level3` — Engine surface: extensions/agi/bin/level3.py (layer=2)
    file: extensions/agi/bin/level3.py
    parents: goal:g2.1
    children: level3:bin-level3

## Your Task
Extend or fork from `goal:g2`. Stay tight — don't wander to other chains.
Acceptable: spawn one child node (hyp from idea, exp from hyp, mvp from exp, outcome from mvp).
When done, signal completion:
```
python3 <plugin>/bin/cli.py done 9001 zoom-r1-measure-t2 \
  --verdict <verdict_state> --confidence <0.0-1.0> \
  --node-id <new_node_id> --parent goal:g2 \
  --notes "<one-line>"
```

If stuck >2 attempts → write `pending` verdict and stop.
