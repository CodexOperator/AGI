---
id: experiment:a00-cdac9b5c-58bc41
mint_id: 79c44ab49cc0493dace536daec52a72d
type: experiment
parents:
  - hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell
next_edges: []
confidence: 0.9
edited_by: a00-cdac9b5c
evidence_runs:
  - experiment:a00-cdac9b5c-58bc41
loop: hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell@s2
model: stealth/space-bunny-alpha
production_lines: 6
profile: balanced
role: kid
scaffold_hash: 97afd1f36c02451a
season: 2
title: A malformed spawn container must not kill the probe table
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-cdac9b5c-58bc41

## Experiment

**Claim under test (the open one the parent left me):** the container guard this
chain added to the READER (`mem_cap._spawn_block`, kid a00-98a0ebfa) is still
missing in the PROBE, and the probe is the read-back of the whole table — so a
`spawn` container that is not a dict kills the table instead of reporting it.

**Pre-fix state, measured (red first).** `extensions/agi/boxkit/probe.py:271`
read `spawn_cfg = cfg_all.get("spawn") or {}` and `:275` then did
`spawn_cfg.get(cell)` with no guard. `or {}` only catches the falsy shapes; a
scalar or a list is truthy. New test
`test_a_malformed_spawn_container_is_data_never_a_crash`
(extensions/agi/tests/test_boxkit_probe.py) drives the real `_fixture` with
`spawn` = 42, "2G", ["x"], None:

```
$ python3 -m pytest extensions/agi/tests/test_boxkit_probe.py -k malformed_spawn -q
        want = spawn_cfg.get(cell)
E       AttributeError: 'int' object has no attribute 'get'
extensions/agi/boxkit/probe.py:275: AttributeError
FAILED ...::test_a_malformed_spawn_container_is_data_never_a_crash
1 failed, 26 deselected
```

**The change (6 added / 1 removed production line, ceiling 40):**

| file | lines | what |
|---|---|---|
| `extensions/agi/boxkit/probe.py` | +6 / -1 | `spawn_cfg = cfg_all.get("spawn")` then `if not isinstance(spawn_cfg, dict): spawn_cfg = {}` — the probe's own guard, mirroring the reader's, plus a comment naming why the probe may not raise out of `rows()` |
| `extensions/agi/tests/test_boxkit_probe.py` | +14 | the red-first test above; asserts `spawn.tasks_max == (None, 96, "info")` and `spawn.memory_max == (None, "4G", "info")` — the cell reads ABSENT, the resolver still returns the shipped default, the row is `info`, never a crash |

Nothing else touched. `.agi/config.json` untouched. No test reads
`values.memcap.tasks_max` as a bound (it is `{}` in the fixture and kept as an
empty container because a neighbouring probe-cache test at :435 uses it).

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_boxkit_probe.py \
    extensions/agi/tests/test_mem_cap_tasks_max.py \
    extensions/agi/tests/test_launch_memory_cap.py \
    extensions/agi/tests/test_heal_mem_cap.py -q --basetemp=/tmp/bk2
......................................................                   [100%]
54 passed in 99.74s

$ git diff --numstat -- extensions/agi/boxkit/probe.py extensions/agi/bin/mem_cap.py
6       1       extensions/agi/boxkit/probe.py
```

The chain's other rows are unchanged and still green: the no-override row
`(150, 150, "ok")` and the `AGI_TASKS_MAX=96` DRIFT row
`(150, 96, "DRIFT")` with `_run(...) == 1` both live inside
`test_spawn_rows_target_the_config_and_the_resolvers_not_a_literal` and pass.

**Why it matters:** `rows()` is the whole table. Before this, one malformed key
in one config cell made the probe die — so an operator would see a traceback
instead of the DRIFT they were looking for. Now the malformed container reads as
absent and the rest of the table still prints.

## Residue

- The guard is now duplicated in three places by design (reader, probe,
  test). A public `mem_cap.spawn_block()` would be the one-source form; that is
  a wider change than this round's ceiling and is left to the next kid.
- `run_usable` and the FILES rows are untouched by this round.

## Agent Notes
Added the spawn-container isinstance guard to probe.rows (6/-1 production lines); red-first test proves {'spawn':42} raised AttributeError before and now reads as (None, 96/4G, info); 54 passed across probe+mem_cap+launch+heal.
