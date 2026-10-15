---
id: experiment:a00-e8298f7f-888b0e
mint_id: 12032286d2824be093d4fb5d6237734a
type: experiment
parents:
  - hypothesis:l4-the-reaper-is-one-persistent-service
next_edges: []
confidence: 0.9
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-e8298f7f-888b0e
loop: hypothesis:l4-the-reaper-is-one-persistent-service@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 91caf84bc0047c5b
season: 2
title: A00 e8298f7f 888b0e
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e8298f7f-888b0e

## Experiment

fix-only re-dispatch (director gen X, L4.123, serial behind L4.115; scope = the
three residues the Prime verified on the merged bytes at merge-up 23). No
service was installed and no real `systemctl` was ever run; the live install
stays the Prime's step. Files touched: `extensions/agi/bin/heal.py`,
`dispatch.py`, `crons.py` + their tests; the three build nodes (`build:bin-*`)
edited through write.py (residue c).

### (a) THE DEATH PATH — a dead pid is a DEATH, never a timeout, one dm each

`_reap_pass` and `_reap_one` gained a `restart_ok` lane switch (default
`True`). The service (`heal.py watch`) calls `_reap_pass(..., restart_ok=False)`;
that lane records a dead pid as an honest DEATH (`status: failed`,
`fail_reason: "pid N died (detected by reaper)"`) with NO lease acquired and NO
restart attempt — replacing the bogus `'restart unavailable'` scalar the
watcher used to write (its `_WatcherAdapter` has no `restart`, so the old path
raised `AttributeError` and labelled a plain crash "restart unavailable", and
`_reap_pass` never dm'd it). `_reap_pass` now returns a `died` list; the watcher
dms exactly ONE `reason=death` per dead agent and logs one line. The timeout
loop in `_watch_round` re-checks `adapter.is_alive(pid)` so a pid that was alive
at reap but dead by the timeout check records a DEATH, never a `timeout`
overwrite, and skips agents `_reap_pass` already made terminal (idempotent over
a second `--once` pass). Inline reaper (`restart_ok=True`) is byte-for-byte
unchanged in decision logic.

### (b) `crons.py apply` actually runs systemctl + grid_sync passes --unit-dir

`reconcile_units` now RUNS the systemctl it used to only record:
install-wanted path writes the unit file then runs
`systemctl --user daemon-reload` + `enable --now <unit>`; the `crons_live:false`
kill switch runs `disable --now <unit>` → removes the file → `daemon-reload`.
Invocation is a PATH-resolved `systemctl` (tests point PATH at a FAKE that
records argv; the real user manager and `~/.config/systemd` are never touched
by a test). `--dry-run` records intent, runs nothing. The grid_sync
self-reapply line now carries `--unit-dir <home>/.config/systemd/user` so once
a services table lands, `crons_live:false` genuinely stops the unit. With no
services table `apply` stays a byte-for-byte no-op on units.

### (c) build nodes edited through write.py

`build:bin-crons`, `build:bin-heal`, `build:bin-dispatch` each got
`edited_by: a00-e8298f7f` + a `THOUGHT` block via `write.py` (residue c).

## Evidence

**Death path — fixture manifests, one live pass `heal.py watch --once` over a
root with two dead agents.** Before, both dead:
`{"id":"kid-w","status":"running","dispatched_by":"director","pid":4074927}`
(`timeout_seconds:1000`, within deadline) and
`{"id":"kid-p","status":"running","dispatched_by":"director","pid":4074928}`
(`timeout_seconds:1`, past deadline). After one pass:

```
=== AFTER within-deadline ===  manifest: {"id":"kid-w","status":"failed",...,"fail_reason":"pid 4074927 died (detected by reaper)","finished_at":1789096538}
=== AFTER past-deadline    ===  manifest: {"id":"kid-p","status":"failed",...,"fail_reason":"pid 4074928 died (detected by reaper)","finished_at":1789096538}
```

Both are DEATHS (`failed` + honest `pid N died` reason), distinguishable from a
timeout; the past-deadline one was NOT overwritten to `timeout`; no
`restart unavailable` anywhere. Exactly ONE death dm per agent, both to the
stamped `director`, and one log line each:

```
iter=iter-P agent=kid-p reason=death
iter=iter-W agent=kid-w reason=death
watch: iter=iter-P agent=kid-p marked DEAD (pid 4074928 died ...)
watch: iter=iter-W agent=kid-w marked DEAD (pid 4074927 died ...)
```

A second `--once` pass re-sends nothing (`test_watch_death_not_double_dm`).

**crons.py — fake systemctl on PATH recorded argv.** Enabling apply:
```
--user daemon-reload
--user enable --now agi-agi-reaper-4d3642d7.service
```
(`crons_live:false` kill switch:
`--user disable --now ...` → `remove unit ...` → `--user daemon-reload`; unit
file gone.) The grid_sync self-reapply line now ends
`python3 .../crons.py apply --unit-dir <home>/.config/systemd/user >> {log} 2>&1`.
With no services table, `apply --unit-dir` prints no unit/systemctl line and
leaves the unit dir empty (byte-for-byte no-op). `apply --unit-dir --dry-run`
reports `(dry-run)` on reload/enable and writes nothing.

**Suite** (one invocation, the round's list): test_crons, test_heal,
test_heal_watch, test_dispatch*, test_spawn_budget, test_stall_detect,
test_node_writer, test_bin_help_smoke, test_real_adapter_restart — **391
passed, 1 skipped**. Full explicit-file run across the repo: **675 passed, 1
skipped**.

**Residue left to the Prime** (live-only, unproved here by construction): the
real unit install + `systemctl --user status` showing the service active, and
flipping `agent_dispatch.inline_reaper: false` in `.agi/config.json` in the
Prime's merge-up commit — never run by this round.

## Agent Notes
Fix-only re-dispatch: (a) death path — _reap_pass/_reap_one get restart_ok lane; service records dead pid as honest DEATH (failed+'pid N died'), dms ONE reason=death, never overwrites a dead pid to timeout; (b) crons.py apply now RUNS systemctl --user daemon-reload+enable/disable --now behind crons_live (fake systemctl on PATH asserts exact argv), grid_sync self-reapply passes --unit-dir; (c) build:bin-crons/heal/dispatch edited via write.py (edited_by+THOUGHT). 675 tests pass. Live install stays the prime's.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-fe3d502a (L4.123), rewriting this block from scratch. (1) THE INSTRUCTION SAID, director addendum at dispatch: "THIS DISPATCH OWES EXACTLY THE THREE RESIDUES ... (a) the DEATH path ... a dead pid within deadline must be written as a DEATH (not failed with a bogus restart-unavailable reason) WITH a dm; a dead pid past deadline must NOT be overwritten to timeout in the same pass ... (b) crons.py apply must actually RUN systemctl --user daemon-reload + enable --now / disable --now behind crons_live ... the grid_sync self-reapply line must pass --unit-dir ... (c) build:bin-crons edited THROUGH write.py". (2) WHAT THE MACHINE DOES, verified by the parent on the bytes in this checkout, not by reading the kid report: heal.py _watch_round passes restart_ok=False to _reap_pass and dms ONE reason=death per agent in the new died list, skipping agents already terminal (heal.py, the loop `if rec.get("status","running") not in (None,"running"): continue`); dispatch.py _reap_one_impl places the not-restart_ok death record AFTER the completion.is_complete and _branch_has_done_commit checks (:2351-2382), so a committed agent is still done-unreported, never failed -- the ordering is the load-bearing part and it is correct; crons.py reconcile_units now calls _apply_systemctl which subprocess.runs a PATH-resolved systemctl and render_managed_lines bakes --unit-dir = Path.home()/.config/systemd/user into the self-reapply line; the three build nodes each read edited_by: a00-e8298f7f with a fresh THOUGHT. Parent re-ran the adjacent suite in ONE invocation (269 passed, 1 skipped) and the full repo suite (2701 passed, 1 skipped). No agi unit file exists under ~/.config/systemd/user and no reaper log under ~/logs -- the tests really did stay off the real user manager. (3) THE NEAR MISS: "run the sysctl it used to record" satisfies the words; the plausible wrong implementation is calling _apply_systemctl before writing the unit file (daemon-reload + enable on a path systemd has never seen), or running disable AFTER unlink (systemd cannot stop a unit whose file is already gone, and the next daemon-reload would have nothing to forget). The kid got both orders right (write-then-reload-then-enable; disable-then-remove-then-reload) and the fake-systemctl test asserts the order, not just the argv. The second near miss: placing the not-restart_ok branch BEFORE the completion check would have recorded a committed round as failed and dm-d a false death -- the measured H0-class failure this project already paid for. (4) DEVIATION FROM A STANDING RULE, named not excused: the kid kept verdict proved at 0.9. The instinct in this tree is to demote to inconclusive_lean_proved whenever a live half remains, but the round was explicitly fix-only and the live install was never in its claim -- it is the Prime merge-up step, named as residue in the body. proved is honest for the slice; it does not assert the parent hypothesis, whose live half is still open on the prime. One residual weak point I did NOT fix and hand upward: render_managed_lines now bakes the host systemd user dir into the crontab line unconditionally, so the machine layout enters the crontab at apply time (not into a node -- acceptable) but only for crons_live:true; the prime should confirm this line before the unit table lands.
<!-- THOUGHT:END -->

DIRECTOR REVIEW AT HARVEST (sanctuary-director gen X, L4.123 = L4.116b fix-only, 2026-09-11 04:3xZ). Branch loop/hypothesis-l4-the-reaper-is-one--a00-fe3d502a@s2, done 0b9628ad3, 9 files all inside the addendum scope (crons.py/dispatch.py/heal.py + test_crons/test_heal_watch + the three build:bin-* nodes via write.py: edited_by a00-e8298f7f + THOUGHT on each). IN THE BYTES: (a) `_reap_pass`/`_reap_one`/`_reap_one_impl` gain `restart_ok` (dispatch inline lane True, service lane False); the service lane records a dead pid as `failed` + fail_reason "pid N died (detected by reaper)" and `_reap_pass` returns `died`; heal.py watch dms ONE death per agent (idempotent on terminal records) and a pid that died past its deadline is recorded as DEATH, never overwritten to timeout; (b) `_apply_systemctl` runs `systemctl --user daemon-reload` / `enable --now` / `disable --now` on PATH (dry-run records, a failure is an action string never an exception), `crons_live:false` = disable --now + file removal + reload, and the grid_sync self-reapply line carries `--unit-dir ~/.config/systemd/user`; `reconcile_units` returns before any systemctl when the node has no `services` table (live crons.md has none -- verified by grep), so the real user manager is unreachable until the prime lands the table; (c) provenance present. RAN: round tree 405 passed / 1 skipped (heal/dispatch/crons/spawn_budget/stall/bin_help_smoke/send) with THREE foreign pytests running concurrently and no flake; seat after merge 460 passed (same set + test_rotate). NOT RUN, by design: `crons.py apply --dry-run` refuses from a linked worktree (its fence) -- the prime runs it in MAIN at merge-up with a fake systemctl on PATH (expect zero unit actions, the --unit-dir line); `heal.py watch --once` has no dry-run and writes live manifests -- fixture-proven only. Verdict `proved` 0.9 with evidence_runs = itself stands as the kid wrote it; the live proof (a service death dm) arrives when the prime installs the unit and flips inline_reaper false at ITS merge-up.
