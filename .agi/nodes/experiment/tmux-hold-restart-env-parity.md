---
id: experiment:tmux-hold-restart-env-parity
mint_id: 4e5109d834cd4969839bf99d97947924
type: experiment
parents:
  - hypothesis:a00-ba3af501-76183c
next_edges: []
edited_by: a00-ba3af501
line_ceiling: 40
loop: goal:g7.31.1.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "restart-passes-env", "class": "gate", "cmd": "grok.restart on real tmux, seat bin writes harness env cell + base environ to a file on each birth; kill pane process; restart", "expected": "the restarted process carries the SAME child env as first spawn (harness env cell AND base environ)", "observed": "first spawn marker hello|base-hello; after kill+restart marker hello|base-hello; rec tmux created False", "result": "held"}
  - {"conjunct": "negative-old-behaviour", "class": "gate", "cmd": "SAME seat, then tmux_hold.reattach WITHOUT env= (the exact call restart made before the fix)", "expected": "env must be lost, reproducing the parent's refuted probe", "observed": "first spawn DT67_PROBE='hello'; after env-less reattach DT67_PROBE=''", "result": "refuted_by_fix"}
  - {"conjunct": "first-spawn-carries-env", "class": "wire", "cmd": "read dispatch.py _open_round / spawn()/_cmd", "expected": "dispatch passes env=spawn_env into tmux_hold.spawn and _cmd prefixes it", "observed": "dispatch.py:2663 tmux_hold.spawn(..., env=spawn_env); tmux_hold._cmd prepends env K=V", "result": "held"}
  - {"conjunct": "no-grok-special-case", "class": "auth", "cmd": "grep -n grok extensions/agi/bin/dispatch.py", "expected": "no harness-name special-case", "observed": "no hits beyond the goal comment", "result": "held"}
  - {"conjunct": "pane-identity-noregress", "class": "wire", "cmd": "test_tmux_hold.py real-tmux tests after the fix", "expected": "same #{pane_id}, created False on held path; created True on gone pane", "observed": "11 passed; held path created False, gone pane created True", "result": "held"}
production_lines: 7
profile: balanced
role: kid
scaffold_hash: 1c42a0e41fb74f0a
season: 2
thought_session: iter-DT.67
title: Restart seam carries the same child env as first spawn
town: core
---
<!-- BODY:BEGIN -->
# experiment:tmux-hold-restart-env-parity

## Experiment

Repair of `goal:g7.31.1.2` (the parent's refuted probe). The pane-hold build
held every pane-identity conjunct, but its restart seam was **not** equivalent
to the first-spawn seam: `grok_bot_adapter.restart`'s hold branch called
`tmux_hold.reattach(...)` with **no `env=`**, while its own non-hold `Popen`
branch passed `child_env(harness=harness, base=dict(os.environ), tier=tier)`.
`tmux respawn-pane` inherits the **tmux server's** environment, not the
dispatch child's, so a reaper-restarted seat came back stripped of its harness
`env` cells, `AGI_*` identity and any minted key.

### Fix

`extensions/agi/bin/adapters/grok_bot_adapter.py` (`restart`): compute
`env = child_env(harness=harness, base=dict(os.environ), tier=tier)` **once**,
before the branch, and pass it as `env=env` to `tmux_hold.reattach(...)`. The
non-hold path now reuses the same value instead of recomputing it. 7 added / 2
deleted production lines (`git diff --numstat`, `grok_bot_adapter.py` only;
test file excluded).

First-spawn already carried env end to end and is unchanged:
`dispatch.py` `_open_round` passes `env=spawn_env` into `tmux_hold.spawn`,
which forwards it to `start`/`reattach`, whose `_cmd` prefixes `env K=V` onto
the respawned argv.

## Measurements against a REAL tmux server (3.4)

Scratch session `agi-dt67-probe-<pid>` created and killed by the test, or
`agi-neg-<pid>` by the ad-hoc probe; **never** the live `agi-rc`.

New proof, `test_real_tmux_restart_carries_the_child_env`
(`extensions/agi/tests/test_tmux_hold.py`): the harness `bin` is a script that
writes `$DT67_PROBE|$DT67_BASE_PROBE` to a marker file and then sleeps, so
**both** births run the same argv (`restart` rebuilds it via `build_command`).
`DT67_PROBE` is a `harness["env"]` cell; `DT67_BASE_PROBE` is in the base
environ. First spawn is seated exactly as dispatch does
(`tmux_hold.spawn(..., env=child_env(...))`). Then the pane **process** is
SIGKILLed (not the window) and `grok.restart` is called.

- first spawn: marker `hello|base-hello`.
- after kill + `grok.restart`: marker `hello|base-hello`, and
  `agent_record["tmux"] == {"created": False, "pane_id": <same>}` — the env
  SURVIVED the restart through the same immutable pane.

Negative probe (the falsifier, run ad hoc under
`.agi/sessions/iter-DT.67/a00-ba3af501/negative-probe.txt`), the exact old
behaviour: same seat, then `tmux_hold.reattach` with **no `env=`** →
first spawn `DT67_PROBE='hello'`, after reattach `DT67_PROBE=''`. The
defect reproduces and the fix closes exactly it.

Supporting fixtures test `test_restart_hold_branch_passes_child_env` names the
seam: `restart`'s hold branch hands `reattach` an `env=` carrying both the
harness cell and the base environ.

## Suite

- `extensions/agi/tests/test_tmux_hold.py -q` → **11 passed** (incl. the 3
  real-tmux tests and the new env-parity proof).
- `extensions/agi/tests/test_grok_bot_adapter.py` +
  `extensions/agi/tests/test_adapters.py -q` → **50 passed**.
- `extensions/agi/tests/test_dispatch.py` +
  `extensions/agi/tests/test_real_adapter_restart.py -q` → **150 passed**.

No pane-identity regression: same `#{pane_id}` + `created: False` on the held
path, `created: True` on a genuinely gone pane. `dispatch.py` still carries no
`grok` special-case.
<!-- BODY:END -->
