---
id: experiment:a00-0a03abce-8cd564
mint_id: 0e3322e261d5417f9fd2d58b4c537b59
type: experiment
parents:
  - hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell
next_edges: []
confidence: 0.9
edited_by: a00-fcfa57a8
evidence_runs:
  - experiment:a00-0a03abce-8cd564
loop: hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: b612fffab844c92b
season: 2
title: Three live residues closed in test_mem_cap_tasks_max.py
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0a03abce-8cd564

DH.464 corrective slice 2, `extensions/agi/tests/test_mem_cap_tasks_max.py`
only. 0 production lines (`git diff --numstat` over non-test paths: empty).
mem_cap.py untouched; `_DEFAULT_MEMORY_CAP` left as landed.

| # | residue | order taken | result |
|---|---------|-------------|--------|
| 1 | FALSE SEAM CLAIM at :12 and :196 | **(b) DROP the stub** | closed |
| 2 | env shadows the cell in the named row | row sets the CELL, env left UNSET | closed |
| 3 | live-config row narrower than the resolver | helper parses like the resolver | closed |

## 1 — the stub, deleted (not re-described)

The old sentence was a fiction and I checked it before acting: no production
site calls `mem_cap.subprocess.run` for a spawn.

```
dispatch.py:2851  subprocess.Popen(mem_cap.wrap_argv(spawn_args, _mem_cap, cfg), ...)
heal.py:3775      proc = subprocess.Popen(heal_argv, ...)
workflow.py:1807  cmd = mem_cap.wrap_argv(cmd, cap, cfg)   # Popen
                  subprocess.run(cmd, ...)                 # only when the
                                                            # Popen seam is INJECTED
grep -n subprocess extensions/agi/bin/mem_cap.py
  12:import subprocess
 234/237/263/270: the PROBE (_PROBE_UNIT), not a spawn
```

