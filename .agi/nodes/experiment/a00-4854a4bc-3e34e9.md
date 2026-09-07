---
id: experiment:a00-4854a4bc-3e34e9
mint_id: 0140148b12be4ea9a9f9b10ff5f619e7
type: experiment
parents:
  - hypothesis:l2-goals-active-exempt
next_edges: []
confidence: 0.9
edited_by: ubuntu
evidence_runs:
  - experiment:a00-4854a4bc-3e34e9
loop: hypothesis:l2-goals-active-exempt@s1
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 57a723e9bc9b77df
season: 1
title: A00 4854a4bc 3e34e9
verdict: proved
---
# experiment:a00-4854a4bc-3e34e9

## Experiment

**Re-briefed hypothesis:** the exemption design is abandoned (owner decision 2026-09-06,
HANDOFF §6 item 10, l3-command-ladder-brief §2.6). Long-term goals become
`goal_kind: perpetual` and there is **no active-goal cap at all**. Fix = DELETE
`cc_dispatch.max_goals_active` and its METRIC-WARNING branch outright; drop
`goals_active` too if nothing reads it. Red-first: 30 active goals print no
warning; suite green.

**What I did** (edits in place, following the re-brief):

1. `.agi/config.json` — removed `"max_goals_active": 18` from `cc_dispatch`.
2. `extensions/agi/bin/metrics.py`:
   - deleted the entire goal:g5 / L5 METRIC-WARNING branch (the old
     `!! METRIC-WARNING goals_active=N exceeds ...` / `METRIC_WARNING
     goal_rotation=a/b` block), replacing it with a one-paragraph note recording
     the owner decision (delete, not redesign).
   - dropped `"goals_active"` from the `compute()` metrics dict, because grep
     shows nothing outside metrics.py reads it (the only other mention, in
     `snapshot-goals.py`, is a comment about `max_goals_active`, which is also
     now dead). Per the re-brief: nothing reads it → drop it too.
3. `extensions/agi/bin/snapshot-goals.py` — updated the stale comment that
   referenced the deleted `cc_dispatch.max_goals_active` cap.
4. `extensions/agi/tests/test_metrics.py` — removed the two tests that pinned
   the deleted warning (`test_exceeding_max_goals_active_warns_but_does_not_refuse`,
   `test_within_max_goals_active_is_silent`); fixed the two `goals_active`
   assertions; added red-first test `test_far_more_active_goals_than_any_legacy_cap_never_warms`
   (30 active goals + a stale `max_goals_active: 1` config key ⇒ no warning,
   no `goals_active` metric).

**Verify commands + actual output:**

Red (before fix) on the LIVE repo:
```
$ python3 extensions/agi/bin/metrics.py .agi
!! METRIC-WARNING goals_active=20 exceeds cc_dispatch.max_goals_active=18 ...
METRIC_WARNING goal_rotation=20/18
METRIC goals_active=20
```

Green (after fix):
```
$ python3 extensions/agi/bin/metrics.py .agi   # grep -i goal_rotation|goals_active|max_goals
(no matching lines)                            # exit 0
$ python3 -m pytest extensions/agi/tests/test_metrics.py -q
60 passed in 4.36s
$ python3 -m pytest extensions/agi/tests/ -q
1734 passed, 1 skipped in 103.64s
```

## Evidence

- New red-first test (now green), asserting the exact re-brief contract with a
  deliberately stale `max_goals_active: 1` config present:
  ```python
  def test_far_more_active_goals_than_any_legacy_cap_never_warms(project, capsys):
      (project / "agi-tree.config.json").write_text(
          json.dumps({"cc_dispatch": {"max_goals_active": 1}}))  # stale, inert
      for i in range(30):
          _goal(project, f"g{i}", "active")
      m = metrics.emit(project)
      out = capsys.readouterr()
      assert "goal_rotation" not in out.out
      assert "max_goals_active" not in out.err
      assert "goals_active" not in m      # dropped, not just silenced
  ```
- Live `metrics.py .agi` after the fix emits no goal-rotation warning and no
  `goals_active` metric; exit 0.
- Full engine suite green: `1734 passed, 1 skipped`.

**Not caused by this change (pre-existing, report only):** the L3.04 dispatch
harness's `driver.sh --smoke` fails before metrics runs with
`ERR: not a loop label: 'hypothesis:l2-goals-active-exempt@s1'`, and there is a
`DRIFT WARNING: engine HEAD 3c0af268f07b but config pins 179f95602839`. Both are
orthogonal to this edit.

THOUGHT: chose DELETE-not-exempt exactly as the re-brief directed. Went further
than the config+warning removal only where the brief authorised it — grep showed
nothing reads `goals_active` once its warning goes, so it was dropped rather than
kept as dead SQL. `goals_horizon`/`goals_retired`/`goals_complete` stay because
they are descriptive counts with independent readers, not cap-trip counters.

## Agent Notes
Re-briefed fix applied: removed cc_dispatch.max_goals_active from config.json, deleted the METRIC-WARNING branch in metrics.py, dropped goals_active (nothing else read it), both removed cap-warning tests swapped for red-first 30-active-goals test, stale config key inert. Live emit shows no warning; suite 1734 passed/1 skipped.

REVIEW (parent a00-80f648c7, L3.04): ACCEPT verdict=proved. Verified independently in code: config max_goals_active gone; metrics.py emits no goals_active/goal_rotation/warning; snapshot-goals.py stale-comment updated; test_metrics.py has the red-first 30-active-goals test pinning "stale max_goals_active=1 inert, no warning, goals_active absent". Live emit silent (grep no matches). Full suite green: 1734 passed, 1 skipped. Diff is surgical, no collateral. Caveat noted (smoke end-to-end path not exercised — pre-existing loop-label + engine-drift, orthogonal to this claim). Verdict proved is against the RE-BRIEFED claim (delete not exempt); original frontmatter testable_claim (exemption) is superseded by the owner decision recorded in the hypothesis node Agent Notes. evidence_runs=[experiment self] exists, gate clean (no bypass).
