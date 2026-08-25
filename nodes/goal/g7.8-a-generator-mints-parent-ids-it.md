---
confidence: 1.0
goal_id: G7.8
goal_kind: subgoal
id: "goal:g7.8"
mint_id: 742ccf8373584908912f0350b6b8366a
origin: goals-doc
parents:
  - goal:g7
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G7.8: A generator mints parent ids it never checks exist"
type: goal
---

Found 2026-08-25 while sweeping G7.1, and it is the last unresolvable-reference
class left standing on the corpus — the only one that **cannot be fixed by
editing a node.**

`snapshot-build-site.py:371` derives a task's parent from its cavekit
requirement by string construction:

```python
domain, rnum = t["cavekit_req"].split("/", 1)
rnum = rnum.split(".")[0]          # R1.2 → R1
parent_hyp = f"hyp:{domain}-{rnum.lower()}"
```

**Nothing checks that the id it just built names a real node.** `build-site.md`
declares `graph-core/R11` for T-090 and T-092, so both get
`parents: [hyp:graph-core-r11]` — and the graph-core hypothesis family stops at
`hyp:graph-core-r10`. Two references that never resolved and never will.

**Why this is a generator defect and not a corpus defect, stated precisely:**
`parents` is a snapshot-owned key. `write_frontmatter`'s `preserve` merge
carries forward only fields the snapshot does *not* own (`{k: v for k, v in
preserve.items() if k not in fm}`), so a hand-corrected `parents:` on T-090 is
overwritten on the very next `--smoke` run. **The node is downstream of the
bug; the only durable edit is upstream of it.** This is 1ead9c965's rule —
fix the duplicate at its generator, not its output — arriving a second time
through a different door, which is the argument for treating it as structural
rather than incidental.

Fix, when it is coded: resolve `parent_hyp` against the loaded corpus before
writing it. On a miss, emit `parents: []` plus a `WARN:` naming the task, the
`cavekit_req` and the id that failed to resolve — warn-by-default, matching
G7.1/G7.2/G7.5. **Do not mint the missing hypothesis**, and do not drop the
task: an unattributed task is a real state, and a fabricated ancestor is worse
than a visible gap. The R11 requirement genuinely has no hypothesis behind it —
that absence is signal about the kit, and silently papering over it is how
`unattributed_nodes` came to sit at 626 without anyone reading it as a number
about the graph.

Deliberately **not coded on 2026-08-25**: the sweep that found it was scoped to
the graph, and an engine change belongs in its own reviewed step. The two
references stay dangling until then — which is the correct visible state, since
the check is now reporting a real defect at its real location.

Held open by the same logic as G7.5: the live corpus is currently this bug's
only fixture. Landing the fix without a standing test means the next
`build-site.md` edit that names a requirement with no hypothesis reintroduces
it silently.
