---
id: experiment:a00-f8cba76b-e1e98d
mint_id: 9f3e74eaf23547e28fed62d92308cfe3
type: experiment
parents:
  - hypothesis:l4-the-fake-systemctl-records-the-env-it-receives
next_edges: []
confidence: 0.95
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-f8cba76b-e1e98d
loop: hypothesis:l4-the-fake-systemctl-records-the-env-it-receives@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c1d3ff17ba3212b4
season: 2
title: fake systemctl records the env it is invoked with, so deleting the bus-env merge turns a test red
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f8cba76b-e1e98d

## Experiment

Made `test_crons.py`'s `fake_systemctl` record the ENV it is invoked with,
so the L4.129 bus-env merge (`env=merged` in `_apply_systemctl`, crons.py:486)
can no longer be deleted unnoticed.

**Fixture change** — the fake now ALSO appends one env line per call to
`tmp_path/systemctl.env`, same order as the argv log:
`XDG_RUNTIME_DIR=<v>|DBUS_SESSION_BUS_ADDRESS=<v>`. argv recording
(`systemctl.calls`) is untouched byte-for-byte, so no existing argv-position
test shifted.

**Assertions added:**
- `test_wanted_unit_runs_systemctl_with_env_when_bus_reachable` now asserts the
  fallback DBUS address reached the subprocess: env line contains
  `DBUS_SESSION_BUS_ADDRESS=unix:path={tmp}/runtime/bus`, and one env line per
  argv call.
- `test_fake_records_caller_bus_unchanged_when_present` — caller has its own
  DBUS_SESSION_BUS_ADDRESS: the fake records the CALLER's value, never the
  fallback (caller-origin vs fallback-origin distinguished).

**Baseline → green:** 62 passed before; 63 passed after.

**FALSIFIER run (proof the test is load-bearing):** temporarily deleted
`env=merged` from `subprocess.run` in crons.py, ran the suite →
`test_wanted_unit_runs_systemctl_with_env_when_bus_reachable` went RED:
`assert 'DBUS_SESSION_BUS_ADDRESS=unix:path=...' in '...|DBUS_SESSION_BUS_ADDRESS='`
(1 failed, 62 passed). Restored crons.py; verified BYTE-IDENTICAL against the
pre-mutation copy. crons.py was never left edited — TESTS ONLY as specified.

## Evidence

Mutation run (deleting `env=merged` only, then restored):
```
FAILED test_crons.py::test_wanted_unit_runs_systemctl_with_env_when_bus_reachable
E AssertionError: fallback bus address must reach the subprocess via the env merge
E  assert 'DBUS_SESSION_BUS_ADDRESS=unix:path=/tmp/.../runtime/bus'
E         in 'XDG_RUNTIME_DIR=/tmp/.../runtime|DBUS_SESSION_BUS_ADDRESS='
1 failed, 62 passed
```
Post-restore, full file: `63 passed`. crons.py confirmed BYTE-IDENTICAL to the
pre-mutation copy via `cmp`.

## Agent Notes
Made fake_systemctl record the env per call (systemctl.env); added fallback + caller-origin assertions; mutation (delete env=merged) turns a test RED; restored crons.py byte-identical. 62->63 green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-63c8fe68, L4.148). Instruction quoted from the target: "the fake records the environment it was invoked with ... the mutation (delete env=merged) turns at least one test RED (paste the mutation run, then restore byte-identical). crons.py byte-identical." Mechanism, not appearance: I re-ran it myself, not from the report. Baseline `python3 -m pytest extensions/agi/tests/test_crons.py -q` -> 63 passed. Then deleted `env=merged` at crons.py:486 (the only call site; `git diff HEAD --quiet -- crons.py` = clean before) and re-ran: 1 failed, 62 passed, `test_wanted_unit_runs_systemctl_with_env_when_bus_reachable` RED on the new assert at test_crons.py:926 with the exact fallback-address mismatch. Restored from a pre-mutation copy: `git diff HEAD --quiet -- extensions/agi/bin/crons.py` exits 0, BYTE_IDENTICAL. Near miss: a fake that records env by reading the parent process env (e.g. `echo $DBUS_SESSION_BUS_ADDRESS`) would go green on the mutation too, because it would print the caller env again; this fixture appends `XDG_RUNTIME_DIR=..|DBUS_SESSION_BUS_ADDRESS=..` from inside the child, so it captures the env `subprocess.run(env=merged)` actually passed, which is the only thing that can move. The caller-origin test (`test_fake_records_caller_bus_unchanged_when_present`) closes the other escape: the fallback can neither be injected when a caller bus exists nor silently absent when it does not. Deviation from no standing rule: none; crons.py is untouched and the new test count matches (62->63).
<!-- THOUGHT:END -->

**2026-09-11T06:30:29Z director review at harvest (sanctuary-director gen XI, L4.148).** Reproduced the mutation in the round worktree: crons.py:486 `env=merged` → `env=None` → `python3 -m pytest extensions/agi/tests/test_crons.py -q` → 1 failed / 62 passed; restored from a copy (git status clean = byte-identical) → 63 passed. Verdict `proved` stands; merged into seat/sanctuary-director@s2 for merge-up 29. Next in the crons queue: g15-15 (`hypothesis:l4-crons-apply-records-one-state-line-when-nothing-changed`), then g15-17.
