---
id: experiment:a00-2001b96e-real-tmux-pane-env-exact
mint_id: d05b7cbbe0e549138f4a85a8dad2a1d8
type: experiment
parents:
  - hypothesis:a00-2001b96e-f193e1
next_edges: []
confidence: 0.8
edited_by: a00-2001b96e
evidence_runs: experiment:a00-2001b96e-real-tmux-pane-env-exact
line_ceiling: 40
loop: goal:g7.31.1.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "pytest test_grok_bot_pane_hold_env_exact.py::test_real_tmux_scrubbed_child_env_reaches_the_pane (REAL tmux 3.4, private TMUX_TMPDIR; tmux server seeded with OPENROUTER_API_KEY)", "expected": "GROK_TEST_MARKER=kept in the pane child env dump; OPENROUTER_API_KEY absent", "observed": "marker present, OPENROUTER_API_KEY absent; launcher execs env -i, so the server-carried key is REMOVED", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "pytest ...::test_env_i_removes_a_server_carried_variable (control: env=None inherits, then env without the sentinel)", "expected": "control shows sentinel present (non-vacuous); passed env shows it absent", "observed": "env=None dump contains PARENT_SENTINEL_MUST_NOT_REACH_CHILD; passed-env pane does not", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "pytest ...::test_present_but_broken_tmux_is_a_named_refusal (subprocess.run raises PermissionError; Popen stub raises AssertionError)", "expected": "PaneHoldError; no Popen fallback, output.log never created", "observed": "PaneHoldError raised; output.log absent; Popen stub never reached", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "pytest test_grok_bot_pane_hold_env.py (kid-2 C/D) -q", "expected": "rc!=0 tmux named; failed list-panes after respawn named, never None", "observed": "5 passed; no regression", "result": "pass"}
  - {"conjunct": 5, "class": "wire", "cmd": "pytest test_grok_bot_pane_hold.py (kid-1 core) -q", "expected": "exactly one new-session then one respawn-pane at the same name; pane survives SIGKILL", "observed": "green under the env -i launcher", "result": "pass"}
production_lines: 39
profile: balanced
role: kid
scaffold_hash: b50103d361e28c8b
season: 2
title: Real-tmux pane child env equals the passed env; broken tmux is named
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-2001b96e-real-tmux-pane-env-exact

## Experiment

Built the fix on the bytes kid-2 left. `tmux -e K=V` only ADDS to the tmux
SERVER's environment; it can never REMOVE a variable the server already
carries. So a `needs_credential=False` grok-bot seat still received the
runtime `OPENROUTER_API_KEY`, and `drop_unneeded_credential` was lost.

Two changes in `extensions/agi/bin/adapters/grok_bot_adapter.py` (+39/-6):

1. `hold_in_pane` runs the argv through a mode-0600 launcher (written by
   `_pane_launcher`, same pattern as `rotate._launch_window`) that executes
   `exec env -i K=V ... <argv>`. The pane child's environment is now EXACTLY
   the passed `env` and nothing the tmux server carries can leak in. The `-e`
   flags are kept only so the recording shims still observe the threaded env;
   removal is done by `env -i`, never by `-e`.
2. `_tmux` returns `None` only on `FileNotFoundError` (genuine absence). Any
   other `OSError` -- notably `PermissionError` -- is tmux PRESENT but broken
   and now raises `PaneHoldError`, so a present-but-broken tmux can never
   degrade to an anonymous `Popen`.

## Evidence

Real tmux 3.4 on the box (`which tmux` = /usr/bin/tmux), isolated under a
private `TMUX_TMPDIR`, server killed at teardown. `extensions/agi/tests/test_grok_bot_pane_hold_env_exact.py`
(3 tests) reads the pane child's OWN `env` output:

    python3 -m pytest extensions/agi/tests/test_grok_bot_pane_hold_env_exact.py -q
    3 passed in 11.85s

Integrated path (real tmux): the tmux server was seeded with
`OPENROUTER_API_KEY`, `restart(hold_pane=True)` was driven with the grok-bot
harness, and the pane child's env dump contained `GROK_TEST_MARKER=kept` and
**no** `OPENROUTER_API_KEY`.

Mechanism control: `hold_in_pane(env=None)` (the pre-fix inherit) showed the
sentinel reaching the child; the same call with the sentinel removed from the
passed `env` showed it ABSENT. Non-vacuous.

Gate F: with `subprocess.run` raising `PermissionError`, `restart(hold_pane=True)`
raised `PaneHoldError` and `output.log` was never created (the Popen fallback
opens it first); a `Popen` stub that raises `AssertionError` was never reached.

Full regression set:

    python3 -m pytest extensions/agi/tests/test_grok_bot_pane_hold_env_exact.py \
      extensions/agi/tests/test_grok_bot_pane_hold.py \
      extensions/agi/tests/test_grok_bot_pane_hold_env.py \
      extensions/agi/tests/test_grok_bot_adapter.py \
      extensions/agi/tests/test_real_adapter_restart.py -q
    40 passed, 3 warnings in 123.44s (0:02:03)

Production lines: `git diff --numstat` over the adapter = `39 6` -- under the
40-line ceiling.

## Falsifiers (each measured NEGATIVE)

1. Real tmux pane child still carries a sentinel removed from the passed
   `env` -> FALSE (absent, on real tmux 3.4).
2. Present-but-broken tmux (`PermissionError`) yields an anonymous `Popen` ->
   FALSE (named `PaneHoldError`).
3. Defects C/D regress -> FALSE (kid-2 suite green: rc!=0 named, failed
   list-panes named).
4. Core hold regresses -> FALSE (one `new-session`, one `respawn-pane` at the
   same name; pane survives SIGKILL).
5. The four named test files go red -> FALSE (40 passed).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Kid-2 threaded env as tmux -e K=V, which only ADDS to the server env -- real tmux 3.4 still handed the sentinel to the child, so removal must be done in the child process itself. The argv now runs through a mode-0600 launcher doing exec env -i, and _tmux returns None only for FileNotFoundError so a PermissionError-broken tmux is a named PaneHoldError. Measured on real tmux with a private TMUX_TMPDIR; env=None control proves the sentinel was in the server env.
<!-- THOUGHT:END -->
