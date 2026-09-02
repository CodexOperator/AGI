---
name: command
structural: true
derived_from: authored-2026-09-02 for G1.10 -- no prior corpus to survey; this
  schema and its one node are minted together, following `[cron].md`'s
  precedent, and the node's shape follows the reader that consumes it rather
  than a census of existing nodes
fields:
  commands: {type: dict}   # name -> {argv: list, about: str, cwd: str, workflow: str}
  workflows: {type: dict}  # workflow name -> list of command names
  ordered: {type: list}    # which workflows are a SEQUENCE, not a set
validation:
  required: [commands]
  types:
    commands: dict
    workflows: dict
spawn:
  allowed_parents: [goal]
  min_parents: 1
  max_parents: 1
---

# command

**Structural node type — the engine's standard commands declared as graph
content (G1.10, `.geometry`).** Sibling of `[cron].md` and minted by copying
it, because the shape is already proven: a `.geometry` node plus one resolver
that reads it, where **editing the node is the change**.

Not `[config].md`, for the same reason a cadence is not: that schema's
`validation.required` is `[locations, config_marker_names]`, which a command
table cannot satisfy, and its `locations.nodes_root` is a live read path a
command declaration has no business relaxing.

## What reads this

`bin/commands.py` resolves `commands` into real argv and can run them
(`list`, `show`, `run`), and `render-context.py` writes the declared set into
`context/INJECTION.md`, so every agent is *handed* the commands instead of
remembering them.

**That second reader is the point of the node existing.** G10.2's rule is that
a `.geometry` node must be the input a code path resolves against, not
documentation about one. A command table nothing reads is a fourth copy of
`CLAUDE.md`'s prose.

## Scope, stated by the owner and load-bearing

> not a command for every custom test call, just the commands that are used
> during standard workflows

This is **not a shell-alias dumping ground.** It declares the small set of
operations the engine cannot run without — primarily the unified read and
write paths, the verification sequence, and the loop itself. A command that
exists to save one person one keystroke does not belong here; a command a cold
session has to be told does.

## Field meanings

- `commands` — name to `{argv, about, cwd, workflow}`. `argv` is a list, never
  a string, so nothing is re-parsed by a shell and no quoting question ever
  arises. `<root>` in any argv element is substituted with the resolved graph
  root and `<engine>` with the engine checkout, which is what keeps the table
  free of absolute paths that would not survive a clone.
- `workflows` — named lists of command names. A workflow is the thing a human
  means by "the known-good verification sequence": a grouping, not a new
  command.
- `ordered` — which of those groupings are a **sequence** rather than a set.
  Only a workflow named here is rendered as "in this order". The distinction
  exists because the rendered list goes into `INJECTION.md` and is read by
  every agent: telling a kid that an unordered inspection set must be run in
  order is a false instruction delivered at scale, and this project has
  already shipped one contradictory contract to every kid (`goal:s8`).

## Why argv and not a shell string

A shell string invites `&&`, pipes, and quoting, and then the node stops being
data and becomes a program the resolver has to interpret. `goal:g9.7`'s
argument applies: the form a human reads and the form the engine runs must be
the same object, and a list of arguments is the only spelling where that is
true without a parser in between.
