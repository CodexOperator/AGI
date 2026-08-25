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
