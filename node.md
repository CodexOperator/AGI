---
id: hyp:level3-node-anatomy
mint_id: f4733a9e9c1f4bf5a779fbda714cfef7
type: hypothesis
parents:
  - goal:g2.1
confidence: 0.5
edited_by: season.py
season: 1
subgraph: false
tags:
  - zoom
  - level3
  - g2.1
testable_claim: A level-3 node's harness-attached slots (payload_ref, origin, contract block) reach 1.000 recall by construction while its model-authored prose stays >=0.792 (the measured DESC-prose baseline) across >=3 trials on >=2 real files, one of which is under bin/.
thought_session: season
title: "Level-3 node anatomy: harness-attached structure, model-authored prose"
---
**Field set — deliberately zero growth.** `Node` has exactly 7 fields
(`id, type, payload_ref, parents, children, tags, origin`); I verified this
against `node.py` and `loader.py`'s `_node_from_frontmatter`, which builds the
in-memory `Node` from only those keys — any other top-level YAML key
(`status`, or a hypothetical `io_map`) is silently dropped, not just at load
but at every downstream consumer that only sees the `Node`/`LoadedNode`
object, not the raw file dict. Cost check: `tests/graph_core/test_node.py::
test_field_set_is_exactly_six` currently **fails on master** (asserts 6
fields, `origin` was added without updating it) — proof this invariant
already drifted once, unenforced. Given that, I add **zero new frontmatter
keys**. Level-3 nodes carry the same 8 keys every node already carries
(`confidence, id, parents, subgraph, tags, testable_claim, title, type`) plus
the two `Node` fields most nodes leave empty, now given concrete meaning:
`payload_ref` = repo-relative path to the code surface (precedent:
`schema_registry/meta_nodes.py` already uses it this way for schema files),
and `origin` = a new convention value, `index-scan`, marking harness
provenance (no loader change needed — `origin` is unvalidated `Optional[str]`).
Harness-attached: `id` (minted), `payload_ref`, `origin`, `parents` (from the
decomposition census), path-derived `tags`. Model-authored: `title`,
`testable_claim`, `confidence`, prose only.

**IO map, as data.** Not frontmatter — frontmatter is exactly the surface
that scored 0.000. It lives as a fenced YAML block at the top of the body,
between harness-owned markers, one entry per input/output:
`{name, how, why, perf, security}`. `how` is mechanical — GitNexus
`context`/`impact` output for the symbol (callers, callees, types) when the
path is covered; honestly `uncovered` when it isn't, e.g. anything under
`bin/*.py`, since GitNexus indexes zero symbols there (verified post-reindex).
`why`, `perf`, `security` are not mechanically derivable — GitNexus can't
judge intent or risk — so they're model-authored *into fixed slots the
harness owns the shape of*: the model fills free text, never the field names
or ordering, so a summarizing pass can't silently drop a slot the way it
dropped invariant citations (0.267 recall) in the measured baseline.

**Stitching — the load-bearing question.** No stitcher exists in the engine
today (checked: no `git-tree-renderer`, no directory-materializer); this is
greenfield design, not a description of running code. Source text lives on
disk exactly once, referenced by `payload_ref` — never inlined into the node
body. Graph→directory is then near-identity for an existing repo: resolve
every canonical node's `payload_ref`, copy that path into the target tree;
non-canonical (sub-file) nodes are skipped for materialization, read-only for
context. Directory→graph is what GitNexus's indexer already does for the
covered half. The round-trip guarantee is narrow and must stay narrow:
**identity of pointer + freshness of contract**, not byte-duplication. What
breaks it, concretely: (1) a file moves and nothing updates `payload_ref` —
no validator currently checks this, so it fails silently; (2) two canonical
nodes claim the same file — ambiguous materialization, must be rejected at
mint time; (3) the contract block has no freshness marker tied to the code
(e.g. a content hash), so it drifts the same way GitNexus's own index goes
stale, invisibly. I did not solve (1)–(3) here, only named them — that's the
open edge of this hypothesis.

**Granularity.** One canonical node per *file*, because the file is the atom
a directory layout actually stitches on — not per class, not per public
surface. Files with several distinct public surfaces may get extra
non-canonical level-3 nodes (payload_ref same file, scoped by a symbol tag)
for narrative purposes only; they own no materialization. Level 4 (functions)
sits below as children of the file-node, preserving G2's `N ⇔ collection at
N+1` invariant. The line/threshold for "several distinct surfaces" is an
unmeasured judgment call, flagged as a deviation.

**Falsifier.** Harness-attached fields (`payload_ref`, `origin`, contract
slot *shape*) must hit 1.000 recall by construction — anything less is a
harness bug, not a model failure, and should be reported separately. The
real test is prose: does it hold >=0.792 (DESC-prose baseline) once a
sizeable mechanical block sits above it in the same file? A drop below that
bar, with mechanical recall still at 1.000, is exactly the pre-registered
"structure survives, prose crowds out" failure mode — distinct from G2's
0.000/0.792 split and the thing this design could still fail on even if the
frontmatter half works perfectly.