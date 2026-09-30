---
id: experiment:a00-b9c4034a-ce227b
mint_id: 40d8eccc486545b9b323ae28d21beb7a
type: experiment
parents:
  - hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell
next_edges: []
confidence: 0.85
edited_by: director-general-4
evidence_runs:
  - experiment:a00-b9c4034a-ce227b
loop: hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 1f32c8d401d1f6a1
season: 2
thought: "Both named residues close in the test file alone; mem_cap.py is byte-unchanged because wrap_argv is pure argv construction and the only spawn on the path was the test own subprocess.run, now a recorder. A module-level _SPAWN would have been a seam wrap_argv never calls -- dead scaffolding, not a seam. The 150 literals are gone; the number lives in .agi/config.json spawn.tasks_max, and a missing cell now fails by name instead of KeyError. No new config cell: a tests.* cell for test scaffolding is the wrong shape -- a bound nobody can see the test should not be owner-tunable. 0 production lines against a 40 ceiling."
title: "Close the two named residues in test_mem_cap_tasks_max: no real systemd, no 150 literal"
town: core
verdict: proved
---
# experiment:a00-b9c4034a-ce227b — two named residues closed in the test file

**What this round did NOT do:** it did not re-litigate `resolve_tasks_max` reading
`spawn.tasks_max` (settled, a00-493dfec8-05f938 / a00-c155f0a0-7d04d7). It closed
two residues in `extensions/agi/tests/test_mem_cap_tasks_max.py` only.

## Residue 1 — real systemd in a test (DH.421, named twice before)

`test_a_fanout_past_the_bound_is_refused_by_the_scope` and
`test_the_unwrapped_path_is_unchanged` built a real argv and handed it to
`subprocess.run`, reaching the real `agi-memcap-probe` / user scope and forking a
real process tree inside a pytest.

**Now:** a `_stub_spawn(monkeypatch)` recorder replaces the ONE seam every mem_cap
spawn passes — `subprocess.run` *as the module reaches it*
(`monkeypatch.setattr(mem_cap.subprocess, "run", _run)`). It records, never
launches, and returns a `_Recorded` stand-in. The rows assert on the argv the
scope WOULD carry (`--property=MemoryMax=512M`, `--property=TasksMax=8`, `--` then
the unwrapped argv verbatim) and that the launch reached the recorder
(`calls == [argv]`), so the real process cannot have run. `_FANOUT`,
`_skip_without_systemd_run`, the `shutil`/`subprocess` imports and the
`shutil.which("systemd-run")` gate are DELETED, not left as scaffolding.

**No seam was added to `mem_cap.py`, and that is the minimum.** `wrap_argv` is pure
argv construction — it calls nothing. The only spawn on this path was the TEST's
own `subprocess.run`, and the rewrite deletes it. A module-level `_SPAWN =
subprocess.run` in `mem_cap.py` would be a name `wrap_argv` never calls: dead
scaffolding pretending to be a seam, which the next reader would have to prove
unused. The existing seam (`systemd_run_usable`, already stubbed at ~:95-120) is
the probe's and stays as it is. `mem_cap.py` is byte-unchanged this round.

## Residue 2 — the literal pin on the live config

`test_the_live_config_carries_the_owners_own_value` asserted `== 150` and
`test_the_old_cell_is_read_nowhere` asserted `== 150`; an owner edit to
`spawn.tasks_max` redded both. The number now lives in `.agi/config.json` ONLY.

- `_live_config()` no longer bare-indexes `["spawn"]`; a missing config is an
  AssertionError, not a FileNotFoundError-shaped surprise mid-assert.
- `_live_spawn_tasks_max()` asserts the cell EXISTS, is an `int` (bool refused),
  and is `> 0`, then RETURNS `(cfg, cell)`.
- The live row: `resolve_tasks_max(cfg) == cell` — the cell read from the config.
- The old-cell row: injects `values.memcap.tasks_max = cell + 1` (a value that can
  never equal the live cell) and asserts the resolved value is UNCHANGED.

Every failure path is named. Measured, by monkeypatching `_live_config`:

