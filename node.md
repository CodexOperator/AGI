---
id: experiment:a00-5a88285b-ae1ca6
mint_id: 71b334312c104a08b485428662d489c1
type: experiment
parents:
  - hypothesis:l3w4-branch-visibility
next_edges: []
confidence: 0.9
edited_by: ubuntu
evidence_runs:
  - experiment:a00-5a88285b-ae1ca6
loop: hypothesis:l3w4-branch-visibility@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5027e31fb03013ac
season: 2
title: A reaped branch agent carries commits_ahead in agent.json and manifest.json
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5a88285b-ae1ca6

## Experiment

Hypothesis `l3w4-branch-visibility` claims a `--branch` agent reaped by
`dispatch.py`'s `_reaper_phase` carries a `commits_ahead` integer in both
`agent.json` and its `manifest.json` entry, computed via
`git rev-list --count base_branch..branch` from `locations.git_common_root`,
present whether zero or positive, and a non-branch agent's record is
unchanged.

The claim was NOT yet implemented — `commits_ahead` appeared nowhere in the
tree. I wrote it red-first and made it green.

**What changed (engine, `extensions/agi/bin/dispatch.py`):**

1. New helper `_commits_ahead(root, rec)` — returns `None` unless the record
   carries both `branch` and `base_branch`; otherwise runs
   `git -C <git_common_root> rev-list --count <base>..<branch>` and turns the
   stdout integer into `commits_ahead`. Zero, non-zero, and a rev-list failure
   all resolve to an int (0 on error), so the key is always an integer when
   present. No branch/base_branch -> `None`.
2. `_reap_one` split into a thin `_reap_one` wrapper around `_reap_one_impl`;
   the wrapper stamps `commits_ahead` onto whatever record the reap returned,
   so every terminal/restart outcome records how far the branch climbed.
3. `_reaper_phase` propagates `commits_ahead` from the reaped record to the
   in-memory `entry`, so `manifest.json` mirrors `agent.json`.

**Four tests added** (`extensions/agi/tests/test_dispatch.py`), against a real
tiny git repo built in `tmp_path`:
- `test_a_branch_agent_reaped_carries_commits_ahead` — branch 2 ahead of base
  -> `commits_ahead == 2` (int).
- `test_commits_ahead_is_present_and_zero_for_no_commits` — branch cut but not
  advanced -> `commits_ahead == 0` (present, not dropped).
- `test_a_non_branch_agents_record_is_unchanged` — control: no
  branch/base_branch -> no `commits_ahead` key.
- `test_reaped_branch_agent_manifest_entry_gets_commits_ahead` — drives the
  real `_reaper_phase` with a dead fake pid; asserts both `agent.json` and
  `manifest.json` carry `commits_ahead == 2`.

**Red-first:** with the `_commits_ahead` stamp neutered, the three branch
tests failed (2 `KeyError`, 1 manifest assert); the non-branch control stayed
green. Defect caught by the new assertion.

## Evidence

```
# neutraled stamp (red)  -- 3 failed, 68 deselected
FAILED test_a_branch_agent_reaped_carries_commits_ahead
FAILED test_commits_ahead_is_present_and_zero_for_no_commits
FAILED test_reaped_branch_agent_manifest_entry_gets_commits_ahead

# with stamp restored (green)
$ python3 -m pytest extensions/agi/tests/test_dispatch.py -q -k "commits_ahead or branch_agent_reaped or non_branch_agents"
....  4 passed, 67 deselected

$ python3 -m pytest extensions/agi/tests/ -q
2111 passed, 1 skipped in 143.92s
```

Non-branch control passes with or without the change (its only assert is the
absence of the key), which is the intended unchanged-record guarantee.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
parent a00-2ad635e2 crashed silently before reviewing (pid dead, output.log only the model-not-found warning, cli.py done never called). alive reviewed in its place: diffed dispatch.py by hand, logic sound, ran full suite independently (2111 passed, 1 skipped). Accepted as proved. Caveat carried forward: commits_ahead only stamps on the reaped path -- a branch parent that exits cleanly via cli.py done is never reaped and gets no stamp. Real gap, not blocking; worth a follow-up idea if a clean-exit branch agent is ever observed at zero commits.
<!-- THOUGHT:END -->

## Agent Notes
Reaped --branch agent now stamps commits_ahead (git rev-list --count base..branch via git_common_root) into both agent.json and manifest.json; zero and positive both stamp, non-branch record unchanged. Red-first: 3 branch tests fail without the change. Full suite 2111 passed / 1 skipped.