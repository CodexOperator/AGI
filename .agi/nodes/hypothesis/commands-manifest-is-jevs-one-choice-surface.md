---
id: hypothesis:commands-manifest-is-jevs-one-choice-surface
mint_id: 1d7b586769154153a77a931938927654
type: hypothesis
parents:
  - goal:g1.25
next_edges: []
ceiling: "3 USD, <= 4 kids, pi parents (owner 09:5xZ: more spend and more spawning)"
confidence: 0.75
edited_by: director-engine
scaffold_hash: 5d388ecc57354d07
season: 2
testable_claim: commands.py manifest prints ONE deterministic JSON choice set from command:commands alone (name, cli, verb, placeholder argv, args schema, purpose, side_effects, proposable; no absolute path, no file written); command:commands declares every verb of the listed engine CLIs or excludes it by name with a reason, proved by a test that introspects every parser and write.py's verb table; propose (Python, CLI, and GET /commands.json + POST /propose on graphweb.py's stdlib server) validates against the entry and returns the argv without executing; the 25 existing commands keep their argv byte-identical.
title: "commands.py manifest is jev's one choice surface: every engine verb a typed entry, ONE machine-readable manifest, propose never executes (assigned: director-engine)"
town: local-maxxing
---
# hypothesis:commands-manifest-is-jevs-one-choice-surface

# hypothesis:commands-manifest-is-jevs-one-choice-surface

## CLAIM
`commands.py manifest` prints ONE JSON choice set built from `command:commands` alone -- per entry: name · cli · verb · argv template
(`<engine>` / `<root>` placeholders, never an absolute path) · args schema (name, type, required, choices) · one-line purpose ·
side_effects (read | graph-write | comms | spawn | spend | network | destructive) · proposable -- the same bytes twice, no file written.
`command:commands` declares every verb of write.py (its script verbs + create), send.py, dispatch.py, workflow.py, cli.py, grid.py,
links.py, rotate.py, spawn_budget.py, provisioning.py, snapshot-goals.py, viewport.py, crons.py and envfile.py, or excludes it BY NAME
with a reason (grid.py checkout, reap --yes, ...). `propose(name, args)` -- in Python, as `commands.py propose <name> --args <json>`, and
in graphweb.py's stdlib server (GET /commands.json, POST /propose) -- validates against the entry and returns the argv, NEVER executing.
The 25 existing commands and `commands.py run` keep their argv byte-identical.

## FALSIFIERS
- a verb of a listed CLI that is neither declared nor excluded (a test introspects every parser and write.py's verb table)
- a declared arg the CLI no longer accepts · two renders that differ at one SHA · an absolute path or a box value in the manifest
- propose (Python, CLI or HTTP) spawns a process or writes a file · an existing command's argv changes

## FILE SCOPE
extensions/agi/bin/commands.py · .agi/nodes/.geometry/commands.md (the node is the change) · extensions/agi/bin/graphweb.py (two
endpoints) · tests. NOT: pane / jev code (MP.02 is the town's) · execution over HTTP · render_for_injection / INJECTION.md.

## CEILING
<= 4 kids · 3 USD · pi parents · <= 12 production lines per conjunct (the node's entries are data, not production lines)

## Agent Notes
assigned: director-engine (owner 09:5xZ 09-23 in the director-engine pane: claim the g7.33 cli grammar part as its own subgoal under an umbrella -- G1 config-maxxing, goal:g1.25 -- work it first thing; more spend and more spawning). Verified 09:2xZ: commands.py has list/show/run/json over 25 commands; graphweb.py already serves stdlib http GET endpoints; no second grammar exists.

director-engine 11:1xZ 09-23: g1.25 mur over EF.21 -- review accept_with_residue, verify DEMOTE (recovered from a schema-echo return): propose validates then silently drops a required arg for 19 of 110 proposable entries (a committed test pins an unmapped placeholder); workflow.py:run (spawn) proposable while dispatch.py is excluded; extras substitute any <x>; [command].md lacks manifest/excluded. Fix round = leaf goal:g1.25.1, EF.37 (dispatched with --owns command:commands so the node edit lands). The jev merge-up and the director-thought notice wait for it.
