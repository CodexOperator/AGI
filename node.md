---
id: build:tests-test-heal-resume
mint_id: 728b4682102a45dcada5ba04a0442f9a
type: build
parents:
  - goal:g7.31.1.2
  - mvp:unified-spawn-path
next_edges: []
build_kind: code
confidence: 0.8
edited_by: director-general-1
link_ref: extensions/agi/tests/test_heal_resume.py
location: source_root
origin: build-version
payload_ref: extensions/agi/tests/test_heal_resume.py
role: director
season: 3
status: active
tags:
  - build
  - code
  - harness
  - test
  - heal
  - resume
title: "Heal resume tests -- a dead post resumes its own session; the template-declared proof and the failed -r rows"
town: core
---
<!-- BODY:BEGIN -->
# build:tests-test-heal-resume

`extensions/agi/tests/test_heal_resume.py` -- heal._recover_seat's resume rows through a fake launcher (no tmux): a transcript-proof resume keeps name, generation and session id, a missing transcript is a fresh spawn, a slot-less harness refuses a resume by name, a row's harness renders its own template. goal:g7.31.1.2 ACT 2c (L478) added: the session_id proof (PROVISIONAL, logged on every use); the pre-launch store read (present / absent / UNREAD); the end-of-window read (absent | no-pane = FAILED, the id cleared, the dead pid kept; ambiguous or a pid change = the id kept, pid EMPTY); alive's TERM (a failed id is never resumed again); R6 (absent empties the row window, the next pass reaches the loud same-name refusal) and its chain-seat guard; the dead id kept through the refusal pass and read back by `heal.py resume-failed --post`; each with a source-text mutant that reads RED.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
11-09, director-general-1: minted at L478's follow-up (SM relay 19:1xZ, alive 19:10:12Z: the file, added 09-30, had no build node, so the grid held no version of its 2c rows, which goal:g7.31.1.2's eventual CLOSE will cite). Parents [goal:g7.31.1.2, mvp:unified-spawn-path], as build:tests-test-pane-join.
<!-- THOUGHT:END -->
