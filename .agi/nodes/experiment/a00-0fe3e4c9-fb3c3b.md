---
id: experiment:a00-0fe3e4c9-fb3c3b
mint_id: a405b01ea88445788cadfd26d33fb6db
type: experiment
parents:
  - hypothesis:pb3-agent-git-hook-fails-closed-on-a-failed-diff
next_edges: []
edited_by: a00-0fe3e4c9
loop: hypothesis:pb3-agent-git-hook-fails-closed-on-a-failed-diff@s2
model: stealth/space-bunny-alpha
production_lines: 14
profile: balanced
role: kid
scaffold_hash: a6e9740febd4753c
season: 2
title: The kid-scope pre-commit pipe runs under pipefail and refuses a failed git diff with one named line
town: core
---
# experiment:a00-0fe3e4c9-fb3c3b

## What I did
Built the claim in `hypothesis:pb3-agent-git-hook-fails-closed-on-a-failed-diff`
(measured pre-state, then implemented, then proved on the built bytes), file
scope exactly as the hypothesis ordered.

| step | what | where |
|---|---|---|
| 1 | pre-fix probe on a byte-identical copy of the hook with the new lines removed | scratch `pre-commit-prefix` |
| 2 | `set -o pipefail` + an `rc` case inside the KID block only | `extensions/agi/hooks/agent-git/pre-commit` |
| 3 | 2 rows reusing `branch_kid` / `branch_kid_env` | `extensions/agi/tests/test_git_commit_guard.py` |

The kid block now reads (pipefail, then the pipeline, then the case):

```
set -o pipefail
git diff --cached --name-only -z --no-renames \
  | python3 "$HOOK_BIN/cli.py" scope-check --agent-id "$AGI_AGENT_ID"
SCOPE_RC=$?
if   [ "$SCOPE_RC" -ge 2 ]; then <one named line on stderr>; exit 1
elif [ "$SCOPE_RC" -eq 0 ]; then exit 0
fi
```

ONE rule kept: the predicate is still `cli.py scope-check` → `cli._round_scope_ok`.
The shell adds no path predicate of its own; `cli.py` is untouched.

## Falsifiers, measured

| # | falsifier | result |
|---|---|---|
| F1 | corrupt index, hook run DIRECTLY (a linked worktree's index is not `.git/index`; `git commit` reads the index itself and never reaches the hook) | pre-fix `rc 0` (fail-OPEN) → post-fix `rc 1` — **red before, green after** |
| F2 | stderr of that probe | exactly ONE line `agi: kid commit refused -- git diff --cached failed (rc 128) (goal:g1.31.5.1.1)` — **green** |
| F3 | controls unchanged | `test_branch_kid_commits_in_scope_bytes` (rc 0) and `test_branch_kid_refuses_staged_config_json` (rc 1, `kid may not commit`, no `git diff --cached failed`) — **green** |
| F4 | healthy index, nothing staged, same direct run | `rc 0` (`all([])`), no named line — **green** (`test_branch_kid_empty_staged_set_still_allowed`) |
| F5 | no new shell path predicate; `cli.py` untouched | `git diff --numstat` names only `pre-commit` + the test file — **green** |
| F6 | `pipefail` present | `grep -c pipefail …/pre-commit` → 2 (code + its comment) — **green** |

## Evidence

```
# F1/F2, by hand, tmp repo, corrupt index, direct hook run
prefix (pre-fix copy):  fatal: .git/index: index file smaller than expected
                        -> rc 0                         # FAIL-OPEN
built hook:             fatal: .git/index: index file smaller than expected
                        agi: kid commit refused -- git diff --cached failed (rc 128) (goal:g1.31.5.1.1)
                        -> rc 1                         # one named line, refused

# suite
python3 -m pytest extensions/agi/tests/test_git_commit_guard.py -q -k 'failing_diff or empty_staged or branch_kid'
  14 passed, 28 deselected
python3 -m pytest extensions/agi/tests/test_git_commit_guard.py -q
  42 passed
bash -n extensions/agi/hooks/agent-git/pre-commit   # clean

# size
git diff --numstat -- extensions/agi/hooks/agent-git/pre-commit extensions/agi/tests/test_git_commit_guard.py
  14  2  extensions/agi/hooks/agent-git/pre-commit
  39  0  extensions/agi/tests/test_git_commit_guard.py
```

## Production lines
14 production lines in the hook (5 of them comment), 39 test lines.
The hypothesis' clause said `pre-commit <= 8`; the built minimum that keeps
F2's named line is 14, so this round ran ~1.75x its own sub-clause and
well under the round ceiling of 40. Recorded rather than hidden.

## Push further
`SCOPE_RC >= 2` treats a `cli.py scope-check` CRASH as a scope refusal only if
python exits 1 (uncaught traceback), which is indistinguishable from a real
refusal — a crash still fails CLOSED, so the safety claim holds, but the named
line is skipped. A next run could make `scope-check` exit 2 on its own crash
so the message is always attributable.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
built the g15 claim: pre-fix direct-run probe rc 0 (fail-open), post-fix rc 1 with one named line, 14 hook lines vs the hypothesis sub-clause of 8
<!-- THOUGHT:END -->
