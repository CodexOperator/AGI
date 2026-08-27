---
name: verdict
derived_from: corpus-survey-2026-08-25 (n=83)
fields:
  title: {type: str}
  parents: {type: list}          # experiment | verdict | hypothesis ids
  next_edges: {type: list}
  verdict: {type: str}           # the taxonomy, below
  confidence: {type: float}
  evidence_runs: {type: list}    # node ids that resolve; see evidence_gate.py
  supports: {type: list}
  contradicts: {type: list}
  tags: {type: list}
  demoted_from: {type: str}      # written by evidence_gate.stamp
  demote_reason: {type: str}     # written by evidence_gate.stamp
  evidence_gate: {type: str}     # 'bypassed' only
  status: {type: str}            # LEGACY SHADOW of verdict: -- see below
validation:
  required: [id, type, mint_id, title, verdict, confidence]
  types:
    confidence: float
    parents: list
  regex:
    verdict: '^(proved|disproved|inconclusive_lean_proved:\d{1,3}|inconclusive_lean_disproved:\d{1,3}|pending)$'
spawn:
  allowed_parents: [experiment, verdict, hypothesis]
  min_parents: 1
  max_parents: 2
---

# verdict

The judgement on a chain's core claim. **The type the evidence gate exists to
police, and until 2026-08-25 the only heavily-used type with no schema at
all.**

ID prefix: `verdict:<short-slug>`.

## Taxonomy

```
proved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N | pending
```

`proved`/`disproved` additionally require `evidence_runs >= 1` resolving to
real node ids. That rule is **not** in the `validation:` block above, because
it is not a per-field check — it is enforced in code by
`bin/evidence_gate.py` on both writer paths, and duplicating it as a regex
here would create a second definition that could drift.

## Spawn rule

`allowed_parents: [experiment, verdict, hypothesis]`, `max_parents: 2`.
Observed across 83 nodes: `experiment` 57, `verdict` 30, `hypothesis` 12.
A verdict on a verdict is a real and common shape (a re-judgement), which is
why `verdict` is in its own allowed list.

`min_parents: 1` — **a verdict may never be parentless.** A judgement with
nothing above it judges nothing. 21 of the 83 verdicts in the corpus are
parentless today; they are a **report, not a purge** (G7: node count never
drops; G7.1: a missing parent is never inferred). The gate runs on the writer
path only, so nothing historical is touched.

## `status:` is a legacy shadow, not a field

61 of 83 verdicts carry a `status:` that repeats `verdict:`. No engine writer
produces it, no engine reader interprets it; kids hand-wrote it. It is
declared in `fields:` so the shape is documented, is **not** in `required:`,
and `evidence_gate.SHADOW_VERDICT_FIELDS` rewrites it in lockstep on a
demotion. Do not write it in a new node.

## Repairs applied to the corpus-observed shape

- `title` is required here but present on only 64/83 — every one of the 19
  without it predates this schema. Required means *for a new node*.
- `synthetic:` appears on 30/83 and is **not** declared: it is a sentinel from
  the pre-H4c era that the evidence gate now rejects outright. Undeclared on
  purpose, so re-introducing it is visibly off-schema.

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
