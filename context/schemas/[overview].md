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
validation:
  required: [id, type, mint_id, title, parents]
  types:
    parents: list
spawn:
  allowed_parents: [bigger_outcome]
  min_parents: 3
  max_parents: 4
  min_parents_by_type: {bigger_outcome: 3}
---

# overview

**The reporting tier between aggregated outcomes and the vision.** Several
`bigger_outcome` nodes, read together, and what they say about whether the
season's goals were met.

ID prefix: `overview:<short-slug>`.

## This schema is PRESCRIPTIVE and describes zero nodes

Every other schema here except `[bigger_outcome].md` and `[vision].md` is
derived from the corpus. **This type has no corpus at all** — it was created
on 2026-08-27 and nothing has been written to it yet. So there are no
observed counts below, and the numbers are chosen rather than measured. A
reader who assumes "derived" will misread it.

Stating that plainly matters more here than elsewhere: the other schemas earn
their rules from 780 nodes of evidence, and this one earns its rules from an
argument. If the argument is wrong the rule should change, and changing it
costs nothing today precisely because no node depends on it.

## Spawn rule

`allowed_parents: [bigger_outcome]`, `min_parents: 3`, `max_parents: 4`,
`min_parents_by_type: {bigger_outcome: 3}`.

**Three, deliberately, and it is the highest floor in the graph.** The
convergence end is supposed to be harder to reach than the middle: an
`overview` resting on one or two aggregates is a restatement, not a reading.
Three is the smallest number at which "what do these say *together*" is a
different question from "what does this say".

`max_parents: 4` leaves exactly one slot above the floor, so a fourth
aggregate can be admitted without the type becoming a bucket. Both sit under
`[shape].md`'s ceiling of 4, which was raised from 2 on the same day and for
the same reason.

## Where it sits

    outcome -> bigger_outcome -> overview -> vision

`bigger_outcome` requires 2 verdicts and 2 outcomes; `overview` requires 3
bigger_outcomes; `vision` requires 2 overviews. The floors compound on
purpose — a vision that satisfies its own rule rests, transitively, on at
least 6 aggregates, 12 verdicts and 12 outcomes. **That is the "harder to
earn" property expressed as arithmetic rather than as intent**, which is the
difference between a design and a wish.

## Not built

`evidence_fraction` is declared so an overview can carry the inherited score
of what it aggregates, and **nothing computes it yet**. The scoring loop it
belongs to — score the overviews, unlock the next season's vision when they
clear a bar — is designed and unbuilt. Declared here rather than omitted so
the field name is fixed before anything writes it; recorded as a residual
rather than claimed.
