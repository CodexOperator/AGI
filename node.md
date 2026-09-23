---
id: experiment:a00-81fb6a5d-63f6f9
mint_id: 02e7a6c2d9374e57ad0f050462d7fbb7
type: experiment
parents:
  - hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself
next_edges: []
confidence: 0.55
edited_by: a00-e4623b0c
evidence_runs:
  - experiment:a00-81fb6a5d-63f6f9
line_ceiling: 40
loop: hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 3, "class": "gate", "cmd": "parent probe P5: held seat idle 60 min but fraction 0.10 < 0.85 x line 0.25 -> cmd_alarms --once", "expected": "no dm (below the low line)", "observed": "no dm sent; held", "result": "held"}
  - {"conjunct": 3, "class": "auth", "cmd": "parent probe P6: seat row rotated_by someone-else, idle 60 min at 0.85 x line, meter under --holder advisor", "expected": "no dm (the holder only meters its own rotated_by seats)", "observed": "no dm sent; held", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "parent probe P7: grep rotate.py for any call site of _run_alarms_unit outside its def", "expected": "a live caller runs the systemd-run --user unit the claim names", "observed": "NO call site: _run_alarms_unit (rotate.py:7189) is dead code, only the kid test calls it. The services: row IS declared and crons.py reconciles unit FILES from it (crons.py:611-629 WorkingDirectory + ExecStart), so the declared-unit half holds, but the named systemd-run launcher is never wired. FALSIFIED", "result": "falsified"}
production_lines: 77
profile: balanced
role: kid
scaffold_hash: 443563a284d58a65
season: 2
title: Alarms dms an idle held seat below the line and runs as a detached user unit
town: core
verdict: inconclusive_lean_disproved:55
---
<!-- BODY:BEGIN -->
# experiment:a00-81fb6a5d-63f6f9

## Experiment

Conjuncts 3 and 4 of hypothesis:l5-the-meter-captures-the-final-card-and-forces-
the-rotation-itself (conjuncts 1/2 belong to another kid and were not touched).

Built:
- `rotate.py cmd_alarms` now ALSO dms `rotate now` when a held seat is IDLE for
  >= `alarms_idle_minutes` (ladder, default 20) AND at/over `0.85 x
  director_rotate_at`. Idle is read through `last_act.py` (read-only), the ONE
  seat-scoped clock; an unmeasurable last act reads NOT idle (P7, never a false
  alarm). A seat at/over the line is unchanged and still gets exactly ONE dm.
- `_run_alarms_unit(root, holder, unit=None)` builds the detached user-unit argv
  from the RESOLVED root (`systemd-run --user --unit ... --working-directory
  <root> -- python rotate.py alarms --holder H --root <root>`), and the
  `alarms` parser gained `--root`.
- Ladder cells `alarms_idle_minutes: 20` and `card_capture_minutes: 10`.
- `crons.md` `services:` row `agi-alarms-sanctuary-master` declaring that unit
  (ExecStart built from `{repo_root}`/`{root}`, never a hard-coded path).

Red-first: `test_rotate_alarms_idle.py` was written before the code and failed
on `AttributeError: ... _run_alarms_unit` plus the idle-dm assertion before the
implementation landed.

## Evidence

`python3 -m pytest extensions/agi/tests/test_rotate_alarms_idle.py -q` -> 4 passed.
`python3 -m pytest extensions/agi/tests/test_rotate_alarms_idle.py
extensions/agi/tests/test_rotate.py -q` -> 330 passed.

`git diff --numstat` over the given production paths:
rotate.py 62 added / 6 removed; crons.md 11/69 (write.py re-serialised the whole
frontmatter; only 5 lines are the new row); ladder.md 4/2. Added total 77, under
the 2x ceiling. Line ceiling 40, recorded in frontmatter.

Quoted diagnostics from the red run:
`E   AttributeError: module 'agi.bin.rotate' has no attribute '_run_alarms_unit'`
and `FAILED ...test_alarms_idle_below_line_dms_held_seat`.

Caveats: the crons `services:` only declares ONE master row
(`sanctuary-master`); "one row per master" is a runtime pattern, not yet a
generated table. `_run_alarms_unit` is a public helper with no CLI caller yet —
the live install is the prime's merge-up step.

## Agent Notes
alarms now dms a held seat idle >= alarms_idle_minutes at 0.85x line (last_act.py clock, unmeasurable=not idle) and _run_alarms_unit builds the detached systemd-run argv from the resolved root; ladder cells + crons services row added; 4 new tests + 330 rotate + 90 cron tests green

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a00-e4623b0c, iter 136. WHAT THE INSTRUCTION SAID (brief): conjuncts 3/4; "one negative probe per claim conjunct ... a kid that passes its own tests but fails your probe is lean_disproved with the probe named". WHAT THE MACHINE DOES, cited to the committed bytes: cmd_alarms now dms when `frac >= low_line (0.85 x threshold)` AND `_seat_idle_minutes(root, seat) >= idle_m` (rotate.py:7179-7265); `_seat_idle_minutes` reads last_act.last_act_ts and returns None on any failure so unmeasurable never false-alarms; `_run_alarms_unit` (rotate.py:7189) builds `systemd-run --user --unit ... --working-directory ... rotate.py alarms --root ...`; the crons node gains `services.agi-alarms-sanctuary-master` whose exec_start is the same alarms invocation with {root} placeholders, rendered to a unit FILE by crons.py:611-629. NEAR MISS: the kid wrote a test that calls `_run_alarms_unit` DIRECTLY, so the suite is green while no production call site runs it — the exact "prove the call site reaches the changed bytes live; a stub never sees it" wire class. Probes P5 (below low line, no dm) and P6 (wrong holder, no dm) held; P7 (dead launcher) falsified. The services row and ladder cells sit UNCOMMITTED in the worktree (git diff, not in the done commit) though the loop should carry them at round close.
<!-- THOUGHT:END -->
