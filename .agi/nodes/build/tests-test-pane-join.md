---
id: build:tests-test-pane-join
mint_id: 4168ea5a27034eb49db43340daa08da1
type: build
parents:
  - goal:g7.31.1.2
  - mvp:unified-spawn-path
next_edges: []
build_kind: code
confidence: 0.8
edited_by: director-general-1
link_ref: extensions/agi/tests/test_pane_join.py
location: source_root
origin: build-version
payload_ref: extensions/agi/tests/test_pane_join.py
role: director
season: 3
status: active
tags:
  - build
  - code
  - harness
  - test
  - tmux
  - pane
title: "Pane join tests -- the registry-free seat join, its council terms as rows and mutants"
town: core
---
<!-- BODY:BEGIN -->
# build:tests-test-pane-join

`extensions/agi/tests/test_pane_join.py` -- the falsifier rows of goal:g7.31.1.2 ACT 2b. REAL process trees (`bash` + `exec -a grok-bot python3 ...`) read through the real `ps -e` table and /proc; only tmux's pane-pid read is stubbed. Rows: inline exec (the harness IS the pane pid, depth 0); launch file (the harness is the child, depth 1); mutant A (always the pane pid) RED on the file row; mutant B (descendants only) RED on the exec row; two matches at the shallowest depth and no match are EMPTY with a named why; argv[0] as launched, not the exe; the join reads pid AND session from one process (-s on a first spawn, -r on a restart); a miss prints ONE loud line; the harness exiting under a lingering shell reads dead; a grok row takes the pane join and a claude / no-harness row the registry; every template but grok-bot keeps the claude registry; an unknown registry is refused by name; a grok first spawn mints a fresh uuid4, a restart never does; claude-code's argv is unchanged; session AND resume together are refused by name, and its mutant renders both.

2c-1 rows: a `#!/bin/sh` wrapper named grok-bot (comm grok-bot, argv[0] /bin/sh) is not the harness, and its mutant (the old argv-or-comm form) commits the shell; comm decides only when argv is empty (a long bin's 15-char comm prefix no longer matches); a template that does not load (TOML error, non-UTF-8, unreadable) falls back to the registry join; a cyclic parent table reads EMPTY and its mutant (the `seen` check dropped) never returns; resume_proof is template-declared, grok-bot `session_id`, every other `transcript`, an unknown value refused.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-09, director-general-1, goal:g7.31.1.2 ACT 2c-1: the 2b words' three items for 2c, each as a row with a mutant where one applies (sp + alive: comm only when argv is empty, alive's shebang row; alive + aio: the template-read fallback widened to parse/OSError/UnicodeDecodeError; aio: the cyclic table), plus the resume-proof vocabulary rows. The shebang row runs a real script, so the match is tested on what the kernel actually reports for a wrapper.
<!-- THOUGHT:END -->
