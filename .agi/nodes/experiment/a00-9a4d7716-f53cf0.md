---
id: experiment:a00-9a4d7716-f53cf0
mint_id: 96f043d2d51e470986b38bda3eb5a5d1
type: experiment
parents:
  - hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow
next_edges: []
confidence: 0.5
edited_by: a00-aa84faa3
evidence_runs:
  - experiment:a00-9a4d7716-f53cf0
loop: hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 222a7c81d6619162
season: 2
title: Probe the remaining round payload fields
town: core
verdict: inconclusive_lean_proved:50
---
<!-- BODY:BEGIN -->
# experiment:a00-9a4d7716-f53cf0

## Experiment — isolate the remaining round payload seam

I inspected the landed `_run_round_stage` and `_round_git_harvest` seam in `extensions/agi/bin/workflow.py`. The existing implementation dispatches exactly once, polls the dispatch manifest, requires the branch's done commit, and harvests the committed range from the recorded `branch`/`base_branch` refs. I then checked the structured return at the completion call site.

The completion return currently contains:

```text
key, hypothesis, parent, branch, old_tip, new_tip, files
```

It does not yet contain `experiments` or `verdict`, and no configured round-mur/round-research-review manifests were added in this seam. Therefore this experiment is a targeted payload-completeness probe, not a claim that the full workflow is finished. The useful negative evidence is explicit: the remaining review context cannot yet be assembled without a separate source-of-truth decision for the parent experiment and verdict nodes.

## Evidence

- Source inspection of `_round_git_harvest` and `_run_round_stage` shows provenance-preserving refs and fail-closed rc 3 behavior already landed by `experiment:a00-f2c939d7-b49ffd`.
- The completion return at `_run_round_stage` is keyed by the fields listed above; it emits no `experiments` or `verdict` fields.
- No production bytes were changed in this continuation, so this is a 0-production-line experiment and does not imply a new code ceiling.

The result supports the parent hypothesis only partially: round dispatch and committed harvest are present, while payload completeness, manifest registration, and end-to-end failure suppression remain open.

## Agent Notes
Source probe confirmed committed harvest is landed while experiments/verdict payload fields and manifest registration remain open.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review: instruction was to isolate remaining payload fields rather than overclaim. Machine inspection of workflow.py:2180-2182 shows the completion return includes key/hypothesis/parent/branch plus committed-range harvest, but no experiments/verdict; the repository also has no configured round-mur/round-research-review manifests. My gate probe is the empty required payload: a completion record cannot produce those two fields, so the review context is incomplete rather than silently valid. The near miss is emitting empty lists/nulls, which would satisfy a key-presence assertion while losing source-of-truth provenance. I accept this as a 50% lean baseline, not evidence for the full claim; no production bytes moved. probes: gate=required experiments/verdict fields absent; wire=round completion return is the live payload source and stops at files.
<!-- THOUGHT:END -->
