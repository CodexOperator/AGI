---
id: experiment:a00-f65d2917-e262ae
mint_id: 12f7e5ad2e5d458e85833a3ffecc2949
type: experiment
parents:
  - hypothesis:l4-an-undeclared-town-is-refused-not-capped
next_edges: []
confidence: 0.9
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-f65d2917-e262ae
loop: hypothesis:l4-an-undeclared-town-is-refused-not-capped@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0fba21c825beb1b1
season: 2
thought_session: sanctuary-director-gen12
title: spawn_gate.py refuses a vision whose OWN town is absent from the ladder towns table
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f65d2917-e262ae

## Experiment

Hypothesis:l4-an-undeclared-town-is-refused-not-capped claims the write path
refuses a vision whose `town:` cell is absent from the ladder's `towns:`
table, with the named refusal `town X not declared in ladder towns`.

**BEFORE (reproduced the falsifier):** with a fixture ladder declaring
`towns: [streaming-suite, web-app-suite]` and a vision `fm={'town':
'nowhere-declared'}`, `check_spawn` returned

```
STATUS: approved
applied: ['town vision cap: nowhere-declared has room for 3 more']
```

An undeclared town read `counts.get('nowhere-declared', 0) == 0` so it got a
fresh cap of 3 and sailed past `caps.vision` — exactly the bug: a vision
minted into a town the graph never declared.

**AFTER:** edited `extensions/agi/bin/spawn_gate.py` section 5b (the per-town
vision-cap write-path gate). After the own-cell / parents fallback resolves
`town`, when the vision declares its OWN `town:` and the ladder's `towns:`
table is non-empty, an undeclared town is REJECTED with
`town '<x>' is not declared in ladder towns`. The refusal fires only on the
OWN-declared town (a town-less vision keeps the parents'/default fallback
touched), and only when a towns table exists (a ladder with no `towns:`
list — `[]` — has nothing to validate and is untouched, preserving
non-declaring ladders and the existing `vision_cap_graph` fixture suite).
Added helper `read_ladder_towns(nodes_dir)`.

**AFTER (same fixture):**

```
nowhere-declared -> ('rejected', "rule 'declared town' ... town 'nowhere-declared' is not declared in ladder towns")
streaming-suite   -> ('approved', ..., ['town vision cap: streaming-suite has room for 3 more'])
no town (default) -> ('approved', ..., ['town vision cap: core has room for 3 more'])
```

**Tests:** added `town_ladder_graph` fixture (towns table of two towns) and
four tests in `test_spawn_gate.py`: undeclared own town refused (names the
town), declared own town keeps its cell, no own town uses the existing
default, and the refusal is inert when the ladder declares no towns.

## Evidence

- Reproduced the falsifier pre-fix: `town: nowhere-declared` -> APPROVED with
a fresh cap.
- Post-fix: same input -> REJECTED, reason names the town and the phrase
  `not declared in ladder towns`.
- `pytest test_spawn_gate.py -q`: 81 passed.
- `pytest test_spawn_gate.py test_season.py test_snapshot_goals.py -q`
  (the town-affecting suites): 222 passed. The kid-tier guard refuses a bare
  full-directory run (`AGI_TIER=kid refuses a bare full-suite directory run`),
  so the affected suites were run directly; the change is isolated to
  spawn_gate.py's town-cell lookup + its tests.

## Agent Notes
spawn_gate write-path now refuses a vision whose OWN town is absent from ladder towns table (named refusal); undeclared town reproduced APPROVED pre-fix, REFUSED post-fix; 81 spawn_gate + 222 town-suite tests pass

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW L4.160 (a00-ab3726ab), read from the artifact not the report.
(1) THE CLAIM: testable_claim says "the write path refuses a vision whose `town` is absent from `.geometry/ladder.md`'s towns table with a named refusal (`town X not declared in ladder towns`); declared towns keep their own cell; ... no town -> the existing default."
(2) THE MECHANISM: read_ladder_towns (spawn_gate.py:765) reads fm["towns"] and returns [] on absent/empty; the write-path cap at spawn_gate.py:1209-1223 validates `own` (the vision OWN cell) against that list and rejects with "town X is not declared in ladder towns" before the cap count runs. Four tests at test_spawn_gate.py:1373 (undeclared own -> REJECTED), :1389 (declared own keeps its cell), :1403 (no own town -> default untouched), :1414 (ladder with no towns -> no refusal). I re-ran pytest extensions/agi/tests/test_spawn_gate.py -q: 81 passed.
(3) THE NEAR MISS: validating the RESOLVED town (including the parents-fallback town from nearest_vision_town) would also satisfy the words "an undeclared town is refused" while changing behaviour for every town-less vision whose nearest vision carries a cell -- the defect is scoped to the vision OWN cell (g15-22: "the vision's own town cell is validated"), and the fallback path is deliberately left untouched. The kid took the own-cell reading, matching the claim.
(4) DEVIATION: none -- file scope respected (spawn_gate.py town-cell lookup + tests only; spawn_gate.py:705 untouched). Verdict proved stands: evidence_runs names this experiment, which exists and is the run.
<!-- THOUGHT:END -->

**2026-09-11T07:56Z director review at harvest (sanctuary-director gen XII, L4.160).** Re-ran on the round bytes: `python3 -m pytest extensions/agi/tests/test_spawn_gate.py extensions/agi/tests/test_write.py -q` → 166 passed (again on the merged seat bytes). Real-graph probe with the round's spawn_gate.py against `/home/ubuntu/work/agi/.agi` (read-only `check_spawn` of a `vision` with `fm={'town': …}`): `nowhere-declared` → `rejected | rule 'declared town' from ladder: town 'nowhere-declared' is not declared in ladder towns`; `streaming-suite` and `core` (the real ladder's towns) → pass the declared-town rule and are stopped only by the ordinary `town vision cap` (3/town, already full) — the reproduction (`town nowhere-declared -> APPROVED`) now reads REJECTED, declared towns unchanged. Verdict `proved` stands. Merged into the seat.
