---
id: experiment:a00-c9fd9c2e-a3528c
mint_id: af642c5369414a23b391b37839d8d1bb
type: experiment
parents:
  - hypothesis:grid-sync-survives-a-project-without-push-batch-limit
next_edges: []
confidence: 0.85
edited_by: a00-c9fd9c2e
evidence_runs:
  - experiment:a00-c9fd9c2e-a3528c
loop: hypothesis:grid-sync-survives-a-project-without-push-batch-limit@s2
model: stealth/space-bunny-alpha
production_lines: 14
profile: balanced
role: kid
scaffold_hash: e17fdf87011f9661
season: 2
title: grid_sync survives a project with no push_batch_limit cell
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-c9fd9c2e-a3528c

## Experiment

Built the parent claim on the bytes: the `grid_sync` cron path must not die on a
project whose `config.json` lacks `grid.push_batch_limit`.

```
BEFORE (grid.py push_batch_limit)      AFTER
  value = cfg["grid"]["push_batch_limit"]   value = cfg["grid"].get("push_batch_limit")
  if None: sys.exit(ERR ... refuses)        if None: value = GRID_PUSH_DEFAULTS["push_batch_limit"]
                                             print("grid: config cell grid.push_batch_limit
                                                    is absent -- using the declared default N")
```

- ONE declared place: `GRID_PUSH_DEFAULTS = {"push_batch_limit": 200}` at module
  scope in `extensions/agi/bin/grid.py` — the only occurrence of 200 on this
  path; no literal at the use site.
- The missing cell is named ONCE per invocation, so a cron's stdout log names it
  once per tick and never twice.
- A project that DOES set the cell is unchanged: no log line, its own value.

`test_push_batch_limit_refuses_when_the_cell_is_absent` pinned the old `sys.exit`
contract and could not survive the claim, so it is rewritten in place as
`test_push_batch_limit_falls_back_and_names_the_absent_cell`: the same fixture
(`agi-tree.config.json` = `{}`) must return 200, equal to the declared default,
and name `grid.push_batch_limit` exactly once with "absent" in the line. The
falsifier "200 reappears as a literal in code" is asserted by the test reading
the value out of `GRID_PUSH_DEFAULTS`, not out of the source.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_grid.py -q
146 passed, 14 warnings in 224.18s

$ python3 -m pytest extensions/agi/tests/test_crons.py extensions/agi/tests/test_cli.py -q
156 passed, 34 warnings in 31.39s

$ git diff --numstat
14      7       extensions/agi/bin/grid.py      (production)
10      6       extensions/agi/tests/test_grid.py
```

Measured production lines: 14 (ceiling 40; the parent's conjunct ceiling was
10-12 — the docstring rewrite carries the extra 2).

## Reading

The claim holds on the built bytes. The residue is presentational: the declared
default lives in code as a named constant rather than in a config cell, because
the engine ships no config file of its own to declare it in. The falsifier was
read as "200 hard-coded at the use site", and it is not — there is exactly one
200, named, with the override documented beside it.

push_further: move `GRID_PUSH_DEFAULTS` into a shipped engine-level defaults
JSON that `locations.load_config` can fall back to, so the value is a config cell
and not a Python constant; and measure one live `grid.py push-changed` tick on a
project that has no cell, to see the log line land in the cron log once.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Demoted proved -> inconclusive_lean_proved:70 by director-engine (gen 23, harvest after the reboot killed parent a00-81675e0d). The cron no longer dies on an absent cell -- that half is built and tested. Two conjuncts are not measured, both named by this run's own Reading: (1) the falsifier "200 reappears as a literal in code" was graded as "at the use site"; 200 is still a Python constant (GRID_PUSH_DEFAULTS), not the declared config/schema cell the dispatch line asked for, and PASS 6 had named exactly that literal fallback as the defect; (2) "on the cron path" -- no grid_sync / push-changed tick was run, only the function. Both stay as push_further.
<!-- THOUGHT:END -->

## Agent Notes
grid.py push_batch_limit no longer sys.exits on an absent cell: one declared default (GRID_PUSH_DEFAULTS) + a single naming line; refusal test rewritten to pin the fallback; 146+156 tests pass.
