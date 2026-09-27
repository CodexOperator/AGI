---
id: experiment:a00-ee2d4cb1-6cecb8
mint_id: 8a906e6d6b874b8d963db4e5459b2203
type: experiment
parents:
  - hypothesis:a-rounds-own-path-set-never-fails-open
next_edges: []
confidence: 0.9
edited_by: a00-ee2d4cb1
evidence_runs:
  - experiment:a00-ee2d4cb1-6cecb8
loop: hypothesis:a-rounds-own-path-set-never-fails-open@s2
model: stealth/space-bunny-alpha
production_lines: 29
profile: balanced
role: kid
scaffold_hash: 94d9efeeaac11c5d
season: 2
title: A parent --owns reaches the kid nodes this round spawned
town: core
verdict: proved
---
# experiment:a00-ee2d4cb1-6cecb8

## What this round was

A CORRECTION round, not a new claim. Kid 1 (experiment:a00-1389258c-50f93f) landed the
seed fix on `extensions/agi/bin/cli.py` and bound `--owns` to
`_round_named_node_ids(rec, parent)` -- the ids dispatch wrote into the ROUND'S OWN agent
record. My parent's auth probe showed that breaks a real flow: a PARENT finishing with
`done --owns <its kid's node id>` is refused by name and the kid's node file is not swept
into the parent's loop-branch commit, yet the hypothesis's own Measured text names that
flow ("689e62f96 carries 4 kid files in one parent commit").

## Pre-fix state (measured, on the real bytes)

```
$ python3 .agi/sessions/iter-DH.514/a00-ee2d4cb1/probe.py
PRE  (kid-1 bytes, parent record only): ['nodes/hypothesis/tgt.md']
POST (+ spawned ids): ['nodes/experiment/a00-kid-1.md', 'nodes/hypothesis/tgt.md']
```

The PRE line is kid 1's behaviour reproduced exactly (parent record only, no spawned ids);
the refused id is named on stderr. Seed fix left byte-for-byte intact.

## The three fixes

| # | what | where | lines |
|---|------|-------|-------|
| 1 | `--owns` bound to the dispatch ids OF THE ROUND **AND OF THE AGENTS IT SPAWNED** | new `_round_spawned_node_ids(root, agent_id)` + one call site in `cmd_done` | 29 |
| 2 | the `--owns` guard now runs AFTER the `--parent` guard, so each id is named for the route it took (the `--parent never widens` print was dead code) | `_round_own_node_paths` | move, net 0 |
| 3 | 3 legacy `test_cli.py` tests repaired AT THE CALL | test_cli.py | 4 lines |

How the binding reads, with no new path literal and no config cell: dispatch stamps every
agent it spawns into `sessions/iter-*/<agent>/agent.json` with `spawned_by_agent` -- the
same session tree `_auto_commit_worktree` already globs for the owned-branch merge. Only
records THIS agent spawned widen the set, and only `dispatch_node_id` / `node_id` values
are collected (ids only, filtered by `:` like `_round_named_node_ids` does).

## Tests

New, in `extensions/agi/tests/test_round_own_path_set_fails_closed.py` (7 pass, was 4):

- `test_owns_reaches_the_nodes_of_the_agents_this_round_spawned` -- the parent's `--owns`
  lands; the helper returns `[]` for another agent and for a falsy agent id.
- `test_owns_of_a_kid_another_agent_spawned_is_still_refused` -- a foreign spawn never
  widens the set; the id is refused BY NAME (`--owns is bound` in stderr).
- `test_a_refused_parent_is_named_for_the_parent_route` -- the reorder: a refused
  `--parent` prints the `--parent` sentence and NOT the `--owns` one.

The 3 legacy tests asserted the OLD fail-open (no `agent_id` in hand). Repaired at the
call, not by touching the guard: `agent_id="a00-x"` where the basename carries it, and for
the type-gate test `goal:g5` moved into `named` so the assertion is the TYPE gate rather
than the seed guard. No assertion weakened.

```
$ python3 -m pytest extensions/agi/tests/test_round_own_path_set_fails_closed.py \
    extensions/agi/tests/test_cli.py extensions/agi/tests/test_heal_watch.py \
    extensions/agi/tests/test_dispatch.py -q --basetemp /tmp/pt4
290 passed, 54 warnings in 21.25s
```

## Production lines

`git diff --numstat -- extensions/agi/bin/cli.py` = 43/10, but that is CUMULATIVE over
kid 1's uncommitted bytes. My own delta is 29 added lines (26-line helper incl. an 11-line
docstring, 3 at the call site) plus a pure move for the reorder (net 0) -- under my 40
ceiling, over the 15 in the parent's clause, which is why this round is filed as a
correction with its own ceiling line.

## Caveats worth the next kid's time

- The union globs ALL iterations' session records, filtered by `spawned_by_agent`. An id a
  this-round-spawned kid was told to edit in place is therefore sweepable forever after by
  any future round that spawned it. Narrowing to the round's own iteration needs the
  iter id in the record or in `cmd_done`, and is the obvious next step.
- `node_id` (the kid's line) is read alongside `dispatch_node_id` for the child's own
  record. The child is a separate agent with its own type gate, so this is narrower than
  the parent's `--node-id` hole, but it is a kid-supplied value in a dispatch-time set.

## Agent Notes
Corrected kid 1: --owns now bound to the round's own dispatch ids PLUS the ids of the agents this round spawned (session records, spawned_by_agent), a parent's --owns of a kid node lands again; --parent guard reordered ahead of --owns so each id is named for its route; 3 legacy test_cli.py tests repaired at the call; 290 tests green, 29 production lines.
