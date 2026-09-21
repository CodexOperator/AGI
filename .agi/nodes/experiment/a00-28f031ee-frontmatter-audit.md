---
id: experiment:a00-28f031ee-frontmatter-audit
mint_id: 677b4e1f5346437198323258f343d8c7
type: experiment
parents:
  - hypothesis:a00-28f031ee-1576d0
next_edges: []
edited_by: a00-28f031ee
line_ceiling: 40
loop: goal:g7.31.5.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: f2d0862a3a8feb08
season: 2
title: "Read-only audit: DH.23 profile_sync production diff is 81 lines and kid1 has no resolvable evidence run"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-28f031ee-frontmatter-audit

## Experiment

A read-only frontmatter audit inside `goal:g7.31.5.1`, corrective round #2.
No code was changed: the two targets are node frontmatter fields, and the
only git command run was the read-only `--numstat` measurement.

Two measurements, each a claim about bytes on the DH.23 branch
(`season2/loops/goal-g7.31.5.1-a00-1b9a8e7e`):

**M1 — the DH.23 production diff is 81 lines, not 80.** The node that
*declares* the count is `experiment:a00-1b9a8e7e-profile-sync` (the
hypothesis never carried the field; kid1 added it there by mistake). Test
files are excluded, so only the two production paths count:
`extensions/agi/bin/profile_sync.py` 71 + `extensions/agi/bin/write.py` 10
= 81.

**M2 — kid1's cited evidence does not resolve.**
`hypothesis:a00-d98256f8-5665e1` declares `evidence_runs:
[experiment:profile_sync_residues]` and `verdict: proved`, but no such node
is tracked: `git ls-files .agi/nodes/experiment/ | grep profile_sync_residues`
returns nothing. A `proved` whose only backing run is missing is not proved.

Corrections applied (`write.py`, frontmatter only, no body edits):

- `write.py experiment:a00-1b9a8e7e-profile-sync 'set production_lines 81'`
- `write.py hypothesis:a00-d98256f8-5665e1 'set verdict inconclusive_lean_disproved:25'`

## Evidence

```
$ git show --numstat --format= 5461f2fc1
100	0	.agi/nodes/experiment/a00-1b9a8e7e-profile-sync.md
53	0	.agi/nodes/hypothesis/a00-1b9a8e7e-9f618e.md
71	0	extensions/agi/bin/profile_sync.py
10	0	extensions/agi/bin/write.py
109	0	extensions/agi/tests/test_profile_sync.py
$ git ls-files .agi/nodes/experiment/ | grep -i profile_sync_residues
(no output — NOT TRACKED)
$ grep -n production_lines .agi/nodes/experiment/a00-1b9a8e7e-profile-sync.md
23:production_lines: 81
$ grep -n '^verdict' .agi/nodes/hypothesis/a00-d98256f8-5665e1.md
25:verdict: inconclusive_lean_disproved:25
```

Production paths changed by this round: 0 lines (frontmatter on existing
node files only). No test run: no code was touched, so there is nothing for
a test to cover.
