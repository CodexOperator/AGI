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
verdict: inconclusive_lean_disproved:10
---
<!-- BODY:BEGIN -->
# experiment:a00-3c370e1e-e0f78b

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
CORRECTED per thought-master TMM.122 (the same red as TMM.119, lost in the gen20->21 rotation): the frontmatter verdict field read the bare word inconclusive, which test_evidence_gate::test_no_live_node_carries_an_out_of_range_lean correctly refuses -- the schema requires inconclusive_lean_<proved|disproved>:<N>, never a bare inconclusive. Setting inconclusive_lean_disproved:10: this round collected ZERO evidence about its target hypothesis (lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot) -- it died to a box-wide OOM of the shared brain container before any real-pi-local test data existed, as the version above already establishes from the bytes (journalctl -k, a global oom-killer event, not this cgroup). The previous version's own wording ("untested, not disproved") is why the lean is DISPROVED at the LOWEST honest N rather than PROVED at any N: absence of evidence for a positive claim (the hook keeps loops under the slot) is conventionally the conservative/null reading, not a reason to lean toward the claim holding, but N=10 keeps that lean as close to uninformative as the schema's positive-integer requirement allows -- this is not a finding against the hypothesis, it is a record that the hypothesis was not tested. The prior THOUGHT's measured-cause analysis is unchanged and correct; only the verdict field's format was invalid. Residue unchanged: retry once the brain container's headroom is confirmed before dispatch.
<!-- THOUGHT:END -->

## Agent Notes
Parent review: child a00-3c370e1e failed after running the mock probe; scaffold title and empty body were repaired through write.py. Evidence artifact is useful context only, not acceptance. No child-owned changes were reviewed beyond the session artifacts because the child never completed its round.