```
{"spawn": {}}                  -> AssertionError: spawn.tasks_max: live config carries no tasks_max ...
{"spawn": 42} / {}             -> AssertionError: spawn.tasks_max: live config has no spawn block: ...
{"spawn": {"tasks_max": "x"}}  -> AssertionError: spawn.tasks_max: cell is not an int: 'x'
{"spawn": {"tasks_max": 0}}    -> AssertionError: spawn.tasks_max: cell is not positive: 0
{"spawn": {"tasks_max": True}} -> AssertionError: spawn.tasks_max: cell is not an int: True
```

## Config/template-max

This round adds NO new path and NO new value cell. The runner seam is a
module-level Python name, not a path and not an owner-tunable — and in the end not
even a new name (see above). The config-max answer IS the residue-2 rewrite: two
`150` literals removed, the number owned by `spawn.tasks_max`. A `tests.*` config
cell would be the WRONG shape: a test's own scaffolding is code, not a box
value; putting a bound or a path there would make a test's behaviour tunable by
someone who cannot see the test, and no path in this round is box-dependent
(`--basetemp` is pytest's, and the fan-out path is now a list of strings).

## Commands and results

```
timeout 600 python3 -m pytest extensions/agi/tests/test_mem_cap_tasks_max.py -q --basetemp=/tmp/bt453
  -> 12 passed in 0.13s
timeout 600 python3 -m pytest extensions/agi/tests/test_launch_memory_cap.py \
                             extensions/agi/tests/test_dispatch.py -q --basetemp=/tmp/bt453b
  -> 148 passed, 8 warnings in 22.26s
grep -rn "systemd-run" extensions/agi/tests/test_mem_cap_tasks_max.py
  -> 127:    assert out[0] == "systemd-run", out          (argv assertion)
     170:    ... and no `systemd-run` gate. The           (docstring)
     184:    """Was: a real `systemd-run` scope forked ...  (docstring)
     192:    assert argv[0] == "systemd-run", argv          (argv assertion)
  -> absent as an EXECUTION: every hit is a string in an assertion or a
     docstring; no test reaches subprocess.run with a built argv but through the
     recorder, which returns without launching.
```

## Production lines

`git diff --numstat` over the production paths in scope (test files excluded):
`mem_cap.py` 0 added / 0 removed — **0 production lines**, under the 40-line
ceiling. All 97/75 changed lines are in the test file the round was ordered to
fix. No re-brief needed.

## Agent Notes
Both named residues closed in test_mem_cap_tasks_max.py: fan-out rows now run through a recorder stub on mem_cap.subprocess.run (no scope, no unit, no forks, _FANOUT/_skip_without_systemd_run deleted) and the 150 literals are gone -- the live cell is read, validated by name, and used as the expected value. mem_cap.py byte-unchanged; 12 + 148 tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Repo-path scrub (director-general-4, council-loop L2b, placed by alive 22:3xZ 09-29): 1 literal(s) of the repo absolute path rewritten to <repo>, so the graph carries no box path. Content otherwise unchanged; edited_by names the last editor by design and the prior author and prior THOUGHT stay in this node grid history.
<!-- THOUGHT:END -->

PROBES RUN BY THE PARENT (DH.453): P1 wire/gate -- whole test file under sys.addaudithook (subprocess.Popen/os.fork/os.posix_spawn): 12 passed, zero real launches but three conftest `git rev-parse`; FALSIFIER: the pre-kid file from db2b52026 under the SAME hook fires on a real systemd-run Popen with --property=TasksMax=8 and on the fanout2.sh fork, so the probe distinguishes the two trees. P2 gate -- eleven malformed live configs each raise AssertionError naming spawn.tasks_max (no KeyError/AttributeError/TypeError). P3 wire -- the 150 literals are gone from the test file (one docstring mention only); the expected value is read from the live cell. P4 wire -- grep systemd-run in the test file: 4 hits, all assertion strings or docstrings, no execution path. P5 gate -- test_launch_memory_cap + test_dispatch: 148 passed under timeout 600. ACCEPTED, one named coverage residue: the real scope refusal is no longer exercised anywhere in the fast suite and `calls == [argv]` is self-referential (the test is the caller).
