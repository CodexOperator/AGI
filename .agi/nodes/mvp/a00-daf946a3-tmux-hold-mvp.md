---
id: mvp:a00-daf946a3-tmux-hold-mvp
mint_id: daf946a3tmuxmvp
type: mvp
parents:
  - experiment:a00-2aac36b5-tmux-hold
next_edges: []
loop: experiment:a00-2aac36b5-tmux-hold@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
title: Specify tmux hold adapter with direct Popen fallback
town: core
---
<!-- BODY:BEGIN -->
# mvp:a00-daf946a3-tmux-hold-mvp

## Minimum viable behavior

Provide `extensions/agi/bin/adapters/tmux_hold.py` as a restart seam that
prefers a live tmux session when available and otherwise calls the command
through `subprocess.Popen` directly. The implementation must preserve the
exact command argv and return the child pid on the fallback path.

## Falsifier

The adapter is not sufficient if a missing tmux executable, an unset session,
or an unavailable session prevents direct execution, or if the fallback
changes the command payload.

## Evidence target

Focused tests cover no-tmux and unset-session runtime states and assert the
exact argv passed to `Popen`.
<!-- BODY:END -->
