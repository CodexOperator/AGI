---
name: outcome
derived_from: corpus-survey-2026-08-25 (n=19)
fields:
  title: {type: str}
  parents: {type: list}        # mvp | verdict ids
  next_edges: {type: list}
  input_shape: {type: str}     # what goes in    -- optional, see below
  output_shape: {type: str}    # what comes out  -- optional, see below
  behavior: {type: str}        # one-line summary -- optional, see below
  edge_cases: {type: list}
  source_files: {type: list}
  status: {type: str}          # open | closed
  confidence: {type: float}
  subgraph: {type: bool}
  tags: {type: list}
validation:
  required: [id, type, mint_id, title, parents, next_edges]
  types:
    parents: list
    next_edges: list
spawn:
  allowed_parents: [mvp, verdict]
  min_parents: 1
  max_parents: 2
---

# outcome

Fusion of in-code documentation + README. Records what an MVP does in
input → output terms. Aggregates upward into `bigger_outcome` and eventually
`vision`.

ID prefix: `outcome:<short-slug>`.

**This is the type `outcome_coverage` — the project's primary metric — is
computed from.** Which is why its schema being fiction mattered more than the
node count suggests.

## Spawn rule

`allowed_parents: [mvp, verdict]`, `max_parents: 2`. Observed over 19 nodes:
`mvp` 19, `verdict` 2. **Zero parentless.**

## Repair: three of the four required fields were carried by no node

Pre-2026-08-25 `required: [title, input_shape, output_shape, behavior]`.
Measured: `title` 19/19, `input_shape` **0/19**, `output_shape` **0/19**,
`behavior` **0/19**. The i/o contract that defines what an outcome node *is*
was declared required and then written by nothing, for all 19 nodes, with no
error ever raised — because no code path ran this schema against a node.

All three are kept declared and moved to optional, on the same reasoning as
`[mvp].md`'s `source_files`: they describe the type's actual job, and the gap
is a finding to report rather than a fact to legislate away. `required:` now
lists only what 19/19 carry.
