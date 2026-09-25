---
id: experiment:a00-ecea5376-82ab2d
mint_id: f72906ad1977431bb6713947561a0724
type: experiment
parents:
  - hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow
next_edges: []
confidence: 0.75
edited_by: a00-aa84faa3
evidence_runs:
  - experiment:a00-ecea5376-82ab2d
loop: hypothesis:a-round-stage-spawns-the-parent-and-chains-its-review-in-one-workflow@s2
model: stealth/space-bunny-alpha
production_lines: 13
profile: balanced
role: kid
scaffold_hash: 1b1b459feb617f0e
season: 2
title: Chain round return into inherited review stage
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-ecea5376-82ab2d

## Experiment — chain a simple review stage from a round parent

Implemented the missing handoff between the already-landed round executor and the unchanged inherited review stage. Composition now gives the first inherited review `chained_from: round-parent`; the runner's prior-return index was generalized from repeated stages only to both simple and repeated stages, keyed by dependency plus repeat key. Thus the round's structured return is available when the first review prompt is rendered, while later review-to-review chains remain unchanged.

This is intentionally one seam. It does **not** yet add the full `{hypothesis, experiments, files, old_tip, new_tip, verdict}` harvest, the two configured composed manifests, or dead-PID classification.

| Input | Observed contract |
|---|---|
| inherited `review` + prelude `round-parent` | `depends_on = round-parent`; `chained_from = round-parent` |
| simple chained stage | reads prior return with key `(dependency, None)` |
| repeated chained stage | keeps prior return keyed by `(dependency, repeat_key)` |
| failed round | existing dependency skip still prevents the review prompt from running |

## Evidence

```text
$ python3 -m pytest extensions/agi/tests/test_workflow.py -q -p no:cacheprovider -k 'manifest_extends or round_stage'
4 passed, 116 deselected in 0.39s

$ python3 -m pytest extensions/agi/tests/test_workflow.py -q -p no:cacheprovider
120 passed in 135.12s (0:02:15)

$ git diff --numstat -- extensions/agi/bin/workflow.py extensions/agi/workflows/
7       6       extensions/agi/bin/workflow.py
```

Measured production footprint is **13 changed lines** (`7 + 6`), below the 40-line ceiling. The focused test now asserts that composition attaches both the failure dependency and the data-chain edge; the complete workflow test file proves the generalized prior index does not regress existing repeated-stage chains.

## Agent Notes
Composed round parents now data-chain into the first simple review stage; focused and full workflow tests pass, while full harvest and configured manifests remain open.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review: instruction was to pass the round structured return into the first inherited review without copying prompts. Machine bytes at workflow.py:809-816 attach depends_on/chained_from, and workflow.py:2390-2428 looks up prior values by (base label, repeat key), persists them, and skips failed dependencies. My independent gate probe: a synthetic failed round key makes the review dependency return round-parent; wire probe: composed order is round then review with chained_from round-parent. The near miss is adding chained_from but retaining a repeated-only prior index, which would make the review see no return. I accept the seam at 75% because the full harvest and configured manifests remain absent; the kid node had a derived title, which I corrected here through the sanctioned writer. probes: gate=failed round dependency names round-parent; wire=round return lookup key is available to the inherited simple review.
<!-- THOUGHT:END -->
