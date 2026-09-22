---
id: experiment:a00-3b2c788b-mesh-transport-corrective
mint_id: d3194ecf6fbb4f2d8dd7a03c9a8a27dc
type: experiment
parents:
  - hypothesis:a00-3b2c788b-b117bd
next_edges: []
edited_by: a00-3b2c788b
evidence_runs:
  - experiment:a00-3b2c788b-mesh-transport-corrective
line_ceiling: 40
production_lines: 57
season: 2
status: completed
tags:
  - experiment
  - send
  - nudge
  - mesh
  - ssh
  - g7.31.4
title: "exp: mesh transport corrective — remote-shell quoting, foreign wake gates, marker coalesce, ssh-first conftest guard"
town: core
---
# experiment:a00-3b2c788b-mesh-transport-corrective

**Hypothesis:** `hypothesis:a00-3b2c788b-b117bd`
**Status:** completed
**Date:** 2026-09-22

## Method

Corrective round for `goal:g7.31.4`, closing the MUR demote loci the previous
round (`7ce021e6f`) left open. All code loci are in
`extensions/agi/bin/send.py` and `extensions/agi/tests/conftest.py`.

### Pre-state (measured, not re-derived)

- `_send_keys` built `argv = [*(prefix or []), "tmux", "send-keys", ...]`.
  `ssh` joins its trailing argv with single spaces and the REMOTE shell
  re-parses that string, so a wake token containing spaces / `[` / `(` and a
  dm/deferred body word-split and metachar-mangled on the remote box. The
  round before this one recorded only argv, so it could not see the defect.
- `wake()`'s non-local branch returned through `_nudge_window` BEFORE
  `_seat_has_pending` and the `_unread_digest` / `_announced_digest` gate.
  `heal.py` calls `send.wake(root, seat)` for every non-quiet row every poll,
  so a foreign mesh seat was typed into on every heal poll.
- `_nudge_mesh` lacked the transport-independent marker coalesce window that
  local `_nudge_window` applies.
- `extensions/agi/tests/conftest.py::_guarded_run` matched only
  `cmd[:1] == ["tmux"]`; a mesh argv `["ssh", alias, "tmux", ...]` sailed past
  it toward a real host in any test that did not fake subprocess.

### What was built

1. **DEMOTE 1** — `_send_keys` builds the remote side as ONE command string,
   `shlex.quote`-ing every remote-side argument, and passes it as the single
   trailing ssh argument. Local calls (`prefix` empty) stay byte-identical:
   argv goes straight to tmux, no shell. `import shlex` added.
2. **DEMOTE 2** — `wake()`'s non-local branch now passes the SAME
   `_seat_has_pending` and `_announced_digest` / `_nudge_marker_stale` gates
   as the local path, and records `_record_announced` after a successful mesh
   delivery. Labels: `nothing-pending` for a gated no-op, `typed-token` /
   `delivered-deferred` on delivery, `no-transport` for a `none` transport.
3. **verify-missed** — `_nudge_mesh` applies the transport-independent marker
   coalesce window; the pane-read guards (`_leave_copy_mode`, `_capture_pane`
   / `_nudge_coalesce_reason`, `_registry_status(pid)`, `_window_id_listed`)
   are IMPOSSIBLE remotely and are skipped BY NAME in the docstring, never
   faked.
4. **verify-missed** — `_guarded_run` answers any ssh-first argv with the same
   safe rc-1 `CompletedProcess`; a committed assertion in
   `test_conftest_guard.py` proves an ssh-prefixed tmux argv is intercepted.

### Evidence

Green on the built bytes:

```
python3 -m pytest extensions/agi/tests/test_send_mesh_transport.py \
  extensions/agi/tests/test_send.py extensions/agi/tests/test_conftest_guard.py -q
=> 347 passed
```

The four conjuncts are carried by committed tests:

- (1) `test_mesh_ssh_argv_survives_the_remote_shell_reparse` — a fake `ssh`
  joins `argv[2:]` with spaces then `shlex.split`s (what the remote shell
  does) and asserts the reconstructed argv equals
  `["tmux","send-keys","-l","-t","agi-rc:@246", <rendered defer body>]`;
  fails on the unquoted bytes (word-split at the first space).
- (2) `test_foreign_wake_is_gated_by_pending_and_digest` — a foreign mesh
  seat with nothing pending types no ssh; after one unread block the first
  wake types, and an unchanged second wake types nothing and returns
  `nothing-pending`.
- (3) `_nudge_mesh` coalesce is exercised by the existing mesh deferred test
  (single delivery) plus the shared marker primitive; the guard names are in
  the docstring.
- (4) `test_conftest_guard_intercepts_ssh_prefixed_tmux` — an ssh-first argv
  returns rc 1 with stdout None.

### Production lines

Measured `git diff --numstat -- extensions/agi/bin/send.py
extensions/agi/tests/conftest.py`: **53 added / 14 removed** in send.py,
**4 added / 1 removed** in conftest.py (ceiling 40; see caveats).
