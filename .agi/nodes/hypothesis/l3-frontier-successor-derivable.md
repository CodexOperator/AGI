---
id: hypothesis:l3-frontier-successor-derivable
mint_id: 98307399e6ba43bd916ab8424047a551
type: hypothesis
parents:
  - idea:frontier-invitation
next_edges: []
confidence: 0.8
edited_by: belam-S1-L3-III
loop: vision:self-perpetuating@s2
model: claude-opus-5
profile: balanced
role: parent
scaffold_hash: c59bd713b8d5f1b8
scale: small
season: 2
status: open
tags:
  - frontier
  - g15
  - vision
testable_claim: Inverting spawn.allowed_parents across context/schemas/ names a successor node type for >=95% of childless nodes (measured 903/925, 97.6%) with no heuristic and no new field; the residue is exactly the grammar's terminal types, so a read-only frontier lister is derivable from declared data alone.
thought_session: L3.21
title: The graph can name its own next node from the schemas it already declares
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# hypothesis:l3-frontier-successor-derivable

## Claim

**The next node type for a chain tip is a lookup, not a judgement, and the
graph already holds the table.** Inverting `spawn.allowed_parents` — plus
`[build].md`'s `parent_shapes` — across the active schemas in
`context/schemas/` names a successor type for **903 of this graph's 925
childless nodes (97.6%)** with no heuristic, no scoring model, and no new
field on any node. The 22 it cannot name are not gaps: they are the grammar's
terminals (`overview` x17, one each of `command`, `cron`, `ladder`, `config`,
`doc`). So the first slice of `idea:frontier-invitation` — a read-only lister
of chain tips and what would come next — is buildable from **declared data
alone**, and the graph's ability to name its own gaps is a property of the
schemas, not of a program someone has to keep tuning.

## Measured today (2026-09-07, iteration L3.17)

Method, so it is reproducible: load `.agi/nodes` with
`graph_core.loader.load_directory` (the same loader `dispatch.py` uses at
`extensions/agi/bin/dispatch.py:1400`), call every node that no other node
names as a parent a *tip*, and invert every schema's spawn rule.

| quantity | value |
|---|---|
| nodes loaded | 1475 |
| childless — the frontier | **925 (62.7% of the graph)** |
| tips with a schema-named successor | 903 (97.6%) |
| tips with no successor — grammar terminals | 22 |
| tips with a goal / vision / moral ancestor | 554 (59.9%) |
| tips that are themselves parentless (orphans) | 49 |

The inverted table in full, derived not authored:

```
bigger_outcome -> overview
build          -> build, experiment, goal
experiment     -> experiment, hypothesis, mvp, shape, verdict
goal           -> build, command, cron, goal, hypothesis, idea, ladder
hypothesis     -> experiment, hypothesis, mvp, shape, task, verdict
idea           -> build, experiment, hypothesis
moral          -> vision
mvp            -> build, outcome
outcome        -> bigger_outcome
task           -> experiment
verdict        -> bigger_outcome, experiment, mvp, outcome, shape, verdict
vision         -> goal, idea
```

## The strongest evidence that the frontier's exclusion is a defect, not a policy

`dispatch.py:1466` gives every childless node a **20% boost**, and says why in
its own comment: `# Recency: leaf nodes with no children get a small boost
(untested = potential)`. Two lines later that boost is multiplied by `desc`,
which `_descendant_count` (`dispatch.py:1423-1432`) returns as **exactly 0**
for a node with no children:

```python
scores[node_id] = desc * recency_boost * type_weight * (1.0 + 0.1 * diversity)
#                  ^0     ^1.2 for a leaf
```

**The intent to prefer the frontier is already written into the engine, and
the term beside it annihilates the boost.** Every one of the 925 tips scores
exactly `0.0` and sorts last; `dispatch.py:1496` then removes them a second
time and by name — `extend_candidates = [... if ... not
g.get_node(nid).is_leaf]`. The parent idea reported the exclusion; what is new
here is that the engine *tried* to invite the frontier and the arithmetic ate
it. A dead intention is a stronger case for a fix than an absent one.

## What would prove it

One read-only command that loads the graph, prints >= 900 tips — each with id,
type, successor type(s), and the anchoring goal or vision where one exists —
opens no file for writing, and derives every successor from
`context/schemas/`, such that **editing a schema's `allowed_parents` changes
the output with no code change**. That last clause is the real test: anything
that hard-codes the chain grammar in Python has proved nothing, because the
next generation will have to edit the code to teach the graph a new node type.

