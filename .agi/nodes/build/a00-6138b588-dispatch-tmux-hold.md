---
id: build:a00-6138b588-dispatch-tmux-hold
mint_id: 8e0ef31c13cd48ccb384f61233d06887
type: build
parents:
  - experiment:a00-6138b588-tmux-hold-build
next_edges: []
build_kind: code
confidence: 0.95
edited_by: a00-6138b588
evidence_runs:
  - experiment:a00-6138b588-tmux-hold-build
loop: goal:g7.31.1.2.2@s2
model: stealth/space-bunny-alpha
origin: build
payload_ref: extensions/agi/bin/dispatch.py
profile: balanced
role: kid
scaffold_hash: 408b568479888a42
season: 2
spawn_check: unverified
spawn_check_reason: schema 'build' is discriminated on 'build_kind', which this node does not set
title: Direct-argv tmux hold inside dispatch open-round
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# build:a00-6138b588-dispatch-tmux-hold

Production implementation for `goal:g7.31.1.2.2`, evidenced by
`experiment:a00-6138b588-tmux-hold-build`.

- Seam: inside production `_open_round` in `extensions/agi/bin/dispatch.py`.
- Identity: sanitised `agi-hold-<seat>-<agent>` plus immutable `pane_id`.
- Durability: direct-argv `respawn-pane` over `remain-on-exit`; SIGKILL leaves
  the dead pane and a later named call respawns that same pane.
- Honesty: `created` reflects the actual founding call; tmux failure is a WARN
  and a recorded reason, then plain Popen.
- Tests: `extensions/agi/tests/test_dispatch_tmux_hold.py` (CI-safe), with
  real-tmux evidence pasted in the experiment node.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Replaces the send-keys race that made both unmerged prior-art holds silently fall back; direct respawn-pane makes the pane process the agent and remain-on-exit preserves identity after SIGKILL.
<!-- THOUGHT:END -->

## Agent Notes
Direct-argv respawn-pane hold inside _open_round keeps the same named pane id across SIGKILL; 157 named engine tests and a real-tmux probe pass.
