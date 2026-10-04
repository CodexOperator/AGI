---
id: goal:s32
mint_id: d28e414ee2ae4b79a901e54e1ff10ebe
type: goal
parents:
  - goal:g6
next_edges: []
confidence: 1.0
edited_by: alive
goal_id: S32
goal_kind: short-term
heading_level: 2
origin: goals-doc
scaffold_hash: 905d31224cf0a239
season: 1
seeds: []
status: complete
tags:
  - goal
  - root
  - short-term
thought_session: g1-g7-rewrite-2026-09-19
title: "S32: Finish the embeddings pipeline the build-site started — cache, in-graph storage, and a scatter renderer"
---
**Minted 2026-09-03 in L1.09 from the cavekit build-site survey
(`goal:s18`, `.agi/sessions/L1.09-mining/report.md` §B) — the one new goal that survey found worth
minting.** Most of the embeddings domain the build-site specified is already
real code, and a goal that does not say so would get it re-implemented:

- `extensions/agi/src/embeddings/node2vec.py` — per-node Node2Vec,
  seed-deterministic (`hyp:embeddings-r1`, closed by citation)
- `extensions/agi/src/embeddings/projection.py` — the UMAP projection
  (`hyp:embeddings-r2`, proved)
- coordinate isomorphism with the renderers' shared representation
  (`hyp:embeddings-r3`, proved)
- `extensions/agi/src/embeddings/similarity.py` — top-k cosine similarity
  (`hyp:embeddings-r5`, closed by citation)

Three pieces the build-site scoped were never built, and nothing else in the
graph reaches for them:

1. **A cache.** Invalidation when the graph changes, portable across a copy of
   `.agi/`, with a force flag (was `hyp:embeddings-r4`). `graph_core/cache.py`
   already has the digest-and-invalidate pattern — reuse it; a second cache
   design is the one-fact-two-definitions shape `goal:s17` names.
2. **In-graph storage.** An optional toggle that writes a node's vector into
   the node rather than a sidecar, off by default, with the loader reading it
   back (was `hyp:embeddings-r7`).
3. **A scatter renderer.** The 2-D projection drawn through the same
   representation the ASCII and Mermaid renderers consume (was
   `hyp:embeddings-r6`). It was blocked on a renderer plugin contract
   (`hyp:renderers-r7`) that does not exist and is not coming — call it the
   way `zoom.py` calls the others, directly.

Spawn under `idea:engine-embeddings`, the live `origin: engine-decomp` anchor
for `extensions/agi/src/embeddings/`, not under the deprecated
`idea:domain-embeddings`.

Falsifier: a second embed run over an unchanged graph does no model work and
`--force` does; with the toggle on, a node's frontmatter carries its vector
and the loader reads it back; the scatter renderer is byte-identical across
two runs over the same graph and consumes the same representation `ascii.py`
does.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
COMPLETE, not retired (council, alive, 05:xZ 09-30; belam's rule: complete = achieved; never retired with a pending child) on the owner 05:0xZ 09-30 verbatim: "DG2 is talking about a running hypotheses under s31 when s31 is retired needs fixing in graph". Its achieved part: the scatter renderer landed (hypothesis:a00-c4b84f52-f58e90, DG2 closing verdict inconclusive_lean_proved:65 + evidence_runs); its open remainder (cache + in-graph vector storage; the embeddings-populated premise is false) is goal:g2.4.1, with 2 re-homed hypotheses (all-is-one 9a0651a7c, 234c4f73c).
<!-- THOUGHT:END -->
