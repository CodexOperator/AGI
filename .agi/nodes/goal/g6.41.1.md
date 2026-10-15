---
id: goal:g6.41.1
mint_id: 777fd541bace4de5bccd80835bc330ce
type: goal
parents:
  - goal:g6.41
next_edges: []
confidence: 0.8
edited_by: belam
goal_id: G6.41.1
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 88f9d171776d0da1
season: 2
seeds: []
status: active
tags:
  - engine
  - heal
  - recovery
  - owner
  - urgent
title: "G6.41.1: the posts survive an oomd kill -- tmux in its own scope, heal RESUMES dead seats (not fresh), aborted rotations resolved, no double spawn, recovery pressure-gated"
town: core
---
# goal:g6.41.1

# goal:g6.41.1

## OWNER 2026-09-29 17:3xZ, verbatim (Prime pane)
"Make the recovery path restart tmux and your session as well not just the remote-control service."

## Why this exists
goal:g6.41: a seat whose process dies without a rotation must come back. Measured 09-29 (read-only investigation for belam-S2-L5-XVI, 17:4xZ): at 17:27:19Z systemd-oomd killed claude-remote-control.service (the top reclaimer, 3.8G; user@ pressure 85.73% > 50%; 91 processes). The tmux server lived in that unit's cgroup, so tmux and every post died with it. Restart=always brought back only the service's ExecStart. Nothing re-creates tmux session agi-rc: there is no new-session for it in extensions/, skills/, src/ or the crontab. heal (`heal.py watch`, which survived) named 8 posts DEAD at 17:28:04 and every relaunch failed "no server running" (heal.py:3039-3045). belam's in-flight gen-17 rotation record silenced heal for it (heal.py:2471-2480, 3526-3528). After agi-rc reappeared at 17:33:06, heal respawned the 8 FRESH at gen+1 (heal.py:3266-3271); only belam was resumed. The live tmux server and 8 of 9 posts sit in the remote-control cgroup again, so the next kill repeats this.

## Target end-state
- P1: rotate._ensure_tmux_session() (beside _launch_window, rotate.py:1734) creates agi-rc when absent, in its OWN scope (`systemd-run --user --scope --slice=agi.slice -- tmux new-session -d -s agi-rc`), outside the remote-control and reaper cgroups. It is called before rotate.py:1778, before heal.py:3035, and at the top of _watch_seats (heal.py:3582).
- P2: heal _recover_seat (heal.py:3146) RESUMES a dead seat whose row carries a session_id with an existing transcript: `claude --resume <sid>` with the row's model/effort/settings via _shell_cmd, same generation and name, then _successor_row_write with the new window and pid BEFORE the ack. A fresh spawn happens only without a transcript.
- P3: a `started` rotation record with a dead row pid and no successor window counts as ABORTED (rewritten in place as aborted-by-crash; heal.py:2453-2481); the predecessor is resumed; every in-flight skip is logged.
- P4: no double spawn. A flock on seats/<post>.launch.lock spans check, launch and row write in _recover_seat and cmd_spawn; _seat_sessions is always built (heal.py:3595-3596); a post whose session_id is open in a live pid is skipped. `rotate.py resume --post <p>` exists for hand resumes.
- P5: recovery is PRESSURE-GATED. _recovery_admitted() (before heal.py:3607) reads /proc/pressure/memory avg10 and user@ memory.current vs memory.high against a config cell; over it = "deferred", no launch. At most one launch per pass, the Prime first; resumes count toward CRASH_LOOP_MAX_PER_HOUR.
- P6: each post runs in its own scope (_shell_cmd via mem_cap.wrap_argv, mem_cap.py:310-325), so an oomd kill takes one post, not tmux and every post.

## Invariants
- The Prime is never downgraded by a recovery: a resume uses the row's model/effort, and the row must name what the Prime runs.

## Falsifier
1. Kill claude-remote-control.service on a test box: within two heal passes agi-rc exists in its own scope and every recover:true post is RESUMED (same session_id), rows re-seated.
2. Negative: `systemd-cgls --user` shows no tmux server and no post claude process inside claude-remote-control.service.

## Out of scope
STATE AT 9966e3050 (council, 20:1xZ): P1 LIVE; P6 BUILT, OFF (config post_scope.live=false, _shell_cmd scope_slice defaults None: fails closed) until the owner says -- so today one oomd kill of the tmux scope still takes every post (self-perpetuating). BUILT, NOT WIRED (all-is-one C2): _cutover_plan + _cutover_to_scopes (rotate.py ~1769-1822 at 9966e3050) have ZERO callers by design -- dummies only, gated on the owner's cutover word after PASS B3 (doc:card-belam §6); step 1 of that cutover re-runs test_r1_cutover_dummy_one_kill_is_one_post with -k at the cutover commit (skip-by-default). Delivery split by the council (18:0xZ): P1+P6 and P5 ride goal:g7.16.1.3 row R (closes on Falsifier 2 + a spawned post's own-scope cgroup + a one-scope kill of a throwaway dummy); P2-P4 and Falsifier 1 (RESUMED) = bundle 5 row 0 · box-local systemd units (an ExecStartPost puts tmux back in the killed cgroup; OnFailure never fires when only the posts die).

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Council 18:0xZ 09-29 (alive convener; all-is-one + self-perpetuating agree), on the Prime's URGENT relay asking the council to place this leaf: Out of scope no longer names goal:g7.16.1.3 (it now HOSTS row R) and the leaf is assigned to the council bundle chain head (director-general-1), not director-engine -- all-is-one: a leaf contradicting its placement is what a mur flags. Falsifier 1 needs P2 (resume), so it rides bundle 5 row 0; R closes on Falsifier 2 alone plus the scope checks. Hygiene left: the doubled # goal:g6.41.1 H1 (replace body 1:3 refused without --force; not forced).
<!-- THOUGHT:END -->

P6 LIVE 2026-09-30 01:5xZ (belam-S2-L5-XIX, owner: "go ahead and install them and finish applying them"): spawn.post_scope = {live: true, slice: app.slice}; test_r1_cutover_dummy_one_kill_is_one_post PASSED live (AGI_LIVE_SYSTEMD=1) at this commit; the running posts move into their own scopes at the planned reboot (every post relaunches), so _cutover_to_scopes stays uncalled.
