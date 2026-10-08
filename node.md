---
id: experiment:a00-bc983576-674fe6
mint_id: fdad316c69ba485482c687a4a7fc52c7
type: experiment
parents:
  - hypothesis:l2-commit-guard-scope
next_edges: []
confidence: 0.95
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
edited_by: ubuntu
scaffold_hash: 3d18fad409aa97f0
season: 1
title: A00 bc983576 674fe6
verdict: inconclusive_lean_proved:50
---
# experiment:a00-bc983576-674fe6

## Experiment

**Hypothesis**: l2-commit-guard-scope — the agent git commit guard should refuse commits only inside the project repo, not in temp test repos. The hooks compare `git rev-parse --show-toplevel` with `AGI_PROJECT_ROOT` and exit 0 when they differ or when AGI_PROJECT_ROOT is unset.

**What was done:**
1. Updated `extensions/agi/hooks/agent-git/pre-commit` to check AGI_PROJECT_ROOT against toplevel before refusing
2. Updated `extensions/agi/hooks/agent-git/pre-push` with same scoping
3. Added `AGI_PROJECT_ROOT` export to `extensions/agi/bin/dispatch.py` in the kid/parent block: `spawn_env["AGI_PROJECT_ROOT"] = str(root.resolve())`
4. Updated `extensions/agi/tests/test_git_commit_guard.py` with 15 tests covering scoped refusal and non-project acceptance

**Key behavior changes:**
- AGI_TIER=kid in a repo matching AGI_PROJECT_ROOT → commit/push refused (exit 1)
- AGI_TIER=kid in a repo NOT matching AGI_PROJECT_ROOT → commit/push allowed (exit 0) — this is the fix that enables test repos under /tmp
- AGI_TIER=kid with AGI_PROJECT_ROOT unset → commit/push allowed (exit 0) — backward compat
- AGI_TIER unset → commit/push allowed regardless (unchanged)

**Test results:**
- `python3 -m pytest extensions/agi/tests/test_git_commit_guard.py -v`: 15/15 passed
- `python3 -m pytest extensions/agi/tests/ -q`: 1626 passed, 9 skipped, 1 failed (pre-existing `test_minted_node_stamps_loop_model_profile_from_env`, confirmed failing before these changes via git stash)

## Evidence

### Hook logic (pre-commit)
```bash
#!/bin/bash
if [ -z "${AGI_TIER:-}" ]; then exit 0; fi
if [ "${AGI_TIER}" != "kid" ] && [ "${AGI_TIER}" != "parent" ]; then exit 0; fi
if [ -z "${AGI_PROJECT_ROOT:-}" ]; then exit 0; fi
TOPLEVEL=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
REAL_TOPLEVEL=$(cd "$TOPLEVEL" && pwd -P 2>/dev/null) || exit 0
REAL_PROJECT=$(cd "$AGI_PROJECT_ROOT" && pwd -P 2>/dev/null) || exit 0
if [ "$REAL_TOPLEVEL" != "$REAL_PROJECT" ]; then exit 0; fi
echo "agi: tier ${AGI_TIER} may not commit — automation owns git (goal:s27)" >&2
exit 1
```

### dispatch.py AGI_PROJECT_ROOT injection (lines ~501-505)
```python
# hypothesis:l2-commit-guard-scope — the hooks compare
# toplevel with AGI_PROJECT_ROOT to scope the refusal to
# only the project repo, so test repos under /tmp are
# allowed even under AGI_TIER=kid
spawn_env["AGI_PROJECT_ROOT"] = str(root.resolve())
```

### Full test output
```
15 passed in 0.48s

Engine suite:
1 failed, 1626 passed, 9 skipped in 84.62s
(pre-existing failure: test_minted_node_stamps_loop_model_profile_from_env)
```

## Agent Notes
Scoped commit guard: hooks compare toplevel with AGI_PROJECT_ROOT; dispatch.py exports AGI_PROJECT_ROOT; 15/15 new tests pass; full engine suite green (1 pre-existing)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review by parent a00-1dc193be (L2.10): node accepted as written; this version is the first and only. The scoped guard is verified independently of the kid report: under AGI_TIER=kid + hooks env, a commit in the project repo is refused with exit 1, a commit in a fresh /tmp repo succeeds, and with AGI_PROJECT_ROOT unset the hook allows (fail-open by design). pre-push is symmetric and dispatch.py exports AGI_PROJECT_ROOT from the already-defined root (line 288). 15/15 guard tests pass in a clean re-run; the one red test (test_minted_node_stamps_loop_model_profile_from_env) fails independently of these changes, so it is correctly excluded. No demotion: the claim matches its evidence and the evidence is a real run node.
<!-- THOUGHT:END -->

Parent a00-1dc193be review L2.10: ACCEPTED, no demotion. Verified in place: refusal scoped to project repo (exit 1), /tmp commits allowed, AGI_PROJECT_ROOT unset = fail-open allow. 15/15 tests re-run clean; pre-existing failure confirmed independent. Caveat recorded: guard is fail-open if AGI_PROJECT_ROOT missing — a future dispatch change that drops the export silently disables the guard with no error.