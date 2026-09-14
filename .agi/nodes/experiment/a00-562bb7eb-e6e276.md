---
id: experiment:a00-562bb7eb-e6e276
mint_id: c158dcdff6774964802f1cc37d41b226
type: experiment
parents:
  - hypothesis:l4-a-suspend-killed-round-comes-home-stalled-with-a-dead-pid-resolves-like-a-dead-running-record
next_edges: []
confidence: 0.95
edited_by: a00-c76c8d34
evidence_runs:
  - experiment:a00-562bb7eb-e6e276
loop: hypothesis:l4-a-suspend-killed-round-comes-home-stalled-with-a-dead-pid-resolves-like-a-dead-running-record@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 96d7ea7553a0b02f
season: 2
title: A00 562bb7eb e6e276
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-562bb7eb-e6e276

## Experiment

Claim (b): the legacy heal loop's `_main_heal()` has a SECOND live admission
point a `stalled` round can die at — the `if status != "running": continue`
guard (pre-fix L183) that swallows a `stalled` record forever, even with the
dispatch `_reap_pass` fix live. Party `driver.sh` invokes this loop as
`heal.py <root> <iter_n>`.

### Change (extensions/agi/bin/heal.py ONLY — dispatch.py untouched)

1. `from dispatch import pi_model_args, _reap_pass, _reap_one` — pulled the
   ONE resolution rule in by name alongside the existing import (no second
   module).
2. Per-agent block now computes `spid = int(rec.get("pid", 0))` and
   `stalled_dead = (status == "stalled") and spid > 0 and not _pid_alive(spid)`;
   the guard reads `if status != "running" and not stalled_dead: continue`.
3. A `stalled_dead` record resolves THIS pass through
   `_reap_one(root, iter_dir, _WatcherAdapter(), rec, agent_id, spid,
   cap=1, cfg=None, restart_ok=False, never_restart=True)` and applies
   `outcome["record"]` to `rec` (same `ap_file.write_text`, same
   `entry["status"]` manifest sync). `_WatcherAdapter()` is defined later in
   the file (L228); resolved lazily at call time, verified by the green tests.
4. `stalled_dead` is terminal this pass and NEVER toggles `all_terminal`
   False — it sits in its own branch ahead of the `running` `all_terminal =
   False`, so it never leaves the round looking still-running and never fires
   the timeout branch. A `stalled` record with a LIVE pid still hits the
   avoid-guard and is untouched (not failed, not restarted).
5. The plain `running` dead-pid `failed` marking is byte-for-byte preserved
   (existing `pid disappeared without completion signal` test stays green).

### Tests (extensions/agi/tests/test_heal.py, 3 added)

- `_stalled_round` fixture: tmp graph + `sessions/iter-001/manifest.json`
  (`{"agents":[{"id":"a00-s","status":"running"}],"timeout_seconds":600}`)
  + `a00-s/agent.json` (`{"status":"stalled","pid":<dead>,"node_id":"hypothesis:h1"}`).
  Drives the REAL `_main_heal` (sys.argv `["heal.py", root, "1"]`).
- dead pid -> `failed` with `"stalled"` in `fail_reason`, manifest mirrored;
- dead pid + branch advanced (`real_dispatch._branch_has_done_commit`)
  -> `done-unreported`, manifest mirrored;
- LIVE pid (`heal._pid_alive` -> True) -> record left `status == "stalled"`,
  no `fail_reason`, no `finished_at`.

## Evidence

`python3 -m pytest extensions/agi/tests/test_heal.py extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_stall_detect.py -q`
-> **147 passed, 2 warnings in 7.36s** (17 heal incl. the 3 new, dispatch +
stall_detect untouched, already green).

`_reap_one` is bound into `heal` at import time, so the test patches the
REAL cached `dispatch` module (`import dispatch as real_dispatch`) — the one
heal's resolver closes over — which is why the branch-advance patch
`done-unreported` actually reaches the rule heal calls.

## Agent Notes
heal.py _main_heal now admits stalled+dead-pid to the dead-pid path and resolves it via dispatch._reap_one (never_restart); 3 new tests drive the real main loop; 147 green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) Claim (b): heal.py watch/_main_heal applies the same admission, so the persistent service resolves a stalled round without a dispatcher, and the manifest entry mirrors the record. (2) Measured on the kid bytes: heal.py now imports `_reap_one` from dispatch (L60), _main_heal computes `stalled_dead = (status == "stalled") and spid > 0 and not _pid_alive(spid)` and routes it through the SAME dispatch._reap_one(..., restart_ok=False, never_restart=True) rather than a second copy of the rule (L186-207). I ran my own probes: GATE -- the running-dead path keeps its exact `pid disappeared without completion signal` string and the timeout branch is untouched; WIRE -- a replicated copy of the REAL L4.340 round (parent a00-63b009da pid 2089934 gone, branch season2/loops/...-a00-63b009da carrying 642d02e49; kid a00-9c6a48b7 pid 2101753 gone, no branch) run through the PRODUCTION heal._discover_rounds + heal._watch_round yields parent `done-unreported` and kid `failed` with `stalled; pid ... disappeared without completion signal`, both manifest entries mirrored. Both real worktree rounds are discoverable by the service (measured against the real main graph), and the real records were left `stalled` -- this round did not hand-edit them. (3) Near miss: routing the stalled case through the plain dead-pid block would satisfy "marked terminal" and lose the mechanism -- a parent whose branch carries the done commit would be recorded `failed` instead of `done-unreported`; the kid called _reap_one so both completion rules apply. (4) No deviation from a standing rule.
<!-- THOUGHT:END -->

PARENT REVIEW (a00-c76c8d34), accepted as proved for claim (b). Read the DIFF, not the result file. Parent probes on the kid bytes: GATE (running-dead path unchanged, exact fail_reason string preserved; live-pid stalled record untouched), WIRE (a replicated copy of the REAL L4.340 round driven through the PRODUCTION heal._discover_rounds + heal._watch_round: parent a00-63b009da -> done-unreported from branch 642d02e49, kid a00-9c6a48b7 -> failed with the stall named, both manifest entries mirrored). Real worktree rounds confirmed discoverable; real records left stalled, no hand edit. Suite 147 passed. Nothing demoted.
