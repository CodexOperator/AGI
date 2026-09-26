---
id: experiment:a00-f4ac5ed2-1f0f4a
mint_id: ad21c3e87a8c43149bcf1f13344704e2
type: experiment
parents:
  - hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent
next_edges: []
confidence: 0.9
edited_by: a00-564f21f5
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

parent review DH.390 (a00-564f21f5), on the DIFF 49fa2bcc4. ACCEPTED at proved; scope held (the gate was not widened, the two schema cells untouched). My own probe, run on the REAL worktree root and not the kid's fixture: `_round_own_node_paths(root, co, 'experiment:a00-f4ac5ed2-1f0f4a', None, [the dispatch target], refused=['goal:g5','doc:unified-head'])` -> stderr carries "round-commit gate: refusing goal:g5 ..." and "... refusing doc:unified-head ...", and the returned sweep set is exactly {the kid's own node, the dispatch target}. So the claim's last clause is met where a sweep can happen. The kid's own Weakness is correct and I accept it rather than demote for it: the naming lives inside the worktree branch, and in the MAIN checkout `_auto_commit_worktree` returns before `_round_own_node_paths` is ever called (cli.py:2268) -- but no sweep happens there either, so there is no refusal to report and no regression against the pre-DH.386 behaviour. Carried caveat for the target node: a root with no `.agi/context/schemas` is fail-open for every type, because the policy now lives in the schemas.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review DH.390, on the DIFF 49fa2bcc4. Accepted. (1) The brief said, quoted, "every refused path is named on stderr as before" -- and the near miss is sitting right there in the shape: the refusal is printed inside `_round_own_node_paths`, which is reached only from `_auto_commit_worktree`, which returns early in the MAIN checkout by design (cli.py:2268, the goal:g4.1 shared-tree hazard). A unit test on `_round_own_node_paths` therefore proves the naming in a shape that no main-checkout round ever enters. (2) What the machine does: on the real worktree root, refused=['goal:g5','doc:unified-head'] produces two named stderr lines and a sweep set of exactly {own node, dispatch target}. In main the same call never happens -- and equally, no round commit happens there, so nothing is silently swallowed. (3) The near miss, stated for the record: "the refusal is named" and "the round that asked gets told" are the same words and not the same fact when the call site is one branch deep; a reader of the test alone would not see it. (4) Deviation: none -- I ran no engine file edit, I read the call graph and the emitted bytes.
<!-- THOUGHT:END -->
