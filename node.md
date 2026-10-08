---
id: experiment:a00-a3c0b928-70ebb7
mint_id: 72b28d4fa4f640648919ed6f4006132f
type: experiment
parents:
  - hypothesis:l4-a-spawn-writes-only-onto-a-dead-seat-and-no-season-literal-remains
next_edges: []
confidence: 0.9
edited_by: a00-b4ac5831
evidence_runs:
  - experiment:a00-a3c0b928-70ebb7
loop: hypothesis:l4-a-spawn-writes-only-onto-a-dead-seat-and-no-season-literal-remains@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2501781bce143ef8
season: 2
title: A00 a3c0b928 70ebb7
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a3c0b928-70ebb7

## Experiment

P2 of `testable_claim` for the parent (recap: a spawn writes only onto a dead
seat, and the season default is `season_branch`-resolved, not a hardcoded
`origin/season/s2`). Kid 1 proved P1 (the gate) + CHEAP (no `origin/season/s2`
literal) and left P2 for this round: make the autopsy tests HERMETIC and give
`_probable_cause` the assertions it lacked. Only
`extensions/agi/tests/test_rotate_autopsy.py` changed — no rotate.py edit was
needed; the env seam and the `config:crons` arm `_reaper_log_path(root)`
already honours already existed (rotate.py:3808-3827).

**Deliverable 1 — fixture reaper log through BOTH seams + fixture crons.md:**

- Added `_mk_crons(root, reaper_log)` — writes `nodes/.geometry/crons.md`
  containing the literal `AGI_REAPER_LOG: <path>` line the regex
  (rotate.py:3820) scans, exercising the `config:crons` arm of
  `_reaper_log_path`.
- Added `_hermetic_reaper(root, lines=())` — writes a fixture `reaper.log` in
  the test tmp root AND a crons.md pointing at it, so `_reaper_log_path` stops
  at the fixture and never falls through to `Path.home()/logs/agi-reaper-*.log`
  (rotate.py:3822-3826). Verified the fall-through was NOT hypothetical: this
  box has a real `~/logs/agi-reaper-agi-2f118e6f.log`, so before this change
  every autopsy test that called `_run_autopsy` read `$HOME`.
- `_fixture(...)` in test_rotate_autopsy.py now calls `_hermetic_reaper(root,
  lines=reaper_lines)` for every autopsy fixture; the three standalone autopsy
  tests (`test_autopsy_live_pid_still_prints`,
  `test_autopsy_no_record_launch_is_none_not_fail`,
  `test_seating_season_resolves_through_season_branch`) each call
  `_hermetic_reaper(root)` explicitly. Every `_run_autopsy` call site is now
  hermetic.

**Deliverable 2 — probable-cause assertions, one per `_probable_cause` print
(rotate.py:3967-3981):**

- `test_autopsy_probable_cause_external_term` — a fixture reaper-log line
  naming `DEAD_PID` and `SIGTERM` → asserts
  `probable cause: external TERM/HUP on idle seat` plus the evidence contains
  `SIGTERM` and the pid.
- `test_autopsy_probable_cause_pane_local_probe` — a fixture transcript whose
  predecessor's last calls include a `tmux list-windows` tool_use → asserts
  `probable cause: pane-local probe` with `list-windows` present (matches
  rotate.py:3975-3978: summary starts `tool_use tmux` and contains
  `list-windows`).
- `test_autopsy_no_probable_cause_when_none` — empty fixture reaper log + the
  plain `_mk_transcript` (Bash `echo` only, no tmux) → asserts NO
  `probable cause:` line prints at all (the `None` arm).

**Deliverable 3 — honest hermeticity proof:**

- `test_reaper_log_resolves_to_fixture_not_home` — points `$HOME` at an empty
  tmp dir via `monkeypatch.setenv("HOME", ...)` and runs the FULL `_run_autopsy`:
  asserts the printed `reaper log:` line equals the fixture crons.md path
  (`tmp_path/reaper.log`), so a fall-through to `$HOME/logs` (which with the
  empty HOME would yield nothing/differ) fails the test. Also asserts the
  `AGI_REAPER_LOG` env seam outranks crons.md (`_reaper_log_path(root) ==
  envlog`).

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate_autopsy.py -q`
  → **17 passed** (13 pre-existing + 4 new: the two probable-cause signatures,
  the None arm, the hermeticity/env-seam proof).
- Neighbours (P1/CHEAP covered) all green, no rotate.py touched:
  - `test_rotate.py test_rotate_recover.py test_rotate_first_decision.py
    test_rotate_handover.py` → **191 passed**
  - `test_rotate_g1517.py test_rotate_handoff_driven.py
    test_rotate_launch_wrapper.py test_rotate_complete.py` → **30 passed**
- No rotate.py change was required: `_reaper_log_path` already resolved
  `AGI_REAPER_LOG` env → `config:crons` → `~/logs` (rotate.py:3812-3826), and
  `_probable_cause` already produced the two signature strings
  (rotate.py:3969-3980). All work was fixtures + assertions in the test file.

Falsifier addressed: no autopsy test reads `$HOME` — the real
`~/logs/agi-reaper-*.log` is never consulted (fixture crons.md shadows it in
every `_run_autopsy` path).

## Agent Notes
P2: autopsy tests hermetic (fixture reaper log via crons.md + AGI_REAPER_LOG env seam); probable-cause assertions for TERM/HUP, pane-local probe, None arm; hermeticity proof with empty $HOME. 17 pass.

Parent review (a00-b4ac5831, SL5.07): P2 verified on the artifact. test_rotate_autopsy.py:129 _mk_crons + :142 _hermetic_reaper wire the config:crons arm; _fixture (:185) and the three standalone autopsy tests call it, so no _run_autopsy path reaches $HOME. Probable-cause arms asserted at :554 (TERM/HUP), :568 (pane-local probe), and the None arm; hermeticity proof at :599 points HOME at an empty tmp dir and still gets the fixture path. Re-ran test_rotate_autopsy.py: 17 passed. Accepted proved (0.9); no rotate.py was touched, P1/CHEAP stayed frozen. No further work on this hypothesis: all three residue items (P1, CHEAP, P2) are landed and green.
