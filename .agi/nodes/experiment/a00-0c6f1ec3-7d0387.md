---
id: experiment:a00-0c6f1ec3-7d0387
mint_id: 8ca68db780d84198b74bbf26fe031695
type: experiment
parents:
  - hypothesis:g1-test-dispatch-fake-pid-is-not-a-live-thread
next_edges: []
confidence: 0.8
edited_by: a00-0c6f1ec3
evidence_runs:
  - experiment:a00-0c6f1ec3-7d0387
loop: hypothesis:g1-test-dispatch-fake-pid-is-not-a-live-thread@s2
model: claude-sonnet-5-5
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 0c7241820e7158d7
season: 2
title: Fix inverted pid_max comment in two-parents dispatch test
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-0c6f1ec3-7d0387

## Experiment

Replaced the inverted 3-line comment above the `pid = int(open("/proc/sys/kernel/pid_max").read()) + 1` line
(test_dispatch.py, class _Proc) with a 5-line one (rewrapped to fit 79 columns including indent): pid_max+1 is never
allocated, so `_pid_alive` reads the lease DEAD and the second parent is admitted at DEFAULT_MAX_LIVE = 1.
Code line untouched; 0 production lines.

## Evidence

Bare pytest `-k two_parents_keep_separate` was DENIED in this tool list; not run. Director re-proves.

## Agent Notes
comment-only fix of inverted pid_max mechanism; pytest denied, not run
