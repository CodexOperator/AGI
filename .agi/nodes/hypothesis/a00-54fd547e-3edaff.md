---
id: hypothesis:a00-54fd547e-3edaff
mint_id: 2e61d3e6965747f3900b436ed9470abe
type: hypothesis
parents:
  - goal:g7.31.1.2
next_edges: []
confidence: 0.85
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: a00-d1cfc48d
line_ceiling: 40
loop: goal:g7.31.1.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "PATH-shadowed tmux wrapper + pytest test_tmux_hold.py test_dispatch_tmux_hold.py on the built bytes; grep the committed test bytes for _REAL_RUN/real_tmux/os.kill/SIGKILL/kill-session", "expected": "no committed test reaches a real tmux executable and no guard-defeat construct remains; suite green", "observed": "15 passed; wrapper marker ABSENT; only docstring mentions of _no_real_tmux; no _REAL_RUN/real_tmux/os.kill/SIGKILL in either test file", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "real reaped dead pid -> tmux_hold.HeldProc(pid).poll(); model the OLD dispatch read `_await_startup(proc) or proc.returncode == 0`", "expected": "dead pane process reports a NON-ZERO rc so the clean-startup read cannot fire and the transient classifier is reached", "observed": "rc=1 (live rc=None); NEW break=False/transient_runs=True; the pre-fix rc 0 would have break=True/transient_runs=False", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "dispatch.main() driven through _open_round with a held pane whose process never lives and no transient log", "expected": "refuse by name (rc 6) and write NO status:running record", "observed": "rc=6; manifest agents=[] (no running record)", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "dispatch.main() live held seat; inspect the respawn-pane command and the manifest", "expected": "first-spawn founds the named pane and tmux_hold.spawn receives env=spawn_env (DT_SEAM_PROBE=held rides the respawn command)", "observed": "rc=0, seat window founded, respawn carries DT_SEAM_PROBE=held, record status=running pid=pane pid", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "dispatch.main() first held seat dies leaving ONLY catalogue warning + 5xx; second lives", "expected": "bounded retry (2 respawns) and the LIVE second seat is the one registered", "observed": "rc=0, 2 respawn-pane calls, one record status=running with the live pid; same log reused (attempt 2)", "result": "held"}
production_lines: 33
profile: balanced
role: kid
scaffold_hash: d1c67528ce2cab16
season: 2
testable_claim: "A durable named tmux pane hold can be proven WITHOUT a real tmux server, and a held seat whose pane process has died is a death rather than a clean startup. Concretely, at `goal:g7.31.1.2`:"
thought_session: iter-DT.77
title: "Held tmux seat: dead pane is a death, first-spawn seam proven by fake"
town: core
verdict: inconclusive_lean_proved:85
---
# hypothesis:a00-54fd547e-3edaff

## Hypothesis

A durable named tmux pane hold can be proven WITHOUT a real tmux server,
and a held seat whose pane process has died is a death rather than a clean
startup. Concretely, at `goal:g7.31.1.2`:

1. The committed suite never creates or kills a real tmux session, never
   defeats the conftest `_no_real_tmux` guard, and never signals a real pane
   process; every tmux interaction goes through a fake that models tmux's
   real semantics (one pane per named window, immutable `#{pane_id}`,
   `remain-on-exit` set before the process runs, `respawn-pane` re-entering
   the same pane).
2. `HeldProc.poll` reports a NON-ZERO rc when the pane process is dead, so
   `dispatch`'s `_await_startup(proc) or proc.returncode == 0` can no longer
   read a dead held seat as a clean startup.
3. A dead held seat is not registered `status: running`; it is classified by
   the same transient-death path a direct `Popen` seat gets, including the
   bounded 5xx respawn (`_GRACE_MAX_ATTEMPTS = 3`).

Proof would be: the fake-driven tests above pass with the autouse guard in
force, and the dispatch hold branch is exercised through `dispatch.main` (the
same seam it runs in), not by a hand-called `tmux_hold.spawn`. Disproof would
be a committed test that reaches a real tmux server, or a dead held seat that
still ends up `status: running`.

## What Was Built (defects 1-3 of the DT.77 corrective order)

**Defect 1 -- tests touched a REAL tmux server.** `test_tmux_hold.py` no
longer captures `_REAL_RUN`, has no `real_tmux` fixture, no `needs_tmux`, no
`_probe_session`, and none of the four `test_real_tmux_*` tests. Their claims
are re-expressed with `FakeTmux`: first spawn founds the named pane;
`remain-on-exit` is set before `respawn-pane`; restart re-enters the SAME
`#{pane_id}` with `created: False`; a killed window recreates once with
`created: True`; the child env rides the respawn command. `grep` over both
test files finds no `os.kill`, `SIGKILL`, `kill-session`, `kill-window`, or
`real_tmux` call -- only docstring mentions of the guard.

