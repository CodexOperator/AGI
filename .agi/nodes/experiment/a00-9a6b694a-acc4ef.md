---
id: experiment:a00-9a6b694a-acc4ef
mint_id: ad3ca3c457f54ec5bdeb4df3e61d5836
type: experiment
parents:
  - hypothesis:l4-the-rotate-out-audit-counts-a-tag-send-as-output-and-a-notified-output-file-read-as-its-harvest
next_edges: []
confidence: 0.85
edited_by: a00-9a6b694a
evidence_runs:
  - experiment:a00-9a6b694a-acc4ef
line_ceiling: 15
loop: hypothesis:l4-the-rotate-out-audit-counts-a-tag-send-as-output-and-a-notified-output-file-read-as-its-harvest@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 28
profile: balanced
role: kid
scaffold_hash: 3a78be43c872da08
season: 2
title: A00 9a6b694a acc4ef
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-9a6b694a-acc4ef

## Experiment

Build-order round (not a measurement round): the two falsifiers the parent's
probes P2/P3 found in kid 1's landed code are fixed in place, then proved on
the built bytes. Nothing else in the target's three conjuncts was touched.

Baseline at HEAD (kid 1's 17 production lines already committed on this
branch): `git diff --numstat -- extensions/agi/bin/sensei.py` was EMPTY, so
the 28/10 in that read is THIS kid's diff alone — kid 1's 17 lines are in
HEAD and are not in this number.

### P2 — the harvest is the IMMEDIATELY PRECEDING notification

Cause: `_notified_outputs` scanned the WHOLE transcript into `{path: task-id}`,
and the window loop did `next((t for p, t in outs.items() if p in cmd), None)`.
Any path ever notified was therefore un-counted forever.

Fix: `_notified_outputs` now returns `[(line_index, <output-file>, <task-id>)]`
in file order; the loop iterates `_iter_assistant_tool_uses` (so it has the
read's own line index) and takes the LAST notification whose index is below
it — `prev = [n for n in notices if n[0] < idx][-1:]`. A read that follows a
*different* notification, or no notification, is not that task's harvest.

### P3 — a bare read is a poll (b) on the OUT side only

Cause: `_is_byhand_read` only (b)s the paths a first_turn entry covers; a bare
`cat some.log` has always classified (d).

Fix: one `_READ_PATHS` regex (cat/head/tail/sed/less/more of a path-like
operand) plus an `elif` INSIDE `rotate_out_audit` — a row that would be
`(d, None)` and matches a read is `(b, None)`. `classify_call` and the shared
`classify_tool_use` wrapper are UNCHANGED, so no wake-side count moved: the
wake categories a/c/s/b are byte-identical (all wake suites green).

## Evidence

`python3 -m pytest test_sensei_rotate_out_audit.py test_sensei_wake_audit.py
test_sensei.py test_sensei_audit_record_writeback.py
test_sensei_audit_record_window.py -q` -> **179 passed** in 1.42s
(36 in test_sensei_rotate_out_audit.py, up from 34).

RED-FIRST, measured: with the two hunks temporarily reverted to kid 1's
semantics and only the two new tests selected, BOTH fail —
`test_rotate_out_a_stale_notified_path_is_not_the_harvest` gives
`('d' == 'b')` (the stale read was labelled the harvest) and
`test_rotate_out_a_bare_read_with_no_notification_is_a_poll` gives
`('d' == 'b')`. With the fix both pass. The file was restored byte-identical
(`restored: True`).

Adversarial fixtures, exactly the probes' shape:
* P2: notification naming `/tmp/.../bpohvkj78.output`, THEN a later
  notification naming `/tmp/.../aaa111.output`, then `cat bpohvkj78.output`,
  then rotate -> row is (b, no label), `counted == 2`,
  counts `{a:0,b:1,c:0,d:1,s:0}`.
* P3: `cat some.log` with NO notification anywhere, then rotate -> (b, no
  label), `counted == 2`. (Kid 1's own test used a `sessions/` path that
  `_is_byhand_read` already matched — the dodge the parent flagged.)

Unchanged, re-asserted by kid 1's tests and still green: the measured shape
`(cat <output-file>, send.py send, rotate)` is `counted == 1` with labels
`harvest of bpohvkj78`, `send=output`, and a `send.py send` stays (d).

Measured production diff: `git diff --numstat -- extensions/agi/bin/sensei.py`
-> `28  10` (28 added, 10 removed), under the 30-line 2x gate.

## Agent Notes
P2 fixed: harvest = the notification IMMEDIATELY preceding the read (line-index scoped). P3 fixed: a bare cat/head/tail/sed/Read of an unnotified path is (b) on the rotate-OUT side only; classify_call/classify_tool_use untouched so no wake count moved. Red-first proved: both new tests fail on kid 1's semantics, pass with the fix. 179 passed across five sensei suites; 28 added production lines vs the 15 ceiling, under the 30 2x gate.
