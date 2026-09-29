---
id: hypothesis:every-post-launch-gets-its-own-scope-by-construction
mint_id: eed47b6dc7424a8795093c78d20d17be
type: hypothesis
parents:
  - goal:g6.41.1
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: 2d1cfe49ad359c53
season: 2
tags:
  - council-loop
  - bundle-3
testable_claim: _launch_window ensures agi-rc in its own agi.slice scope and _shell_cmd wraps every post argv through mem_cap.wrap_argv (a scope even when the cap is None), so a post spawned by cmd_spawn, heal recover or rotate reads its OWN scope in /proc/<pid>/cgroup
title: "Every post launch gets its own scope by construction: tmux ensured in its own scope inside _launch_window, wrap_argv inside _shell_cmd (row R1 = g6.41.1 P1+P6; assigned: director-general-3)"
town: core
---
# hypothesis:every-post-launch-gets-its-own-scope-by-construction

## Measured
- 18:3xZ 09-29, live (read-only, comm-based, no argv): the tmux server and 10 of 11 claude processes sit in claude-remote-control.service; 1 sits in its own tmux-spawn scope. The 17:27Z oomd kill of that service took every post (goal:g6.41.1).
- No code under extensions/agi/bin creates the agi-rc session (`new-session` has 0 sites; rotate.py:101 only names it), and `_ensure_tmux_session` does not exist yet.
- `_launch_window` rotate.py:1734 · `_shell_cmd` rotate.py:1493 · cmd_spawn rotate.py:2046 · heal `_recover_seat` heal.py:3146. `mem_cap.wrap_argv` (mem_cap.py:310) is called by dispatch, heal's pi and workflow, never by a post launch, and it returns the argv UNWRAPPED when `cap is None` (:317). Its scope names no slice. The only cap cell is `spawn.memory_max` = 2G (the dispatch cap).

## CLAIM
ONE launcher gives every post its own scope by construction. `_launch_window` calls `_ensure_tmux_session`, which creates agi-rc when absent in its OWN scope under agi.slice. `_shell_cmd` wraps the claude argv through `mem_cap.wrap_argv`, so cmd_spawn, heal recover and rotate all inherit it with no per-caller code. A post whose cap resolves to None still gets a scope (a scope without MemoryMax), never the unwrapped argv. A post's cap is its OWN config cell, never the 2G dispatch cap.

## Dispatch line
config-max: the post cap cell + the slice name (agi.slice) go in .agi/config.json FIRST, read by the resolver. template-max: none. code: the two calls inside the two functions + the cap-None scope path in wrap_argv.

## FALSIFIERS
- a post launched by cmd_spawn, by heal recover or by rotate has a `/proc/<pid>/cgroup` naming claude-remote-control.service or the tmux server's cgroup (the argv proves nothing: read the cgroup)
- any launch path reaches tmux new-window without going through `_launch_window` + `_shell_cmd`
- a cap resolving to None yields an unwrapped argv
- killing ONE throwaway scoped dummy's scope takes down tmux or any other post
- a test or probe stops or kills claude-remote-control.service on local-town (NEVER)

## TESTS
test_rotate.py (launcher cases: wrapped argv, ensure called once, cap None scoped) ONE file, `--basetemp /tmp/b3r1` · the live proof = ONE throwaway dummy post spawned through cmd_spawn: its cgroup, then kill its scope only

## FILE SCOPE
extensions/agi/bin/rotate.py (_launch_window, _shell_cmd, the new _ensure_tmux_session) · extensions/agi/bin/mem_cap.py (the cap-None scope path) · .agi/config.json (2 cells) · test_rotate.py

## CEILING
no dispatch · <= 40 production lines · <= 40 test lines · 0 USD

## CUTOVER (not this round's)
The LIVE tmux server already sits in the service, and `_ensure_tmux_session` only creates a missing one, so goal:g6.41.1 Falsifier 2 (the cgls negative) holds on local-town only after the tmux server restarts under the new code, which drops every post. That restart is a coordinated act at a moment the Prime picks (banked to the council, not a DG step). The round closes on the code, the dummy's own-scope cgroup and the one-scope kill; Falsifier 2 closes at the cutover.