I took order (b), not (a): keeping a recorder around a seam nothing passes is
the residue wearing a longer docstring. `_stub_spawn`, `_Recorded` and both
`calls == []` assertions are gone; the row is now
`test_the_wrapped_argv_carries_both_bounds` and asserts only on argv. The
module docstring now states the real shape (three callers, the Popen/run
split, the probe's own `run`) instead of naming a seam that does not exist.

## 2 — the cell carries the bound

The named row set `AGI_TASKS_MAX=8` AND `_cfg(tasks_max=8)`. `resolve_tasks_max`
reads the env FIRST (`mem_cap.py:81-82`), so the cell was unfalsifiable there.
Measured, env unset, a cell of 99999:

```
$ env -u AGI_TASKS_MAX python3 -c "... wrap_argv(['x'],'512M',{'spawn':{'tasks_max':99999}})"
['--property=TasksMax=99999']     # the cell is the only source now
```

The `setenv` is deleted; the autouse `_no_ambient_tasks_max` fixture (which
clears the var) does the work. The OTHER direction stays proven and is now
named in the file: `test_an_unreadable_cell_falls_back_and_never_uncaps`
sets `AGI_TASKS_MAX=5` over a cell of 8 and expects 5.

## 3 — the live cell is parsed the way the resolver parses it

Old helper: `assert isinstance(val, int)` -> the owner's own edit `150` ->
`"150"` reddened the file with "cell is not an int" while production was fine
(`resolve_tasks_max` does `int(str(raw).strip())`, `mem_cap.py:84`). The helper
now does the resolver's own parse, then asserts `resolve_tasks_max(cfg) IS
parsed` and that it is >= 1, raising a NAMED AssertionError for a cell that
does not parse or parses below 1. Probe (scratch, not in the suite):

```
$ python3 -m pytest $SESS/test_probe_cell_parse.py -q
3 passed
  owner edit 150 -> "150"  : green, value 150
  cell "abc"               : AssertionError "does not parse as a number"  (not KeyError)
  cell "0"                 : AssertionError "below 1"
```

## The named tests

```
$ timeout 600 python3 -m pytest extensions/agi/tests/test_mem_cap_tasks_max.py \
    extensions/agi/tests/test_launch_memory_cap.py extensions/agi/tests/test_dispatch.py \
    extensions/agi/tests/test_heal_mem_cap.py -q --basetemp=/tmp/bt-a00-0a03abce
164 passed, 8 warnings in 9.44s
```

## What is NOT closed

The DH.453 NAMED COVERAGE RESIDUE stands and is still named in the file: the
real systemd scope REFUSING a fan-out past TasksMax is exercised nowhere in
the fast suite. This file asserts the bound ON THE ARGV; the three production
callers apply it. Unchanged by this round.

## Agent Notes
All three DH.464 residues closed in test_mem_cap_tasks_max.py: dropped the fake subprocess.run stub (no production site passes it), env no longer shadows the cell (cell 99999 now yields TasksMax=99999), live-cell helper parses like resolve_tasks_max so 150 -> "150" stays green; 164 named tests pass, 0 production lines

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review DH.464 round 2 (agent a00-fcfa57a8). MY probes, not this round's suite: .agi/sessions/iter-DH.464/a00-fcfa57a8/probe2.py and probe6_hermetic.py.

(1) WHAT THE INSTRUCTION SAID. Three residues, quoted from the director's orders I forwarded verbatim this time, after round 1's brief pointed at an ORDERS block that was not in it and the kid derived five different ones: (1) the false seam claim at test_mem_cap_tasks_max.py:12 and :196 -- subprocess.run is NOT the one seam every mem_cap spawn passes; dispatch.py and heal.py spawn via subprocess.Popen, only workflow.py keeps a subprocess.run -- so name the three sites or DROP the stub; (2) the fan-out row must set the CELL with AGI_TASKS_MAX explicitly unset, plus a second row proving the env wins; (3) the live-config row must accept exactly what the resolver accepts, so an owner edit 150 -> "150" stays green. FILE SCOPE: that test file only, 0 production lines, mem_cap.py out of scope.

(2) WHAT THE MACHINE ACTUALLY DOES. The diff 0a5c61906..4b8177f4d is 67 added / 65 removed in extensions/agi/tests/test_mem_cap_tasks_max.py and NOTHING else: `git diff --numstat` over extensions/agi/bin/ is empty, so the 0-production-line clause is true of the bytes and not only of the prose. Residue 1 is closed by DELETION, option (b): _stub_spawn, _Recorded and every `calls == []` assertion are gone, and the docstring now says the opposite of what it used to -- there is no spawn seam inside mem_cap, the cap is applied by the CALLER -- naming dispatch.py, heal.py and workflow.py and the Popen/run split. I checked the replacement for truth rather than for tone: mem_cap.py reaches subprocess.run at exactly two lines, :234 (`systemctl --user reset-failed <_PROBE_UNIT>.scope`) and :263 (the systemd-run probe itself), and both are the probe, neither a spawn of the wrapped argv; dispatch.py has 1 wrap_argv site and hands it to subprocess.Popen, heal.py has 2 sites and Popen, workflow.py wraps and reaches run only in its injected-seam branch. Residue 2 is closed: the row is now test_the_wrapped_argv_carries_both_bounds, the setenv line is gone, and my P3 shows the cell alone carrying the bound (cell 8 -> TasksMax=8, cell 77 -> TasksMax=77 with the env unset) while the env still outranks a DIFFERENT cell (env 8 over cell 77 -> 8), which is the second behaviour the orders asked to keep named and the file now says so in both rows. Residue 3 is closed: _live_spawn_tasks_max parses the cell the way the resolver does, int(str(raw).strip()), and P1 walks it -- "150" and " 150 " now pass and resolve to 150, while "abc", "0x96", None, True, [], {"a": 1}, 0 and -4 each fail with a message NAMING spawn.tasks_max and the exact reason, never a KeyError. P4/P5: the standing claim is untouched by two rounds of edits to this file -- live 150 -> 150, values.memcap.tasks_max=7 injected -> still 150, every bad cell -> 96, {"spawn": 42} and friends -> 96/4G through the one _spawn_block guard. P6 is the probe with teeth in the direction that matters: the whole file under sys.addaudithook over subprocess.Popen / os.fork / os.posix_spawn / os.system gives 12 passed and ZERO real-launch events, and the neighbourhood suites the orders named give 152 passed under timeout 600 with --basetemp under /tmp.

(3) THE NEAR MISS. The stub could have been KEPT and merely re-described -- the docstring rewritten to say "the seam mem_cap would use if it spawned" -- which satisfies the words of the order and leaves a monkeypatch of a name no production site reaches, plus a `calls == []` assertion that a reader cannot tell apart from the self-referential one it replaced. What defeats it is that the seam was deleted and the argv assertions kept, so the file now contains claims about wrap_argv only. The second near miss is narrower and I name it rather than hide it: the replacement docstring says the only subprocess.run calls inside mem_cap are the probe's, and that is true in substance -- :234 is the probe unit's `reset-failed` cleanup, not a spawn -- but a reader who greps two call sites against one sentence has to check :234 by hand. A half-sentence naming the systemctl cleanup would remove that. Not a falsifier; a caveat.

(4) IF I DEVIATED FROM A STANDING RULE. None, and I record why the two rounds came out differently rather than crediting the second kid with more care: in round 1 I forwarded a POINTER to the director's orders ("they are in the ORDERS below") and the orders text lives in my own system prompt, so the block below did not exist. The kid then read the bytes, found five real defects, closed all five, and reported proved -- and still missed three of the five I meant. In round 2 the orders text was IN the file, and three of three landed. The difference was the transmission, not the round.

probes: P1 gate (cell "150"/" 150 " accepted and equal to the resolver; "abc"/"0x96"/None/True/[]/{} fail by name, 0/-4 by name, no KeyError) / P2 wire (no "one seam" / "every mem_cap spawn" CLAIM left -- only the quoted-and-corrected history at :16; _stub_spawn gone; mem_cap.py's only subprocess.run sites are :234 and :263, both the probe; dispatch/heal use Popen, workflow uses run only in its injected-seam branch) / P3 gate (cell alone carries TasksMax=8 and 77 with the env unset; env=8 still outranks cell=77; the only setenv left is the deliberate env-over-cell row) / P4 auth (env 5 over cell 8 -> 5; env unset cell 8 -> 8; no cell -> 96) / P5 wire (live 150, old key inert, bad cells -> 96, non-dict spawn -> 96/4G, no production diff this round) / P6 wire (whole file under a Popen/fork/posix_spawn/system audit hook: 12 passed, zero real launches; test_launch_memory_cap + test_dispatch + test_heal_mem_cap: 152 passed, timeout 600). ACCEPTED, verdict left proved: the corrective slice is now closed in full -- R1 and R4 by a00-0990792d, R2, R3 and R5 by this round, each with a parent probe behind it.
<!-- THOUGHT:END -->

Parent review DH.464 (a00-fcfa57a8): ACCEPTED, verdict left proved. All three corrective residues closed in the bytes and by parent probes P1-P6: the false ONE-seam sentence replaced by a true account naming dispatch.py/heal.py/workflow.py with the stub DELETED, the fan-out row now carries the bound from the cell with the env unset (env-over-cell still proven in the other row), and the live helper parses the cell exactly as resolve_tasks_max does so an owner edit to "150" stays green. 0 production lines, 12 rows hermetic under a Popen/fork audit hook, 152 neighbourhood tests green. One caveat named in the THOUGHT: the replacement docstring accounts for one subprocess.run site in mem_cap and there are two, the second being the probe unit reset-failed cleanup.
