---
name: overview
derived_from: not-derived -- new type, 2026-08-27; zero overview nodes exist yet
fields:
  title: {type: str}
  parents: {type: list}      # bigger_outcome ids
  next_edges: {type: list}
  season: {type: int}        # which season's overviews this belongs to
  tags: {type: list}
  status: {type: str}        # open | closed
  confidence: {type: float}
  evidence_fraction: {type: float}   # inherited score of what it aggregates
  judged_against: {type: str}  # the vision this report is judged against
  lens: {type: str}            # the morals above, stamped for readers
  alignment: {type: str}       # aligned | adjust | unknown
  adjust: {type: str}          # one line: what shifts in the vision
  season_parents: {type: list} # season edge, not lineage
  tokens_in: {type: int}       # telemetry roll-up: tokens consumed
  tokens_out: {type: int}      # telemetry roll-up: tokens produced
  cost_usd: {type: float}      # telemetry roll-up: cost in USD
  accepted_bytes: {type: int}  # telemetry roll-up: accepted diff bytes
  moral_audit: {type: dict}    # five-key dict: faith, love, empathy, antifragility, beauty; each has value (aligned|violated|unknown) and evidence pointer
validation:
  required: [id, type, mint_id, title, parents]
  types:
    parents: list
spawn:
  allowed_parents: [bigger_outcome]
  min_parents: 1
  max_parents: 4
---

# overview

**Report node for tier 2.** A season rollover report judged against its vision
through the lens of the morals above. Composed from several `bigger_outcome`
nodes, read together, and what they say about whether the season's goals were
met.

ID prefix: `overview:<short-slug>`.

## Ladder rationale (season-ladder-and-morals-brief §1)

An overview is judged against its vision through the lens of the morals above.
The judgment record (`judged_against`, `lens`, `alignment`, `adjust`) is
stamped on the report node. An overview additionally carries `moral_audit:` —
five answers to the five moral questions (§3 of the design brief), each
`aligned | violated | unknown` with an evidence pointer. Counts are measured
at season close, never enforced as floors.

`min_parents: 1` replaced the previous `min_parents: 3` with
`min_parents_by_type: {bigger_outcome: 3}` per the season-ladder design brief.
The old floor was the highest in the graph but existed only as design intent:
zero overview nodes had ever been minted, so it expressed a wish rather than a
measured property. The new floor ensures DAG consistency.

Collapse ratios are data, not rules: overview→vision ratio is LT goals per
vision. `max_parents: 4` leaves room above the floor for legitimate density.

## Not built

`evidence_fraction` is declared so an overview can carry the inherited score
of what it aggregates, and **nothing computes it yet**. The scoring loop it
belongs to — score the overviews, unlock the next season's vision when they
clear a bar — is designed and unbuilt. Declared here rather than omitted so
the field name is fixed before anything writes it; recorded as a residual
rather than claimed.

## moral_audit shape

A dict with exactly five keys. Each key maps to an object with:
- `value`: one of `aligned`, `violated`, `unknown`
- `evidence`: pointer to the node(s) supporting the claim (str or list)

Keys: `faith`, `love`, `empathy`, `antifragility`, `beauty`.

Example:
```yaml
moral_audit:
  faith: {value: aligned, evidence: "experiment:a00-1234-abcd"}
  love: {value: unknown, evidence: []}
  empathy: {value: aligned, evidence: "experiment:a00-5678-efgh"}
  antifragility: {value: aligned, evidence: ["experiment:a00-9012-ijkl", "experiment:a00-3456-mnop"]}
  beauty: {value: violated, evidence: "overview:cluttered-format"}
```

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
