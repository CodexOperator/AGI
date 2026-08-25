# agi — Artificial Graph Intelligence

A unified repository housing **graph algorithms** and the **research loop harness** that operates on them. The loop dogfoods by treating the agi codebase itself as graph nodes — researching, mapping, and incrementally evolving its own algorithms and harness.

This repo is the result of folding [`CodexOperator/autoresearch-tree`](https://github.com/CodexOperator/autoresearch-tree) (research loop harness — engine, bridge, skill) into the canonical AGI graph code at `~/.hermes/agi/`. Both git histories are preserved via subtree merge.

## What's inside

| Path | Purpose |
|------|---------|
| `extensions/agi/` | Research loop engine — driver, bin/ scripts (snapshot, render, dispatch, heal, zoom, cli), hooks, lib, src/, tests |
| `extensions/agi/src/graph_core/` | Graph framework — node, edge, types, persistence (filesystem + sqlite), loader, db_loader, cache |
| `extensions/agi/src/agi_algos/` | Graph algorithms — graph_builder, query_engine, benchmark, pi_tree_adapter, asciirender |
| `extensions/agi/src/renderers/` | Renderers — ascii (project graph), mermaid, git_diff, representation |
| `extensions/agi/src/embeddings/` | Embedding stack — node2vec, projection, similarity (gensim + UMAP) |
| `extensions/agi/src/schema_registry/` | Schema governance — fingerprint, active_set, cascade, validation, dsl, meta_nodes, loader |
| `extensions/agi-bridge/` | TypeScript pi extension — hooks `before_agent_start`, refreshes `INJECTION.md` per agent turn |
| `skills/agi/SKILL.md` | The Claude/agent skill that drives loop iterations |
| `TODO.md` | Persistent register of deferred work (DB-only state migration, ASCII renderer unification, metric overhaul, …) |
| `HANDOFF.md` | **Start here on a new machine.** Bootstrap from zero, current state, pending actions, known bugs. |

> ⚠️ **Before running the loop in any project, read `TODO.md` → H0.** A stale project-local `bin/snapshot-build-site.py` can silently delete that project's entire node corpus. `HANDOFF.md` §1 has the one-line check.

## The working rule

**Every change starts as a node in the graph and is built back into the engine.** The graph is the sequence of decisions; this repo is what falls out of it. A fix applied only as a file edit carries no reasoning, no parent, and nothing a later reader can argue with — so find the node first, write one if the reasoning is new, and let the code follow.

Two rules that make that workable, and both are easy to get wrong:

- **A version is a grid commit, not a second node file.** Update a node **in place**; the git grid records one version per change on `refs/grid/node/<mint-id>`. Never mint a `@v2` file or a `supersedes:` pair — that duplicates history the grid already has.
- **Two identifiers, two jobs.** A node's **mint id** is assigned once and never changes; it is what grid refs and provenance key on. Its **address** is derived and expected to change whenever the node is retagged or regrouped. Never key durable history on the address.

## Layout

The graph lives **outside** the engine, one level inside the project, with the engine clone underneath it — `<project>/<project>-tree/agi`:

```
fantasia/
  fantasia-tree/        the graph repo (GOALS.md, agi-tree.config.json, nodes/)
    agi/                gitignored clone of this repo
```

An engine checkout therefore never contains a graph, which is why this repo needs no tree-related gitignore. The one exception is this repo's own pair, where both hops are symlinks so `agi/agi-tree/agi` resolves back here — an engine edit made from inside the tree has to land in the real checkout, not a copy nobody ships.

## Companion repositories

- [`CodexOperator/agi-tree`](https://github.com/CodexOperator/agi-tree) — graph **data**: a live research project instance whose nodes correspond to actual files and functions in this repo.

## Pi extension auto-discovery

This repo declares pi extensions and skills in the top-level `package.json` (`pi.extensions: ["./extensions"]`, `pi.skills: ["./skills"]`). Pi auto-discovers `extensions/agi/` and `extensions/agi-bridge/` when run from any directory rooted under this repo.

## CLI

Both `agi` and `autoresearch-tree` resolve to the same `extensions/agi/driver.sh` during the transition. Both invocations are equivalent.

## History

This repo carries two preserved histories merged via `git subtree`:

1. **Origin: `~/.hermes/agi/`** — graph algorithm research (lru-cached graph builder, ASCII renderer, query engine, BFS reachability, schema parsing, hook/script/pipeline node ingestion).
2. **Origin: `CodexOperator/autoresearch-tree`** — research loop harness (engine, bridge ext, skill, embeddings, schema registry, sqlite migration scaffolding).

`git log` over this repo surfaces commits from both origins. The fold itself is captured in commits prefixed `fold:` for locatability.
