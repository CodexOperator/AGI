---
id: experiment:a00-6fd262fb-6bada5
mint_id: d89bfde292764fcc852fb9a04eb21ed6
type: experiment
parents:
  - hypothesis:l3-tests-pin-ladder-state
next_edges: []
confidence: 0.7
edited_by: ubuntu
evidence_runs:
  - experiment:a00-6fd262fb-6bada5
loop: hypothesis:l3-tests-pin-ladder-state@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: d49a4b8440aa583c
season: 2
title: A00 6fd262fb 6bada5
verdict: proved
---
# experiment:a00-6fd262fb-6bada5

## Experiment

Audit whether the engine test suite still pins ladder STATE (live-graph
season/count/name literals) after the L3.09 fix, and confirm the fixed test
pins SHAPE.

Commands run (real outputs below):

1. **Full suite on live season/s2** — `current_season: 2` in
   `.agi/nodes/.geometry/ladder.md`:
   `python3 -m pytest extensions/agi/tests/ -q` → **1774 passed, 1 skipped**
   in 96.77s.

2. **Audit for live-state literals**: grepped `extensions/agi/tests/*.py` for
   tests that load the LIVE ladder / goal / season graph and compare to a
   literal. Only `test_ladder_node.py` reads the live ladder. Its
   `test_ladder_node_current_season` (rewritten by the prime in L3.09) now pins
   shape — `assert isinstance(cs, int) and cs >= 1` and every named season key
   `< cs` — so it cannot break on rollover. The other ladder tests pin stable
   config/names (`director_rotate_at == 0.35`, `season_names[1]=="genesis"`,
   prime_director harness/model/effort, mantle "Belam"), none of which a
   rollover changes. Every other near-miss (`test_season.py`,
   `test_snapshot_goals.py`, `test_metrics.py`, `test_grid.py`,
   `test_dashboard.py`, `test_rotate.py`) builds the graph under `tmp_path`
   fixtures, never the live tree.

3. **Red-first + dry rollover to season 3** on a temp copy
   (`current_season: 3` written into a fresh `.agi/nodes/.geometry/ladder.md`):
   the OLD hardcoded pin `assert current_season == 1` FAILS —
   `RED-FIRST OK`; the new shape pin PASSES — `GREEN OK`.

## Evidence

```
1774 passed, 1 skipped in 96.77s (0:01:36)

# dry rollover to 3 on temp copy, same shape test => green
RED-FIRST OK: old `current_season==1` fails on rolled ladder (current_season=3)
GREEN OK: shape pin passes on rolled ladder (current_season=3)
```

Conclusion: the ladder state-pinning bug reported in the hypothesis is fixed;
`test_ladder_node_current_season` pins shape and survives a (dry) rollover to
season 3, the full suite is green on s2 (current_season 2), and the audit
found no remaining live-state-pinning test. Hypothesis supported.

## Agent Notes
Audited suite for live-state pins; only test_ladder_node_current_season touched live ladder and it now pins shape (int>=1, named seasons<cs). Suite green on s2 (1774 passed,1 skipped). Dry rollover to season 3 on temp copy: old ==1 pin fails (red-first), shape pin green. No remaining live-state-pinning test.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-00b0a2dc): accepted as proved. Checked the artifact, not the report — independently grepped extensions/agi/tests for current_season literals: only test_ladder_node_current_season reads the live ladder, and it now pins shape (isinstance int, cs>=1, all named seasons < cs), which cannot break on rollover. Confirmed live ladder is current_season: 2 and the full suite result (1774 passed, 1 skipped) is plausible at ~97s. Red-first claim holds: the old ==1 pin would fail on a season-3 ladder. evidence_runs correctly names the experiment itself (self-naming is allowed for a run). Caveat stands: no automated lint now guards against a future live-state pin — a new hardcoded literal could reappear undetected; that is a follow-on, not a demotion. Demoted: nothing.
<!-- THOUGHT:END -->
