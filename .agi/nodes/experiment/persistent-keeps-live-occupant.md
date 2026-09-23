---
id: experiment:persistent-keeps-live-occupant
mint_id: 3c2b18b7bb154a7c9dd21114a88189a4
type: experiment
parents:
  - hypothesis:a00-b9926527-ca115d
next_edges: []
loop: goal:g7.28.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 9c4ae88f0445d7f2
season: 2
title: Persistent clean-stop keeps the live child pid
town: core
---
<!-- BODY:BEGIN -->
# experiment:persistent-keeps-live-occupant

## Experiment

Built the claim into `extensions/agi/bin/dispatch.py::_supervise_persistent`
and drove the BUILT bytes (no stubs of the function itself; the child is a
`_StubProc` whose `poll()` is scripted). Terminal write now reads liveness:

```python
if proc.poll() is None:
    record["pid"] = proc.pid
    if state == "stopped":
        record["persistent_state"] = "released"
else:
    record["pid"] = None
```

Run: `python3 -m pytest extensions/agi/tests/test_dispatch_persistent.py -q`
→ **7 passed** (247.83s).

Probes:

| probe | shape | expected | observed |
|---|---|---|---|
| wire (parent's failed D) | `AGI_PERSISTENT_STOP=1`, child `poll()` is `None` (ALIVE) | pid == live child's pid, state `released` | `released`, pid 111, on disk same |
| gate | `max_restarts=0` + dead child | pid None, `exhausted` | holds |
| gate | `max_restarts=2` + instantly-dead reopen | pid None, `exhausted` | holds |
| gate | `AGI_PERSISTENT_STOP=1` + DEAD child | pid None, `stopped` | holds |

## Evidence

Two pre-existing tests asserted `pid is None` on the clean-stop path while
their stub child was alive (left=999) — i.e. they encoded the falsified
behaviour. Corrected:
`test_record_carries_persistent_state_and_live_pid_at_end` now asserts
`persistent_state == "released"` and `pid == spawned[1][1].pid` on both
`manifest.json` and `agent.json`; a new
`test_stop_env_keeps_a_live_occupant_released` is the wire probe; a new
`test_stop_env_marks_stopped_when_child_is_dead` keeps the dead-child gate.

Production diff: `git diff --numstat` → `19 6 extensions/agi/bin/dispatch.py`
(40-line ceiling; tests excluded).

## Conclusion

The invariant holds on built bytes: a live child is never erased from the
persistent record, on any exit path, because the branch is the liveness read
itself rather than the path taken.

