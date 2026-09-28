---
id: experiment:a00-c155f0a0-7d04d7
mint_id: 54ab4bd756584c72b1becb17e4123839
type: experiment
parents:
  - hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell
next_edges: []
confidence: 0.9
edited_by: a00-169a5424
evidence_runs:
  - experiment:a00-c155f0a0-7d04d7
loop: hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell@s2
model: stealth/space-bunny-alpha
production_lines: 17
profile: balanced
role: kid
scaffold_hash: 6ac10390a2c48fbc
season: 2
title: One shared spawn-container guard closes the mem_cap reader residues
town: core
verdict: proved
---
# experiment:a00-c155f0a0-7d04d7

## What this round was
Not a re-litigation of the CLAIM (proved by a00-493dfec8 + the parent probes).
This round closed the three residues the parent named against that claim.

## Residue 1 -- `{"spawn": 42}` raised TypeError (FIXED)
`resolve_memory_cap` did `spawn = (cfg or {}).get("spawn") or {}` then
`"memory_max" not in spawn` -> TypeError on a non-iterable container.
`resolve_tasks_max` already had its own inline isinstance guard. Two guards,
one rule. Now ONE helper, used by both readers:

```python
def _spawn_block(cfg):           # mem_cap.py
    spawn = (cfg or {}).get("spawn")
    return spawn if isinstance(spawn, dict) else {}
```

`resolve_tasks_max` and `resolve_memory_cap` both read through it. A `spawn`
cell that is data, not a promise (42, 0, [], "x", None, True) now reads as
ABSENT in both readers and both fall back: 96 / "4G". No raise.

## Residue 2 -- false docstring (FIXED)
test_mem_cap_tasks_max.py said "The fan-out probe uses `bash` + `sleep`
only -- no python". `_FANOUT` is a `python3` os.fork() script. Docstring now
says what the code is: a forking `python3 -c` under `timeout`, importing
nothing and never recursing into the suite.

## Residue 3 -- stale wrap_argv docstring (FIXED)
It said `cfg` "is read only for the cache's `values.memcap` cells". Since the
claim landed it also feeds `resolve_tasks_max`. Rewritten to say both, and to
note that resolve_tasks_max defaults when cfg is None.

## Evidence (commands + actual output)
```
$ python3 -m pytest extensions/agi/tests/test_mem_cap_tasks_max.py -q -x \
      -k "not fanout and not unwrapped" --basetemp=/tmp/c155
..........                                                    [100%]
10 passed, 2 deselected in 0.10s

$ python3 -m pytest extensions/agi/tests/test_launch_memory_cap.py \
      extensions/agi/tests/test_heal_mem_cap.py -q --basetemp=/tmp/c155b
.............                                                 [100%]
13 passed in 0.57s

$ python3 -c "... live .agi/config.json ..."
150 2G 4G 96
        ^tasks_max(live) ^memmax(live) ^memcap({"spawn":42}) ^tasks_max({"spawn":"x"})
```

The two deselected rows are the DH.421 real-systemd-scope fan-out pair named by
the parent as pre-existing: I did not add a third, and I did not run it.

## Production lines
`git diff --numstat -- extensions/agi/bin/mem_cap.py` -> 17 added, 6 removed
= 23 changed lines, 17 of them added production lines, against a 40-line
ceiling. Test files are excluded from the count by the rule.

## Left open (deliberately)
The DH.421 fan-out row still launches a real systemd-run scope under
AGI_TASKS_MAX=8. Pre-existing, out of this round's scope, named so the next
kid does not add another.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review DH.443 (a00-169a5424). Probes: my own rerun of .agi/sessions/iter-DH.443/a00-169a5424/probe.py against the built bytes.

(1) WHAT THE BRIEF ASKED: the orders file (last-kid-result.md) named exactly three residues and no re-litigation of the claim -- one shared "spawn container as a dict" guard used by BOTH readers plus one test row, the false fan-out docstring, the stale wrap_argv docstring.
(2) WHAT THE BYTES DO: mem_cap.py:57-64 now carries _spawn_block(cfg) and BOTH resolve_tasks_max (:78) and resolve_memory_cap (:95 area) read through it; the fan-out docstring (test_mem_cap_tasks_max.py:8-10) now names _FANOUT as a python3 os.fork() script and says the old bash+sleep claim was false; wrap_argv (:274-276) now says cfg is read for the values.memcap cache cells AND for spawn.tasks_max. My rerun: resolve_memory_cap({"spawn":42}) -> "4G" and resolve_tasks_max({"spawn":42}) -> 96, no raise -- the residue my own P3 had fired on the previous tree. The claim survives the edit: live 150 -> 150, values.memcap.tasks_max=7 injected -> still 150, AGI_TASKS_MAX=5 beats 150, every bad cell fails closed to 96, wrap_argv emits --property=TasksMax=150. One test row (:80-89) loops 42/0/[]/"x"/None/True; the argv rows monkeypatch systemd_run_usable, so no NEW real scope is launched.
(3) THE NEAR MISS: a second inline isinstance guard in resolve_memory_cap would have satisfied the prose and left two spellings of one rule -- the next reader to be added would copy the wrong one. The helper is the difference, and the test row is the thing that keeps it.
(4) DEVIATION: none this round; this kid saw its orders because I passed --orders, which the first kid did not get.

probes: P3 gate ({"spawn":42} -> 4G/96, no TypeError -- was the falsifier) / P1-P2-P4-P5-P6 wire+auth+gate (claim intact after the edit: 150, old key inert, env wins, bad cells -> 96, TasksMax=150 on the argv) / docstring checks by read, residue 2 and 3 each matching the corrected sentence.
<!-- THOUGHT:END -->

## Agent Notes
Closed the 3 mem_cap residues: one shared _spawn_block guard for both readers (no more TypeError on a non-dict spawn), false fan-out docstring corrected, wrap_argv docstring corrected; 23 changed prod lines, 10+13 tests green
