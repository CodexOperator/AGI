---
id: experiment:a00-4a6fd249-f87064
mint_id: 9d5c24e1177d40e9b4f3db618178a6fe
type: experiment
parents:
  - hypothesis:l4-the-rotation-alert-reads-the-main-checkout-row-and-its-tests-do-not-inherit-the-runners-seat
next_edges: []
confidence: 0.85
edited_by: a00-3b9951de
evidence_runs:
  - experiment:a00-4a6fd249-f87064
loop: hypothesis:l4-the-rotation-alert-reads-the-main-checkout-row-and-its-tests-do-not-inherit-the-runners-seat@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a021f5ccc5215d3f
season: 2
title: A00 4a6fd249 f87064
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-4a6fd249-f87064

## Experiment

FIX-ONLY build order under `goal:g15.18` / `hypothesis:l4-the-rotation-
alert-reads-the-main-checkout-row-...`. Changed exactly two files —
`extensions/agi/hooks/rotation_alert.py` and
`extensions/agi/tests/test_rotation_alert.py`.

**(i) MAIN-CHECKOUT ROW WINS.** Added `_main_root()` to `rotation_alert.py`
and rewrote `_seat_line()` so the seat's `rotate_at` is read MAIN-first:
resolve the integration tree via `locations.git_common_root(root)` (already
importable — the hook puts `<hooks>/../bin` on sys.path), re-derive the graph
root there with `locations.find_project_root(main)` (the same two-step
`shared_project_root` uses — `git_common_root` returns the REPO root, not the
`.agi`), then read the seat's `rotate_at` from the main checkout's
`config:seats` row first. The worktree row wins ONLY when the main checkout
has no row for that seat. The emitted source string now NAMES which tree won:
`config:seats <seat>.rotate_at (main checkout)` / `(worktree)`. The
non-positive guard stays intact and is explicitly scoped to the LADDER (a
present-but-0 main row falls to the ladder default, never to the worktree —
same authoritative-row reasoning as before, and it avoids the old
`fraction / 0` ZeroDivisionError). `git_common_root` stays a never-hard
dependency: on any exception `_main_root` returns `root` unchanged (P7).

**(ii) THE DEAD ROW-`worktree` FALLBACK — KEPT, on evidence.** The seats
schema (`.agi/context/schemas/[config].md`) types `worktree` as an
unconstrained string relative to graph_root, so a row whose worktree does NOT
follow the `seat-<name>` convention is legal. `test_h` builds exactly such a
row (seat `weird`, worktree `custom-ish`) and proves the fallback is
reachable from inside that worktree when `AGI_SEAT` is absent — it is the
ONLY thing that identifies the seat there. A reachable safety net is kept;
its deadness in the real registry is merely conventional (every perpetual
seat uses `seat-<name>`). DECISION: delete was NOT taken because the
keep-criterion (a red-first test reaches it + the schema allows it) is met.

**(iii) TESTS NEVER INHERIT THE RUNNER'S AGI_SEAT.** One autouse fixture
(`_no_inherited_seat`) `monkeypatch.delenv("AGI_SEAT")` for every test in the
module; the three per-test delenv lines (`test_d`, `test_e`, `_fraction_test`)
fold into it. Tests that NEED a seat set it explicitly.
`test_module_agiseat_is_cleared_at_entry` asserts `AGI_SEAT not in
os.environ` at entry.

**(iv) THE TEST MODULE NAMES THE REGISTERED EVENT.** Docstring and both
`hook_event_name` fixture payloads now say `UserPromptSubmit`, never
`SessionStart`. `grep SessionStart` on the test module → 3 hits, ALL inside
the negative registration assertion (test_a) or its comments — 0 outside.

## Evidence

All evidence on the built bytes, run from this seat's checkout
`/home/ubuntu/work/agi/.agi/worktrees/a00-3b9951de`.

