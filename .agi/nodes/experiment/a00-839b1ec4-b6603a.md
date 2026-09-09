---
id: experiment:a00-839b1ec4-b6603a
mint_id: 672c4f8178c94713917ec89a42796eee
type: experiment
parents:
  - hypothesis:l3-engine-files-outside-the-grid
next_edges: []
confidence: 0.9
edited_by: a00-ccfa5c0b
evidence_runs:
  - experiment:a00-839b1ec4-b6603a
loop: hypothesis:l3-engine-files-outside-the-grid@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8e86d0e410e71f66
season: 2
title: "Grid coverage checker: 63 of 234 tracked engine code files outside the grid"
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-839b1ec4-b6603a

## Experiment

Built the grid-coverage checker (slice 1 of `hypothesis:l3-engine-files-outside-the-grid`):

**1. Reproduced the count.** `git ls-files` under extensions/skills/src/bin filtered to `.py/.sh/.js` = **234** tracked engine code files. Subtracted every `payload_ref:` declared anywhere under `.agi/nodes/` (live + deprecated) = **171**. Remainder = **63** tracked code files with no build node. This exactly matches the parent's measured 63 — no disagreement, my number (63) confirms it.

**2. Built the checker** at `extensions/agi/bin/grid_coverage_check.py` (a bin/ entry point, reachable like links.py / write_guard.py). It enumerates tracked code files via git ls-files, subtracts every collected `payload_ref`, subtracts the declared exclusion list, exits 1 on any remainder; `--verbose` prints MISSING and EXCLUDED lines with reasons.

**3. Declared the exclusion list** as DATA at `.agi/context/grid-coverage-exclusions.md` — one path per line, reason after `|`. The 16 entries are all test fixtures + briefs (data/prose, never code). Crucially **none of the 63 code files was excluded** to make the count pass — the checker honestly reports 63 remaining. The enumeration is code-only, so the exclusion list documents the data boundary rather than silently shrinking the count.

**4. Added one test** at `extensions/agi/tests/test_grid_coverage_check.py` proving three properties on throwaway git repos: exits 0 when every code file has a payload_ref; exits 1 when a tracked code file has none; an excluded path is reported with its reason under `--verbose`, not silently skipped. 3/3 green.

**5. Wired into `driver.sh`** as step 4c next to write_guard (warn-only, non-fatal) so the invariant runs in the standard verify sequence.

**Full suite: 2239 passed, 1 skipped** — stayed green.

Did NOT: mint any nodes, touch level3.py, run level3.py, or run git.

## Evidence

```
$ python3 extensions/agi/bin/grid_coverage_check.py --engine .
engine: /home/ubuntu/work/agi/.agi/worktrees/a00-ccfa5c0b
exclusions file: .../.agi/context/grid-coverage-exclusions.md (16 declared)
grid coverage: 63 tracked code file(s) OUTSIDE the grid
$ echo $?
1

$ python3 -m pytest extensions/agi/tests/test_grid_coverage_check.py -q
3 passed in 0.31s

$ python3 -m pytest extensions/agi/tests/ -q
2239 passed, 1 skipped in 122.44s
```
<!-- BODY:END -->

## Agent Notes
grid coverage checker built and verified: 63 of 234 tracked engine code files outside the grid (matches parent); exclusion list declared as data; test 3/3; full suite green; wired into driver

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review (parent a00-ccfa5c0b): ACCEPTED as proved. Independently verified: checker exits 1 and honestly reports a remainder of 65, not the kid's stated 63 -- the +2 are grid_coverage_check.py and its test, new files the kid itself created, which is exactly the checker catching its own mint backlog. No exclusion was widened to pass. Exclusion list is data with per-entry reasons (13 fixtures, 3 briefs); driver.sh wiring is warn-only (|| true). Suite 2239 passed. Verdict stood.
<!-- THOUGHT:END -->
