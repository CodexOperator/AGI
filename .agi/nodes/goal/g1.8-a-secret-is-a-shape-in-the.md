---
confidence: 1.0
goal_id: G1.8
goal_kind: subgoal
heading_level: 3
id: "goal:g1.8"
mint_id: 6755ca16b6d64d65bf37945b3d97d5cb
origin: goals-doc
parents:
  - goal:g1
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G1.8: A secret is a shape in the graph and a value on the box"
type: goal
---

**A credential is the one kind of file the graph must describe and must never
hold.** Every other file in this repo is graph content: `level3.py` mints a node
for it, `grid.py` versions it, a clone gets it. A provider key inverts that —
the *set* of keys the loop needs is exactly the kind of thing a fresh machine
must be told, and the *values* are exactly the kind of thing that must never be
committed, pushed, or snapshotted into a ref.

So this goal splits the file in two and gives each half to the side that should
own it:

| | committed | tracked by grid | who owns it |
|---|---|---|---|
| `.env.example` — the shape | yes | yes, like any build node | the graph |
| `.env` — the values | never | never | the box, set once at init |

**The consequence is the interesting part, and it is a feature.** A gitignored
file has no history — not remotely, not locally. Change `OPENROUTER_API_KEY`'s
*value* and nothing anywhere records that anything happened; that is correct,
because a version history of a secret is a leak with a changelog. Change its
*shape* — add a key, retire one, restate what a key is for — and that lands in
`.env.example`, which is an ordinary tracked file with an ordinary build node
and an ordinary grid ref. **Shape is versioned, value is not**, and the seam
between them is a `.gitignore` line rather than a mechanism.

## What exists now

- `.env.example` at the repo root — committed, the shape.
- `.env` beside it — gitignored, mode 0600, written by hand once.
- `driver.sh` sources `.env` after resolving the project and before any
  dispatch, so `dispatch.py`, pi, and every pi child inherit it. Resolution is
  `locations.py --what source`, the same resolver every other entry point
  calls, so the file found belongs to the project actually being run.
- `extensions/agi/bin/env-get.sh` — prints one value and nothing else, so
  `~/.pi/agent/auth.json` can use pi's `"!command"` key form and resolve the
  same single file rather than holding a second copy of the secret.

That is one value, one file, two readers, and no path by which a key reaches
git.

## What is NOT built, and is the rest of this goal

1. **A schema for it.** A `secret` (or `config-template`) node type declaring
   which keys a project requires, so `--smoke` can say *"`.env` is missing
   `OPENROUTER_API_KEY`"* instead of the loop failing later inside pi with a
   provider error. Today the requirement is prose in `.env.example`; nothing
   reads it.
2. **`init` writes the stub.** G1.5's job, this file's case: bringing a project
   up should render `.env.example` → `.env` and stop, telling the operator the
   one manual step that is genuinely irreducible — typing the secret.
3. **A verifier.** A check that no tracked file, no grid ref and no session
   transcript contains a value from `.env`. Cheap to write, and the only thing
   that turns "we are careful" into something falsifiable.

## Falsifier

A fresh clone on a new box, with `.env` absent, runs `driver.sh --smoke` and is
told exactly which keys it needs and where to put them — from the graph, not
from a human remembering. Filling them in is then the only manual step, and a
second `--smoke` is clean. **Until item 1 exists this goal is not met**, because
the current state tells the operator nothing until pi itself fails.

## Why this is a G1 subgoal

G1 is the commitment that no mundane step is un-named, and G1.5 is that `init`
leaves nothing to install by hand. A key that must be typed on each box is the
irreducible manual step — but *knowing which keys, and being told when one is
missing* is not irreducible, and is exactly the class of "repeated, mechanical,
therefore script it" that G1 exists to close.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version, written at the moment the need appeared: an OpenRouter key had
to go on this box and there was no declared answer for where credentials live.
The temptation was to answer only the immediate question — put the key in
`~/.pi/agent/auth.json` beside the MiniMax one and move on, which works today
and is what pi documents. Rejected because it puts the secret in a file the
graph does not describe, on a path no project inherits, and the next box
re-derives the whole arrangement from nothing.

The split that made this a goal rather than a chore: a gitignored file is
usually treated as a hole in the graph, and here the hole is load-bearing.
Naming `.env.example` as the graph's half and `.env` as the box's half turns
"we cannot version this" from a limitation into the actual design — the shape
gets a build node and a grid ref, the value gets neither, and the asymmetry is
what makes it safe. Scoped as a G1 subgoal rather than a top-level goal because
it is G1.5's `init` story applied to one file class, and because 44 goals are
already `active`; this adds a 45th and should be among the first retired once
items 1–3 land.
<!-- THOUGHT:END -->
