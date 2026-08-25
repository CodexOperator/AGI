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

Found 2026-08-25 while sweeping G7.1. **Corpus side resolved the same day; the
missing validation is what keeps this `active`.**

**First, a correction worth keeping, because the wrong framing nearly bought an
engine change that was not needed.** This was initially written up as "cannot be
fixed by editing a node", as though the graph had a region the normal rules did
not reach. That is backwards. `task:t-090` and `task:t-092` carry
`origin: build-site` — they are **derived nodes, exactly like `nodes/goal/` is
derived from this file.** "Edit the source, not the output" is not an exception
to how this system works, it *is* how it works; the only real question was which
source. Nothing here contradicts the philosophy, and the rule that already
covers it is the one at the top of this document.

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

**The real root cause was in the kit, and the generator was reporting it
honestly.** `parse_kits()` mints one hypothesis per `### Rn:` block found in
`context/kits/cavekit-<domain>.md`. `cavekit-graph-core.md` contained
**R1 through R10 and stopped there.** Meanwhile `build-site.md` opens the same
domain with `### Domain: graph-core (11 R, 47 criteria, T-001..T-018, T-090,
T-092)` and gives both tasks `Cavekit Requirement: graph-core/R11` with eight
acceptance criteria named individually (R11.1 `traverse_bfs` … R11.8
`detect_cycle`). **The plan declared eleven requirements; the kit defined ten.**
`hyp:graph-core-r11` was never minted because there was nothing to mint it from.

So the dangling reference was not noise — it was the only symptom of a
**genuine inconsistency between two cavekit inputs**, and it pointed straight at
it. That is the integrity check doing precisely its job.

**Fixed 2026-08-25 at the input**: added the missing `### R11: Traversal and
Query API` block to `cavekit-graph-core.md`, transcribing the eight criteria
`build-site.md` already spelled out. The generator minted `hyp:graph-core-r11`
on the next run and both task references resolve. **Node count went up, not
down; nothing was hand-written into `nodes/`, and no reference was invented** —
R11 was always a real, documented requirement with a title and eight criteria.

Two things worth carrying forward from the fix:

> **[truncated: 2256 of 5660 characters dropped at a block boundary to fit the 4000-character cap. `GOALS.md` section `G7.8` is the complete text; raise `goal_body_cap` in the project config to keep more.]**
