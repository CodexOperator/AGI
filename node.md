---
id: idea:engine-self-decomposition
mint_id: 404c121212fa40ed99e1dc5e4eefa3e6
type: idea
parents:
  - goal:g6
confidence: 1.0
edited_by: season.py
scale: big
season: 1
status: open
tags:
  - engine
  - seed
  - l19
thought_session: season
title: "Engine self-decomposition: a generated idea layer"
---
The idea layer should be a **census of the engine's changeable surfaces, regenerated
from the engine**. G6's invariant says generated, never hand-written; this node takes
the four positions that decision requires and pre-registers what would falsify it.

## 1. The unit: one node per changeable surface

The unit is a **top-level `src/` package** or an **executable entry point** — not a
file, not a symbol. Against the engine as it stands: 6 `src/` packages, 12
`bin/*.py`, `driver.sh`, `hooks/cc-session-start.sh`, `lib/find-root.sh`,
`scripts/migrate_to_sqlite.py`, `extensions/agi-bridge/index.ts` = **23 units**.
Five have an idea node today (`graph_core`, `renderers`, `chain_engine`,
`schema_registry`, `embeddings`). **18 do not** — including every entry point.

A unit deserves a node when a change to it is a thing you'd argue about. File grain
mints ~120 nodes, most of them `types.py`-shaped, and the argument never lives
there. Symbol grain is what a code index already gives for free. Deliberately **not**
represented: files, symbols, `src/` sub-packages, `tests/`, data files like
`lib/agent-prompt.md`. Sub-packages are a judgement call I'm making explicit —
`graph_core/persistence` is arguably its own argument (H0h, the sqlite backend), and
the first re-run after a real split will show whether 23 was too coarse.

## 2. Seed source: I checked GitNexus, and it is the wrong source for this unit

The MCP tools were unreachable this session (`PreToolUse` hook timeout on
`list_repos`, `cypher`, `query`; four attempts), so I read the index off disk:
`.gitnexus/meta.json` (155 files, 1622 nodes, 4035 edges, 128 processes, indexed at
`9781bff`) plus `strings` over the kuzu store `.gitnexus/lbug`.

Control first: the longest `def`/`class` signature from `chain_engine/chains.py`,
`graph_core/graph.py`, `renderers/ascii.py` and `agi_algos/graph_builder.py` is
present, as are the shell function headers from `driver.sh` and `lib/find-root.sh`.
The probe works. The same probe against **all twelve `bin/*.py`: zero hits, every
file.** Not one harness function signature is in the index. Seven bin paths appear
as bare strings (`cli`, `dispatch`, `evidence_gate`, `grid`, `metrics`,
`snapshot-build-site`, `snapshot-goals`); five (`benchmark`, `heal`, `post_wire`,
`render-context`, `zoom`) do not appear at all. Caveat I can't resolve without the
MCP tool: `strings` cannot tell a `File` node's path from prose in an indexed
markdown file, and all seven are also quoted in `driver.sh`, the tests and the kit
docs — so their presence may be citation, not indexing.

One finding cuts the same way: `extensions/agi/scripts/import_agitree_nodes.py`
appears in the store and **has never existed in this repo** (`git log --all
--diff-filter=A` returns nothing). It is a path *proposed* in `TODO.md` line 195. A
naive harvest would mint an idea node for a file nobody wrote.

So GitNexus covers the library half — precisely the half that already has nodes —
and has no symbol coverage of the half where every 2026-08 change landed. **Seed
from `git ls-files` plus a directory walk.** GitNexus earns its place one zoom level
down (which symbols, which processes, inside a module), not at the census.

## 3. The 14 stale nodes: deprecate in place

Correction to the received framing: **only 7 of 14 carry `origin: build-site`**. The
other 7 — `exporters`, `cli-invocation`, `bootstrap-discovery`, `chain-bootstrap`,
`session-management`, `test-coverage`, `vector-embedding-isomorphism` — carry **no
`origin` at all**, with visibly different frontmatter shape. No origin-guarded prune
can ever reach them. Half the stale mass is structurally immune to the mechanism
usually proposed to clean it.

Position: **do not re-point, do not prune, deprecate in place.** Re-pointing
`domain-exporters` at a live module launders a 2026-05 argument about Obsidian
export into a claim about code that never existed, and its 99 descendants inherit a
false parent. Set `status: deprecated`, leave body and `next_edges` untouched, mint
fresh nodes alongside. Two of the 14 name modules that do not exist and are
unambiguous; the other 12 are judgement calls the generator should **propose, not
execute** — emit a `STALE:` line per idea node with no matching surface and let a
human or a verdict decide. A generator that silently deprecates is one bad heuristic
away from H0 with better manners.

## 4. Re-runnable without damage: three named failure modes

1. **Field erasure (H0i, fixed 2026-08-21).** `write_frontmatter` rebuilt
   frontmatter from scratch and dropped `next_edges` on every re-snapshot — 15 nodes
   lost their chains and the run reported success. A new generator has that exact
   shape. It must reuse `write_frontmatter(..., preserve=existing_fm)` rather than
   reimplement it, and ship the round-trip test H0i said was missing: write, add a
   foreign field, write again, assert survival.
2. **Prune reach.** Stamp `origin: engine-decomp`; prune only that stamp
   (`snapshot-goals.py:324-329`). Never touch unstamped or `build-site` nodes. A
   vanished source tree must be a no-op that prunes nothing — the
   `snapshot-goals.py:277` rule that stops a renamed `GOALS.md` wiping the goals.
3. **The override door.** Wire it plugin-only in `driver.sh`, no project-local
   lookup. That override mechanism *is* the H0 data-loss defect; L15 refused to
   extend it to `snapshot-goals.py` and this must refuse identically.

Parent-pointing is free: `collect_parent_refs` (`snapshot-goals.py:250`) already
derives each goal's `seeds:` from `parents:`. The goal→unit mapping is the one thing
not derivable from the file tree — it needs a declared table in config, and a unit
with no goal should be emitted parentless and flagged, never guessed.

## 5. Falsifier, pre-registered

Baseline: **11 of the 14 hand-written ideas (79%) have at least one `next_edges`
child.** That is the number to beat.

Generation is **worse** if, 20 iterations after the first full pass, the fraction of
generated idea nodes with ≥1 child hypothesis sits below 79%. That means coverage
bought at the cost of thought — 23 nodes nobody could argue with, the H3 padding
pattern re-run at the idea layer.

Two hard failures need no waiting period, and either kills it outright:
- Two consecutive runs against an unchanged engine produce a **non-empty** diff
  under `nodes/`. That is H0i again — disqualifying, not a bug to fix later.
- A module rename lands and the old node is not retired in the same run. If a human
  cleans up after it, it is not the source of truth, and `domain-exporters` happens
  again with a script's name on it.