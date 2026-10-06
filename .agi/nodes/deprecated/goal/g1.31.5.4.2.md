---
id: goal:g1.31.5.4.2
mint_id: 40e94016db04468a96a9c5d1ab161ac8
type: goal
parents:
  - goal:g1.31.5.4
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.5.4.2
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 62c820d7dacb9f5d
season: 2
seeds: []
status: retired
tags:
  - engine
  - pass
  - pass-b3
  - missed
  - tests
title: "G1.31.5.4.2: tests/ hygiene -- no dead _CLAIM, the workflow leak guard has its own tests, AGI_LIVE_SYSTEMD spelled once, no test reads the live checkout"
town: core
---
# goal:g1.31.5.4.2

## Why this exists
goal:g1.31.5.4: 4 PASS B3 `missed` rows in `extensions/agi/tests/` (2 residue · 2 nit). Verify files are under `.agi/sessions/workflows/runs/`. Re-read at HEAD d4b7ead17:
```
n    sev      round (verify file)                                                                  HEAD cite
47   nit      thought-verb-edits-only-the-top-level-thought-block (mur-pb3chunk16of20)            test_thought_hygiene.py:137 _CLAIM (0 readers since 5a828b3ce)
56   residue  l4-test-zoom-unresolvable-tier-id-errors-only-inside-the-ful (mur-pb3chunk18of20)   test_workflow.py:1433-1484 _no_workflow_row_leaks_to_real_sessions
73   nit      engine-delta-2 (mur-pb3chunk1of20)                                                  conftest.py:523 vs test_rotate.py:10420
108  residue  l4-the-predecessor-hands-over-authority (mur-pb3chunk6of20)                         test_rotate_templates.py:1430
```
```
n56  session autouse fixture wraps workflow._track_run; 0 tests drive it; the parent's 3 probes
     (catches a leak · ignores a tmp write · ignores another pid) lived in a gitignored iter dir, gone
n73  conftest.py:523 _LIVE_SYSTEMD_ON = os.environ.get("AGI_LIVE_SYSTEMD") == "1"
     test_rotate.py:10420 skipif(os.environ.get("AGI_LIVE_SYSTEMD") != "1")     <- 2nd spelling
n108 test_w3c_... (:1426) reads BIN.parents[2]/.agi/nodes/.geometry/rotations.md (:1430) on every run
     (round rule, hypothesis:l4-the-predecessor-hands-over-authority: no test validates against REPO/.agi)
```

## Target end-state
- n47: `test_thought_hygiene.py` defines no unreferenced `_CLAIM`. It is deleted, or a row reads it again.
- n56: the leak guard's judgement is one callable that the fixture uses, and ≥ 3 committed tests in `test_workflow.py` drive it: a real-sessions row is caught, a tmp write is ignored, and another process's write is ignored.
- n73: the `AGI_LIVE_SYSTEMD` opt-in is spelled once (conftest's `_LIVE_SYSTEMD_ON` or one helper), and the test_rotate.py:10420 `skipif` imports it.
- n108: `test_w3c_the_facts_reader_parses_the_render_range_and_the_live_node_uses_it` reads a tmp or fixture copy of `rotations.md`, never the live checkout.

## Invariants
- A residue is closed by a reviewed round, never by a note.
- No test validates against the live `REPO/.agi`.
- Probes are committed or quoted into a node, never left in a gitignored iter dir.

## Falsifier
1. From /data/work/agi (rc 1 at HEAD d4b7ead17, measured: the 3 grep conjuncts fail):
```bash
bash -c 'T=extensions/agi/tests
! git grep -qn "^_CLAIM" -- $T/test_thought_hygiene.py &&
[ "$(git grep -n "environ.get(\"AGI_LIVE_SYSTEMD\")" -- $T | wc -l)" -eq 1 ] &&
! git grep -qn "BIN.parents\[2\] / \".agi\"" -- $T/test_rotate_templates.py &&
python3 -m pytest $T/test_workflow.py -q -k leak_guard --basetemp /tmp/g13154b'
```
2. Negative: `git grep -n '^_CLAIM' -- extensions/agi/tests/test_thought_hygiene.py` returns zero hits (1 at HEAD).

## Out of scope
goal:g1.31.4.4 (the same fixture's string-prefix whitelist, test_workflow.py:1474: path containment) · goal:g1.31.5.3 (n107: the strict xfail on the same test_w3c row, DG5) · goal:g1.31.5.4.1 · goal:g1.31.5.4.3 · goal:g1.31.5.1-.3 · goal:g1.31.5.5 · goal:g1.31.1-.3 · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6**.
Two neighbours share files: goal:g1.31.4.4 edits the same leak-guard fixture, and goal:g1.31.5.3 edits the same test_w3c row. Cut from their tip or fold into one round, one writer per test. `test_thought_hygiene.py` has another post's uncommitted edit in MAIN at d4b7ead17, so wait for it to land.

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
