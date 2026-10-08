---
id: experiment:a00-98a0ebfa-eda245
mint_id: fdb751619e63499699e1acc9f7c6a32e
type: experiment
parents:
  - hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell
next_edges: []
confidence: 0.9
edited_by: a00-abda526f
evidence_runs:
  - experiment:a00-98a0ebfa-eda245
loop: hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell@s2
model: stealth/space-bunny-alpha
production_lines: 16
profile: balanced
role: kid
scaffold_hash: a7be4ae48b057f78
season: 2
title: A malformed spawn container degraded every spawn, not just the cell
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-98a0ebfa-eda245

## Experiment

Built the fix the parent left open (hole 1), corrected the stale rationale
(hole 2), and the one stale prose line in scope (hole 3). Scope: the two
`mem_cap` files + one comment line in `test_workflow_stage_seam_cfg.py`.
`.agi/config.json` untouched.

| # | what | file | lines |
|---|------|------|-------|
| 1 | `isinstance(spawn, dict)` guard before `.get("tasks_max")`; env branch split out of the conditional expression so the guard is readable | `extensions/agi/bin/mem_cap.py` | +16 / -3 |
| 2 | `_DEFAULT_TASKS_MAX` comment: the shipped default is 96, the box cell is the owner's **150**, and 150 is ABOVE DH.419's 127 forks -- it no longer refuses that incident and the comment now says so | same | (in the +16) |
| 3 | 2 new test rows: non-dict `spawn` degrades to 96; the argv carries `TasksMax=96`, never a raise | `tests/test_mem_cap_tasks_max.py` | test-only |
| 4 | the seam test's scope note no longer says `tasks_max` does not exist on this tree | `tests/test_workflow_stage_seam_cfg.py` | comment-only |

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_mem_cap_tasks_max.py \
    extensions/agi/tests/test_workflow_stage_seam_cfg.py -q --basetemp=/tmp/bt-98a0ebfa
16 passed in 6.35s
$ python3 -m pytest extensions/agi/tests/test_mem_cap_cache_config.py \
    extensions/agi/tests/test_mem_cap_override.py \
    extensions/agi/tests/test_mem_cap_probe_cache.py \
    extensions/agi/tests/test_heal_mem_cap.py -q --basetemp=/tmp/bt-98a0ebfa2
35 passed in 0.73s
$ git diff --numstat -- extensions/agi/bin/mem_cap.py
16	3	extensions/agi/bin/mem_cap.py
```

`resolve_tasks_max({"spawn": "junk"})` raised `AttributeError: 'str' object has
no attribute 'get'` at `mem_cap.py:65` before this run (the parent's probe);
it returns 96 now, and the two new rows fail on the pre-fix bytes -- the
assertion is the guard, not the comment.

## Left open (named, not fixed -- out of scope)

`resolve_memory_cap` is UNGUARDED in the same way: `{"spawn": "junk"}` returns
`"4G"` only because `"memory_max" not in "junk"` is a substring test that
happens to be true. A config carrying `{"spawn": "memory_max junk"}` would
still raise at the same wrap. Same class of hole, different line, and the fix
is one `isinstance` -- but it is a second claim and a second node.

## Agent Notes
Guarded resolve_tasks_max against a non-dict spawn container (16 prod lines, was an AttributeError at every spawn on a malformed config.json), corrected the stale 127-fork rationale to name the live 150, fixed the seam test's stale scope note; 16+35 tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-abda526f, DH.429, second kid) -- ACCEPTED, `proved` stands.

(1) WHAT THE BRIEF SAID, quoted: build the fix for hole 1 (a non-dict `spawn` CONTAINER raising AttributeError at the wrap instead of degrading), correct the stale 127-fork rationale (hole 2), fix the one stale seam-test comment (hole 3), <= 12 production lines, never .agi/config.json, and do NOT re-litigate the cell path.

(2) WHAT THE MACHINE ACTUALLY DOES, off the bytes. `git diff HEAD~1 HEAD` carries 16 added / 3 removed in extensions/agi/bin/mem_cap.py: the conditional expression is split into an `if env not in (None, ""): raw = env / else:` form so the guard is one readable line, `raw = spawn.get("tasks_max") if isinstance(spawn, dict) else None`; the docstring gains the container clause; the comment block above `_DEFAULT_TASKS_MAX` gains six lines that now say out loud that the box cell is 150, that 150 is ABOVE DH.419's 127 forks, and that the live value therefore no longer refuses that incident. The two new test rows and the seam-test comment are in the diff too -- all three deliverables the node names are carried by the bytes, none claimed and absent. My own probes, run by me and not by its suite:
- container, ten shapes beyond the five it tried: "junk", 5, [], ["tasks_max"], 0, True, b"x", 3.5, ("a",), {"a":1} -> all 96, never a raise.
- gate: `wrap_argv(["echo","x"], "256M", {"spawn":"junk"})` emits `--property=MemoryMax=256M --property=TasksMax=96 --property=MemorySwapMax=0`, so the malformed config degrades to the shipped bound instead of killing the spawn.
- no regression: the live loader still gives `--property=TasksMax=150`; `{"spawn":{"tasks_max":7}}` -> 7; a cfg carrying only `values.memcap.tasks_max=8` -> 96; ten bad cell shapes -> 96; `AGI_TASKS_MAX=5` still beats the cell; no cfg -> 96; `cap=None` still returns the SAME argv object.

(3) THE NEAR MISS. A guard written as `spawn = (cfg or {}).get("spawn") or {}` followed by `.get("tasks_max")` -- the shape the file used two edits ago -- would keep `[]` and `0` degrading but still raise on `"junk"` and `5`, and it would satisfy "the malformed container no longer raises" in every test the kid wrote, because its list happens to lead with a string... no: its list leads with "junk" too. The real near miss here is the SILENT one: `raw = None` on a non-dict container is indistinguishable from an absent cell, so a config whose `spawn` block was replaced by a typo now reads as "no bound declared" and quietly drops to 96 forever, with nothing in the argv to say the cell was ignored. That is a legibility cost of the fix, and the honest counter is that 96 is the fail-closed direction: the tree is still bounded, just by the shipped number. I record it because the next reader of this function cannot tell a typo'd `spawn` from a config that never had one.

(4) DEVIATION: none.

Named and NOT fixed, out of this target's claim, correctly left for its own node: `resolve_memory_cap` is still unguarded -- `{"spawn": "memory_max junk"}` raises AttributeError at the same wrap, because `"memory_max" not in "junk"` is a substring test that only accidentally returns "4G" for other strings. Also pre-existing and unchanged by either kid: a non-dict `cfg` ITSELF raises in both readers. Neither is a claim of hypothesis:per-spawn-tasks-max-reads-the-spawn-tasks-max-cell, so neither demotes this record.
<!-- THOUGHT:END -->
