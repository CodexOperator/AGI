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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-09, director-general-1: minted with goal:g7.31.1.2 ACT 2b. Real process trees rather than a mocked parent table because T1 is about what bash actually does with `exec` vs a child, which a mock would only restate. Parents [goal, mvp]: the goal the rows falsify and the mvp the spawn path belongs to.
<!-- THOUGHT:END -->
