---
id: idea:schema-declared-spawn-gate
mint_id: a1065992cbef4e589f0cea52d809f02d
type: idea
parents:
  - goal:s17
next_edges: []
confidence: 0.8
edited_by: season.py
scale: big
season: 1
status: open
tags:
  - s17
  - schema
  - geometry
thought_session: season
title: The spawn rule is data in a schema; the gate is only the enforcement
---
# idea:schema-declared-spawn-gate

**The graph already knows its own spawn rules — it just has never been asked.**
Eleven node types, 778 nodes, and every one of them carries a `type:` and a
`parents:` list. The rule "which types may parent which, and how many" is not
a design question; it is a **measurement** that nobody had taken and nothing
had written down.

So the idea is not "design a schema". It is: **take the measurement, write it
where the loader already looks, and put the check where a write happens.**

## Three parts, and they must stay separate

1. **Data.** Each type's rule lives in a `spawn:` block in
   `context/schemas/[<type>].md`. The schema registry already reads that
   directory and already has the bracketed-means-active convention; nothing
   new is needed to hold the fact.
2. **Geometry.** Two facts are cross-cutting and belong in one place, not
   eleven: which shapes may be parentless, and the ceiling on parent count.
   That is `[shape].md`, and it is what G10.2 means by the graph describing
   its own geometry.
3. **Enforcement.** One module, on the writer path, shaped like
   `evidence_gate.py` — which is the in-house precedent for exactly this
   problem and already answered the hard question (warn vs fail vs demote).

## The failure mode this idea exists to avoid

Writing the rule table into Python. It is the obvious move and it recreates
the exact defect S17 names: the engine root is defined three times
(`find-root.sh`, `level3.py`'s `DEFAULT_ENGINE_ROOT`, `grid.py`'s
`default_engine_root()`), and the two Python ones differ by one index because
one counts from a directory and the other from a file. Neither is wrong;
both will break silently the day `bin/` moves. **A rule with two homes has no
home.** So the gate reads and never restates.

## Why a linter would not do

`GOALS.md`'s design ethic: no prose-only controls where a code control is
possible. A linter someone remembers to run is a prose control with a
shebang — the same thing the six pre-existing schemas already were. Three of
them declared `required:` fields that **zero** nodes have ever carried
(`run_id` 0/75, `source_files` 0/26, `input_shape`/`output_shape`/`behavior`
0/19), and no error was ever raised, because nothing ran them. A rule nothing
executes decays into fiction without anyone noticing.

## The measurable this idea is aimed at

Not chain length. The check either changes what gets written or it does not.
The falsifier is behavioural: attempt an illegal spawn and see whether the
terminal names the rule and the file, attempt a legal one and see whether it
says so.