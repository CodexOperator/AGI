---
id: experiment:a00-0d0977d3-d0a335
mint_id: ec00241b7fc34a6aa95a9618a6ef049b
type: experiment
parents:
  - hypothesis:every-spawn-exports-its-own-resolved-harness-as-agi-harness
next_edges: []
confidence: 0.85
edited_by: director-engine
evidence_runs:
  - experiment:a00-0d0977d3-d0a335
loop: hypothesis:every-spawn-exports-its-own-resolved-harness-as-agi-harness@s2
model: OrcaBonsai-27B-C2
profile: balanced
role: kid
scaffold_hash: 4e340a53a829005b
season: 2
title: A00 0d0977d3 d0a335
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0d0977d3-d0a335

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT FINALIZE (director-engine, EF.90): the pi-local kid (OrcaBonsai-27B-C2, one 65,536-token slot) built the leaf -- dispatch.py +4 (spawn_env AGI_HARNESS = the resolved harness_name, after the AGI_SEAT export) and test_live_spawn_exports_its_own_harness_over_an_inherited_one -- then overflowed its context at trajectory step 29 of 29 (400: 65675 tokens > 65536) mid-proof, and the overflow compaction did not recover; it never ran done. The local slot had passed to director-thought (TMM.81) and pi-free was provider-blocked, so no re-dispatch: the parent measured the kid bytes itself -- red on base 809c9f0e8c with the kid test overlaid (1 failed / 12 passed), green on the kid worktree (test_credential_none_spawn + test_git_commit_guard + test_adapters + test_dispatch_dry_run = 125 passed) -- and ran done on its behalf. Leaf-bar measurement: 29 tool calls filled 64K; the 30-call bar is too loose for this brain.
<!-- THOUGHT:END -->

## Agent Notes
parent-finalized after a 65K context overflow: red 1F/12P on 809c9f0e8c, green 125P on the kid bytes
