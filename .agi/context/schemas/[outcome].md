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
