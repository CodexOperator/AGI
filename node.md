---
id: goal:g1.10
mint_id: 4c7e0b93a15d42f6b8e2d7f1a06c9358
type: goal
parents:
  - goal:g1
confidence: 1.0
edited_by: season.py
goal_id: G1.10
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: active
tags:
  - goal
  - subgoal
thought_session: season
title: "G1.10: The engine's standard commands are declared in a node, not memorised"
---
**Config-maxxing applied to the one surface that has escaped it: the commands
themselves.** Everything else about a run is declared — metrics, dispatch,
harnesses, schemas, cron cadences. The commands an operator actually types to
make the engine work are declared nowhere. They live in `CLAUDE.md` prose, in
`SKILL.md`'s table, in `QUICKSTART.md`, and in whatever the last session's
`HANDOFF.md` happened to write down.

**Scope, stated by the owner and load-bearing:** *"not a command for every
custom test call, just the commands that are used during standard workflows."*
A `commands` node is not a shell-alias dumping ground. It declares the small
set of operations the engine cannot run without — **primarily the unified read
and write paths** (`goal:g13`), plus snapshot, render, metrics, grid commit,
dispatch and verification.

## The precedent is already built and running

`.agi/nodes/.geometry/crons.md` is graph content declaring cron cadences;
`crons.py apply` is the one command that reconciles reality with the
declaration; **editing the node is the change.** No schedule is typed at a
shell. This goal is that exact shape, widened by one surface: a
`.geometry/commands.md` node, a `type: command` schema beside `[cron]`, and
one resolver that turns a declared name into the argv it stands for.

That the precedent exists is most of the argument. This is not a new mechanism;
it is the second user of a mechanism that has already survived a migration
freeze and a live kill-switch test.

## What it buys, and it is not convenience

**Three failure modes this session produced, all the same defect.** A step that
is mechanical but undeclared gets done slightly differently each time, and the
differences stay invisible until one of them is wrong:

- Six node parsers agreeing only by accident (`goal:g13`).
- A manifest merge whose atomicity was asserted in a commit message and
  nowhere else (`goal:s28`).
- A scaffold omitting schema-required fields nobody declared it must supply
  (`goal:s31`).

A declared command is read once and executed identically forever. An
improvised one is re-derived by every reader, and this project has now paid for
that three times in one day.

**It also closes a documentation leak.** `CLAUDE.md` and `SKILL.md` both carry
hand-maintained command tables. `goal:s17` is the standing complaint about
hand-maintained second copies, and `goal:g1.9` made the same argument for
briefs: a document that restates a rule enforced elsewhere is a copy that will
drift. Rendering those tables *from* the node is the same fix one surface over.

## What it must not become

**Not a wrapper that hides what it runs.** An operator and an agent must both
be able to ask what a declared name expands to and get the literal argv back.
The failure mode is a command layer that becomes its own thing to learn — the
`goal:g1.2` complaint (a second manual) arriving through a new door.

**Not a writer.** Declaring a command must not mean the engine may invent or
edit one. The node is authored; the resolver reads it.

## Falsifier

Change the argv of a standard workflow step by editing only the node, and have
every caller — `driver.sh`, the skill's table, a fresh operator following
`QUICKSTART.md` — pick up the change with nothing else edited by hand. Then ask
the resolver what a declared name expands to and get the literal command back.

If either half fails, this is a config file that happens to contain strings
rather than a declaration the engine reads.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted 2026-09-02 at the owner's direction, in the same conversation that
renamed `goal:g1` to config-maxxing — and the rename is what makes this goal
legible. Under the old "zero-operations" framing it reads as a convenience:
one more mundane step turned into a command. Under config-maxxing it reads as
the point, because the claim is not "typing is tedious" but "undeclared actions
drift", and this session produced three separate proofs of that.

Filed `active` at the owner's explicit instruction, who said they will be using
it immediately and accepted that it pushes `goals_active` further past the cap.
That is the owner's call to make and it is recorded here rather than silently
absorbed.

The scope sentence is quoted verbatim because it is the whole design. A
commands node that accepts every one-off invocation becomes a shell-alias file
with a node wrapper, which is worse than nothing: it would have all the
maintenance cost of a declaration and none of the guarantee, since nothing
could depend on an entry being present.

`.geometry/crons.md` is named as the shape to copy rather than described from
scratch, deliberately. The strongest argument available is that the mechanism
already runs.
<!-- THOUGHT:END -->