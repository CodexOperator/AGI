---
id: goal:s7
mint_id: 1f929b0d5c964abaac19a9e93514d04c
type: goal
parents:
  - goal:g6
confidence: 1.0
edited_by: all-is-one
goal_id: S7
goal_kind: short-term
heading_level: 2
origin: goals-doc
season: 1
seeds: []
status: retired
tags:
  - goal
  - root
  - short-term
thought_session: g1-g7-rewrite-2026-09-19
title: "S7: `snapshot-goals.py` needs two passes to wire a new sub-goal"
---
Found 2026-08-23 while adding G1.3–G1.5, G6.6 and G6.7. Adding a sub-goal and
running the script once mints the child node with a correct `parents:` list, but
the **parent's `seeds:` list does not contain it**. A second run adds it.
Reproduced twice: pass 1 wrote `goal:g1.5` and left `goal:g1` unchanged; pass 2
added `- goal:g1.5` to `goal:g1`.

Cause is ordering — the parent's frontmatter is composed before the children of
that pass exist, so each run wires the sub-goals it knew about at entry.

## 🔴 Amended 2026-08-27: G6.9 turned "needs two passes" into "never"

**The second pass no longer fixes it, because the pass that did the wiring is
not run any more.** Seed wiring lived in the `GOALS.md -> nodes` direction.
G6.9 reversed the arrow, and `driver.sh` now runs `snapshot-goals.py --render`
and nothing else — which writes `GOALS.md` *out of* the nodes and never
recomputes `seeds:`. So a sub-goal added after 2026-08-25 gets a correct
`parents:` and its parent is **never** told, no matter how many times the loop
runs.

Measured over the whole corpus on 2026-08-27 — every goal→sub-goal edge whose
parent does not list the child:

    goal:g1 missing goal:g1.7
    goal:g2 missing goal:g2.10, goal:g2.11
    goal:g4 missing goal:g4.5
    goal:g7 missing goal:g7.9

Five, and the pattern in them is the damage this row already predicted:
**every one is a recently-added sub-goal, and three of the five are the exact
items the current handoff names as next.** The newest work is reliably the work
that is invisible from above.

Repaired by hand in the same commit, which closes the data but not the defect:
nothing prevents the sixth. The fix S7 already asks for — compose parent seed
lists after all nodes for the pass are known, and assert the fixed point in a
test — now has to be re-homed into the render direction rather than restored in
the direction that no longer exists. Pairs with **G7.1**: that goal checks the
reference that exists, this one is the reference that silently does not.

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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
all-is-one (council) 02:2xZ 09-30, S-goal retirement (alive convenes; belam owner-task). OWNER 01:2xZ 09-30 verbatim: "All S goals should have been retired in favor of nested sub sub goals or whatever that fit under the umbrella goals." Measured, the defect as written is DEAD: the two-pass seed wiring lived in the GOALS.md -> nodes pass, which retired with GOALS.md (goal:g7.16.1.4.1); a goal is now minted by write.py create with its parents set in one call. What is still OPEN is the underlying one-source defect this row found: a goal stores its forward edges twice (seeds beside each child parents), and nothing maintains the copy (482 goal->sub-goal edges, 448 missing from the parent seeds; 125 of 504 goals carry a non-empty seeds). So: retire this S node and mint ONE leaf for the remainder (the s34 -> goal:g4.6.1 precedent): goal:g4.18.6.6, horizon until the council places it. Retired IN PLACE, not moved to deprecated/goal/: the agi-goal skill retires a goal by status, and 39 retired goals already live in goal/ (no deprecated/goal/ dir exists).
<!-- THOUGHT:END -->
