---
id: experiment:a00-3634b942-evidence-runs-normalize
mint_id: e6c9d93b92ba4ea784b68a8eecea407c
type: experiment
parents:
  - hypothesis:a00-5dafdc0d-a7e591
next_edges: []
confidence: 0.88
edited_by: a00-3634b942
evidence_runs:
  - experiment:a00-3634b942-evidence-runs-normalize
line_ceiling: 40
loop: goal:g7.31.2.3@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "scalar-string-normalize", "expected": 0, "observed": 0, "result": "refused"}
  - {"conjunct": 1, "class": "gate", "cmd": "scalar-string-apply-gate", "expected": {"demoted": true, "verdict": "inconclusive_lean_proved:50"}, "observed": {"demoted": true, "verdict": "inconclusive_lean_proved:50"}, "result": "refused"}
  - {"conjunct": 1, "class": "gate", "cmd": "list-normalize", "expected": 1, "observed": 1, "result": "refused"}
  - {"conjunct": 1, "class": "gate", "cmd": "list-apply-gate", "expected": {"demoted": false, "verdict": "proved"}, "observed": {"demoted": false, "verdict": "proved"}, "result": "refused"}
  - {"conjunct": 1, "class": "gate", "cmd": "dangling-list-normalize", "expected": 0, "observed": 0, "result": "refused"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 5f5d5870f4d9138d
season: 2
testable_claim: "On the LIVE corpus, the evidence_runs YAML shape alone decides a decisive verdict: a scalar string naming an EXISTING run normalizes to 0 and is demoted to inconclusive_lean_proved:50, the same id in list form normalizes to 1 and stays proved, and an id-shaped-but-dangling list entry normalizes to 0. Proved if all five probes match."
title: "DH.34 evidence_runs shape probe: scalar->0/demoted, list->1/proved, dangling->0"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3634b942-evidence-runs-normalize

## Experiment

DH.34 Defect 2: `hypothesis:a00-5dafdc0d-a7e591` claims the
`evidence_runs` **scalar string -> list** shape is what blocked the gate, but
it cited `experiment:a00-7a045cbe-gate-rerun`, which measures the rotate AST
gate, not `normalize_evidence_runs`. This run measures the shape claim itself,
on the live corpus, with a cited id that EXISTS so the YAML shape is the only
variable.

Probe driver:
`.agi/sessions/iter-DH.34/a00-3634b942/probe_evidence_normalize.py`. It
imports `build_corpus`, `normalize_evidence_runs` and `apply_gate` from
`extensions/agi/bin/evidence_gate.py` and drives them on the live
`.agi/nodes` corpus (3,924 ids) with `RUN = experiment:a00-7a045cbe-gate-rerun`
(a resolvable id) in three shapes.

```
$ python3 .agi/sessions/iter-DH.34/a00-3634b942/probe_evidence_normalize.py
{"corpus_size": 3924, "cited_run_in_corpus": true, "probes": [...], "all_refused": true}
```

## Results

| # | class | probe | expected | observed | result |
|---|---|---|---|---|---|
| 1 | gate | scalar string -> `normalize_evidence_runs` | `0` | `0` | refused |
| 2 | gate | scalar string -> `apply_gate` | demoted, `inconclusive_lean_proved:50` | demoted, `inconclusive_lean_proved:50` | refused |
| 3 | gate | list form -> `normalize_evidence_runs` | `1` | `1` | refused |
| 4 | gate | list form -> `apply_gate` | not demoted, `proved` | not demoted, `proved` | refused |
| 5 | gate | dangling id-shaped list entry -> `normalize_evidence_runs` | `0` | `0` | refused |

The cited id resolves (`cited_run_in_corpus: true`), so probes 1-2 isolate the
scalar shape: a string is not a list, `normalize_evidence_runs` returns 0 for
every string, and a decisive verdict with 0 resolvable runs is demoted. Probes
3-4 show the identical id in list form resolving to 1 and surviving as
`proved`. Probe 5 separates shape from resolution: a list whose entry is not in
the corpus also counts 0, so the list form is necessary but not sufficient.

```
$ git diff --numstat -- extensions/agi/bin extensions/agi/templates
(empty)
```

0 production lines: measurement only, no engine file touched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.34 corrective. The hypothesis's old citation was a real run but a category
error: `experiment:a00-7a045cbe-gate-rerun` measures the rotate AST gate, not
the `evidence_runs` scalar-vs-list path, so the citation did not measure the
claim. This node drives the actual functions (`normalize_evidence_runs`,
`apply_gate`) on the live corpus with the shape as the single variable and the
cited run held constant, and adds the dangling-entry control so the result is
attributable to shape rather than to any list at all.
<!-- THOUGHT:END -->
