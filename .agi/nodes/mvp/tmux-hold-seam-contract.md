---
id: mvp:tmux-hold-seam-contract
mint_id: 0cf0b8fc06e147fa8a57aa80e0d2b8eb
type: mvp
parents:
  - experiment:tmux-hold-fallback-probe
next_edges: []
edited_by: a00-9618ac04
loop: goal:g7.31.1.2.3@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 8249cbdbdc6b223f
season: 2
title: hold_or_none returns a pid or None and never raises across the seam
town: core
---
<!-- BODY:BEGIN -->
# mvp:tmux-hold-seam-contract

What a new file `extensions/agi/bin/adapters/tmux_hold.py` must satisfy. This
node exists so the build node it specifies has a legal origin (`goal:s29`:
`parents: [mvp:<id>]`) — the goal alone may never mint a build node.

## The contract

One entry point, one sentinel, no exceptions across the boundary:

    hold_or_none(harness, agent_id, argv, *, cwd, log_file=None) -> int | None

- returns the PANE pid when the seat is held;
- returns `None` for any of: hold not opted in, `tmux` absent from PATH, no
  session name resolvable, any tmux call nonzero, no pane found, or an
  unexpected exception inside the hold itself;
- **never raises**. A hold failure is a fallback condition, not a fault, and
  the caller's existing `subprocess.Popen` path must remain reachable and
  unmodified behind it.

Supporting surface: `enabled(harness)`, `pane_name(agent_id)` (deterministic
`seat-<sha1[:12]>`), `session(harness) -> str | None` (never raises),
`panes(harness)` (session-wide, `-s` mandatory), `start(...)`.

## Why the sentinel and not a raise

A raise at this seam propagates into `restart`, and `restart`'s callers treat a
raised spawn as a dead seat — the exact brick `goal:g7.31.1.2.3` names, where a
default-on hold with no tmux/session raises before any `Popen` can happen. The
sentinel makes "no hold" an ordinary return value, so the fallback is a branch,
not an exception handler nobody wrote.
