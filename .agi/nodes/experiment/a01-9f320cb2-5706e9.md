---
id: experiment:a01-9f320cb2-5706e9
mint_id: e14fb522aef84ef9a8979397b78dbf32
type: experiment
parents:
  - hypothesis:verify-runs-grid-commit-before-smoke
next_edges: []
scaffold_hash: c487feeffdd7863a
title: A01 9f320cb2 5706e9
---

# experiment:a01-9f320cb2-5706e9

## Experiment

**Question:** Does the `verify` workflow produce `unevidenced_decisive_verdicts > 0` because smoke runs before grid-commit? If so, what are the current unevidenced decisive verdicts, and would grid-commit's evidence gate demote them?

The hypothesis claims the verify workflow orders grid-commit before smoke so evidence runs before metrics. Sibling a00-508e2451-cbc9e9 disproved the ordering claim: actual declaration is smoke→tests→goals-check→viewport-verify→grid-commit. Sibling a01-0963819d-ab5d20 proved the mechanism works: running evidence gate before smoke yields `unevidenced_decisive_verdicts=0`. Conjunct (3) — a red-on-purpose test for this ordering — remains untested.

**What I did — Phase 1: Current-state probe.**
Ran `commands.py run smoke` (the first step of the verify workflow) to capture current metrics. Then ran `evidence_gate.py enforce --dry-run` to show what `grid.py commit --all` would demote — without mutating the graph (sibling a01's live demotion was necessary for its mechanism proof; a dry run avoids overclaiming what I did not verify by writing).

**Results:**
- Smoke: `unevidenced_decisive_verdicts=2`, `decisive_evidence_fraction=0.967`, `decisive_verdicts=61`
- Gate dry-run: 2 verdicts would be demoted (`experiment:a00-4c170302-65ca06` and `experiment:a01-daf87fe4-71cde8`, both `proved -> inconclusive_lean_proved:50`)

The verify workflow reads metrics BEFORE the evidence gate runs, so `unevidenced_decisive_verdicts=2` is reported by the workflow's own first step (smoke), and then grid-commit (the last step) immediately demotes both — meaning the verify workflow's own output includes unevidenced verdicts that are stale within moments. The hazard from goal S34 row 8 is confirmed live.

**Phase 2 — Does a red-on-purpose test exist?**
Searched the test suite (`extensions/agi/tests/`) for any test that asserts the ordering constraint (grid-commit before smoke, or any guard against the hazard). No such test exists. The test suite has 155 tests, none check that grid-commit runs before metrics. Conjunct (3) remains open.

## Evidence

### Phase 1: Smoke (verify step 1)

```
$ python3 commands.py run smoke
METRIC unevidenced_decisive_verdicts=2
METRIC decisive_evidence_fraction=0.967
METRIC decisive_verdicts=61
METRIC verdicts_evidence_backed=122
METRIC evidence_fraction=0.375
```

### Phase 1: Gate dry-run (what grid-commit would demote)

```
$ python3 evidence_gate.py enforce --dry-run
EVIDENCE-GATE would demote experiment:a00-4c170302-65ca06: proved -> inconclusive_lean_proved:50
EVIDENCE-GATE would demote experiment:a01-daf87fe4-71cde8: proved -> inconclusive_lean_proved:50
evidence-gate enforce: 2 unevidenced decisive verdict(s), 2 would demote, 0 refused
```

### Declaration order (from .geometry/commands.md, via a00-508e2451-cbc9e9)

```yaml
workflows:
  verify:
    - smoke        # ← step 1: reads metrics
    - tests
    - goals-check
    - viewport-verify
    - grid-commit  # ← step 5: demotes unevidenced verdicts
```

### No red-on-purpose test exists

```
$ python3 -m pytest extensions/agi/tests/ -q -k "order or verify or grid"
155 passed, 1327 deselected
```

No test asserts the ordering or catches the stale-metric hazard.

