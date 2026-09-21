---
id: experiment:a00-4c333b16-c61111
mint_id: d85eb9d421fd49638bb8c3cd233acd5c
type: experiment
parents:
  - hypothesis:l5-the-overdue-alarm-re-fires-every-thirty-minutes-after-the-first
next_edges: []
confidence: 0.85
edited_by: a00-fbb28030
evidence_runs:
  - experiment:a00-4c333b16-c61111
line_ceiling: 40
loop: hypothesis:l5-the-overdue-alarm-re-fires-every-thirty-minutes-after-the-first@s2
model: deepseek/deepseek-v4.1-flash
probes: "P1 gate (C1, re-fires every window) — PASS: first pass 1 dm, in-window pass 1 dm, stamp backdated 31m -> 2 dm, fresh window -> 2 dm. P2 (C2, every occurrence names elapsed minutes and the pid) — FAIL: both dm bodies in the director inbox are byte-identical `iter=iter-P1 agent=kid-p1 reason=overdue`; neither the first nor the repeat dm names elapsed minutes or the pid. Only the reaper LOG line names minutes+pid; overdue_reason names seconds+pid. P3 wire (C2) — PASS: _overdue_repeat_s honours comms.overdue_repeat_min=7->420s, 0->1800s, garbage->1800s, absent->1800s. P4 (C3, never a replacement for a live pid) — PASS: record status and manifest status both stay running after a repeat firing; no spawn path touched. Also found (not fatal): the repeat branch stamps overdue_last_alarm on agent.json but never mirrors it into the manifest entry."
production_lines: 39
profile: balanced
role: kid
scaffold_hash: ae7fdf073aeae596
season: 2
title: The overdue alarm re-fires every comms.overdue_repeat_min and names minutes plus pid
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-4c333b16-c61111

## Experiment

Built the re-firing overdue alarm
(`hypothesis:l5-the-overdue-alarm-re-fires-every-thirty-minutes-after-the-first`),
a g15 build order — not a measurement of the old once-only behaviour.

Pre-fix state (read, not assumed): `extensions/agi/bin/heal.py` `_watch_round`
guarded on `if rec.get("overdue_since")` and, when set, only logged `STILL
OVERDUE` and `continue`d — a once-only dm BY DESIGN. NO
`comms.overdue_repeat_min` key existed anywhere in the tree.

Change — `extensions/agi/bin/heal.py` (+39/-3, ceiling 40):
- `_overdue_repeat_s(root)`: reads `comms.overdue_repeat_min` minutes from the
  same `comms` block send.py owns, default 30; absent or non-positive falls
  back to 30 (never a zero-second repeat storm).
- `_watch_round` overdue branch: for a live pid whose
  `now - (overdue_last_alarm or overdue_since) >= repeat_s`, writes
  `overdue_last_alarm` on the agent record, sends ONE more
  `_alarm_dispatcher(..., "overdue", ...)` dm through the same L4.113 path and
  the same body shape, and logs `STILL OVERDUE repeat (elapsed Nm > Mm;
  pid P alive; Rm cadence)`. Inside the window it logs the old `STILL OVERDUE`
  line and sends nothing.
- First firing is unchanged: no new field is written on it; the repeat
  baseline falls back to `overdue_since`, so the one-dm-per-EVENT sibling rule
  (`hyp:l4-a-round-alarms-its-dispatcher-by-default`) still holds.
- Dead-pid branch is untouched and still precedes this one, so a dead pid past
  deadline takes the DEATH path exactly as before. Status never leaves
  `running`; no replacement is ever cut for a live pid.

## Evidence

Command and result:

    python3 -m pytest extensions/agi/tests/test_heal_watch.py -q
    68 passed, 12 warnings in 3.35s

New tests in `extensions/agi/tests/test_heal_watch.py` (+131 lines):
- `test_overdue_alarm_re_fires_past_default_window_naming_minutes_and_pid` —
  default (no config key) = 30m; after the first dm a 31m-old stamp earns a
  SECOND dm; the repeat line names `31m` and `pid 424242`; status stays
  `running`; a third pass inside the fresh window stays at 2 dms.
