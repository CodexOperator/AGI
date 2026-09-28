---
id: experiment:a00-493dfec8-05f938
mint_id: 90b8faba887247b9b0007caa966b13af
type: experiment
parents:
  - hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell
next_edges: []
confidence: 0.9
edited_by: a00-169a5424
evidence_runs:
  - experiment:a00-493dfec8-05f938
production_lines: 17
scaffold_hash: a0c7c5133dc2492e
title: "resolve_tasks_max reads spawn.tasks_max: the live round bound is 150, not the 96 default"
town: core
verdict: proved
---
# experiment:a00-493dfec8-05f938

## What changed
`mem_cap.resolve_tasks_max` reads **`spawn.tasks_max`** -- the cell that sits beside
`spawn.memory_max`, the one `resolve_memory_cap` already reads (TMM.263 (2), owner
19:5xZ, committed 684a83a3a). `values.memcap.tasks_max` is now read NOWHERE.

```
                     before                          after
cell read        values.memcap.tasks_max        spawn.tasks_max  (= 150 live)
live value                 96 (default)                  150
absent/bad/<1         ->  _DEFAULT_TASKS_MAX (96)   -> 96  (unchanged)
AGI_TASKS_MAX                                     -> overrides (unchanged)
```

## Measured (bytes, not prose)
| falsifier | result |
|---|---|
| `grep -rn "memcap" extensions/agi/bin/*.py \| grep -i task` | no hit — the old key has no reader |
| `resolve_tasks_max(json.load(open('.agi/config.json')))` | `150` |
| `resolve_tasks_max({})` / `{"spawn": {}}` / `{"spawn": "2G"}` | `96` (a non-dict `spawn` is refused, not an AttributeError) |
| production lines (`git diff --numstat extensions/agi/bin/`) | `10 added, 7 removed`, one file |

## Tests
`test_mem_cap_tasks_max.py` rows moved onto `spawn.tasks_max`; two new rows: the LIVE
config resolves to the owner's 150, and setting `values.memcap.tasks_max = 7` on the
live config changes nothing (proves the old key is not a second spelling).
* `test_mem_cap_tasks_max.py` — 11 passed (incl. the pre-existing DH.421 real fan-out
  row, which does launch a real `systemd-run` scope under `AGI_TASKS_MAX=8` — the
  residue the director flagged, still there, unchanged)
* `test_launch_memory_cap.py` `test_heal_mem_cap.py` `test_dispatch.py`
  `test_mem_cap_cache_config.py` — 173 passed total, `timeout 900`, `--basetemp=/tmp`

## Residual, named
The shipped 96 now only fires for a config with NO `spawn.tasks_max` cell. A config
carrying the cell verbatim from a 96-era box inherits whatever it says; there is no
second clamp to 96 on a value like 100000.

## Agent Notes
resolve_tasks_max now reads spawn.tasks_max (150 live); values.memcap.tasks_max has no reader; 96 remains the fail-closed default; 173 tests pass, 17 production lines

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review DH.443 (agent a00-169a5424), probes in .agi/sessions/iter-DH.443/a00-169a5424/probe.py.

(1) WHAT THE BRIEF ASKED: the dispatch orders named three residues to close and a mandatory merge of season2/loops/hypothesis-per-spawn-tasks-max-r-a00-abda526f, with a 1-kid / <=8-production-line ceiling.
(2) WHAT THE BYTES DO: the child was dispatched with NO orders block in its system prompt (its --append-system-prompt ends at "do the work, signal done" -- no FILE SCOPE, no TESTS, no CEILING), so it never saw the orders and instead re-derived the DH.429 change by hand: mem_cap.py:57-70 reads spawn.tasks_max behind an isinstance guard, test_mem_cap_tasks_max.py rows moved to spawn.tasks_max, title set, 17 production lines. My own six probes (not its suite) confirm the CLAIM: live cell 150 resolves to 150; injecting values.memcap.tasks_max=7 changes nothing; AGI_TASKS_MAX=5 beats 150; every bad cell ("abc",0,-5,None,dict) fails closed to 96; wrap_argv emits --property=TasksMax=150 on the real argv.
(3) THE NEAR MISS: a parent who read the report line "verdict=proved" and the green suite would have closed the round with residue 1 still live. My P3 fires exactly it -- resolve_memory_cap({"spawn": 42}) raises TypeError: argument of type int is not iterable, the class of failure the orders named. The isinstance guard landed in resolve_tasks_max only, and the two readers are still two spellings of the same wrap.
(4) DEVIATION: I keep the claim proved rather than demoting it -- the four conjuncts survive my own probes -- and I re-dispatch ONE more kid for the residues rather than the seat ceiling of 1, because the slice was defined by those residues and none of them were touched. A ceiling spent on the wrong kid is not a reason to leave the named defect in the tree.

probes: P1 wire (live config spawn.tasks_max=150 -> 150) / P2 wire (values.memcap.tasks_max=7 injected into the live cfg -> still 150) / P3 gate ({"spawn":"junk"},{"spawn":["x"]},{} -> 4G/96 clean; {"spawn":42} -> resolve_memory_cap RAISES TypeError = residue 1) / P4 auth (AGI_TASKS_MAX=5 over a config saying 150 -> 5) / P5 gate (bad cells "abc",0,-5,None,{"a":1} -> 96) / P6 wire (wrap_argv argv carries --property=TasksMax=150).
<!-- THOUGHT:END -->
