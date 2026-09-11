---
id: goal:g15.20
mint_id: 398da4fb1dbf4c15b4105f685f9d90fd
type: goal
parents:
  - goal:g15
  - build:bin-rotate
next_edges: []
confidence: 0.7
edited_by: sanctuary-director
goal_id: G15.20
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 89ab27c5e33fd2a3
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - l4
  - sanctuary-director
title: "G15.20: Why prime X died at 17:51:50Z — find the cause from the evidence on the box and land the prevention if it is preventable"
town: core
---
<!-- BODY:BEGIN -->
# goal:g15.20

## Agent Notes
**Prime X died without a rotation; the loop must know why.** Owner 2026-09-11 17:5xZ: "do a goal to figure out why the crash happened if there's a good, preventable reason other than something somewhat random due to VPS cloud environment."

## Why this exists

- `goal:g15` is the parent because a preventable crash of the loop's prime is a bug in the loop, fixed in-loop; an environmental one is recorded so the next one is recognised in one read.
- `build:bin-rotate` is the parent because the prime's lifecycle (spawn, pin, reap) lives there and any prevention lands beside it.

## Evidence already measured (sanctuary-director 163547Z, 17:52-17:58Z)

- X = `belam` gen 10, @281, pid 3526521, transcript `e18063bd-…`; last transcript entry 17:31:13Z, transcript mtime 17:45:46Z; meter 0.36 (not due to rotate).
- `belam.log` (X's debug file): `[bridge:repl] Sent control_response for get_context_usage` 17:49:19Z (the owner's GUI); `[ERROR] SSETransport: Stream read error: The socket connection was closed unexpectedly` 17:51:09Z — the SAME error at the same second in `belam-S1-L4-V.log` and `belam-S1-L4-VI.log` (whose processes SURVIVED); `CCRClient: Heartbeat sent` until 17:51:45Z; pid gone by 17:52:10Z; the tmux window @281 gone (a pane whose process exits closes its window).
- No rotation record after 14:03Z; no `rotate-self` process; `heal.py watch` journal empty for the interval; no kernel OOM line (`journalctl -k`, `dmesg`); box memory 24 GB with 3.5 GB free at 17:57Z; `hermes-gateway.service` in failed state (unrelated?).

## Testable claim

(1) Read the last 60 s of X's log before the pid vanished (17:51:10-17:52:10Z, all levels) and its transcript tail, and name the exit: a signal (from whom — `ps`/journal/tmux `remain-on-exit` state), an uncaught error in the claude process, a remote-control disconnect that ends the session (the bridge's disconnect handling — compare with V/VI which took the same SSE error and lived: what differed — X was the ACTIVE remote-control target in the GUI), or an explicit GUI action; (2) if preventable: land the prevention (e.g. the spawn's `--remote-control` reconnect setting, a wrapper that restarts claude in place, or `remain-on-exit on` for seat windows so a dead pane keeps its @id and its last screen for the post-mortem) and prove it by reproducing the trigger on a throwaway seat; (3) if environmental (VPS network blip): record the signature (the exact log lines) on this node and make `goal:g15.19`'s detector name it as `probable-cause: remote-control disconnect` when the same lines precede a death. FALSIFIER: a cause named without a log line that shows it. CEILING: 1 kid (an investigation round; code only under (2)). FILE SCOPE: read-only over `.agi/sessions/*.log` and the transcript; writes only under (2) in extensions/agi/bin/rotate.py spawn region + tests. Quote log LINES, never a key.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
OWNER 2026-09-11 17:5xZ, verbatim to sanctuary-director after prime X died: 'add doing graceful recovery in case of crashes. Also do a goal to figure out why the crash happened if there's a good, preventable reason other than something somewhat random due to VPS cloud environment.' and 'Make sure both the goals I just shared go as subgoals under g15'.
<!-- THOUGHT:END -->