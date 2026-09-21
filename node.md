---
id: goal:g1.8
mint_id: 6755ca16b6d64d65bf37945b3d97d5cb
type: goal
parents:
  - goal:g1
confidence: 1.0
edited_by: season.py
goal_id: G1.8
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
title: "G1.8: A secret is a shape in the graph and a value on the box"
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

- `.env.example` at the repo root — committed, the shape, with its own build
  node like any other tracked file.
- `.env` beside it — gitignored, mode 0600, written by hand once.
- **`nodes/.geometry/secrets.md`** — the declaration. Where both files live,
  which keys are required, optional, and forbidden. **The first `config` node
  in the corpus**, which is the code path `[config]`'s schema had been waiting
  on since it was written (**goal:g10.2**).
- `extensions/agi/bin/envfile.py` — the one reader. Resolves the node, expands
  `<source_root>` against `locations.py`, and checks the file. Named `envfile`
  and not `secrets` because `bin/` goes on `sys.path` in a dozen entry points
  and a module called `secrets` there shadows the standard library's for all of
  them — confirmed, not theorised.
- `driver.sh` — asks `envfile.py` for the path, runs the check every pass, then
  sources the file before any dispatch, so `dispatch.py`, pi, and every pi child
  inherit it.
- `extensions/agi/bin/env-get.sh` — prints one value and nothing else, so
  `~/.pi/agent/auth.json` can use pi's `"!command"` key form and resolve the
  same single file rather than holding a second copy of the secret.

One value, one file, one declaration, two readers, and no path by which a key
reaches git. **Per project, not per box** — both paths resolve against
`source_root`, so `fantasia/.env` and `fantasia/agi/.env` are different files
found by the same nearest-enclosing rule, with no flag (**goal:g8.2**). The cost
is that a key needed by two projects is typed twice; the alternative is a
machine-global store no project's graph describes.

## What is NOT built, and is the rest of this goal

1. ~~A schema, so `--smoke` reports a missing key.~~ **Done 2026-08-31.**
   `driver.sh --smoke` on a project with no `.env` now prints the file to
   create, the mode to set, and the keys to fill in.
2. **`init` writes the stub.** G1.5's job, this file's case: bringing a project
   up should render `.env.example` → `.env` and stop, telling the operator the
   one manual step that is genuinely irreducible — typing the secret.
3. **A verifier.** A check that no tracked file, no grid ref and no session
   transcript contains a value from `.env`. Cheap to write, and the only thing
   that turns "we are careful" into something falsifiable.
4. **An OpenRouter dispatch path, if CC-side kids are to use it.** Claude
   Code's own subagent tool can only spawn Claude models, so `cc_dispatch`
   cannot route to OpenRouter by configuration alone — it needs a dispatcher
   that calls the API. Decided when the need appeared: **use the OpenRouter
   Python SDK, not raw `requests`/`curl`**, so a minor change on their side
   does not silently break the loop. Until that exists, OpenRouter models are
   reachable through the pi runtime only.

   **The dispatcher itself is specified under `goal:g4.3`, not here** — its
   two spawn modes (kids directly, and parents that spawn their own kids) and
   its per-tier models are statements about the runtime split. This goal owns
   only the question of how the key reaches it.

## Falsifier

A fresh clone on a new box, with `.env` absent, runs `driver.sh --smoke` and is
told exactly which keys it needs and where to put them — from the graph, not
from a human remembering. Filling them in is then the only manual step, and a
second `--smoke` is clean. **Half met as of 2026-08-31:** the telling works and
is tested; the clone still has to create `.env` by hand rather than `init`
rendering the stub, which is item 2.

## Why this is a G1 subgoal

G1 is the commitment that no mundane step is un-named, and G1.5 is that `init`
leaves nothing to install by hand. A key that must be typed on each box is the
irreducible manual step — but *knowing which keys, and being told when one is
missing* is not irreducible, and is exactly the class of "repeated, mechanical,
therefore script it" that G1 exists to close.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 declared the split and shipped it with the path written into two shell
scripts. The owner rejected exactly that on reading it: a path known only to
code is a path the graph cannot answer questions about, and this repo already
carries the scar of that class of fact — the ancestor walk, restated eleven
times until nobody could change the rule once. So v2 moves the location into
`nodes/.geometry/secrets.md` and gives it one reader.

Two things fell out that v1 could not have predicted. First, the `[config]`
schema had been sitting since 2026-08-25 with zero nodes minted against it and
a note that minting one waited on "a code path that reads more than one field";
this is that path, reading five, so the schema stopped being speculative rather
than a new type being invented beside it. Second, the reader could not be
called `secrets.py`: `bin/` goes on `sys.path` in a dozen entry points, and a
module by that name there shadows the standard library's `secrets` for every
one of them. Confirmed by import, not reasoned about, and renamed to
`envfile.py` before anything depended on it.

Item 1 is struck because it is done and tested, not because it was descoped —
`--smoke` on a project with no `.env` now names the file, the mode and the
keys. Item 4 is new and is a constraint discovered while answering the owner's
model-routing question: Claude Code's subagent tool spawns Claude models only,
so `cc_dispatch` cannot reach OpenRouter by configuration, and the SDK-over-raw
decision is recorded here rather than left to whoever writes that dispatcher.
<!-- THOUGHT:END -->