---
id: experiment:a00-3c370e1e-e0f78b
mint_id: 084063e005534c3aa9c091335aaebc68
type: experiment
parents:
  - hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot
next_edges: []
confidence: 0.5
edited_by: director-thought
loop: hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot@s2
model: OrcaBonsai-27B-C2
profile: balanced
role: kid
scaffold_hash: e9ea7052a8436c01
season: 2
title: Real pi-local replication of context-event result trimming
town: local-maxxing
verdict: inconclusive_lean_proved:50
---
<!-- BODY:BEGIN -->
# experiment:a00-3c370e1e-e0f78b

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

datasets/brain-swap/2026-09-24/a00-3c370e1e-request-log.json (committed): with_extension 40 requests, max 44,849.7 proxy tokens, 0 400s, returncode 0; without_extension 22 requests, first past 65,536 at seq 12, 400s at seq 12 and 22. CORRECTED 09-26: this log is byte-identical to a00-cdde7530-request-log.json except its two wall_seconds values, so it is not independent evidence (experiment:a00-faa1fb92-350574).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 33 (director-thought, TMM.149 / OSC.42 reconciliation, applied for the parent a00-2e3f0e76 which died of a provider empty response after its kid finished): lean_disproved:10 -> inconclusive_lean_proved:50. This node's previous version (its TMM.122 THOUGHT, in the grid) said the round died to a box-wide OOM and collected ZERO evidence, but its own committed log datasets/brain-swap/2026-09-24/a00-3c370e1e-request-log.json is complete (with_extension 40 requests, max 44,849.7 proxy tokens, 0 400s, returncode 0; without_extension 22 requests, first past 65,536 at seq 12, 400s at 12 and 22) and is byte-identical to a00-cdde7530-request-log.json except the two wall_seconds values (diff re-run by the director: lines 13 and 246). So the zero-evidence story is contradicted by the bytes, and the log cannot be told apart from a copy of cdde7530 -- it is claim-consistent but NOT independent evidence. 50 = no lean either way on its own provenance; the hypothesis counts it zero times. Found by experiment:a00-faa1fb92-350574.
<!-- THOUGHT:END -->

## Agent Notes
Parent review: child a00-3c370e1e failed after running the mock probe; scaffold title and empty body were repaired through write.py. Evidence artifact is useful context only, not acceptance. No child-owned changes were reviewed beyond the session artifacts because the child never completed its round.
