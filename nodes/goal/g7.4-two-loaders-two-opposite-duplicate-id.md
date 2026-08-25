---
confidence: 1.0
goal_id: G7.4
goal_kind: subgoal
id: "goal:g7.4"
mint_id: 4ff23be4b8354c6ca25479ccdeccc730
origin: goals-doc
parents:
  - goal:g7
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G7.4: Two loaders, two opposite duplicate-id policies"
type: goal
---

`graph_core/loader.py::load_directory` keeps the **first**-sorted file on an id
collision and, as of 2026-08-22, reports every collision via
`graph.duplicate_ids`, a `WARN:` line, and `DuplicateIdError` under `strict`.
`snapshot-goals.py::load_existing_nodes` keeps the **last**-sorted file, by
plain dict overwrite, and reports nothing.

**Not cosmetic — it silently narrows the integrity check that was just built.**
`collect_parent_refs` and the whole G7.1 check read off `load_existing_nodes`,
so when a duplicate pair disagrees on `parents:`, the losing file's references
are invisible and its dangling refs are never reported. Measured on this
corpus: an independent raw scan finds **89** dangling parent references;
`snapshot-goals.py` finds **88**. The missing one is
`nodes/task/t-090-bfsdfs-traversal-primitives.md → hyp:graph-core-r11`, whose
id `task:t-090` is shared with `t-090-schema-as-file-with.md` — one of G7.2's
17 pairs, where the wrong sibling wins.

Fix: one duplicate-id policy, in one place, reported the same way by both
readers. First-wins plus a warning is the established behaviour; make
`load_existing_nodes` conform rather than inventing a third rule. The 88-vs-89
gap is the regression test.
