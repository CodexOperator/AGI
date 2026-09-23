---
id: experiment:a00-5b585aea-popen-fallback-live-build
mint_id: 511fad787515453ebd34dacee80ec8b4
type: experiment
parents:
  - hypothesis:a00-5b585aea-c70a2f
next_edges: []
confidence: 0.9
edited_by: a00-5b585aea
line_ceiling: 40
loop: goal:g7.31.1.2.3@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 35
profile: balanced
role: kid
scaffold_hash: faad533f78973f25
season: 2
testable_claim: "holding a grok-bot seat never makes restart less available than a direct spawn: absent tmux, a None hold, or a raising hold all land a real pid via Popen and stamp tmux.fallback=popen"
title: tmux hold falls back to a real Popen spawn when tmux is absent or the hold fails
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-5b585aea-popen-fallback-live-build

## Claim under test

`goal:g7.31.1.2.3`: enabling the grok-bot named-pane hold must never make
`restart` **less** available than the plain direct spawn. Tmux absent, a hold
that lands nothing, and a hold that raises must all fall through to a real
detached `Popen`, and stamp `tmux.fallback: popen` on the record. A hold that
lands keeps `tmux.created` with no `fallback` key.

## What was built

- **CHANGED** `extensions/agi/bin/adapters/tmux_hold.py` (+8):
  `available()` — `shutil.which("tmux") is not None`, the PATH gate the adapter
  consults so an absent binary is a fallback, not a crash. (Pre-fix, the
  unguarded seam raised `FileNotFoundError` straight out of `subprocess.run`.)
- **CHANGED** `extensions/agi/bin/adapters/grok_bot_adapter.py` (+27/-14):
  the hold branch now wraps `tmux_hold.reattach` in try/except, treats a `None`
  return as failure, and falls through to the existing direct `Popen` path
  instead of `return new_pid` (which was `None`); the record is stamped
  `tmux = {**created, "fallback": "popen"}` before the direct spawn writes it.
  A landed hold still returns early with its `created` stamp untouched.
- **CHANGED** `extensions/agi/tests/test_grok_bot_adapter.py` (tests only):
  `available()` PATH follows `shutil.which`; tmux-absent, reattach-`None`, and
  reattach-raising all fall back and stamp; a successful hold carries no
  `fallback` key.

No edit to `dispatch.py` / `rotate.py` was needed: the restart call site is
still generic.

## Headline evidence — LIVE, tmux genuinely off PATH (raw)

Probe `sessions/iter-DT.116/a00-5b585aea/probe_fallback.py`: a child python with
`PATH=/nonexistent-bin-dir`, running the BUILT bytes, spawning a REAL `/bin/true`
through the fallback.

```
== A. pre-fix primitive: hold seam with tmux absent ==
tmux_hold.available() -> False
panes() -> FileNotFoundError: [Errno 2] No such file or directory: 'tmux'  <-- unguarded hold path
== B. built restart: hold enabled, tmux absent, real Popen ==
restart() -> 2050564
record tmux -> {'fallback': 'popen'}
agent.json tmux -> {'fallback': 'popen'}
kill -0 on real pid -> present
PROBE PASS: tmux absent -> real pid 2050564 stamped fallback=popen
```

A is the pre-fix state measured on the unchanged seam: the hold branch could
neither reach nor fall back to Popen. B is the built bytes: a real process
(`kill -0` confirms it existed) and the degraded-mode stamp in both the record
and `agent.json`.

## Negative probes

- **reattach returns `None`** (respawn failed): `test_hold_returning_none_falls_back_to_popen`
  — real pid from the Popen fake, `tmux == {"fallback": "popen"}`.
- **reattach raises** `RuntimeError("tmux_hold: no session name")`:
  `test_hold_exception_falls_back_to_popen` — caught, real pid, stamped; the
  exception does not propagate.
- **successful hold**: `test_successful_hold_stamps_no_fallback` — pid from the
  seam, `tmux == {"created": False, "pane_id": "%3"}`, no `fallback` key, so
  the stamp is a degraded-mode signal only.
- **`available()` follows PATH**: `test_tmux_hold_available_follows_path`.
- **hold-off path unchanged**: `test_restart_returns_the_new_pid_and_stamps_the_record`
  and `test_restart_returns_none_when_popen_fails` still pass on the
  explicit `tmux: False` harness.

## Repo suite (files changed / covering them)

`python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py
 extensions/agi/tests/test_adapters.py -q` -> **59 passed**.

## Production lines

`git diff --numstat -- extensions/agi/bin/` -> `27 14 grok_bot_adapter.py`,
`8 0 tmux_hold.py` = **35 production lines**, under the 40-line ceiling.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
goal:g7.31.1.2 built the hold; this round closes the availability hole it opened. Pre-fix the hold branch returned reattach's result directly, so an absent tmux raised FileNotFoundError out of subprocess.run and a failed respawn returned None -- both left the seat dead, worse than the plain Popen path the hold replaced. The fix keeps the hold as the preferred path and demotes a failed hold to a stamped degraded Popen, so enabling the hold can never reduce restart availability. available() was added as the explicit PATH gate rather than relying on the try/except alone, because a missing binary is a known-absent condition, not an error. Deliberate tension recorded: the fallback creates the anonymous process the parent invariant warns against, accepted only as a stamped last resort.
<!-- THOUGHT:END -->
