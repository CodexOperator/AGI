# autoresearch-tree iteration 9001 — agent zoom-r1-measure-t3

## Zoom Level: 3 — Code nodes
Level 3 is actual code: one level3 node per source file (nodes/level3/*.md), each with a payload_ref to the real file and a mechanically-generated IO contract (inputs/outputs — harness-owned, never authored by a summarising model). goal:g2.1 calls this the level that makes the graph an executable artifact rather than a description of one, and it is the only level with a real index behind it today.

Target node: **goal:g2**
5 level-3 (level3) node(s) within 2 hops of target `goal:g2`.

### Code nodes in scope
-   `level3:bin-zoom` — Level-3: extensions/agi/bin/zoom.py (layer=2)
    file: extensions/agi/bin/zoom.py
    parents: idea:engine-zoom
-   `level3:src-embeddings-init` — Level-3: extensions/agi/src/embeddings/__init__.py (layer=2)
    file: extensions/agi/src/embeddings/__init__.py
    parents: idea:engine-embeddings
-   `level3:src-embeddings-node2vec` — Level-3: extensions/agi/src/embeddings/node2vec.py (layer=2)
    file: extensions/agi/src/embeddings/node2vec.py
    parents: idea:engine-embeddings
-   `level3:src-embeddings-projection` — Level-3: extensions/agi/src/embeddings/projection.py (layer=2)
    file: extensions/agi/src/embeddings/projection.py
    parents: idea:engine-embeddings
-   `level3:src-embeddings-similarity` — Level-3: extensions/agi/src/embeddings/similarity.py (layer=2)
    file: extensions/agi/src/embeddings/similarity.py
    parents: idea:engine-embeddings

## Your Task
Extend or fork from `goal:g2`. Stay tight — don't wander to other chains.
Acceptable: spawn one child node (hyp from idea, exp from hyp, mvp from exp, outcome from mvp).
When done, signal completion:
```
python3 <plugin>/bin/cli.py done 9001 zoom-r1-measure-t3 \
  --verdict <verdict_state> --confidence <0.0-1.0> \
  --node-id <new_node_id> --parent goal:g2 \
  --notes "<one-line>"
```

If stuck >2 attempts → write `pending` verdict and stop.
