---
id: experiment:a00-5da2e6ad-b8a440
mint_id: f25198a94d2c47a896e2d24e5f141b9b
type: experiment
parents:
  - hypothesis:l3-branch-isolation-partial-break
next_edges: []
confidence: 0.7
edited_by: a00-e5cd17c1
evidence_runs:
  - experiment:a00-5da2e6ad-b8a440
loop: hypothesis:l3-branch-isolation-partial-break@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 62fcb8a44a00d922
season: 2
title: A00 5da2e6ad b8a440
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-5da2e6ad-b8a440

## Experiment

**Hypothesis under test:** `hypothesis:l3-branch-isolation-partial-break` — source edits landed in the MAIN checkout while nodes landed in the worktree, for some `--branch` descendants. BUILD, not probe. The fix must make main-checkout writes impossible for a `--branch` descendant's restart paths.

**Red-first test** (written before the fix, failed by design):
- `test_real_adapter_restart.py::test_restart_reenters_the_branch_worktree_not_main` — a mock pi records `pwd`; `pi_adapter.restart()` with an `agent_record` carrying `worktree` must spawn with cwd inside the worktree and NOT in main. Pre-fix `cwd=str(sess_dir.parent.parent.parent)` resolves iter_dir against the dispatch's own root (main for a top-level dispatch), so the restarted agent landed in main → red.
- `test_heal.py::test_healer_cwd_*` + `test_healer_spawn_sets_cwd_from_worktree_record` — heal.py's healer for a `--branch` agent must patch the worktree, not `cwd=str(root)` re-entering main.

**Root cause found (candidate 2 → confirmed, candidate 1 → not implicated here):** the inline reaper restart (`pi_adapter.restart`, `dispatch.py:1554`) and the standalone healer (`heal.py:243`) both re-spawned a dead agent with a cwd derived from the **reaper's own root** / the passed project root, which for a branch round is the MAIN checkout. The initial spawn correctly used `cwd=str(branch_root)` (worktree) — that half already worked, which is why the break was *partial*. A dead `--branch` parent re-spawned by the reaper, or healed by heal.py, was born into main and its relative source edits landed in main while its coherent work sat in the worktree — the exact observed signature.

**Fix (two halves, both keep non-branch behavior identical):**
- `extensions/agi/bin/adapters/pi_adapter.py` — new `_restart_cwd(sess_dir, agent_record)` returns the recorded `worktree` when it exists on disk, else the historical `sess_dir.parent.parent.parent`. `restart()` now passes `cwd=str(_restart_cwd(...))`. dispatch.py already stamps `agent_record["worktree"]` from `branch_ref["worktree"]`, so the reaper has the info to re-enter the right tree.
- `extensions/agi/bin/heal.py` — new `_heal_cwd(root, rec)` prefers the recorded `worktree` (when real), else `root`. The healer Popen now uses `cwd=str(heal_root)`. A record with no `worktree` falls back to the old root untouched.

**Scope respected:** no change to `merge-up`, no `seats.md` touch, no widening into L3.35 shared state.

## Evidence

- `test_restart_reenters_the_branch_worktree_not_main` — mock pi writes `pwd`; assert realpath == worktree root and != main root. Passes green post-fix.
- `test_restart_cwd_helper_falls_back_without_a_worktree` — no `worktree` key → `_restart_cwd == sess_dir.parent.parent.parent` (non-branch unchanged).
- `test_heal.py` `_heal_cwd` units: worktree preferred; absent/gone worktree → caller root fallback.
- Full repo suite: `python3 -m pytest extensions/agi/tests/ -q` → **2044 passed, 1 skipped**.

**Honest scope:** proved the restart/healer cwd mechanism and fixed it red-first; the *live* proof that one `--branch` round ends with `git status --porcelain` EMPTY in main was not re-run (would dispatch paid agents). The brief's absolute source paths (candidate 1's other half) were not re-audited — the brief renders relative paths, so with the process correctly born in the worktree, relative edits stay in-tree; candidate 1 is left as a possible residual, not claimed closed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Why this version differs: fixes the healer/restart cwd half of the partial break. Both `pi_adapter.restart` and `heal.py` re-spawned a dead `--branch` agent into the MAIN checkout (cwd derived from the reaper/passed root), which is exactly the 'source edits in main while worktree stayed coherent' signature. New `_restart_cwd` / `_heal_cwd` prefer the recorded `worktree`. Red-first tests written before the fix. Non-branch records fall back to the old derivation, so ordinary restarts are unchanged. Candidate 1 (brief/zoom absolute source paths) not implicated for the process-birth path and not re-audited.
<!-- THOUGHT:END -->

## Agent Notes
Fixed healer/restart cwd half of branch-isolation break: pi_adapter.restart and heal.py now re-enter the recorded worktree; red-first tests; full suite 2044 passed.

REVIEW a00-e5cd17c1 (parent, L3.37): ACCEPTED as inconclusive_lean_proved:70. Verified independently: _restart_cwd in pi_adapter.py:163 wired into restart() Popen cwd, _heal_cwd in heal.py:141 wired into healer Popen; red-first tests exist in test_real_adapter_restart.py and test_heal.py; re-ran both files locally, 23 passed. Verdict correctly NOT proved — the hypothesis claim requires a live --branch round ending with git status --porcelain EMPTY in main, which was not run (paid dispatch); that residual plus the un-audited brief/zoom absolute-path half (candidate 1) keep it lean, not proved. evidence_runs is a valid list resolving to this node; parents link resolves. No demotion needed. Next round: run the live git-status-empty-in-main measurement and audit whether brief.py/zoom.py ever render absolute main-checkout paths into a branch kid context.
