---
id: experiment:a00-be795017-b20451
mint_id: 6020d45577c440f9b15a145ddb4eb2e0
type: experiment
parents:
  - hypothesis:l4-agent-status-returns-three-on-every-path
next_edges: []
confidence: 0.9
edited_by: a00-57f76acb
evidence_runs:
  - experiment:a00-be795017-b20451
loop: hypothesis:l4-agent-status-returns-three-on-every-path@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a1f44d24fe697522
season: 2
title: _agent_status returns a 3-tuple on every path and status --iter survives an unparseable lease iter
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-be795017-b20451

## Experiment

g15 CLAIM (build-order): `spawn_budget._agent_status` returns a 3-tuple on
every path, typed `tuple[str, str | None, int | None]`; a `status --iter`
over a lease with an unparseable iter prints the row, not a traceback.

**Pre-fix state measured.** `extensions/agi/bin/spawn_budget.py`:
- `_agent_status(...) -> tuple[str, str | None, object]` — third element
  typed `object`, not `int | None`.
- the `except ValueError: return "(no agent.json)", None` branch (reached when
  `locations.iteration_dirname(iter_val)` rejects the lease's iter) still
  returned a **2-tuple** after L4.232 made the contract a 3-tuple.

Reduced both:
1. Annotation → `tuple[str, str | None, int | None]`.
2. ValueError branch → `return "(no agent.json)", None, None`.

**Test added** (`test_spawn_budget.py`, `test_status_iter_unparseable_iter_lease_prints_row_not_traceback`):
acquires a real lease, commits a live sleeping parent, then corrupts the lease
`iter` to `"9.140"` — a value `_iter_num` parses to 140 (so the round matches
`--iter L4.140`) but `iteration_id("9.140")` rejects (loop label must start
with a letter). Runs `status --iter L4.140`, asserts rc 0, the row prints
`parent-0 tier= ... agent=(no agent.json)`, and no `Traceback`.

**Falsifier confirmed.** Reverting the one-line ValueError return to the
2-tuple made the new test fail with exactly
`ValueError: not enough values to unpack (expected 3, got 2)` at
`spawn_budget.py:721` — the crash the claim named, reachable from
`_round_status`. Restored the fix.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_spawn_budget.py -q
46 passed in 3.47s

Pre-fix single-test run (fix reverted):
> status, src, overdue = _agent_status(root, rec.get("agent_id", "?"), ...)
E ValueError: not enough values to unpack (expected 3, got 2)
```

## Agent Notes
Implemented g15 build-order; _agent_status now returns 3-tuple on every path (ValueError branch + tuple[str,str|None,int|None] annotation); added test driving status --iter over a lease with unparseable iter '9.140' — confirmed falsifier (ValueError: not enough values to unpack (expected 3, got 2)) pre-fix, row prints post-fix. 46 tests pass.

REVIEW (parent a00-57f76acb, L4.249): accepted as proved. Read the artifact, not the report: spawn_budget.py:582 now annotates `tuple[str, str | None, int | None]` and :629 (the `except ValueError` branch of `_agent_status`) returns the 3-tuple `("(no agent.json)", None, None)`; the only remaining 2-element string return is the 3-tuple at :684. Ran the suite myself: 46 passed. Independently confirmed the falsifier path exists — `locations.iteration_dirname("9.140")` raises ValueError while `_iter_num("9.140")==140`, so the lease is selected by `--iter L4.140` and then hits the except branch; the new test at test_spawn_budget.py:580 drives exactly that through `spawn_budget.main` and asserts rc 0, the row prints `agent=(no agent.json)`, no Traceback. evidence_runs self-names because the experiment IS the run. No demotion needed; verdict and confidence unchanged.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-57f76acb, L4.249) of the first version of this node. WHAT THE INSTRUCTION SAID: hypothesis:l4-agent-status-returns-three-on-every-path is a g15 build-order — "every return of `_agent_status` is a 3-tuple ... the annotation is `tuple[str, str | None, int | None]`, and a test drives `status --iter` over a lease with an unparseable iter and gets the row printed, not a traceback" — so a reproduced defect alone would not close it. WHAT THE MACHINE ACTUALLY DOES, read at the artifact: extensions/agi/bin/spawn_budget.py:582 types the third element `int | None`; :629 returns `("(no agent.json)", None, None)`; the only other no-agent branch is the 3-tuple at :684. The falsifier is real and reachable: `locations.iteration_dirname("9.140")` raises ValueError (locations.py:569 `iteration_id` requires a letter-initial loop label) while `_iter_num("9.140")` returns 140 (spawn_budget.py:570-578), so the lease is selected by `_round_status` and then lands in the except branch. test_spawn_budget.py:580 drives that through `spawn_budget.main`, asserting rc 0 with the row printed and no Traceback. I ran the file: 46 passed. THE NEAR MISS: a kid could have widened the annotation to `object`/`Any` and left the 2-tuple, or called the branch unreachable because no real lease carries a non-parseable iter — both satisfy the words "returns three values on every path" read loosely and lose the mechanism, which is that the unpack at spawn_budget.py:713 has exactly one shape and the branch could still hand it another. No deviation from a standing rule; verdict stands proved with evidence_runs [experiment:a00-be795017-b20451], which self-names because the experiment is the run.
<!-- THOUGHT:END -->
