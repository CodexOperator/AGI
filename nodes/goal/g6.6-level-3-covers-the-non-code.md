---
confidence: 1.0
goal_id: G6.6
goal_kind: subgoal
id: "goal:g6.6"
origin: goals-doc
parents:
  - goal:g6
seeds:
  - exp:noncode-surface-census
status: active
tags:
  - goal
  - subgoal
title: "G6.6: Level 3 covers the non-code surfaces too"
type: goal
---

**A projection that omits half the engine cannot rebuild it.** `level3.py`'s
scope is deliberately narrow and says so in its own docstring:
`extensions/agi/src/**/*.py` plus `extensions/agi/bin/*.py`, about 70 files.
Everything else in `agi` is outside the graph entirely —

- `skills/agi/SKILL.md`, the document that tells every agent what this loop *is*
- `extensions/agi/lib/agent-prompt.md`, the kid brief itself
- `extensions/agi/driver.sh`, `lib/find-root.sh`, `hooks/cc-session-start.sh` —
  the shell surfaces, including the one that injects context into every session
- `extensions/agi-bridge/index.ts`, `schema.sql`, `README.md`, `run-loop.sh`

That was the right call for a first pass and it is now the thing blocking
**G6.1**. Stitch cannot assemble `agi` from `agi-tree` while the skill, the kid
brief and the session hook are files the graph has never seen. Worse, they are
the *highest-leverage* files in the repo: a change to `agent-prompt.md` alters
every kid in every future iteration, and today that change can be made with no
node behind it — which is exactly the open loop **G6** exists to close, in the
one place where it costs the most.

What has to exist: a level-3 node per non-code surface, carrying the same
derived contract shape as a code node — what it takes, what it promises — so
`stitch.py --verify` reports drift on a prose file the same way it does on a
module. Prose has no signature to parse, so the contract has to come from
somewhere else; deciding what a `SKILL.md` node's contract *is* is the real work
here, not the scanning.

Note the reflexive case and do not skip it: **G1.3 and G1.4 are changes to
`agent-prompt.md` and `dispatch.py`.** Under G6.1 they should originate as node
versions, which means this sub-goal is on their critical path, not parallel to
it. If they land as direct engine edits, they are two more entries in the
evidence that the arrow still points the wrong way.

Falsifier: run `stitch.py --verify` after editing one word of `SKILL.md`. If it
reports no drift, the surface is not covered.
