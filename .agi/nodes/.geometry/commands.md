---
id: command:commands
mint_id: b7e4f0a91c2d4e8fa63b5d7c8e1f2a04
type: command
parents:
  - goal:g1.10
commands:
  smoke:
    argv:
      - bash
      - <engine>/extensions/agi/driver.sh
      - --smoke
      - --max-iters
      - 1
    about: snapshot + render + metrics, no dispatch — verify the node count did not drop
    workflow: verify
  tests:
    argv:
      - python3
      - -m
      - pytest
      - <engine>/extensions/agi/tests/
      - -q
    about: the engine's own suite
    workflow: verify
  goals-check:
    argv:
      - python3
      - <engine>/extensions/agi/bin/snapshot-goals.py
      - --render
      - --check
    about: GOALS.md and the goal nodes are byte-identical inverses
    workflow: verify
  viewport-verify:
    argv:
      - python3
      - <engine>/extensions/agi/bin/viewport.py
      - --verify
    about: goal:g9.7 — one render, two readers
    workflow: verify
  grid-commit:
    argv:
      - python3
      - <engine>/extensions/agi/bin/grid.py
      - commit
      - --all
    about: version every changed node and its payload
    workflow: verify
  links:
    argv:
      - python3
      - <engine>/extensions/agi/bin/links.py
      - links
    about: goal:g13 — every node's link resolves; broken_links must be 0
    workflow: read
  schema:
    argv:
      - python3
      - <engine>/extensions/agi/bin/links.py
      - schema
    about: goal:s31 — which nodes violate their type's required list (dry)
    workflow: read
  budget:
    argv:
      - python3
      - <engine>/extensions/agi/bin/spawn_budget.py
      - status
    about: goal:g4.8 — live agents against the tree-wide bound
    workflow: read
  credentials:
    argv:
      - python3
      - <engine>/extensions/agi/bin/provisioning.py
      - status
    about: goal:g1.11 — whether per-spawn keys are being issued
    workflow: read
  secrets:
    argv:
      - python3
      - <engine>/extensions/agi/bin/envfile.py
      - --check
    about: goal:g1.8 — required keys present, forbidden keys absent
    workflow: read
  crons:
    argv:
      - python3
      - <engine>/extensions/agi/bin/crons.py
      - show
    about: the crontab the graph declares
    workflow: read
  write-guard:
    argv:
      - python3
      - <engine>/extensions/agi/bin/write_guard.py
      - check
    about: goal:g13.1 — unsanctioned node writes; silent is healthy
    workflow: verify
  dispatch-help:
    argv:
      - python3
      - <engine>/extensions/agi/bin/dispatch.py
      - --help
    about: dispatch --help exits 0 — agents can be spawned
    workflow: verify
  verify:
    argv:
      - python3
      - <engine>/extensions/agi/bin/verification.py
    about: the ONE rotation check — levels quick|rotation|full, --suite opt-in (hypothesis:l4-unified-verification)
    workflow: verify
  verify-suite:
    argv:
      - python3
      - <engine>/extensions/agi/bin/verification.py
      - --suite
    about: the PRIME's rotation check — the rotation level plus the engine suite; the suite window is granted, one runner at a time
    workflow: verify
  view:
    argv:
      - python3
      - <engine>/extensions/agi/bin/viewport.py
      - --live
    about: the live graph, agents drawn as spiders where they are working
    workflow: see
  view-llm:
    argv:
      - python3
      - <engine>/extensions/agi/bin/viewport.py
      - --emit
      - llm
    about: goal:g9.7 — exactly what a kid is handed, from the same frame stream
    workflow: see
  view-both:
    argv:
      - python3
      - <engine>/extensions/agi/bin/viewport.py
      - --emit
      - both
    about: human and llm views side by side, from ONE stream
    workflow: see
  write:
    argv:
      - python3
      - <engine>/extensions/agi/bin/write.py
    about: goal:g13.1 — named node operations; a hand edit becomes an engine action
    workflow: see
  session-complete:
    argv:
      - python3
      - <engine>/extensions/agi/bin/cli.py
      - session-complete
      - <iter>
      - --dry-run
    about: hypothesis:l4-session-dirs-come-home-when-the-round-is-done — bring a finished round's session dir home from a worktree, COPY-THEN-VERIFY; start every inspection with --dry-run
    workflow: read
edited_by: sanctuary-director
ordered:
  - verify
season: 1
status: active
tags:
  - geometry
  - command
  - structural
thought_session: sanctuary-director-genIII-L4
title: Standard command declaration
workflows:
  verify:
    - smoke
    - tests
    - goals-check
    - viewport-verify
    - grid-commit
  read:
    - links
    - schema
    - budget
    - credentials
    - secrets
    - crons
  see:
    - view
    - view-llm
    - view-both
    - write
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
roundtrip probe
<!-- THOUGHT:END -->