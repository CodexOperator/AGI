---
id: mvp:dg3-r1-own-scope-launch
mint_id: c23b9d7ea1f5452c8f38b86158bf12db
type: mvp
parents:
  - verdict:dg2-r1-per-post-scope
next_edges: []
commit_hash: 63898e64f
confidence: 0.7
edited_by: director-general-3
scaffold_hash: 5147a540ea464e16
season: 2
source_files:
  - extensions/agi/bin/rotate.py
  - extensions/agi/bin/mem_cap.py
  - extensions/agi/bin/heal.py
  - .agi/config.json
status: implemented
tests_pass: true
title: tmux ensured in its own scope; every post launch scoped behind ONE switch (OFF until the owner's word)
town: core
---
# mvp:dg3-r1-own-scope-launch

# mvp:dg3-r1-own-scope-launch

## The minimum (built at 63898e64f, director-general-3, council bundle 3 stage 3)
```
P1   rotate.ensure_tmux_session: agi-rc absent -> systemd-run --user --scope --slice=agi.slice -- tmux new-session -d -s agi-rc;
     _launch_window calls it first; heal._launch_recovered before its own new-window (DG2 correction 1)
P6   mem_cap.scope_argv (POST-ONLY arm; wrap_argv's `cap None -> argv` untouched) wraps launch-wrapper + claude, cap-free;
     _shell_cmd scopes by default, spawn_window (the ONE caller) passes mem_cap.resolve_post_scope(config)
     cell spawn.post_scope = {live: false, slice: agi.slice} -> None on this box: live launches stay unscoped
cut  _cutover_plan (pure) + _cutover_to_scopes (StartTransientUnit(PIDs) Delegate=yes, Attach on repeat, until MainPID alone)
     DUMMIES ONLY; the live cutover = owner's word after PASS B3 (doc:card-belam §6)
```

## Tests
test_r1_* 5/5 (strict xfails -> pass; the dummy cutover ran on dg2-r-dummy-* units, 0 left) · rotate 336p · launch_wrapper 6p + session_start_seat_pre_spawn 3p (exact unscoped line now asks scope_slice=None) · rotate_recover 26p (fakes count new-window only) · launch_memory_cap 9p · mem_cap_tasks_max 14p · heal_* green

## CEILING
DISCLOSED: +121 prod lines incl. docstrings; cutover helpers ~45 code lines vs the raised ~40.

## Falsifier
1. the 5 R1 tests pass. 2. goal:g6.41.1 Falsifier 2 (no tmux / post in claude-remote-control.service) closes only after the live cutover -- NOT this round. BANKED: the slice (agi.slice shares MemoryHigh 9.26G / MemoryMax 10.29G with agi-work + agi-engine; the remote-control service holds 8.4G) -> (a) a dedicated uncapped posts slice, (b) raise agi.slice, (c) agi.slice as is; recommend (a) before flipping live.
