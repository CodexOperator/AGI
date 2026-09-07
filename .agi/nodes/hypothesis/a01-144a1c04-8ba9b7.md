---
id: hypothesis:a01-144a1c04-8ba9b7
mint_id: 069862672b874e4a8c14d19558c0cecd
type: hypothesis
parents:
  - idea:domain-graph-core
confidence: 0.5
edited_by: season.py
evidence_runs: 0
season: 1
thought_session: season
title: A01 144a1c04 8ba9b7
verdict: pending
wired_at: 1788197188
wired_from: a01-144a1c04
---

# hypothesis:a01-144a1c04-8ba9b7

## Hypothesis

**Claim:** graph-core's node model can support **recursive bodies** (a node body that embeds or references other nodes, to arbitrary depth) purely as a *read-time* resolution layer over the existing flat `parents:`/`next_edges:` frontmatter — with no schema change, no second persistence format, and no write-time expansion.

**Rationale:** existing primitives already give identity (`mint_id` vs derived address), flat edge lists, and directory-walking auto-discovery (zoom.py already walks 2 hops). Nothing in the format forbids an edge pointing back at an ancestor; recursion is only a risk if resolution happens at write time (cycles → infinite expansion). Deferring expansion to read time with a visited-set sidesteps cycles by construction.

**Testable consequences / proof:**
1. A read-time resolver can inline nested node bodies over the live graph (including `deprecated/` siblings, live-first) and terminate on every cycle-containing subgraph — property test with deliberately cyclic edges.
2. Node count and `mint_id` invariants hold unchanged after round-trip: `active_node_count + deprecated_node_count` never moves, addresses recompute identically.
3. Renderers that strip authored regions (THOUGHT blocks) can strip inlined regions too, so GOALS.md-style derived output stays flat.

**Disproven if:** resolution needs write-time materialization to stay correct (e.g., provenance or grid versioning of an inlined body can't be keyed on the parent's version alone), or termination requires constraints the flat edge format can't express.

## Test Plan

Spawn one experiment: implement a `resolve_body(node, graph, depth, visited)` prototype in `src/` against the existing primitives, property-test it on cyclic and self-referential fixtures, verify the three consequences above.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. -->
Prior graph-core hypotheses (r1 generic primitives, r10 bootstrap, r11 traversal) stop at flat edges and walking. Recursive bodies are named in the domain seed but no hypothesis tests whether they cost a format change or are free at read time. This one claims free — smallest-possible version of the feature, falsifiable by one prototype + property test.
<!-- THOUGHT:END -->