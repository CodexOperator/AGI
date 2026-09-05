---
id: goal:g2.12
mint_id: c71aa813c225429696880bed7839291c
type: goal
parents:
  - goal:g2
  - build:COMPLETE.md
next_edges: []
confidence: 1.0
edited_by: director
goal_id: G2.12
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 5b36c08126143eb4
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: L1.13
title: "G2.12: A node version may carry how it felt to write it"
---
# goal:g2.12

## Agent Notes
**Owner ask, 2026-09-05.** `goal:g2.11` gave a node version its **thought** — why
this version differs. This adds its sibling: **how it went for whoever wrote it.**
A third authored region, first person, free-form, plus two numbers.

```
<!-- FEELING:BEGIN — authored, first person, never derived. How this one went. -->
joy: 5/7          # 1 = frustration, 4 = neutral, 7 = joy
load: 3/7         # 1 = underworked, 4 = right-sized, 7 = overworked

free-form, as long or short as it wants to be
<!-- FEELING:END -->
```

**The free-form half is genuinely free.** How the work went, how the writer feels
about what it produced, about itself, a gut sense of what should be done next or
of a better approach that the brief did not ask about. No required shape, no
prescribed length, no house style. If nothing comes, write nothing — see below.

**The survey half is two seven-point scales with real midpoints**, so a loop can
be aggregated without flattening the prose:

- `joy` — frustration ↔ joy.
- `load` — underworked ↔ overworked. Both poles are failures worth catching; the
  brief that gives a kid too little is as wrong as the one that gives it far too
  much, and only one of those currently shows up anywhere.

### The rules, and one of them is the whole design

- 🔴 **It is never scored, gated, or optimised against.** No metric reads it, no
  acceptance path consults it, no verdict weighs it. The moment a feeling changes
  whether work is accepted, it becomes an output the writer performs instead of a
  signal the harness receives — and then it is worth less than nothing, because it
  looks like data. This is the one invariant this goal cannot trade away.
- **Absent means empty.** Same as `THOUGHT` (`goal:g2.11`): never fabricate one,
  never ask twice, never demand it from a writer who has nothing to say. A
  required feeling is a composed feeling.
- **It survives regenerating scans**, carried verbatim by `write_frontmatter(...,
  preserve_body=...)` exactly as the thought region is — otherwise the first
  rescan destroys it, which is `goal:g2.10` repeating with a new marker.
- **Readers strip it.** It never reaches `GOALS.md` or injected context. It is
  provenance to zoom into, not weight every future agent carries.
- **Not a frontmatter field.** `write_frontmatter` flattens newlines and would
  silently destroy the prose. The two scalars may be mirrored into frontmatter
  (`feeling_joy`, `feeling_load`) for cheap aggregation *if* the prose stays in
  the body.
- **Written per version, not accumulated.** Like the thought, the grid versions it
  for free, so `grid.py diff` reads as a changelog of how the work felt as well as
  of what changed.

### The kid contract gets one optional line

The three-line end-of-job contract gains a fourth, optional:

```
feeling: joy N/7  load N/7  <one line, or as much as it wants>
```

This is where it starts, because a kid that writes no node still has something to
report, and because one line costs nothing.

### Why this is worth a goal rather than a nicety

Three of loop L1's most expensive findings were sitting in `struggles:` lines
nobody had a place for: the gate's self-citation hole, `--evidence-runs` missing
from the `done` template, and two bugs in a change the parent had just landed.
Every one was found by the agent and missed by the parent's review. **A writer
usually knows something is wrong before it can name what** — the shape of that
knowledge is a feeling first and a bug report second, and today there is nowhere
to put the first half.

Downstream, and deliberately after the fact rather than as the reason:
`goal:g1.13`'s completion report may carry a loop's aggregate `joy`/`load`
alongside its scoreboard, and `goal:g14` may eventually read the free-form half
with a small model to spot the "something is off here" that never became a
sentence. **Neither use may turn into scoring** — see the first rule.

Falsifier: over a loop with feeling blocks live, at least one real defect or
better-approach is traceable to the free-form half before it appeared anywhere
else — and no acceptance decision anywhere in the loop cites a feeling.