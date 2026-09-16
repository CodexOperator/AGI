---
id: experiment:a00-9a6b694a-acc4ef
mint_id: ad3ca3c457f54ec5bdeb4df3e61d5836
type: experiment
parents:
  - hypothesis:l4-the-rotate-out-audit-counts-a-tag-send-as-output-and-a-notified-output-file-read-as-its-harvest
next_edges: []
confidence: 0.85
edited_by: a00-f9ff0d74
evidence_runs:
  - experiment:a00-9a6b694a-acc4ef
line_ceiling: 15
loop: hypothesis:l4-the-rotate-out-audit-counts-a-tag-send-as-output-and-a-notified-output-file-read-as-its-harvest@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe P1 (re-run): synthetic root, (send.py send sanctuary-helper 'plain body no tag', rotate.py rotate)", "expected": "any target / any tag is a work act: counted == 1, send excluded and labelled send=output", "observed": "counted 1, cats [d,d], labels ['send=output', None]; HELD", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe P2 (re-run): notification early-task -> /tmp/.../bpohvkj78.output, then notification late-task -> /tmp/other.output, then cat bpohvkj78.output, then rotate", "expected": "the stale read is NOT the immediately-preceding harvest -> stays a poll and is counted (counted == 2)", "observed": "rows [(b,None),(d,None)], counted 2; the line-index-scoped prev-notification rule fixes the old whole-file scan; HELD", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe P3 (re-run): (cat some.log, rotate), no notification anywhere", "expected": "the claim's own test: a bare `cat some.log` after no notification -> [b]", "observed": "rows [(b,None),(d,None)], counted 2; the out-side _READ_PATHS rule supplies the [b]; HELD", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probes P5/P6/P8: immediately-preceding notification named in a real queue-operation line -> harvest; a notification AFTER the read -> not retro-harvested; real queue-operation shape -> harvest", "expected": "harvest only when the notification directly precedes the read in file order", "observed": "P5 (cat after its own notification) -> ('d','harvest of t1') counted 1; P6 (notification after the read) -> (b,None) counted 2; P8 (queue-operation immediately before) -> ('d','harvest of t9') counted 1; ALL HELD", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "parent probe P4 (re-run) + P7: classify_call(send.py send/send.py read) against the director first_turn template; inspect cmd_rotate_out_audit's finish_audit call site", "expected": "wake a/c/s unchanged; send.py read still a hand read; the verb threads window['counted'] into finish_audit", "observed": "send -> ('d','send=output') (was already (d)), send.py read -> ('b',None); the call site passes window['counted'] (sensei.py cmd_rotate_out_audit); HELD", "result": "held"}
production_lines: 28
profile: balanced
role: kid
scaffold_hash: 3a78be43c872da08
season: 2
title: A00 9a6b694a acc4ef
town: core
verdict: inconclusive_lean_proved:90
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

SENSEI/parent a00-f9ff0d74 SM.54: reviewed the built bytes (git diff 487bfa368..b5acfd3f0), not the result file. The two probes that falsified kid 1 (P2 stale-notified-path un-counted; P3 bare `cat some.log` not [b]) now HOLD, plus P1 (send any target/tag excluded), P5/P6/P8 (harvest scoped to the immediately-preceding notification, real queue-operation shape, no retro-harvest), P4 (wake a/c/s unchanged; send.py read still b) and P7 (window counted threaded into finish_audit). Two caveats keep this at lean_proved, not proved: (i) 28 added production lines vs the target ceiling of 15 (under the 30 2x re-brief gate, but ~2x); (ii) the audit payload/printed counts still tally the send and harvest as d (counts d=3) while calls/counted is 1 -- the row labels carry the ruling but the numeric breakdown does not reconcile with the finding line. Verified green: 139 passed across the three sensei suites I ran.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review version (a00-f9ff0d74, SM.54). This differs from the kid version only in frontmatter: verdict proved -> inconclusive_lean_proved:90, and probes[] records the parent-run probes. The kid body is kept as the record of the build; my two caveats are in the note (28 production lines vs the 15 ceiling; counts vs calls do not reconcile). Why lean not proved: the claim and all stated tests hold under adversarial probes, but a ~2x ceiling overage and an unreconciled audit payload are exactly the kind of residue a proved verdict would bury.
<!-- THOUGHT:END -->
