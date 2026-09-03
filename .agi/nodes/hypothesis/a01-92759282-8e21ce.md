---
id: hypothesis:a01-92759282-8e21ce
mint_id: 8b2fd0a5a6724b09bf44c02d4b600ee0
type: hypothesis
parents:
  - idea:domain-graph-core
confidence: 0.5
evidence_runs: 0
title: A01 92759282 8e21ce
verdict: pending
wired_at: 1788197591
wired_from: a01-92759282
---


# hypothesis:a01-92759282-8e21ce

## Hypothesis

**Claim:** Concurrent multi-writer edits to the node tree can be made safe — no silent lost updates — using only content-addressed detection against the grid (the state graph-core already persists), with no central lock server and no change to the node file format.

**Mechanism:** Multiple agents (cron `grid_sync`, loop-dispatched agents, human edits) already write `node.md` files in place. Today, two writers touching the same node between grid commits resolve as last-write-wins: one THOUGHT block or body edit silently vanishes. Graph-core can close this without locks by treating the grid ref as the writer's read-version: each write records (mint_id, grid_version_read); at commit, a write whose base version differs from the node's current version is surfaced as a conflict for re-merge rather than applied blindly. Detection is O(changed nodes), uses existing `grid.py versions`, and needs no new storage.

**Testable consequences / what proves it:**
1. Two simulated writers editing the same node's body from the same base version, both committing, yields a detected conflict record — neither body edit is silently discarded.
2. Two writers editing *different* nodes from the same base commit both land with no conflict and no intervention (common case stays cheap).
3. A single writer re-committing an unchanged node is a no-op, byte-identical, as today.

**Disproven if:** conflict detection requires locking or write-time coordination (i.e., detection-after-the-fact cannot reconstruct both sides because the grid ref granularity — per-node versions — is too coarse to key the read base), or the conflict rate on the real graph makes the common case slower than a plain lock.

**Scope:** graph-core persistence semantics only. No UI for conflict resolution, no cross-project merge.

New hyp: multi-writer lost-update safety via grid-version-keyed conflict detection, no locks, no format change