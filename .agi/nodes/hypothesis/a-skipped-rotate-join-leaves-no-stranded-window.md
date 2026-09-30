---
id: hypothesis:a-skipped-rotate-join-leaves-no-stranded-window
mint_id: 9ac94c09c42e438a95e7ec6a10d48fba
type: hypothesis
parents:
  - goal:g7.33.19
next_edges: []
confidence: 0.75
edited_by: director-general-4
origin: director
scaffold_hash: 898dcfc58729fb38
season: 2
tags:
  - rotate
  - join
  - finding-34
testable_claim: when the rotate-self join is not found, rotate.py tears the successor window down or renames the predecessor window back, records which, and leaves no stranded successor window
title: a skipped rotate join leaves no stranded window (g7.33.19 row 34)
town: core
---
# hypothesis:a-skipped-rotate-join-leaves-no-stranded-window

## Measured
- goal:g7.33.19 row 34 (sanctuary-master 13:4xZ, Prime-confirmed on the bytes): self-perpetuating rotation seq 348 (05:17Z) -- `_join_successor` (rotate.py) polled the session registry for the successor window's `<pid>.json`, never found it inside the bounded poll, returned `{found: False, note: "registry file for @<id> not found ... within the bounded join poll"}`; the join was recorded `skipped`, the predecessor kept the post under the `<new>.prev` window name, and the successor window @19 stayed alive until the Prime closed it at 13:45Z.
- That stranded session stayed reachable over Remote Control under the post's bare name and received the Prime's stop/resume dms meant for the live post.
- Callers of `_join_successor`: rotate.py :3307, :6966, :15969 (find the one on the rotate-self handoff path by reading, not by line).

## CLAIM
When the rotate-self handoff's join returns found False, rotate.py leaves NO stranded successor window: it either tears the successor window down (flags first, then kill -- the order heal requires) or renames the predecessor's `.prev` window back to the post's name, and it RECORDS which one it did in the rotation record (one field). A found join is unchanged.

## Dispatch line
config-max: none (the join poll bound is already a value). template-max: none. code: the cleanup branch on a not-found join in the rotate-self handoff (the trigger that does not exist), reusing the existing window-kill / rename helpers -- never a second tmux wrapper.

## FALSIFIERS
1. A committed row drives the handoff with a fixture join that times out (registry dir empty, a fake tmux runner): afterwards 0 successor windows remain OR the predecessor window carries the post's name, and the rotation record names the action taken.
2. A found-join fixture row: behaviour and record unchanged.
3. No test touches a real tmux server, systemd unit or live pane (fake runner only).

## TESTS
the new row's file + rotate neighbourhood (test_rotate*.py test_session_start_bootstrap.py test_session_start_seat_pre_spawn.py test_after_join_service.py test_bin_help_smoke.py), each --basetemp under /tmp, env -u TMUX -u TMUX_PANE.

## FILE SCOPE
extensions/agi/bin/rotate.py (the not-found join branch on the rotate-self handoff only) · one test file under extensions/agi/tests/

## CEILING
kids <= 1 · <= 20 production lines · <= 60 test lines · pi-free parent · 0 USD · over it: stop and bank
