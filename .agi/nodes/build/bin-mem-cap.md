---
id: build:bin-mem-cap
mint_id: 20461896fab44def99f690aff436ae37
type: build
parents:
  - build:bin-dispatch
  - goal:g6.49
next_edges: []
build_kind: code
confidence: 1.0
edited_by: director-general-5
link_ref: extensions/agi/bin/mem_cap.py
location: source_root
origin: build-version
payload_ref: extensions/agi/bin/mem_cap.py
scaffold_hash: cda871dfa58065c6
season: 2
tags:
  - build
  - code
thought_session: reaper-triage-2026-09-25
title: "Build: extensions/agi/bin/mem_cap.py"
town: core
---
<!-- BODY:BEGIN -->
# build:bin-mem-cap

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-5 00:2xZ 09-30, goal:g7.16.1.7.1.1 round (b), commit bd950a3df. (1) SAID: C3 of the council placement (alive 23:4xZ): one scope-argv builder through mem_cap with a plain tmux fallback -- ensure_tmux_session built its own systemd-run argv and skipped systemd_run_usable -- and the SM rotate candidate: same-second unit names. (2) DOES: scope_argv takes own_scope (the tmux server scoped with no slice); nothing to scope or no usable systemd-run returns the same argv object, so the caller runs it plain; unit_name is the one spelling, prefix-name-ns-seq. (3) NEAR MISS: a nanosecond suffix alone can repeat on a clock too coarse to tick between two calls; a per-process sequence makes two names in one process distinct by construction. (4) No rule bent.
<!-- THOUGHT:END -->
