---
name: experiment
derived_from: corpus-survey-2026-08-25 (n=75)
fields:
  title: {type: str}
  parents: {type: list}        # hypothesis | verdict | goal | task | idea | experiment | level3
  next_edges: {type: list}
  verdict: {type: str}         # optional pre-judgement; the real one is a verdict node
  confidence: {type: float}
  evidence_runs: {type: list}
  contradicts: {type: list}
  supports: {type: list}
  subgraph: {type: bool}
  testable_claim: {type: str}
  tags: {type: list}
validation:
  required: [id, type, mint_id, title]
  types:
    confidence: float
    parents: list
  regex:
    verdict: '^(proved|disproved|inconclusive_lean_proved:\d{1,3}|inconclusive_lean_disproved:\d{1,3}|pending)$'
spawn:
  allowed_parents: [hypothesis, verdict, goal, task, idea, experiment, level3]
  min_parents: 1
  max_parents: 2
---

# experiment

A run executing a hypothesis. **The node that carries actual output** — a
command, its inputs, and what it really printed. Verdict taxonomy is
finite-state; the decisive judgement belongs in a child `verdict` node.

ID prefix: `exp:<short-slug>`.

## Spawn rule

`max_parents: 2`, and this is the widest `allowed_parents` list in the graph —
7 observed parent types over 75 nodes: `hypothesis` 40, `verdict` 31, `goal`
7, `task` 1, `level3` 1, `idea` 1, `experiment` 1. The list is transcribed
from the corpus, not designed; nothing was added "just in case".

`min_parents: 1`. 4 of 75 are parentless today — a report, not a purge.

## Repair: this schema previously required fields no node has ever carried

The pre-2026-08-25 version declared `required: [title, run_id, verdict]`.
Measured against the corpus:

| field | present | share |
|---|---|---|
| `title` | 67/75 | 89% |
| `run_id` | **0/75** | 0% |
| `verdict` | 5/75 | 7% |

`run_id` was never written by anything, and `verdict` on an experiment is the
exception rather than the rule. A `required:` list that 100% of the corpus
fails is not a control — nothing ran it, so nothing objected. **Repair rule
applied to every schema in this directory: a field may only be `required:` if
the corpus demonstrably uses it (majority present).** `run_id` is dropped
entirely — declaring a field nothing writes invites someone to write a
placeholder into it. `verdict` stays declared and optional, with its regex
kept so the taxonomy is still enforced when present.
