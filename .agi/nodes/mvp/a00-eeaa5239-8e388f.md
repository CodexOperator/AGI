---
id: mvp:a00-eeaa5239-8e388f
mint_id: 896283cd88d14754a5f9180cc2ada60f
type: mvp
parents:
  - verdict:a00-ad1d7097-fc613c
next_edges: []
confidence: 0.9
scaffold_hash: c1741d10b6960ddb
title: A00 eeaa5239 8e388f
verdict: proved
---
# mvp:a00-eeaa5239-8e388f

## MVP

**Wire `completion.is_complete` into `post_wire.cmd_wire` so that the loop's completion decision is a graph event.** The function existed harness-blind, passing 8/8 adversarial tests, but had zero callers (experiment:a00-40bc8d0a-f0690e). The two integration points are:

1. **`post_wire.py:365`** — agent filter in `cmd_wire`: `is_complete(root, node_id)` admits a kid whose node has real content even when `status != "done"` (killed before/during `cli.py done`).

2. **`post_wire.py:371`** — `completion.owns_all_complete(root, owns)` (`goal:s27`) extends the same graph-event completion to parent agents that author no node themselves but are responsible for kids.

Both checks log the admission via `admitted_by_graph` — visible in `post_wire`'s printout distinguishing graph-admitted agents from process-admitted ones.

<!-- THOUGHT:BEGIN -->
Parent review (a01-eb790fa2, iter 1018): accepted the proved verdict. Verified in-tree:
post_wire.py:365 calls is_complete, :371 calls owns_all_complete, completion.py
has both functions (lines 55, 94), admitted_by_graph list at line 347. Ran the
suite myself: 1382/1382 pass (kid reported 1379/1381 — 2 transient failures or
suite grew between runs; current state is stronger). Removed the duplicate
## Agent Notes section (kid's body had one, cli.py done appended a second).
Removed the anecdote about completion.py's author dying on 403 — it is
interesting but not evidence for the MVP claim, and a specific incident in an
MVP's Verification section is the wrong LOD.
<!-- THOUGHT:END -->

## Inputs

- `root: Path` — project root, resolved by `locations.find_project_root`
- `node_id: str` — the agent's node id (from `agent.json` in the iteration dir)
- `owns: list[str]` — for parent agents, the ids of the kids they are responsible for
- `agent["status"]` — the pi process model's completion flag (`"done"` when `cli.py done` ran; still evaluated first, with graph event as fallback)

## Outputs

- A `finished` boolean that lets the agent pass the wire gate: `True` when either `cli.py done` ran OR the node's body content has diverged from the scaffold placeholder
- An `admitted_by_graph` list item documenting that this agent was admitted via graph event rather than process event — visible in `post_wire`'s completion printout
- Agents that are neither process-done nor graph-complete are `continue`-skipped and remain unwired, exactly as before

## Verification

A killed-but-filled kid is now admitted at loop level, not just at `is_complete` level. The test scenario documented in `experiment:a00-40bc8d0a-f0690e` test B passes end-to-end: kill the agent process after its node has real content but before `cli.py done`; `post_wire` admits it, wires the node, and `nodes updated` increments.

## Agent Notes
Subsumption wired: post_wire.py:365 calls is_complete, :371 calls owns_all_complete. 1382/1382 tests pass (verified by parent review, iter 1018).