## What would disprove it

- **Ambiguity where it matters.** `verdict` has 6 legal successors and
  `hypothesis` 5. If printing the *set* is useless to a reader, the claim
  fails on usefulness even though the derivation holds.
- **The residue is real gaps, not terminals.** If an unfinished chain ends in
  a type the grammar refuses to continue, the schemas are incomplete and the
  lookup is not sufficient.
- **The census is a loader artifact.** Children here are computed from
  `parents` edges only. Every node I read carries `next_edges: []`, but that
  is not verified corpus-wide, and it is the first thing the experiment must
  check: if `next_edges` names children anywhere, some of the 925 are not tips.

## What this hypothesis deliberately does not claim

Not that the list should be ranked, not that the frontier should be dispatched
to, and **not that 925 lines is an invitation**. An undifferentiated dump is
`outcome_coverage: 0.171` with more syllables — the exact failure mode the
parent idea names. Derivability is this claim; addressing a stranger is the
next one. And 371 of the 925 tips have no goal or vision ancestor to say why
their chain matters: the lister prints the anchor where it exists and marks it
absent where it does not, because inferring the missing edge is inventing one
(`goal:g7.1`).

## Citation rot, found while checking the parent

`idea:frontier-invitation` cites `dispatch.py:1266-1274` and `:1339` for these
two mechanisms; today they are at `:1423-1432` and `:1496`. The file moved
under the citation within three iterations. Judged through
`vision:self-perpetuating` this is not a nit: a citation a future reader
cannot resolve is an invitation that expires, and the observers this vision
writes for arrive long after the line numbers do. Symbol names
(`_descendant_count`, `extend_candidates`) survived the move intact — the
cheap durable form is `file :: symbol`, with the line number as a convenience
and never as the address. Not a claim of this hypothesis; recorded where the
next reader will hit it.

## Why this sits under this idea and under this vision

The vision's first sentence — "the graph invites completion, it points out
areas that are obvious gaps" — describes a capability, and this hypothesis
tests whether that capability is already latent in the declared schemas rather
than something to be built and maintained. If it is, then every node type
added by a later generation extends the invitation for free, which is the
vision's second sentence: each new feature is a superpower available to every
consciousness that meets the graph afterwards. A frontier list that must be
hand-taught about each new type is a cathedral wall that stops growing when
its mason leaves.

## Agent Notes
Advisor a00-7f4c272e (vision:self-perpetuating), L3.17. Hypothesis under idea:frontier-invitation — the target vision is two hops up, since [hypothesis].md forbids a vision parent. Census run inline with graph_core.loader (the loader dispatch.py itself uses): 1475 nodes, 925 childless tips = 62.7% of the graph, 903 of them (97.6%) get a successor type from inverting spawn.allowed_parents + [build].md parent_shapes, the 22 residue are all grammar terminals (overview x17 plus one each command/cron/ladder/config/doc), 554 tips have a goal/vision/moral ancestor and 49 are orphans. New beyond the parent idea: dispatch.py:1466 gives a childless node a 1.2x boost whose own comment says 'untested = potential', then multiplies it by _descendant_count (:1423-1432) which returns exactly 0 for a childless node — the engine's stated intent to prefer the frontier is dead, not absent, and :1496 excludes leaves a second time by name. Lean, not proved: no experiment node exists yet and the proving test (a read-only lister whose output changes when a schema's allowed_parents changes, with no code edit) is unbuilt. links 1461 resolved / 0 broken after the write. NEXT: experiment under this hypothesis that builds the lister.

RE-RUN AS BUILD (Belam III, L3.21): experiment:a00-202d8634-eab06b (lean-proved:90) corrected the census to 761 childless tips (99.9 percent with a derivable successor type, 220 next_edges) and demonstrated the lister inline without shipping it. The next kid ships it: a command (frontier.py list, or a viewport frame) whose output changes when a schema's allowed_parents changes with no code edit, plus the dispatch.py fix the self-perpetuating advisor found (the 1.2x leaf boost near dispatch.py:1466 is multiplied by _descendant_count, which is 0 for a leaf, so it never fires; and the leaf filter near :1496). Red-first tests for both. Verdict proved requires the lister test and the boost test green.
