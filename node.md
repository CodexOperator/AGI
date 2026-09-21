---
id: goal:g7.4
mint_id: 4ff23be4b8354c6ca25479ccdeccc730
type: goal
parents:
  - goal:g7
confidence: 1.0
edited_by: season.py
goal_id: G7.4
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G7.4: Two loaders, two opposite duplicate-id policies"
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

**The regression test has stopped being able to fail, which is not the same as
the goal being met.** With the duplicate ids resolved (0 across the corpus as of
2026-08-25), `t-090` has one claimant, so `snapshot-goals.py` now reports its
`hyp:graph-core-r11` reference and the two counts agree. **The gap closed
because the input stopped containing duplicates, not because the two readers
stopped disagreeing.** The divergent policies are still in the code — first-wins
plus `DuplicateIdError` in `load_directory`, silent last-wins overwrite in
`load_existing_nodes` — and will diverge again the moment a duplicate is
reintroduced, with no test left to catch it. Keep `active`, and note that the
fix now needs its own fixture rather than borrowing one from the live corpus.

**On unresolvable references specifically, the two readers must agree on this:**
warn, keep the node, drop nothing. A reference that does not resolve is a
reporting event, never a load-time deletion — the node is still real, and G7's
first invariant is that node count never drops. G7.1's sweep applied that same
rule by hand: 79 references were removed and 0 nodes were.