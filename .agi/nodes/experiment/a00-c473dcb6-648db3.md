---
id: experiment:a00-c473dcb6-648db3
mint_id: 47528fc418e4448ba7f42db8a7ea9085
type: experiment
parents:
  - hypothesis:brainstorm-and-research-review-contracts-match-their-manifests
next_edges: []
confidence: 0.98
edited_by: a00-5ced85f3
evidence_runs:
  - experiment:a00-c473dcb6-648db3
loop: hypothesis:brainstorm-and-research-review-contracts-match-their-manifests@s2
model: stealth/space-bunny-alpha
production_lines: 11
profile: balanced
role: kid
scaffold_hash: 1519f2f484d07ac7
season: 2
title: Brainstorm goal gate and research refute manifest contracts pass
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# Brainstorm and research-review contracts repaired in production

## Method

| production half | change | focused guard |
|---|---|---|
| `agi-brainstorm` | Both descriptions name `goal` as required; JS throws before `phase()`/dispatch when `goal` is absent, null, or whitespace-only. | Executed the workflow body under Node with `{idea: "idea:x"}` and required the named error. |
| `agi-research-review` refute | Manifest prompt instructs and declares `batch_empty`; manifest schema defines it as boolean and requires it, matching JS. | Parsed stated top-level keys from manifest prompt, manifest schema, and JS prompt and compared them exactly. |

Changed production files:

- `extensions/agi/workflows/agi-brainstorm.js`
- `extensions/agi/workflows/brainstorm.json`
- `extensions/agi/workflows/research-review.json`

Changed test files:

- `extensions/agi/tests/test_workflow.py`
- `extensions/agi/tests/test_research_review_refute_contract.py`

## Result

```text
python3 -m pytest extensions/agi/tests/test_workflow.py::test_brainstorm_manifest_and_js_require_nonempty_goal extensions/agi/tests/test_research_review_refute_contract.py -q -p no:cacheprovider
...                                                                      [100%]
3 passed in 0.72s
```

The final permitted `git diff --numstat` over production paths reported 11 added and 3 removed lines, below the 40-line production ceiling.

## Evidence

The pre-fix scratch reproduction remains `experiment:a00-a236a08e-6de386`. This run changes the named production bytes and passes one focused contract test per workflow, satisfying the build claim rather than merely reproducing its defect.

## Agent Notes
Built both production contract fixes and passed 3 focused contract tests; production delta is 11 added/3 removed lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The instruction said to implement both contract repairs, and the machine bytes now show the required goal check at agi-brainstorm.js:12-14, required-goal documentation in brainstorm.json, and batch_empty in both the research-review manifest prompt and schema. The near miss was only changing the test to accept the old divergence; instead the production workflow now rejects before phase/agent dispatch. Negative probes: gate—Node execution with idea only exits nonzero with the named non-empty goal error; wire—manifest prompt/schema extraction returned the exact seven refute keys including batch_empty. The first kid was a measurement-only run and remains demoted; this build run is accepted as the evidence for the repaired claim.
<!-- THOUGHT:END -->
