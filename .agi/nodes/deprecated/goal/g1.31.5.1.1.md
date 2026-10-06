---
id: goal:g1.31.5.1.1
mint_id: 091bb46cd2b447c48a04a816205a2109
type: goal
parents:
  - goal:g1.31.5.1
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.5.1.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 579ad3f0b4cba24e
season: 2
seeds: []
status: retired
tags:
  - engine
  - pass
  - pass-b3
  - missed
  - red
  - hook
title: "G1.31.5.1.1: the agent-git pre-commit kid-scope pipe runs under pipefail -- a failed git diff --cached refuses the commit, never exits 0"
town: core
---
# goal:g1.31.5.1.1

## Why this exists
goal:g1.31.5.1: PASS B3 round `l4-a-branch-kid-commits-its-own-bytes-under-the-agent-git-ho`, verify file `.agi/sessions/workflows/runs/mur-pb3chunk12of20/verify_l4-a-branch-kid-commits-its-own-bytes-under-the-agent-git-ho.json`, `missed` row n19 (red, pre-existing, from the l4-sm36 one-scope-rule round d3d96c3f8). The reviewer left it UNVERIFIED. It was measured at HEAD d4b7ead17 in a tmp repo:
```
tmp repo, .git/index corrupted     git diff --cached   rc 128
AGI_TIER=kid, own worktree          pre-commit          rc 0    <- FAIL-OPEN
control: staged .agi/config.json    pre-commit          rc 1    (refuses, as designed)

pre-commit:76-77   if git diff --cached --name-only -z --no-renames | python3 cli.py scope-check; then exit 0
                   (0 'pipefail' in the file; the if tests only the LAST command of the pipe)
cli.py:2300        paths = [p for p in sys.stdin.read().split("\0") if p]   -> []
cli.py:2302        return 0 if all(...) for p in paths)                     -> all([]) is True -> 0
```

## Target end-state
- `extensions/agi/hooks/agent-git/pre-commit:76-77`: the scope pipe runs under `set -o pipefail`, so a failed `git diff --cached` fails the `if`. The kid commit falls through to the refusal at the end of the file (`exit 1`), which means an empty change list that came from a FAILED diff fails CLOSED.
- A committed test in `extensions/agi/tests/test_git_commit_guard.py` feeds the hook a failing `git diff --cached` (a corrupted index in a tmp repo) and asserts the hook exits non-zero. A control row asserts that a healthy in-scope kid commit still exits 0.

## Invariants
- A residue is closed by a reviewed round, never by a note.
- ONE scope rule: the hook keeps delegating to `cli._round_scope_ok` through `scope-check` (hypothesis:l4-sm36 one-scope-rule). No second predicate is added in shell.
- An empty change list from a SUCCESSFUL diff stays whatever `scope-check` says today. Only a FAILED producer refuses.

## Falsifier
1. From /data/work/agi (rc 1 at HEAD d4b7ead17, measured: the hook exits 0):
```bash
bash -c 'T=$(mktemp -d); trap "rm -rf $T" EXIT; H=$PWD/extensions/agi/hooks/agent-git/pre-commit
cd $T && git init -q r && cd r && printf garbage > .git/index &&
! AGI_TIER=kid AGI_PROJECT_ROOT=$T/r AGI_TREE_PROJECT_ROOT=$T/r AGI_AGENT_ID=a00-fixture bash $H 2>/dev/null' &&
python3 -m pytest extensions/agi/tests/test_git_commit_guard.py -q -k failing_diff --basetemp /tmp/g13151a
```
2. Negative: `git grep -L pipefail -- extensions/agi/hooks/agent-git/pre-commit` returns zero hits (1 at HEAD).

## Out of scope
goal:g1.31.5.1.2 · goal:g1.31.5.1.3 · goal:g1.31.5.2 · goal:g1.31.5.3 · goal:g1.31.5.4 · goal:g1.31.5.5 · goal:g1.31.1-.4 · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6**.

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
