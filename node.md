---
id: experiment:a00-8cf36a73-62bc40
mint_id: a6f47c00bf2f417587c6a90bf8b9f957
type: experiment
parents:
  - hypothesis:l5-the-overdue-alarm-re-fires-every-thirty-minutes-after-the-first
next_edges: []
confidence: 0.9
edited_by: a00-fbb28030
evidence_runs:
  - experiment:a00-8cf36a73-62bc40
  - experiment:a00-4c333b16-c61111
line_ceiling: 40
loop: hypothesis:l5-the-overdue-alarm-re-fires-every-thirty-minutes-after-the-first@s2
model: deepseek/deepseek-v4.1-flash
probes: "C2 gate (naming conjunct, the one kid 1 failed) — PASS on these bytes: raw dm blocks in the director inbox are [0] 'iter=iter-Q agent=kid-q reason=overdue' (first firing, byte-identical — negative control) and [1] 'iter=iter-Q agent=kid-q reason=overdue elapsed_m=31 pid=555111' (repeat names elapsed minutes and the pid). C1 gate (re-fires every window) re-probed on these bytes — PASS: 1/1/2/2 dms across first, in-window, 31m-backdated, fresh-window passes. C3 gate (dead pid must not be rescued by an old repeat stamp) — PASS: with overdue_last_alarm an hour old and the adapter reporting the pid dead, the record takes the DEATH path (status=failed, fail_reason='pid ... died (detected by reaper)'), manifest mirrors failed. Wire (mirror) — PASS: manifest overdue_last_alarm == agent.json overdue_last_alarm after the repeat. Wire (call site) — PASS: only the repeat call site passes detail=, so death/timeout bodies are untouched (test_dispatch_alarms.py 9 passed). Regression on changed bytes: test_heal_watch+test_brief+test_cli+test_spawn_budget = 320 passed."
production_lines: 24
profile: balanced
role: kid
scaffold_hash: 45886c119b8605b0
season: 2
title: The repeat overdue dm names its elapsed minutes and pid, and mirrors its stamp
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-8cf36a73-62bc40

## Experiment

Closes conjunct **C2** of
`hypothesis:l5-the-overdue-alarm-re-fires-every-thirty-minutes-after-the-first`:
the REPEAT overdue dm must name, **in the body the recipient reads**, the
elapsed minutes and the pid — not only in the reaper log line.

Parent kid `a00-4c333b16` built the re-firing cadence (commit `285548917`);
my probe of those bytes found the repeat dm body byte-identical to the first
firing's: `iter=iter-P1 agent=kid-p1 reason=overdue`. The receiver could not
tell a repeat from a first firing, nor how overdue the pid was.

### What changed (diff vs HEAD, `extensions/agi/bin/heal.py`, +24/-6)

1. `_alarm_dispatcher` gains an optional `detail: str = ""` suffix appended to
the dm body (`iter=... agent=... reason=... <detail>`). Default empty, so
DEATH / TIMEOUT / first-OVERDUE callers are byte-for-byte unchanged.
2. The repeat branch passes
`detail=f"elapsed_m={elapsed // 60} pid={pid}"`, producing e.g.
`iter=iter-U agent=kid-u reason=overdue elapsed_m=31 pid=424242` — ONE line,
`reason=overdue` still a token so existing counters resolve.
3. The repeat branch now MIRRORS `overdue_last_alarm` onto the matching
manifest entry (the first firing already mirrors `overdue_since` /
`overdue_reason`), so a manifest-only reader can see the repeat happened.

Status still stays `running`; the DEATH path is untouched; exactly one repeat
dm per window. The FIRST firing's body deliberately stays exactly
`iter=<iter> agent=<id> reason=overdue` (constraint 1: sibling hypothesis
`l4-a-round-alarms-its-dispatcher-by-default` owns it and other tests key on
the shape). Where the node's claim says "each occurrence naming elapsed minutes
and the pid", the repeat occurrences do; the first firing is pinned by the
sibling claim, so I did not change it. Recorded, not silently dropped.

## Evidence

Test file: `extensions/agi/tests/test_heal_watch.py` (+74), two new tests:

* `test_overdue_repeat_dm_body_names_minutes_and_pid` — asserts on the parsed
  **dm body** (`_dm_bodies` splits the inbox block on the header/body blank
  line): first body is exactly `iter=iter-U agent=kid-u reason=overdue`
  (negative control) and the second contains `reason=overdue`, `elapsed_m=31`,
  `pid=424242`; a third pass inside the window sends nothing.
* `test_overdue_repeat_stamp_is_mirrored_onto_the_manifest` — the repeat's
  `overdue_last_alarm` on `agent.json` equals the manifest entry's, status
  still `running`.

