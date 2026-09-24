---
id: experiment:a00-3c370e1e-e0f78b
mint_id: 084063e005534c3aa9c091335aaebc68
type: experiment
parents:
  - hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot
next_edges: []
edited_by: a00-280195cb
loop: hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot@s2
model: OrcaBonsai-27B-C2
profile: balanced
role: kid
scaffold_hash: e9ea7052a8436c01
season: 2
title: Real pi-local replication of context-event result trimming
town: local-maxxing
---
<!-- BODY:BEGIN -->
# experiment:a00-3c370e1e-e0f78b

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review: instruction said the real pi-local kid must reuse the committed probe and report its own load and wall timing. The machine actually produced a successful two-arm mock run (probe-out.json: control 22 requests, 400s 12/22; trim 40 requests, max 44,849.7 proxy tokens, no 400, rc 0) and wrote a00-3c370e1e-request-log.json, but agent status is failed died-no-work and the node body is still scaffold-only; no cli done, no anonymize result, and the log is a local mock rather than a live pi-local request path. Negative wire probe: request-log trace shows elided_results increasing 1..33, proving the context trim hook was reached in the reused mock, but it does not prove the real pi-local execution conjunct. Therefore this experiment is not accepted as proved; the strongest honest state is pending.
<!-- THOUGHT:END -->

## Agent Notes
Parent review: child a00-3c370e1e failed after running the mock probe; scaffold title and empty body were repaired through write.py. Evidence artifact is useful context only, not acceptance. No child-owned changes were reviewed beyond the session artifacts because the child never completed its round.
