---
id: experiment:a00-54fd547e-dt77-hold-proof
mint_id: b65d82ccf7064bd79c7e0a4b0867b1fa
type: experiment
parents:
  - hypothesis:a00-54fd547e-3edaff
next_edges: []
edited_by: a00-54fd547e
loop: goal:g7.31.1.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
season: 2
title: "DT.77 fake-driven proof of the durable tmux hold and dead-seat refusal"
town: core
probes:
  - {"conjunct": "no-real-tmux", "class": "gate", "cmd": "grep -nE '_REAL_RUN|real_tmux|needs_tmux|_probe_session|os.kill|SIGKILL|kill-session|kill-window' extensions/agi/tests/test_tmux_hold.py extensions/agi/tests/test_dispatch_tmux_hold.py", "expected": "no committed tmux session creation/kill and no signal to a pane process", "observed": "only two docstring mentions of the conftest guard; zero calls", "result": "held"}
  - {"conjunct": "fake-semantics", "class": "gate", "cmd": "pytest extensions/agi/tests/test_tmux_hold.py -q", "expected": "first spawn founds the named pane, remain-on-exit set before respawn, restart re-enters the SAME pane with created False, killed window recreates once with created True, child env rides respawn", "observed": "12 passed", "result": "held"}
  - {"conjunct": "dead-pane-rc", "class": "gate", "cmd": "pytest test_tmux_hold.py::test_heldproc_reports_a_dead_pane_as_a_nonzero_death -q", "expected": "HeldProc.poll returns 1 for a dead pane, None for a live one", "observed": "passed", "result": "held"}
  - {"conjunct": "dead-seat-not-running", "class": "gate", "cmd": "pytest test_dispatch_tmux_hold.py::test_dead_held_seat_is_never_registered_running -q", "expected": "dispatch refuses rc 6 with a named issue line; no agent record status running", "observed": "passed", "result": "held"}
  - {"conjunct": "transient-retry", "class": "gate", "cmd": "pytest test_dispatch_tmux_hold.py::test_transient_death_of_a_held_seat_triggers_the_bounded_retry -q", "expected": "catalogue+520 death re-spawns under the SAME log, writes attempt 2, registers the live re-spawned seat", "observed": "passed", "result": "held"}
  - {"conjunct": "first-spawn-seam", "class": "gate", "cmd": "pytest test_dispatch_tmux_hold.py::test_first_spawn_through_dispatch_founds_the_pane_and_threads_env -q", "expected": "dispatch._open_round's hold branch founds the named pane with the adapter's real hold_harness and threads DT_SEAM_PROBE=held", "observed": "passed", "result": "held"}
  - {"conjunct": "suite-green", "class": "gate", "cmd": "pytest test_tmux_hold.py test_dispatch_tmux_hold.py test_adapters.py test_grok_bot_adapter.py test_dispatch.py test_dispatch_transient_respawn.py test_conftest_guard.py -q", "expected": "all green", "observed": "213 passed", "result": "held"}
---
<!-- BODY:BEGIN -->
# experiment:a00-54fd547e-dt77-hold-proof

## Experiment

The run the DT.77 corrective order asked for: fix the three named defects in
the durable tmux pane hold and re-prove on the built bytes.

**Build.** `HeldProc.poll` now reports a nonzero rc (`1`) for a dead pane
process instead of `0`. `dispatch.py` resolves the adapter's `hold_harness`
once before `_open_round`, and after the startup-grace loop refuses a held
seat whose process has exited (`proc.returncode is not None`) with rc 6 and a
`_report_unregistered_scaffold` detail of "held pane process died"; the
transient-5xx branch above it is reached exactly as a direct `Popen` seat's
is. No `grok`/harness-name special case was added to `dispatch.py` or
`rotate.py`; the existing adapter-declared hold and pane identity are
untouched.

**Tests.** `test_tmux_hold.py` was rewritten to remove `_REAL_RUN`, the
`real_tmux` fixture, `needs_tmux`, `_probe_session`, and all four
`test_real_tmux_*` tests; their claims are re-expressed against `FakeTmux`,
which models a window-per-session, immutability of `#{pane_id}`,
`remain-on-exit` set before `respawn-pane`, and the append-only seat log.
`test_dispatch_tmux_hold.py` drives `dispatch.main` end to end (the seam
`_open_round` actually runs in) with a `grok-bot` config harness that
declares no tmux cell, so the hold is resolved from the adapter's real
`HOLD_PANE`/`hold_harness`; `_alive` and `_GRACE_SLEEP` are faked and tmux
calls go to the fake.

## What Is FAKED and What Is Real

- FAKED: every tmux call; the pane process's liveness (`_alive`); the grace
  sleeps (`_GRACE_SLEEP`).
- REAL: the dispatch hold branch, grace loop, transient classifier and
  registration/refusal; `adapters.load`/`resolve`; the grok adapter's
  `hold_harness`/`child_env`/`build_command`; the exact command bytes
  `tmux_hold._cmd` hands to `respawn-pane`.
- NOT PROVEN HERE: that a real tmux server preserves a pane across a real
  process death. The fake encodes that semantics, and the corrective order
  forbids a real server in the committed suite. This is a modelling
  assumption, stated plainly rather than smuggled in as a shell-out.

## Probes

All probes are `gate` class and ran as named. See frontmatter for the
command/expected/observed record. Production change measured with
`git diff --numstat` over the given production paths: 5/1
`ADAPTERS/tmux_hold.py` + 28/8 `dispatch.py` = **33 added lines** against a
40-line ceiling.