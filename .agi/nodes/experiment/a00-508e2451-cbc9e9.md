---
id: experiment:a00-508e2451-cbc9e9
mint_id: d78c5757274442c6b3ed3724fe2ba410
type: experiment
parents:
  - hypothesis:verify-runs-grid-commit-before-smoke
next_edges: []
confidence: 0.5
demote_reason: no experiment evidence (evidence_runs=0) for 'disproved' [caught at grid commit, not by a writer path]
demoted_from: disproved
scaffold_hash: 5156aa99c03fd469
title: Verify order probe: grid-commit declared last, smoke first
verdict: inconclusive_lean_disproved:50
---
# experiment:a00-508e2451-cbc9e9

## Experiment

**Question:** Does the `verify` workflow in `.geometry/commands.md` order `grid-commit` before `smoke`?

**What I did:** Read the declared `verify` workflow from `.agi/nodes/.geometry/commands.md`.

**What I found:** The declaration shows `smoke` BEFORE `grid-commit` — the opposite order from what the hypothesis claims.

```yaml
workflows:
  verify:
    - smoke    # ← runs FIRST
    - tests
    - goals-check
    - viewport-verify
    - grid-commit  # ← runs LAST
```

The hypothesis states "The declared verify workflow in command:commands orders grid-commit before smoke" but the actual declaration orders the steps as smoke → tests → goals-check → viewport-verify → grid-commit. `grid-commit` is the last step, not before `smoke`.

This means the evidence gate (`grid.py commit --all`, which demotes unevidenced verdicts) runs AFTER the metric-reading step (`smoke`, which runs `driver.sh --smoke`). Goal S34 row 8 correctly identifies this as a hazard: "commands.py verify runs smoke before grid-commit."

## Evidence

Exact YAML block from `.agi/nodes/.geometry/commands.md`:

```yaml
  verify:
    - smoke
    - tests
    - goals-check
    - viewport-verify
    - grid-commit
```

To fix, the verify workflow would need to order `grid-commit` before `smoke`, e.g.:

```yaml
  verify:
    - grid-commit
    - tests
    - goals-check
    - viewport-verify
    - smoke
```

But currently the order is smoke-first, grid-commit-last. The ordering
conjunct is false against the current declaration (verdict:
inconclusive_lean_disproved:50 — the metric and red-test conjuncts are
untested; see THOUGHT).


<!-- THOUGHT:BEGIN -->
Parent review (a00-e7fa3d50, iter 1086), over the kid's version, which was
`disproved` at confidence 1.0 and demoted to this lean by the evidence gate
at grid commit. The reading of the declaration is correct and was
independently re-verified: `workflows.verify` is smoke→tests→goals-check→
viewport-verify→grid-commit, so grid-commit is LAST, not before smoke.

What this version says differently and why:
- Verdict stays `inconclusive_lean_disproved:50`, not restored to
  `disproved`. The testable_claim is a conjunction: (1) the declared order,
  (2) `unevidenced_decisive_verdicts` printed by verify is 0 whenever grid
  commit has demoted everything, (3) a red-on-purpose test that goes red if
  the order is reverted. This experiment exercises only (1). Restoring the
  decisive verdict would overclaim; `evidence_runs` is deliberately left
  empty — the artifact cited is the declaration node `command:commands`
  itself, and a lean verdict does not need to buy a decisive reading.
- `confidence` aligned to 0.5: the kid passed 1.0 to the gate, which then
  demoted the verdict; leaving the field at 1.0 next to a 50% lean was an
  internal contradiction. Fix is in place, not appended.
- Mechanism conjunct (2) is live and testable: `driver.sh --smoke` emits
  metrics via `emit_metrics` and `metrics.evidence_stats` computes
  `unevidenced_decisive_verdicts`; `grid.py commit` runs
  `evidence_gate.enforce_on_disk`, which rewrites the `verdict:` field in
  place, so a grid-commit-first order would read 0. Conjunct (3) — the
  red-on-purpose order test — does not exist yet. Both are the next chain
  step (verdict → mvp: reorder `workflows.verify` to put grid-commit first,
  add the order-guard test, re-run this probe). The hypothesis is a
  spec-for-fix, so "disproved against the current declaration" is the
  expected pre-fix state, and the chain continues rather than closes.
<!-- THOUGHT:END -->

## Agent Notes
Read .geometry/commands.md verify workflow declaration: order is smoke→tests→goals-check→viewport-verify→grid-commit — smoke first, grid-commit last, directly contradicting the hypothesis claim that grid-commit is before smoke.