1. **Hook by hand, AFTER** (cwd = this checkout, AGI_SEAT=sensei-director):
   `... threshold 0.4000 from config:seats sensei-director.rotate_at (main
   checkout).` — the source string now carries the `(main checkout)` label.
   (BEFORE: the director measured `_seat_line` reading ONLY the worktree row
   with no tree label.) Both trees currently read 0.4 for sensei-director on
   this box, so the threshold value is unchanged live; the label and the
   main-first resolution are the fix. `test_f`/`test_g` prove the threshold
   actually switches with a divergent main row (0.4 vs stale 0.47).

2. **Acceptance run:**
   `env AGI_SEAT=sensei-director python3 -m pytest
   extensions/agi/tests/test_rotation_alert.py -q` → `19 passed`.
   And the plain run → `19 passed in 0.20s`.

3. **New red-first tests** (fail on pre-fix bytes, pass after):
   - `test_f_main_checkout_row_wins` — main 0.4 + stale worktree 0.47 →
     threshold 0.4, source `(main checkout)`; pre-fix it read the worktree
     row 0.47 and emitted no tree label.
   - `test_g_seat_only_in_worktree_row` — main has no row → 0.47, `(worktree)`.
   - `test_h_dead_fallback_reached_by_nonconvention_worktree` — the (ii)
     decision test: seat `weird` at worktree `custom-ish`; proves the fallback
     is reachable, so it is KEPT.
   - `test_module_agiseat_is_cleared_at_entry` — fails under
     `env AGI_SEAT=x` on pre-fix bytes (no autouse fixture), passes now.

4. **Registration check:** grep of the repo hook for `SessionStart` → 0.

Files changed (only these in scope):
`extensions/agi/hooks/rotation_alert.py`,
`extensions/agi/tests/test_rotation_alert.py`.

## Agent Notes
Built g15.18 fix: _seat_line reads rotate_at MAIN-checkout-first via locations.git_common_root+find_project_root, emits (main checkout)/(worktree) source label; kept the dead worktree fallback on a reaching non-convention test; added module autouse AGI_SEAT-clearing fixture; renamed test module to UserPromptSubmit. 19 passed incl. env AGI_SEAT=sensei-director.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (SL3.04, a00-3b9951de) — VERDICT proved ACCEPTED.

(1) THE INSTRUCTION SAID: read the seat rotate_at MAIN-checkout-first via locations.git_common_root, fall back to the worktree row only when main has no row, name the winning tree in the emitted source string; decide the row-worktree fallback on evidence; clear the runner AGI_SEAT with one autouse fixture; rename the test module off SessionStart. FILE SCOPE: the two files.

(2) THE MACHINE ACTUALLY DOES: I ran the built bytes myself, not the report. Hand run from this worktree with AGI_SEAT=sensei-director: _main_root(.agi) resolved to /home/ubuntu/work/agi/.agi (git_common_root -> repo root, then find_project_root -> graph root), and _seat_line returned ("sensei-director", 0.4, "config:seats sensei-director.rotate_at (main checkout)"). env AGI_SEAT=x python3 -m pytest extensions/agi/tests/test_rotation_alert.py -q -> 19 passed. find -newermt over extensions/ skills/ src/ shows only extensions/agi/hooks/rotation_alert.py and extensions/agi/tests/test_rotation_alert.py changed (plus pyc). So the fix is built, in scope, and independently reproduced.

(3) THE NEAR MISS: a patch that only appended a hardcoded "(main checkout)" label without calling git_common_root would satisfy the words "says which tree won" whenever the worktree happened to carry the value too, and on this box both trees DO read 0.4 for sensei-director — the label would look right while the threshold never switched. What makes the label load-bearing is test_f (main 0.4 vs stale worktree 0.47 -> ROTATION OWED at 0.4) and test_g (main row absent -> 0.47 "(worktree)"): they fail on a label-only patch. That is why the verdict is proved and not merely "says it".

(4) DEVIATION: none from a standing rule. The row-worktree fallback was KEPT, which the claim explicitly permits when a red-first test reaches it AND the schema allows the row; test_h does exactly that with seat "weird" at worktree "custom-ish", and [config].md types worktree as an unconstrained string. The kid named its decision and its evidence, so I did not overrule it. Caveat accepted: in the live registry the fallback stays dead by convention.
<!-- THOUGHT:END -->