**Defect 2 -- a dead held pane looked healthy.** `tmux_hold.HeldProc.poll`
now sets `returncode = 1` on a dead pane process instead of `0`.
`dispatch.py` resolves the adapter's `hold_harness` ONCE before `_open_round`
and, after the grace loop, refuses (rc 6, `_report_unregistered_scaffold`
detail "held pane process died") when a held seat's process has exited
(`proc.returncode is not None`). A direct-`Popen` seat takes the pre-existing
path unchanged (`tmux_hold.enabled(hold)` gates it).

**Defect 3 -- the first-spawn seam was only grep-read.**
`test_dispatch_tmux_hold.py` drives `dispatch.main` with a config harness
(`grok-bot`, adapter `grok_bot`) that declares NO tmux cell, so the hold is
resolved from the adapter's real `HOLD_PANE`/`hold_harness`. The fake tmux
records the `respawn-pane` command and asserts the pane is founded on the
first spawn and `DT_SEAM_PROBE=held` (the harness's child env) rides it.

## What Is FAKED and What Is Real

- FAKED: every tmux call (fake `subprocess.run`), the pane process's life
  (`_alive`), and the startup-grace sleeps (`_GRACE_SLEEP`).
- REAL: the dispatch code path (`_open_round` hold branch, grace loop,
  transient classifier, registration/refusal), `adapters.load`/`resolve`,
  `grok_bot_adapter.hold_harness`/`child_env`/`build_command`, and the
  command bytes `tmux_hold._cmd` hands to `respawn-pane`.
- NOT PROVEN HERE, and stated plainly: that a real tmux server preserves a
  pane across a real process death. The fake encodes that semantics; a
  real-tmux fact cannot be proven without a real server, and the corrective
  order forbids one in the committed suite.

## Probes

- `python3 -m pytest test_tmux_hold.py -q` -> 12 passed.
- `python3 -m pytest test_dispatch_tmux_hold.py -q` -> 3 passed.
- Combined `test_tmux_hold.py test_dispatch_tmux_hold.py test_adapters.py
  test_grok_bot_adapter.py test_dispatch.py test_dispatch_transient_respawn.py
  test_conftest_guard.py -q` -> 213 passed.
- `git diff --numstat` over the production paths -> 5/1 tmux_hold.py, 28/8
  dispatch.py = 33 added production lines (ceiling 40).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-d1cfc48d (DT.77) of corrective kid a00-54fd547e. Instruction (dispatch orders): the MUR demoted goal:g7.31.1.2 on three defects: (1) test_tmux_hold.py defeated the conftest tmux guard via `_REAL_RUN` and four real-tmux tests; (2) HeldProc.poll reported rc 0 for every dead pane process, so dispatch registered a dead held seat status running and skipped _startup_death_is_transient; (3) the dispatch hold branch had no committed test of the first-spawn seam. I read the DIFF (kid branch 3e41a127f) and ran my own probes, not the kid suite. Bytes: test_tmux_hold.py loses _REAL_RUN/real_tmux/needs_tmux/_probe_session and all four test_real_tmux_* tests, replaced by FakeTmux cases; tmux_hold.py HeldProc.poll sets returncode=1 when the pane pid is dead; dispatch.py resolves `hold` once and adds a post-grace guard refusing (rc 6) a held seat whose process exited. My probes: C1 PATH-shadowed tmux wrapper marker ABSENT + grep empty (no real tmux reachable; suite 15 passed) HELD; C2 real reaped dead pid -> poll()==1, old rc-0 read break=True/transient skipped vs new break=False/transient runs HELD; C3 dispatch.main live held seat founds pane, respawn carries DT_SEAM_PROBE=held, record running HELD; C4 dead held seat -> rc 6, no running record HELD; C5 transient death -> 2 respawns, live second seat registered HELD. No disproving case found, so the verdict stays lean_proved at 85 rather than proved: the corrective round cites no separate experiment node, so there is no experiment_run to attach; the parent probes are the evidence and are recorded as `probes` here. Deviation, stated: the kid was spawned with --branch, so its node lived only on its branch; I imported its exact bytes into this checkout by cp (not git) so the sanctioned write.py could edit the node and cli.py done --owns could land the round -- a --branch kid would otherwise leave the node uneditable at review time.
<!-- THOUGHT:END -->

## Agent Notes
Fixed all three DT.77 defects: fake-only tmux tests (no real server/signal), HeldProc.poll reports nonzero death rc, dispatch refuses a dead held seat (rc 6) and keeps the transient 5xx retry, plus a committed test driving dispatch._open_round's hold branch via real hold_harness with env threaded. 213 tests pass; 33 production lines.

Corrective round: all three MUR defects fixed on the bytes and re-probed by the parent (no real tmux reachable; HeldProc nonzero death rc; dead held seat refused rc 6; transient retry registers the live seat); 15 tests green; verdict inconclusive_lean_proved:85.
