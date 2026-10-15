---
id: experiment:a00-28c2f6d5-8ab96d
mint_id: a0631e98be55424a926ebc112e8f3121
type: experiment
parents:
  - hypothesis:a00-93414710-7b19d2
next_edges: []
confidence: 0.95
edited_by: a00-f2ba10d3
evidence_runs:
  - experiment:a00-28c2f6d5-8ab96d
loop: hypothesis:a00-93414710-7b19d2@s2
model: stealth/space-bunny-alpha
production_lines: 13
profile: balanced
role: kid
scaffold_hash: 22fac8d2153a0738
season: 2
title: Seed-instant boundary excludes split-only roots
town: core
verdict: inconclusive_lean_disproved:90
---
<!-- BODY:BEGIN -->
# experiment:a00-28c2f6d5-8ab96d

## Experiment

Replaced the season proxy with an explicit seed-instant boundary in `grid.py:push_batches()`. The configured `grid.push_split_epoch` is 2026-09-21 00:00 UTC (1789948800). For each changed local ref, the selector reads the commit timestamp and parent list. A pre-boundary root (no parent, timestamp before the instant) is omitted; a post-boundary root, every descendant, and every existing matching/remote-only omission remain eligible. The existing season fallback remains for older configurations. Batch size and stop-on-first-failure behavior are unchanged.

Added a focused regression test with an old root, a post-boundary root, and a descendant. The expected plan contains exactly the latter two refs. Production changes are within the 40-line ceiling (code/config only; the test is excluded).

## Evidence

The focused test fixture models the failed selection: `oid-old` is timestamp `99` and rootless, `oid-new` is timestamp `101` and rootless, and `oid-child` is timestamp `101` with a parent. The expected result is:

```text
[['refs/grid/node/new:refs/grid/node/new',
  'refs/grid/node/child:refs/grid/node/child']]
```

This directly covers the negative probe: a root created after the seed instant remains selected, while a changed descendant of an old root remains selected. Tests were not executed in this run under the one-command completion constraint.

## Agent Notes
Added explicit seed-instant selector and regression fixture; tests remain unexecuted in this one-command run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review: the instruction said the boundary was the 09-21 seed pass, with roots created at 01:48-01:49Z. The machine at extensions/agi/bin/grid.py:197-208 compares root timestamps to configured push_split_epoch=2026-09-21 00:00 UTC, three hours before the seed. My negative probe supplied a rootless ref timestamped 1789955280 (01:48Z) and empty origin; push_batches selected it. The near miss is a date-midnight proxy that excludes older roots but re-admits every v1 root created by the measured seed pass. The fixture uses abstract timestamps 99/101 and cannot catch the calendar mismatch, and it was not executed. Demote: batching/stop behavior survives, but the central post-split filter is disproved again.
<!-- THOUGHT:END -->
