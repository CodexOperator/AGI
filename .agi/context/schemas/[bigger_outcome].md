---
name: bigger_outcome
derived_from: corpus-survey-2026-08-25 (n=17 as bigger_outcome, +2 as bigger-outcome; both renamed 2026-08-26, n=19)
fields:
  title: {type: str}
  parents: {type: list}      # outcome | mvp ids
  next_edges: {type: list}
  tags: {type: list}
  status: {type: str}        # open | closed
  confidence: {type: float}
  subgraph: {type: bool}
  judged_against: {type: str}  # the long-term goal this report is judged against
  lens: {type: str}            # the vision above, stamped for readers
  alignment: {type: str}       # aligned | adjust | unknown
  adjust: {type: str}          # one line: what shifts in the LT goal
  season: {type: int}          # which season this bigger_outcome belongs to
  season_parents: {type: list} # season edge, not lineage
  tokens_in: {type: int}       # telemetry roll-up: tokens consumed
  tokens_out: {type: int}      # telemetry roll-up: tokens produced
  cost_usd: {type: float}      # telemetry roll-up: cost in USD
  accepted_bytes: {type: int}  # telemetry roll-up: accepted diff bytes
validation:
  required: [id, type, mint_id, title, parents, next_edges]
  types:
    parents: list
    next_edges: list
spawn:
  allowed_parents: [outcome, verdict]
  min_parents: 1
  max_parents: 4
---

# bigger_outcome

**Report node for tier 1.** A mid-season report judged against its long-term
goal through the lens of the vision above. Composed from several `outcome`
nodes. Aggregates upward into `vision`, via `overview`.

ID prefix: `bigger_outcome:<short-slug>`.

## Ladder rationale (season-ladder-and-morals-brief §1)

A bigger_outcome is judged against its long-term goal through the lens of the
vision above. The judgment record (`judged_against`, `lens`, `alignment`,
`adjust`) is stamped on the report node. Counts are measured at season close,
never enforced as floors.

`min_parents: 1` replaced the previous `min_parents: 4` with
`min_parents_by_type: {verdict: 2, outcome: 2}` per the season-ladder design
brief. The old floor was the wrong model — it expressed a design intent no
node met and no gate could enforce on existing nodes. The new floor ensures
DAG consistency: a report with no plan is an orphan.

Collapse ratios are data, not rules: bigger_outcome→overview ratio is LT goals
per vision. `max_parents: 4` leaves room above the floor for legitimate
density.

## One spelling, as of 2026-08-26

`bigger_outcome` (19 nodes) is the only spelling in the corpus. The two
`bigger-outcome` nodes were renamed on 2026-08-26 — file, `id:` and `type:` —
and the five ids that referenced them were rewritten in the same pass.

`spawn_gate.canonical_type` still folds `-` → `_` before matching, and stays.

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
