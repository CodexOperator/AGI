---
id: goal:g4.6
mint_id: 3b187e5eec3246059655916829807d8f
type: goal
parents:
  - goal:g4
next_edges:
  - hypothesis:a00-9bae6ee8-52d7f5
confidence: 1.0
edited_by: season.py
goal_id: G4.6
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: complete
tags:
  - goal
  - subgoal
thought_session: season
title: "G4.6: One spawn path; a harness is an adapter named in config"
---
**There is no single place where an agent is spawned, and that is the real
shortfall `goal:g4.3` has been masking.** Today `dispatch.py` builds a pi
command inline (`pi_model_args`, `_build_pi_args`, a hardcoded `--runtime pi`
in `zoom_command`, `_scrubbed_env`), `zoom.py` branches its completion
contract on two string literals, and the config carries two sibling blocks —
`agent_dispatch` and `cc_dispatch` — that mean overlapping things in different
shapes, one of which is read by no code at all. Adding a third harness means
touching all three files and inventing a third config shape.

**A harness must be a named entry in config with an adapter behind it**, and
`dispatch.py` must not know which one it is spawning. The config names every
spawn path and links it to its keys, its models per tier, and its harness
binary. Minimal branching is allowed, and only inside a `*-adapter.py`.

## What has to exist

1. **One spawn function.** Target selection, the spawn gate, scaffolding,
   manifest recording, wiring and the evidence gate are shared and stay
   shared. Only command construction varies.
2. **A harness is config.** Each declares its adapter, its binary, its
   provider, its env keys, and a model **per tier**. Adding a harness is a
   config entry plus one adapter file — never an edit to `dispatch.py`.
3. **Tier is a parameter on that path, not a second path.** `parent` and
   `kid` differ in model and brief. This is `goal:g4`'s per-tier model
   assignment finally having somewhere to land: `cc_dispatch.kid_model` and
   `parent_model` have existed for weeks and are read by **no code**.
4. **Completion is harness-agnostic, and it is not process inspection.**
   Today "done" means `cli.py done` writing `agent.json` while `heal.py` polls
   a pid. Both are the pi process model wearing a general name — a Claude Code
   kid has no pid to poll, and a kid that finished its node but died before its
   report looks identical to one that never started. **The finish signal should
   be the graph changing**: the scaffolded node acquiring real content is the
   event, observable by any harness, and observable the same way from the
   spawned agent's own point of view. `cli.py done` becomes one way to announce
   a completion, never the definition of one.

## Where this sits, and the drift it corrects

`goal:g4.3` says "anywhere the engine invokes `pi`, allow invoking Claude Code
instead — a runtime flag, not a parallel code path." That was written when the
Claude Code adaptation was a **stop-gap**, and it inherits the stop-gap's
frame: two named runtimes, reaching parity with each other. Under that frame
"unify" means "make the second one work like the first", which is why the CC
half has stayed configuration with nothing behind it while the pi half grew.

The frame is wrong, not the goal. There should be **one** spawn path and *N*
harnesses hanging off it, with pi and Claude Code as the first two entries and
neither privileged. `goal:g4.3`'s invariant — a runtime flag, not a parallel
code path — is exactly right and is inherited here verbatim; what changes is
that the flag selects an adapter from config rather than choosing between two
hardcoded branches.

## Falsifier

Add a third harness with **no edit to `dispatch.py`** — one config entry and
one `*-adapter.py`. Then spawn a parent and a kid on it. If either requires a
change outside those two files, the seam is in the wrong place. Second half,
and the one that decides whether this is real: `grep` the shared path for
branches keyed on harness name and find **zero** outside the adapter lookup.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Marked complete in the 2026-09-01 sweep, with all five clauses landed and
tested rather than argued.

The spawn half landed 2026-09-01 (`2857a7f64`): `bin/adapters/` with a
resolved-once harness, `harnesses`/`spawn` in config, tier selecting the model,
falsifiers 1-3 as tests. Clause 5 — completion as a graph event — landed the
same day: `bin/completion.py`'s `is_complete(root, node_id)` is harness-blind
(ast-verified: no `pid`, no `agent.json`, no harness name), `post_wire` reads
verdict data from node frontmatter first, and `cmd_wire` admits an agent whose
node is complete regardless of what the process reported.

The evidence that mattered was not a test. The kid that WROTE `completion.py`
died on a provider 403 immediately after, was marked `failed`, and produced
`nodes updated: 0` — the exact loss this clause prevents, suffered by the change
that prevents it, on the first live try.

`heal.py` still polls pids and is deliberately left to `goal:g4.7`; post_wire
alone closes the loss, so heal's stamp no longer decides anything.
<!-- THOUGHT:END -->