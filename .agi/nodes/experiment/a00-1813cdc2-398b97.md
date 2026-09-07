---
id: experiment:a00-1813cdc2-398b97
mint_id: 66f4268a94a14b138f8f9546f1d47362
type: experiment
parents:
  - hypothesis:verify-runs-grid-commit-before-smoke
next_edges: []
confidence: 0.95
demote_reason: no experiment evidence (evidence_runs=0) for 'disproved' [caught at grid commit, not by a writer path]
demoted_from: disproved
edited_by: season.py
scaffold_hash: e412a75c8c987451
season: 1
thought_session: season
title: A00 1813cdc2 398b97
verdict: inconclusive_lean_disproved:50
---
# experiment:a00-1813cdc2-398b97

## Experiment

**Goal:** Verify the hypothesis claim that the verify workflow in `command:commands` orders grid-commit before smoke.

**Method:** Inspected the declared workflow in `.geometry/commands.md` and executed the verify workflow via `commands.py run --workflow verify`.

**Result — hypothesis DISPROVED.**

The declared order is:

```
smoke → tests → goals-check → viewport-verify → grid-commit
```

grid-commit is **last**, not before smoke. During a live verify run:
- `smoke` (driver.sh --smoke) runs first and reports `unevidenced_decisive_verdicts=2`
- `grid-commit --all` runs last and demotes 1 unevidenced verdict
- This means the metric is read BEFORE the evidence gate has had a chance to demote, directly contradicting the hypothesis claim that "the evidence gate has run before the metric is read."

If the intended design is to have grid-commit before smoke, the workflow declaration needs to be reordered.

## Evidence

**Workflow declaration from commands.md:**

```yaml
workflows:
  verify:
    - smoke
    - tests
    - goals-check
    - viewport-verify
    - grid-commit
```

**commands.py resolve:**
```
Workflow verify: ['smoke', 'tests', 'goals-check', 'viewport-verify', 'grid-commit']
```

**Verify run output excerpt:** Smoke ran first and reported metrics (unevidenced_decisive_verdicts=2), then steps completed, then grid-commit ran last ("grid: ... 1 demoted by the evidence gate"). The full run passed (exit 0, 124.4s).

**Test suite:** 1481 passed, 1 failed (pre-existing `test_publish_alarm.py::test_the_fallback_leaves_no_worktree_behind` — no code changed).