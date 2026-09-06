---
name: experiment
derived_from: corpus-survey-2026-08-25 (n=75)
fields:
  title: {type: str}
  parents: {type: list}        # hypothesis | verdict | task | idea | experiment | build
  next_edges: {type: list}
  verdict: {type: str}         # optional pre-judgement; the real one is a verdict node
  confidence: {type: float}
  evidence_runs: {type: list}
  contradicts: {type: list}
  supports: {type: list}
  subgraph: {type: bool}
  testable_claim: {type: str}
  tags: {type: list}
  payload_ref: {type: str}    # path of the file this experiment IS, relative to `location`
  location: {type: str}       # NAME of the base it resolves against; default source_root
validation:
  required: [id, type, mint_id, title]
  types:
    confidence: float
    parents: list
  regex:
    verdict: '^(proved|disproved|inconclusive_lean_proved:\d{1,3}|inconclusive_lean_disproved:\d{1,3}|pending)$'
spawn:
  allowed_parents: [hypothesis, verdict, task, idea, experiment, build]
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
6 declared, 7 observed parent types over 75 nodes: `hypothesis` 40, `verdict`
31, `goal` 7, `task` 1, `build` 1 (recorded as `level3` before the 2026-08-27
rename), `idea` 1, `experiment` 1. The list was transcribed
from the corpus, not designed; nothing was added "just in case". `goal` was
removed from `allowed_parents` on 2026-09-01 under `goal:s22` — an experiment
is a run executing a hypothesis, and a goal may not skip the hypothesis step.
Existing `goal -> experiment` edges (the 7 observed) stay resolvable as prior
art; the gate only stops new ones.

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

## The `THOUGHT` block (goal:g2.11)

A node body may carry one authored region, marked exactly like the harness
markers it sits beside:

```
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
why this version differs from the last one
<!-- THOUGHT:END -->
```

**`body` is state; `thought` is delta.** The body says what this node asserts
now. The thought says why *this version* differs from the previous one — it is
rewritten from scratch on each change, not accumulated.

- **Absent means empty.** No node is required to carry one, which is why
  introducing the block churned 0 of 786 existing nodes. Fill it when there is
  something to say; never fabricate one after the fact.
- **It survives regeneration.** Writers that rebuild a body (`level3.py`,
  `snapshot-build-site.py`, `decompose-engine.py`) carry this region across
  verbatim via `write_frontmatter(..., preserve_body=...)`. Before 2026-08-27
  they did not, and 8,034 authored contract fields were destroyed unread
  (goal:g2.10).
- **Versioning is free.** The grid snapshots `node.md` once per version, so
  each grid commit already carries the thought current at that version.
- **Not in frontmatter, deliberately.** `write_frontmatter` flattens newlines,
  so multi-line prose in a frontmatter field is silently destroyed. The short
  scalar `thought_session:` is reserved there for goal:g2.7 / goal:g10.1 to
  point at the chat that produced a version; it is not populated yet.
- **Readers strip it.** Thought is provenance to zoom into, not weight every
  reader carries forever. `snapshot-goals.py --render` strips it explicitly via
  `strip_thought()`; `render-context.py` and `zoom.py` never see it because
  they read frontmatter only (`load_node_file(..., body=False)`) and so carry
  no body text at all. The rule binds any future reader that *does* read
  bodies.
