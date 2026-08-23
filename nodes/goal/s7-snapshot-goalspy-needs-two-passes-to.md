---
confidence: 1.0
goal_id: S7
goal_kind: short-term
id: "goal:s7"
origin: goals-doc
seeds: []
status: active
tags:
  - goal
  - root
  - short-term
title: "S7: `snapshot-goals.py` needs two passes to wire a new sub-goal"
type: goal
---

Found 2026-08-23 while adding G1.3–G1.5, G6.6 and G6.7. Adding a sub-goal and
running the script once mints the child node with a correct `parents:` list, but
the **parent's `seeds:` list does not contain it**. A second run adds it.
Reproduced twice: pass 1 wrote `goal:g1.5` and left `goal:g1` unchanged; pass 2
added `- goal:g1.5` to `goal:g1`.

Cause is ordering — the parent's frontmatter is composed before the children of
that pass exist, so each run wires the sub-goals it knew about at entry.

**Why it is worth a row rather than a shrug.** The edge exists in one direction
only, so nothing looks broken: the child's `parents:` is right, traversal
upward works, and `--verify` has no complaint. What breaks is downward
traversal — a renderer or a kid walking `seeds:` from `goal:g1` cannot see the
newest sub-goal, which is reliably the one being worked. `driver.sh` runs the
script every iteration so a live loop self-heals on the next pass, which is
exactly what makes this easy to never notice; a fresh clone plus a single run
renders a graph whose most recent work is invisible from above.

Fix: compose parent seed lists after all nodes for the pass are known, or make
the wiring a second phase over the completed set. Assert the fixed point in a
test — run twice, second run writes nothing. Related to **G7.1** (referential
integrity on every parent reference), which checks the reference that exists;
this is the reference that silently does not.
