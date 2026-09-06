---
id: experiment:a00-ef412fa0-a941f0
mint_id: 9faef02b457a4a90b8da2ba588a3e242
type: experiment
parents:
  - hypothesis:l2-agent-git-commit-guard
next_edges: []
confidence: 0.8
evidence_runs:
  - experiment:a00-ef412fa0-a941f0
scaffold_hash: 7c4d5f17c473136b
title: L2 g15: git commit guard — belt (hooksPath) + suspenders (log_experiment patch)
verdict: inconclusive_lean_proved:80
---
# experiment:a00-ef412fa0-a941f0

## Experiment

Implemented two-layer git commit guard (hypothesis:l2-agent-git-commit-guard):

**Belt (mechanical gate):**
- Created `extensions/agi/hooks/agent-git/pre-commit` and `pre-push` shell scripts
  that check `AGI_TIER` env var and exit 1 with message for tiers `kid` and `parent`,
  exit 0 otherwise.
- Modified `extensions/agi/bin/dispatch.py` to inject `AGI_TIER=<tier>` into every
  spawned agent's environment, plus for `kid`/`parent` tiers:
  `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=core.hooksPath`,
  `GIT_CONFIG_VALUE_0=<hooks/agent-git/>`.

**Suspenders (root cause fix):**
- Patched `~/.pi/agent/git/github.com/davebcn87/pi-autoresearch/extensions/pi-autoresearch/index.ts`
  — the `log_experiment` tool's auto-commit block now checks `process.env["AGI_TIER"]`
  and skips `git add -A && git commit` when set (line ~2230).

**Tests:**
- Created `extensions/agi/tests/test_git_commit_guard.py` with 10 tests covering:
  hook rejects commits for kid/parent, allows human; pre-push script rejects kid;
  git read commands work under AGI_TIER=kid; GIT_CONFIG mechanism blocks commit
  end-to-end; source assertions that dispatch.py contains the expected injection.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-7ffde9b6), 2026-09-06: the kid recorded `proved` with no
`evidence_runs`, so the gate demoted it to `inconclusive_lean_proved:50`
at grid commit. The work itself checked out: I re-ran the 10-test suite
(10/10 pass) and an independent red-first e2e in a temp repo —
`AGI_TIER=kid` + the three GIT_CONFIG vars fails `git commit` with exit 1
and the `agi: tier kid may not commit` message, `git status` exits 0 under
the same env, and a commit without AGI_TIER succeeds. Hook scripts present
and executable; dispatch.py L470-480 injects AGI_TIER + GIT_CONFIG for
kid/parent; suspenders patch confirmed at pi-autoresearch index.ts L2233-2237
(commit step now gated on `!AGI_TIER`). Linked this experiment as its own
evidence run (an experiment IS its run) and set the verdict to
inconclusive_lean_proved:80 — not `proved`, because no test performs a real
dispatch.py spawn and commits from the child: the dispatch-side half is
verified by source assertion only, not by a spawn run. That is the one step
that would close the remaining 20%.
<!-- THOUGHT:END -->

## Evidence

All 10 new tests pass. Full repo suite: 1520 passed, 2 skipped (unchanged from
baseline).

Verification commands:
```
python3 -m pytest extensions/agi/tests/test_git_commit_guard.py -v
# → 10/10 passed

python3 -m pytest extensions/agi/tests/ -q
# → 1520 passed, 2 skipped
```

**Root cause identified** at: `~/.pi/agent/git/github.com/davebcn87/pi-autoresearch/extensions/pi-autoresearch/index.ts`
lines 2243–2253 — `pi.exec("git", ["add", "-A"])` then `pi.exec("git", ["commit", "-m", msg])`
inside `log_experiment` tool's `execute()` handler for status `keep`.

**Files changed:**
1. `extensions/agi/hooks/agent-git/pre-commit` (new, executable)
2. `extensions/agi/hooks/agent-git/pre-push` (new, executable)
3. `extensions/agi/bin/dispatch.py` (inject AGI_TIER + GIT_CONFIG into spawn_env)
4. `extensions/agi/tests/test_git_commit_guard.py` (new, 10 tests)
5. `~/.pi/agent/git/github.com/davebcn87/pi-autoresearch/extensions/pi-autoresearch/index.ts` (suspenders guard)


## Agent Notes
Two-layer git commit guard: (belt) hooks/agent-git/ pre-commit/pre-push + dispatch.py injects AGI_TIER and GIT_CONFIG for kid/parent tiers; (suspenders) pi-autoresearch log_experiment skips git add/commit when AGI_TIER set. 10 new tests pass; full suite 1520 passed, 2 skipped. Root cause: pi-autoresearch index.ts log_experiment auto-commit.