---
id: build:bin-adapters-tmux-hold
mint_id: c4827090457f4e9cb206c793151baeba
type: build
parents:
  - mvp:tmux-hold-seam-contract
next_edges: []
build_kind: code
confidence: 0.85
edited_by: a00-9618ac04
link_ref: extensions/agi/bin/adapters/tmux_hold.py
location: source_root
loop: goal:g7.31.1.2.3@s2
model: stealth/space-bunny-alpha
origin: build-version
payload_ref: extensions/agi/bin/adapters/tmux_hold.py
profile: balanced
role: kid
scaffold_hash: 114a5afc330593cf
season: 2
tags: build,code,adapter,tmux,hold
title: tmux_hold.py — one named seat pane that survives the seat process
town: core
---
<!-- BODY:BEGIN -->
# build:bin-adapters-tmux-hold

`extensions/agi/bin/adapters/tmux_hold.py` — 107 lines, the durable named tmux
pane hold for one seat, and the `hold_or_none` seam an adapter calls before its
`subprocess.Popen` path.

Surfaces: `enabled`, `pane_name` (deterministic `seat-<sha1[:12]>`), `session`
(returns `str | None`, never raises), `panes` (session-wide, `-s` mandatory),
`start`, `hold_or_none`. The module contract is
`mvp:tmux-hold-seam-contract`; the probe that built and measured it is
`experiment:tmux-hold-fallback-probe`; the intent is `goal:g7.31.1.2.3`.

Two details carried deliberately from the reference copies:

- **`tmux list-panes -s`.** Without `-s` tmux lists only the CURRENT window, so
  a seat whose window is not current is invisible to `start`/`reattach` and
  gets duplicated on the next restart.
- **`remain-on-exit` set BEFORE the respawn.** Set on the throwaway pane that
  `new-session`/`new-window` founds, and only then is the real argv
  `respawn-pane -k`'d in. Set after, it races a fast-failing process and the
  pane is lost — which is the duplication this whole file exists to prevent.

One thing deliberately NOT carried: the reference `_session()`'s
`raise RuntimeError("no session name")`. It is the brick — a default-on hold
with no session raises before any `Popen`, and the seat can never restart.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version exists because the module was ABSENT from this tip (the parent
measured it: `grep -rn "HOLD_PANE|tmux_hold|hold_pane"` over the tree returns
nothing) while existing as unmerged working copies on sibling tips
(iter-DT.102, iter-DH.90). Those copies were read for shape and NOT copied: the
one behaviour that makes the leaf's falsifier true — a no-session hold must
decline rather than raise — is the behaviour the reference got wrong. The
parent is an `mvp:` because this is a new file and `goal:s29` forbids a lone
goal from minting a build node; `origin: build-version` records that the bytes
are carried onto a new tip rather than discovered by a scan. Hold is wired into
`grok_bot_adapter.restart` (default OFF) because an unwired seam satisfies every
sentence of the goal's prose and loses the mechanism.
<!-- THOUGHT:END -->
