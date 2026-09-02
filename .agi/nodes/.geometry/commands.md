---
commands:
  smoke:
    argv: ["bash", "<engine>/extensions/agi/driver.sh", "--smoke", "--max-iters", "1"]
    about: "snapshot + render + metrics, no dispatch — verify the node count did not drop"
    workflow: verify
  tests:
    argv: ["python3", "-m", "pytest", "<engine>/extensions/agi/tests/", "-q"]
    about: "the engine's own suite"
    workflow: verify
  goals-check:
    argv: ["python3", "<engine>/extensions/agi/bin/snapshot-goals.py", "--render", "--check"]
    about: "GOALS.md and the goal nodes are byte-identical inverses"
    workflow: verify
  viewport-verify:
    argv: ["python3", "<engine>/extensions/agi/bin/viewport.py", "--verify"]
    about: "goal:g9.7 — one render, two readers"
    workflow: verify
  grid-commit:
    argv: ["python3", "<engine>/extensions/agi/bin/grid.py", "commit", "--all"]
    about: "version every changed node and its payload"
    workflow: verify
  links:
    argv: ["python3", "<engine>/extensions/agi/bin/write.py", "links"]
    about: "goal:g13 — every node's link resolves; broken_links must be 0"
    workflow: read
  schema:
    argv: ["python3", "<engine>/extensions/agi/bin/write.py", "schema"]
    about: "goal:s31 — which nodes violate their type's required list (dry)"
    workflow: read
  budget:
    argv: ["python3", "<engine>/extensions/agi/bin/spawn_budget.py", "status"]
    about: "goal:g4.8 — live agents against the tree-wide bound"
    workflow: read
  credentials:
    argv: ["python3", "<engine>/extensions/agi/bin/provisioning.py", "status"]
    about: "goal:g1.11 — whether per-spawn keys are being issued"
    workflow: read
  secrets:
    argv: ["python3", "<engine>/extensions/agi/bin/envfile.py", "--check"]
    about: "goal:g1.8 — required keys present, forbidden keys absent"
    workflow: read
  crons:
    argv: ["python3", "<engine>/extensions/agi/bin/crons.py", "show"]
    about: "the crontab the graph declares"
    workflow: read
id: "command:commands"
mint_id: b7e4f0a91c2d4e8fa63b5d7c8e1f2a04
ordered:
  - verify
parents:
  - goal:g1.10
status: active
tags:
  - geometry
  - command
  - structural
title: "Standard command declaration"
type: command
workflows:
  verify: [smoke, tests, goals-check, viewport-verify, grid-commit]
  read: [links, schema, budget, credentials, secrets, crons]
---

**The commands the engine cannot run without, declared once.** Every other
thing a run does is configuration — metrics, dispatch, harnesses, schemas,
cron cadences, the spawn budget, credentials. The commands an operator types
were declared nowhere: they lived in `CLAUDE.md` prose, `SKILL.md`'s table,
`QUICKSTART.md`, and whatever the last `HANDOFF.md` wrote down. Four copies,
drifting independently — `goal:s17`'s shape, and this repo has already paid
for it once with the ancestor walk restated eleven times.

## Scope, and it is narrow on purpose

The owner's words: *"not a command for every custom test call, just the
commands that are used during standard workflows."* **This is not a
shell-alias dumping ground.** A command that saves one person one keystroke
does not belong here. A command a cold session has to be *told* does.

Two workflows today, and they are the two halves `goal:g13` names:

- **`verify`** — the known-good sequence, in order. It was prose in
  `HANDOFF.md` §5, which is a file the next director deletes by default.
- **`read`** — the inspection surface. Each entry answers one question about
  the graph's health, and each belongs to a goal that made it answerable.

Only `verify` is listed under `ordered`. `read` is a **set**, and rendering it
as a sequence would put a false instruction into `INJECTION.md`, which every
agent is handed — the same class of mistake as the contradictory kid contract
`goal:s8` records.

## What reads this

`bin/commands.py` resolves and runs (`list`, `show`, `run`), and
`render-context.py` writes the set into `context/INJECTION.md` so **every
agent is handed the commands rather than expected to remember them**.

That second reader is why this node is allowed to exist. `goal:g10.2`'s rule
is that a `.geometry` node must be the input a code path resolves against,
never documentation about one — and a command table nothing reads is a fifth
copy of the prose rather than the deletion of the other four.

## `argv`, never a shell string

A shell string invites `&&`, pipes and quoting, and then this node stops being
data and becomes a program the resolver interprets. `goal:g9.7`'s argument one
layer down: the form a human reads and the form the engine runs must be the
same object. `<root>` and `<engine>` are substituted at resolve time, so no
absolute path — machine state `goal:g8.2` keeps out of the graph — appears
here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by copying `.geometry/crons.md` rather than designing something,
because the owner's instruction for G1.10 said the shape was already built and
running. Copying it also inherits the property that matters: a `.geometry`
node with exactly one resolver, where editing the node IS the change.

The scope sentence is quoted from the owner verbatim and placed above the
table rather than below it, because the failure mode for a node like this is
not being wrong — it is growing. Every future session will have one more
command it would be convenient to add, and the only defence is that the
constraint is the first thing read.

`grid-commit` is in `verify` and not in `read` even though it writes, because
the verification sequence has always ended with it and splitting the sequence
to keep a category pure would make the node disagree with the practice it
describes. A workflow is an order, not a taxonomy.
<!-- THOUGHT:END -->
