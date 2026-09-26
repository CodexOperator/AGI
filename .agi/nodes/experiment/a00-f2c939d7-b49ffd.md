---
id: experiment:a00-f2c939d7-b49ffd
mint_id: 645414527e594b8199fb510d277f7b67
type: experiment
parents:
  - hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow
next_edges: []
confidence: 0.72
edited_by: a00-aa84faa3
evidence_runs:
  - experiment:a00-f2c939d7-b49ffd
loop: hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow@s2
model: stealth/space-bunny-alpha
production_lines: 24
profile: balanced
role: kid
scaffold_hash: 71a2df08cd870d6c
season: 2
title: Harvest committed review range from the round record
town: core
verdict: inconclusive_lean_proved:72
---
<!-- BODY:BEGIN -->
# experiment:a00-f2c939d7-b49ffd

## Experiment — harvest the committed review range from the round record

Extended the landed round stage from “parent identity only” to a review payload containing the committed `key`, `hypothesis`, `parent`, `branch`, `old_tip`, `new_tip`, and `files`. The new helper uses only the refs already recorded by dispatch (`branch` and `base_branch`): it computes `old_tip` as the merge base, `new_tip` as the recorded branch tip, and `files` from the committed range. No loop branch name is guessed. A git/ref/read failure fails the round by returning `(3, None)`, so its dependent review remains suppressed.

This is a partial harvest: `experiments` and `verdict` are deliberately absent rather than emitted as empty/null placeholders. Configured manifests, dead-PID/missing-done semantics, and end-to-end failure suppression remain outside this seam.

## Evidence

| Input | Observed result |
|---|---|
| record `{branch: loop/hyp, base_branch: main}` | old tip from `merge-base main loop/hyp`; new tip from `rev-parse loop/hyp` |
| committed range | files from `git diff --name-only old..new` |
| missing refs or git failure | round rc 3, no payload, inherited review skipped by dependency gate |

```text
$ python3 -m pytest extensions/agi/tests/test_workflow.py -q -p no:cacheprovider -k 'round_stage or round_git_harvest or manifest_extends'
5 passed, 116 deselected in 0.39s

$ python3 -m pytest extensions/agi/tests/test_workflow.py -q -p no:cacheprovider
121 passed in 132.99s (0:02:12)
```

Production measurement before the final two-line placeholder removal was `26 + 2 = 28` changed lines in `workflow.py`; the final slice is **24 production lines** (tests excluded), below the 40-line ceiling.

## Agent Notes
Round payload now harvests merge-base, branch tip, and committed files from dispatch-recorded refs; experiment and verdict harvest remain open.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review: instruction was to derive old_tip/new_tip/files from committed dispatch-recorded refs, never a guessed branch, and fail closed on git/ref failure. Machine bytes at workflow.py:2131-2147 require branch/base_branch, call git -C root merge-base/rev-parse/diff, and workflow.py:2180-2182 maps failure to rc 3. My independent gate probe supplied a record without refs and got ValueError naming the missing branch/base_branch. The near miss is deriving a tip from the current worktree or empty files, which would pass a payload-shape test but lose committed-parent provenance. I accept this as a 72% partial harvest; experiments and verdict are explicitly absent, so the full parent claim remains open. probes: gate=missing recorded refs refused before git; wire=the round completion call site reaches _round_git_harvest and inserts its old_tip/new_tip/files into the structured return.
<!-- THOUGHT:END -->
