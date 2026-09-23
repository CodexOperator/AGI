---
id: experiment:a00-3a04e059-da77bd
mint_id: 33c44d146ce146b2812e2282df1b7a6e
type: experiment
parents:
  - hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself
next_edges: []
confidence: 0.85
edited_by: a00-c6d54e05
evidence_runs:
  - experiment:a00-3a04e059-da77bd
line_ceiling: 44
loop: hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself@s2
model: deepseek/deepseek-v4.1-flash
probes: "\"kid: probe_eligible.py (director/master/prime/parent/council, absent cells) all OK; pytest test_rotation_alert_captive.py 9 passed (3 red before build); hook binary direct: line=0.4700 ladder-default before sys.path fix -> 0.4000 row-owned after. PARENT-P1 wire: director f=0.42>=0.5*0.4 with AGI_HOOK_NO_SPAWN -> handoff + rotate-self --force recorded, stops names the captive ratio: HELD. PARENT-P2 auth: parent/prime/master-default at the same f -> no capture: HELD. PARENT-P2d auth: master with captive_rotate_masters true -> captures: HELD. PARENT-P3 gate: _merge_in_flight set -> no capture: HELD. PARENT-P4 gate: no captive cell -> no capture even at f=0.99: HELD. PARENT-P5 adversarial: two prompts under NO_SPAWN record twice -> CAVEAT, NOT a claim falsifier: NO_SPAWN short-circuits _gated_rotate gate-e before the latch, so the once-per-generation latch is unobservable under NO_SPAWN and the pre-existing _force_capture path records identically; named as a production hardening in THOUGHT.\""
production_lines: 81
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
Off by name until the ladder declares a captive cell. Ladder cells added live:
`captive_rotate_ratio: 0.85`, `captive_rotate_masters: false`.

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
PARENT REVIEW (a00-c6d54e05). (1) INSTRUCTION: the parent brief says "read each kid DIFF, never its result file ... run one negative probe per claim conjunct yourself ... a kid that passes its own suite but fails your probe is lean_disproved with the probe named". (2) MACHINE: I read the kid diff `git show a63959d87 -- extensions/agi/hooks/rotation_alert.py` (78+/3- : module-level sys.path.insert of ../src, `_captive_rotate_eligible`, `_captive_rotate`, `_force_capture(line=...)`, and the early return in main before the over_line branch) and ran six probes from /home/ubuntu/work/agi/.agi/worktrees/post-sensei-director/.agi/sessions/iter-154/a00-c6d54e05/probes_a.py against the built bytes: P1 wire, P2 auth (parent/prime/master-default), P2d auth (master+cell true), P3 gate (merge-in-flight), P4 gate (cells absent = off by name) all HELD; P5 (two prompts) is a CAVEAT not a falsifier. The claim conjuncts hold on the bytes. (3) NEAR MISS -- two artifacts nearly produced a FALSE falsification of a correct kid, both named so a reader can discount them: (a) my first probe run inherited AGI_POST=director-sanctuary from the parent process env, so `_seat_line` resolved the WRONG seat (a real registry row) and P1/P2d read FALSIFIED with n_caps=0; the fix was popping AGI_POST as well as AGI_SEAT -- the hook was right and the probe harness was wrong. (b) P5 double-records captures under AGI_HOOK_NO_SPAWN, but that is the test seam: `_gated_rotate` gate (e) declines BEFORE the once-per-generation latch is claimed, so NO_SPAWN cannot observe a latch and the pre-existing `_force_capture` path records identically; therefore P5 does not falsify the claim, it surfaces a PRODUCTION hardening (the captive path calls `_force_capture` with no gate (d) latch, so two prompts inside the rotate-self window could spawn twice -- the same unlatched shape the accepted conjunct-2 force already carries, made more reachable by the lower 0.85x line). Left for the next kid, not a demotion. (4) NO DEVIATION from the standing rules. Kid deviations accepted and recorded: (i) off by NAME, not default-0.85-when-absent (so the captive path cannot break the byte-identical over-line tests); (ii) the 7-line module-level sys.path.insert -- I verified the necessity: run directly the hook had no `src` on sys.path, `geometry_config.load_rows` returned [] and the DIRECTOR role was invisible, i.e. production-dead while the suite stayed green; the fix is the right one and the hook now reads row-owned rotate_at. CAVEATS: 81 production lines against the owner slice estimate of 12 (1.84x the node resolved 44, under the 2x 88 stop, so no rebrief was owed) -- the overage is the sys.path fix plus the eligibility/capture split; and the unlatched captive spawn above.
<!-- THOUGHT:END -->

## Agent Notes
Built trigger (a): rotation_alert.py captively rotates a DIRECTOR at f >= captive_rotate_ratio x line (ratio/masters ladder cells, off-by-name default), reusing _force_capture with a captive stops line; 9 new tests + 108 regression pass. Found and fixed a production-dead seat-row read (hook lacked src/ on sys.path). production_lines 81/ceiling 44.