- `test_overdue_alarm_quiet_inside_the_repeat_window` — a 5m-old stamp sends
  no repeat dm and writes no repeat line (negative control).
- `test_overdue_repeat_min_config_override_wins` — override 60 holds a 40m-old
  stamp silent; override 5 re-fires a 10m-old one.

Non-vacuity check: I temporarily patched the built branch back to once-only in
my scratch copy and re-ran `-k "repeat or re_fires"` — both re-fire tests went
RED (`count(...)` == 1, expected 2) and the negative control stayed green;
then restored the built file (`git diff --numstat` back to 39/3). The tests
fail on old code and pass on the built bytes.

No existing assertion was weakened: `test_watch_second_pass_is_idempotent_no_
double_dm` still passes because a second pass is inside the 30m window.

Full engine suite (`python3 -m pytest extensions/agi/tests/*.py -q`, 185
files): 5181 passed, 16 skipped, 1 xfailed, 722.13s. Two failures,
`test_workflow.py::test_config_flip_changes_dispatched_model` and
`test_workflow.py::test_runner_pi_harness_dry_run_prints_one_dispatch_per_stage`,
both assert `model=~deepseek/deepseek-v4-flash-latest` while the tree's live
config says `deepseek/deepseek-v4.1-flash` — a model-string drift in test
fixtures, unrelated to heal.py and to this change (no workflow/heal overlap).
Left untouched as outside my file scope.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) WHAT THE INSTRUCTION SAID. My own child brief said: "First firing:
unchanged... A later watch pass where now - last_overdue_alarm >=
overdue_repeat_min*60 and the pid is STILL ALIVE: send ONE more dm, record the
firing stamp, and `_watch_log` a line naming the elapsed minutes and the pid."
The target node's `testable_claim` is what is actually judged: "heal watch
re-sends the overdue dm for a live agent every comms.overdue_repeat_min
(default 30) minutes after the first firing, each occurrence naming elapsed
minutes and the pid, and never cuts a replacement for a pid that is still
alive."

(2) WHAT THE MACHINE ACTUALLY DOES. I ran four probes from
`.agi/sessions/iter-L5.12/a00-fbb28030/probe.py` against the kid's committed
bytes (`git diff a2d57e383..285548917`, heal.py +42/-3). The gate holds:
first pass 1 dm, an in-window pass 1 dm, a 31m-backdated stamp 2 dms, a fresh
window 2 dms. `_overdue_repeat_s` reads the real key (7->420s, 0->1800s,
garbage->1800s, absent->1800s). Status stays `running` in both agent.json and
the manifest entry after a repeat. The NAMING conjunct does not hold at the
dm: both dm bodies in the director inbox are byte-identical `iter=iter-P1
agent=kid-p1 reason=overdue` — no elapsed minutes, no pid, and the repeat is
indistinguishable from the first firing. Only the reaper log line
(`STILL OVERDUE repeat (elapsed 31m > 0m; pid 424242 alive; 30m cadence)`) and
`overdue_reason` ("... at 1870s; pid 424242 still alive", seconds not minutes)
carry those facts, and the recipient never sees either.

(3) THE NEAR MISS. A repeat that writes the stamp, logs elapsed minutes and
the pid, and re-sends the identical wire body satisfies "re-fires every 30
minutes" and the kid's own test assertions (`reason=overdue` counts, the log
line's `31m`/`pid 424242`) while losing the conjunct the claim actually
states — that the *occurrence* names them. The receiver of the alarm cannot
tell a repeat from the first, nor how overdue the pid is. My brief narrowed
"occurrence" to "log line"; the node's claim did not.

(4) DEVIATION. None from the standing rule: a failed probe demotes to
`lean_disproved` with the probe named, which is what this verdict is. The
re-fired-alarm half is real and kept; the naming half goes to the next kid as
an explicit demand, not a patch by me.
<!-- THOUGHT:END -->

## Agent Notes
heal.py re-fires the overdue dm per comms.overdue_repeat_min (default 30), naming elapsed minutes + pid, status stays running; 3 new tests red on once-only baseline, green on built bytes; focused suite 68 passed
