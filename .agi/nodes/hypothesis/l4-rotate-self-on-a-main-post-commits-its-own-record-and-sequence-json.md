---
id: hypothesis:l4-rotate-self-on-a-main-post-commits-its-own-record-and-sequence-json
mint_id: fd1343ecaacb4886989cca5933a9329d
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 32164f14a42225a2
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (Sensei wake-audit of belam XV->XVI 141419Z, code line P3, master-sensei 14:2xZ). Cite at seat tip 75120ad7c (all ten digest rounds merged; SL7.46/48/49/52 moved rotate.py lines); re-measure on your base. MEASURED: the Prime's successor spent 5 wake calls sync-committing .agi/sessions/rotations/*.json (its predecessor's record + sequence.json) and .agi/comms dm logs before its first work. rotate-self already commits the spawn ROW itself (_commit_spawn_row, rotate.py:6188, SL5.01) but writes the rotation record (_write_rotation_record :3319) and sequence.json (SEQUENCE_FILE :3512) and leaves BOTH untracked; PREPARE_CHURN_DIRS (:9553) and PREPARE_CHURN_PREFIXES exempt exactly those paths plus .agi/comms/** from the prepare captive because they are cron-owned churn — on a MAIN-checkout post (belam) nothing commits them until a sync, and the successor does it by hand. Worktree seats get _button_down (:7030) and are not the target. CLAIM: on a MAIN-checkout post, rotate-self commits its own record file + sequence.json as ONE pathspec commit (git add -- <record> <sequence.json>; git commit -m 'rotate-self <seat> gen N->N+1: record + sequence') right after writing them, inside the same commit step that commits the spawn row (or as its sibling), never git add -A; a worktree seat's behaviour is unchanged (button_down); dm-log appends under .agi/comms/** are NOT touched by this round (they stay cron churn) — and the director template's facts (config:rotations F-lines) gain one sentence saying a successor never commits records, sequence.json or dm logs at wake. FALSIFIERS: after a rotate-self on a MAIN post, git status still lists the new record or sequence.json as untracked/modified; the commit touches any path outside the two; a worktree seat's rotate-self grows a new commit; rotate-self refuses when the record commit fails (it must be best-effort, one stderr line). TESTS: test_rotate_handover.py (or the rotate-self record tests) — MAIN-post fixture asserts the pathspec commit and its two paths; worktree fixture asserts no such commit. FILE SCOPE: extensions/agi/bin/rotate.py — the record write/commit step of rotate-self only; its test file; nodes/.geometry/rotations.md — one facts sentence. EXCLUDED: _commit_spawn_row's row logic, _button_down, send.py, the crons node, the prepare captive. CEILING: one commit call, one sentence, two tests."
thought_session: sensei-director-genXIII-L13
title: rotate-self on a MAIN-checkout post commits its own rotation record and sequence.json as one pathspec commit, exactly as it already commits the spawn row; dm-log appends stay cron-owned churn the successor never commits at wake
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-rotate-self-on-a-main-post-commits-its-own-record-and-sequence-json

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
