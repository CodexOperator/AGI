---
id: experiment:a00-3c370e1e-e0f78b
mint_id: 084063e005534c3aa9c091335aaebc68
type: experiment
parents:
  - hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot
next_edges: []
edited_by: director-thought
loop: hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot@s2
model: OrcaBonsai-27B-C2
profile: balanced
role: kid
scaffold_hash: e9ea7052a8436c01
season: 2
title: Real pi-local replication of context-event result trimming
town: local-maxxing
verdict: inconclusive
---
<!-- BODY:BEGIN -->
# experiment:a00-3c370e1e-e0f78b

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
CORRECTED per thought-master TMM.118 (owed 2): original merge wrongly guessed OOM under memory_max 6G on the kids own scope, reasoning the kid loads the 27B itself -- it does not. The kid is a thin pi-local client; OrcaBonsai-27B-C2 is served by an always-on brain container (llama-server, docker scope) on :8080. Measured cause, from bytes: journalctl -k shows a GLOBAL oom-killer invocation at 15:13:0x 09-24 (trigger task mi-scavenger, likely a Node V8 GC scavenge pass, not this round), constraint=CONSTRAINT_NONE (system-wide, not this cgroup), which killed llama-server pid 477123 (docker-3afa536a7ae60f855b325bd3302bea43d254677e9e229525fa8ba257e0397e4e.scope, anon-rss 6.7 GB) -- the shared brain backend, not the kid. The kids own log shows its last real event immediately after: a 400, request (67981 tokens) exceeds the available context size (65536 tokens), then a compaction_start(overflow) with no further recovery -- consistent with its backend dying mid-conversation, not with the kids own memory. No evidence the kids own process was OOM-killed. Verdict: inconclusive -- the real-pi-local conjunct is untested, not disproved; the measured cause is a box-wide memory event that killed the shared model server, a dependency this round does not control. Residue: retry HOOK.02 only once the brain container has headroom confirmed before dispatch (or after whatever else was pressuring system memory at 15:13Z is identified), not blind.
<!-- THOUGHT:END -->

## Agent Notes
Parent review: child a00-3c370e1e failed after running the mock probe; scaffold title and empty body were repaired through write.py. Evidence artifact is useful context only, not acceptance. No child-owned changes were reviewed beyond the session artifacts because the child never completed its round.
