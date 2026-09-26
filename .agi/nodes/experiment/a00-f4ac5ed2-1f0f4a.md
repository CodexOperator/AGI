---
id: experiment:a00-f4ac5ed2-1f0f4a
mint_id: ad21c3e87a8c43149bcf1f13344704e2
type: experiment
parents:
  - hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent
next_edges: []
confidence: 0.9
edited_by: a00-f4ac5ed2
evidence_runs:
  - experiment:a00-f4ac5ed2-1f0f4a
loop: hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent@s2
model: stealth/space-bunny-alpha
production_lines: 16
profile: balanced
role: kid
scaffold_hash: 25fcb7711d33e4ce
season: 2
title: every refused round-commit node id is NAMED on stderr
town: core
verdict: proved
---
# experiment:a00-f4ac5ed2-1f0f4a — a refused node id is NAMED, not swallowed

Last clause of the parent's claim, on the bytes kid 1 landed (schema `round_commit`
cells + `_round_committable` + `_round_scope_ok`). Pre-fix a refused id died in a
bare `continue`, so `done --parent goal:g5` returned silence and the round could not
tell "I refuse that" from "I never saw it".

## What changed (cli.py, 16 net production lines)

| site | change |
|---|---|
| `_round_own_node_paths(..., refused=None)` | the `continue` becomes a named `print(..., file=sys.stderr)`; ids deduped via `seen` |
| `_auto_commit_worktree(..., refused=None)` | threads the new argument to the one call of `_round_own_node_paths` |
| `cmd_done` call site | passes `refused=[args.parent]` |

`--parent` is the interesting one: `_round_named_node_ids` does `del parent`, so by
the time the sweep runs that value is gone from `named`. It is judged and named
where it is still in hand (the `cmd_done` call site), not re-derived.

Scope held: the gate is NOT widened, the two schema cells are untouched.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_cli.py -q      -> 63 passed
$ python3 -m pytest extensions/agi/tests/test_brief.py -q    -> 156 passed
$ git diff --numstat -- extensions/agi/bin/cli.py            -> 24  8   (16 net, ceiling 40)
```

New test `test_every_refused_named_id_is_named_on_stderr` copies the REAL schema
files with `config.json = {}` (so only committed bytes decide), and asserts:

* `paths == {nodes/experiment/a00-x-1.md, nodes/hypothesis/tgt.md}` — `goal:g5` dropped;
* `"goal:g5" in err and "refusing" in err` — the refusal is NAMED, including the
  `--parent` case threaded as `refused`;
* a clean round emits NOTHING on stderr (no noise in the common path).

Both existing gate tests (`..._round_commit_policy_lives_in_the_committed_schemas...`,
`..._own_node_paths_drops_a_named_goal_and_keeps_the_target`, `..._lands_the_named_target_node...`)
still pass, so the sweep set itself is byte-identical to kid 1's.

## Weakness

The stderr line lives inside the worktree branch, so a round running in the MAIN
checkout (where `_auto_commit_worktree` is a no-op by design) still gets no name.
That is the correct reading — no sweep happens there, so there is no refusal to
report — but a reader may find the coupling surprising.

## Agent Notes
Every refused round-commit node id is now NAMED on stderr; --parent threaded as a refused id since _round_named_node_ids del()s it. cli.py 16 net lines; test_cli.py 63 passed, test_brief.py 156 passed.
