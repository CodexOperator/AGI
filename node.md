---
id: goal:s23
mint_id: 8274f7365bf5494ebecab0336e63ba85
type: goal
parents:
  - goal:g15
confidence: 0.8
edited_by: season.py
goal_id: S23
goal_kind: short-term
heading_level: 2
origin: goals-doc
season: 1
seeds: []
status: complete
tags:
  - goal
  - root
  - short-term
thought_session: season
title: "S23: A deprecated node still reaches injected context"
---
**Measured 2026-09-02, during the goal sweep.** `build:TODO.md` and
`idea:engine-todo` were marked `status: deprecated` and moved to
`.agi/nodes/deprecated/`. `driver.sh --smoke` was re-run. **`build:TODO.md` is
still on line 85 of `INJECTION.md`.** Retirement is invisible to the renderer.

**This started as a proposal for a new lifecycle state.** The owner asked for
`legacy` — retired as far as graph-walking, so it never clutters context and no
agent ever reads it, while chains stay valid until their edges can be remapped.
Investigating it produced a better answer than building it: **`deprecated`
already means exactly that.** `CLAUDE.md` already requires readers to glob the
retired sibling live-first precisely so edges keep resolving. The state exists
and is documented; the renderer simply does not honour it.

**Minting `legacy` would have been a second state meaning the first one**, which
is the failure this project keeps paying for — `goal:s17` (two definitions of
one fact), `goal:g2.5` (mint id vs address), `goal:g7.4` (two loaders, two
policies). One of them is *always* the one a given reader consults.

## The distinction that has to survive the fix

**Load it; do not render it.** These are different operations and collapsing
them breaks something real in each direction:

- **Loading must keep including deprecated nodes.** `stitch.py`, `level3.py`,
  `node_writer.py` and `zoom.py` read the retired sibling deliberately. A
  reader that stops seeing a retired node fails quietly and in its own way —
  orphaned engine file, re-minted duplicate, unresolvable edge, missing title.
- **Injection must stop including them.** Context is the scarcest thing an
  agent has. A retired node in the map is weight every agent carries for the
  rest of the project's life, to describe something deliberately not being
  worked.

So the fix belongs in the render/chain-selection path, not in the loader, and
certainly not in a new `status` value.

## Deliberately out of scope, and it is the harder half

**Remapping edges so a node with real children can retire cleanly.** TODO was
retirable *only* because it is a two-node island — `build:TODO.md` has 0
children, `idea:engine-todo` has 1 child and no parents. A node with live
descendants cannot be retired today without stranding them, and the answer is
to re-parent those chains onto appropriate goal/idea parents first. That is
`goal:g4.5`'s and `goal:g13`'s territory (edges as first-class, one write path
that can perform a remap), not this goal's.

## Falsifier

Deprecate a node that currently appears in `INJECTION.md`, re-render, and it is
gone from the map — while `stitch.py --verify`, `level3.py` and a `zoom.py`
`--level small` on one of its neighbours all still resolve it. Both halves, or
the fix has traded a context leak for a silent reader failure.