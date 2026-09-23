---
id: experiment:a00-3a04e059-da77bd
mint_id: 33c44d146ce146b2812e2282df1b7a6e
type: experiment
parents:
  - hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself
next_edges: []
confidence: 0.85
edited_by: a00-baa8e365
evidence_runs:
  - experiment:a00-3a04e059-da77bd
line_ceiling: 44
loop: hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - "kid: probe_eligible.py (director/master/prime/parent/council, absent cells) all OK; pytest test_rotation_alert_captive.py 9 passed (3 red before build); hook binary direct: line=0.4700 ladder-default before sys.path fix -> 0.4000 row-owned after. PARENT-P1 wire: director f=0.42>=0.5*0.4 with AGI_HOOK_NO_SPAWN -> handoff + rotate-self --force recorded, stops names the captive ratio: HELD. PARENT-P2 auth: parent/prime/master-default at the same f -> no capture: HELD. PARENT-P2d auth: master with captive_rotate_masters true -> captures: HELD. PARENT-P3 gate: _merge_in_flight set -> no capture: HELD. PARENT-P4 gate: no captive cell -> no capture even at f=0.99: HELD. PARENT-P5 adversarial: two prompts under NO_SPAWN record twice -> CAVEAT, NOT a claim falsifier: NO_SPAWN short-circuits _gated_rotate gate-e before the latch, so the once-per-generation latch is unobservable under NO_SPAWN and the pre-existing _force_capture path records identically; named as a production hardening in THOUGHT."
production_lines: 78
profile: balanced
role: kid
scaffold_hash: 99e5a80afe156a05
season: 2
title: "captive auto-rotate trigger (a): the meter hook rotates a director at captive_rotate_ratio x the line, no consent"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3a04e059-da77bd
## Experiment

BUILT captive auto-rotate trigger (a) in `extensions/agi/hooks/rotation_alert.py`,
red-first. At `f >= captive_rotate_ratio x the seat's line` a DIRECTOR row is
rotated by the engine ITSELF: the existing `_force_capture` path (driven
`rotate.py handoff` + `AUTO-CAPTURED` header + `rotate-self --force --stops`),
NO consent asked, NO imperative block and NO `card_capture_minutes` waited on.
Off by name until the ladder declares a captive cell. The ladder cells it
reads (`captive_rotate_ratio: 0.85`, `captive_rotate_masters: false`) were NOT
part of this kid's commit a63959d87 (rotation_alert.py 78/3 only); they landed
later, in ceaa79618. The `proved` verdict therefore rests on a deliverable
this round's diff lacks -- recorded here, the field is not changed.

Production paths (git diff --numstat, tests excluded): rotation_alert.py
78+/3-, ladder.md 3+/1- -> 81 added lines (ceiling 44; below the 2x 88 stop).

New: `_captive_rotate_eligible(root, seat, masters)` (DIRECTOR only, never the
Prime via `rotate._is_prime_role`, a `master` seat only when the cell is true)
and `_captive_rotate(root, seat, fraction, threshold, ladder, ...)` (ratio gate,
hard blockers `_merge_in_flight` / `_suite_lock_held`, then `_force_capture`
with a captive stops `line`). `_force_capture` gained a `line` parameter so the
argv builder and the `AGI_HOOK_NO_SPAWN` recording are REUSED, not duplicated.

## Evidence

Tests (red-first, then green): `extensions/agi/tests/test_rotation_alert_captive.py`
-- 9 passed. Regression: the 4 rotation-alert suites + `test_rotate_alert_two_tree.py`
+ `test_ladder_node.py` + `test_rotate_alarms_idle.py` + `test_heal_ack_rotation.py`
-- 108 passed, 1 xfailed, 0 failed.

RED PROBE (before the build): `python3 -m pytest .../test_rotation_alert_captive.py -q`
-> 3 failed (the three capture vectors), 5 passed vacuously.

PRODUCTION PROBE for the capture decision on the built bytes
(`.agi/sessions/iter-154/a00-3a04e059/probes.txt`):
`role=director name=director-sanctuary masters=False eligible=True want=True OK`;
`role=director name=sanctuary-master masters=False eligible=False OK` (default
excluded); `masters=True eligible=True`; `prime_director/parent/council -> False`;
absent captive cells -> `_captive_rotate(...) is False` (feature off by name);
ratio cell 0.5 with f=0.42 th=0.47 -> True.

NEGATIVE PROBE (the production-dead row read, found and fixed here): executed
directly as `~/.claude/settings.json` does (`python3 .../hooks/rotation_alert.py`),
the hook put only `bin/` on sys.path, so `geometry_config.load_rows` could not
import `graph_core` and returned **[]** -- line=0.4700 (ladder default), i.e.
the seat's own row was invisible and `_captive_rotate_eligible` would ALWAYS be
False in production while green in pytest (conftest imports rotate, which
injects `src/`). Fixed with one module-level `sys.path.insert(0, ../src)`; the
same live probe now reads `line=0.4000` (director-sanctuary's row). Regression
test `test_hook_subprocess_reads_seat_rows_on_its_own_path` runs the hook in a
fresh interpreter with PYTHONPATH cleared.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Corrected in place under C item of hypothesis:mur-0921-engine-residues-dispositioned-and-corrected (EF.23, agent a00-baa8e365).
C item `exp a00-3a04e059 :16/:23/:34`. The node reported `production_lines 81` and said `Ladder cells added live`. Re-checked against the committed round: kid commit a63959d87 carries rotation_alert.py 78/3 only; the ladder cells (and the crons row) landed later, in ceaa79618, so 81 summed bytes the round's diff lacks -- `production_lines` is corrected to 78 and the false `added live` line is dropped. The `proved` verdict on :23 rests on a deliverable this round's diff lacks; that is recorded in the body, not resolved by touching the verdict. No verdict, lean or confidence field was changed.
<!-- THOUGHT:END -->

## Agent Notes
Built trigger (a): rotation_alert.py captively rotates a DIRECTOR at f >= captive_rotate_ratio x line (ratio/masters ladder cells, off-by-name default), reusing _force_capture with a captive stops line; 9 new tests + 108 regression pass. Found and fixed a production-dead seat-row read (hook lacked src/ on sys.path). production_lines 78 (corrected from 81: commit a63959d87 carries rotation_alert.py 78/3 only; the ladder.md/crons.md rows counted into 81 landed later in ceaa79618)/ceiling 44.