**Pre-fix check (required):** temporarily reverting only the repeat branch to
kid 1's bytes (comment + mirror + detail removed; restored immediately after)
and running the two new tests against those bytes:

```
python3 -m pytest extensions/agi/tests/test_heal_watch.py -q \
  -k "overdue_repeat_dm_body or mirrored_onto_the_manifest"
2 failed, 68 deselected in 0.84s
AssertionError: manifest mirrors the repeat stamp
assert None == 1789678498
```

Both new tests FAIL on the pre-fix bytes (no `elapsed_m`/`pid` in the repeat
body; no mirror), so they prove the fix rather than restating it.

**On the built bytes** (exact command and result):

```
python3 -m pytest extensions/agi/tests/test_heal_watch.py -q
70 passed, 12 warnings in 3.86s

python3 -m pytest extensions/agi/tests/test_dispatch_alarms.py \
  extensions/agi/tests/test_heal_watch.py \
  extensions/agi/tests/test_no_live_root_writes.py \
  extensions/agi/tests/test_kid_reports_to_parent.py -q
102 passed, 13 warnings in 6.40s
```

Production lines: `git diff --numstat -- extensions/agi/bin/heal.py` =
`24  6`, under the 40-line ceiling (`production_lines: 24`).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) WHAT THE INSTRUCTION SAID. The target's `testable_claim`: "heal watch
re-sends the overdue dm for a live agent every comms.overdue_repeat_min
(default 30) minutes after the first firing, each occurrence naming elapsed
minutes and the pid, and never cuts a replacement for a pid that is still
alive." My brief to this kid named the conjunct I had just falsified on its
predecessor: "Make the REPEAT occurrence name elapsed minutes and the pid in
the dm body the dispatcher actually receives, not just in the log line", plus
the mirror divergence my probe found.

(2) WHAT THE MACHINE ACTUALLY DOES. I read this kid's diff
(`git diff 285548917..7247da491`: heal.py +30/-6, test_heal_watch.py +74) and
ran my own probes from
`.agi/sessions/iter-L5.12/a00-fbb28030/probe.py` and `probe2.py` against the
committed bytes, not its tests. `_alarm_dispatcher` gained an optional
`detail` suffix and the repeat call site passes `detail=f"elapsed_m={elapsed //
60} pid={pid}"`; the same block now mirrors `overdue_last_alarm` onto the
manifest entry. My probe reads the two dm blocks in the director inbox raw:
`[0] 'iter=iter-Q agent=kid-q reason=overdue'` (first firing, byte-identical,
negative control holds) and `[1] 'iter=iter-Q agent=kid-q reason=overdue
elapsed_m=31 pid=555111'` (repeat, names minutes and pid). Cadence re-probed
on these bytes: 1 dm first pass, 1 in-window, 2 past the 31m-backdated window,
2 in the fresh window — one dm per window, not per pass. Manifest mirror
verified live (`overdue_last_alarm` equal on agent.json and the manifest
entry). Dead-pid gate: a record with an old `overdue_last_alarm` but an
adapter reporting the pid dead takes the DEATH path (`status=failed`,
`fail_reason='pid ... died (detected by reaper)'`) — the repeat never rescues
a dead pid. Regression on the changed bytes:
`test_heal_watch.py test_brief.py test_cli.py test_spawn_budget.py` = 320
passed, `test_dispatch_alarms.py` = 9 passed.

(3) THE NEAR MISS. Appending the detail to the SHARED `_alarm_dispatcher`
body instead of to the repeat call site would have widened every death and
timeout dm, breaking the sibling hypothesis
(`hypothesis:l4-a-round-alarms-its-dispatcher-by-default`) and the
`test_dispatch_alarms.py` exact-body assertions, while still satisfying "the
repeat dm names the minutes". The kid gated it behind an optional `detail`
kwarg that only the repeat site passes, which is why the death/timeout bodies
are untouched.

(4) RESIDUAL, recorded as a caveat rather than patched by me. The FIRST
firing's dm still names neither elapsed minutes nor pid — deliberate, to keep
the one-dm-per-event sibling intact and `reason=overdue` counters resolving;
if "each occurrence" is read to include the first firing, that conjunct is
unmet and this node is the wrong place to fix it. `overdue_reason` names the
elapsed time in SECONDS, not minutes. My verdict is `proved` against the
claim as written (re-fires, repeat names minutes+pid, live pid never
replaced), citing both experiment nodes as evidence.
<!-- THOUGHT:END -->

## Agent Notes
Repeat overdue dm body now names elapsed_m and pid (detail suffix on _alarm_dispatcher); repeat stamp mirrored onto manifest; first-firing body unchanged; 2 new tests fail on pre-fix bytes, 70 passed on built bytes; heal.py +24/-6, under 40-line ceiling.
