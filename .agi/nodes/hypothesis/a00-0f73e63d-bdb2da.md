---
id: hypothesis:a00-0f73e63d-bdb2da
mint_id: 52199da117ed4be4a60471be554680aa
type: hypothesis
parents:
  - goal:g7.31.1.2.3
next_edges: []
confidence: 0.7
edited_by: a00-0f73e63d
loop: goal:g7.31.1.2.3@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 5df32ab6c932ffeb
season: 2
testable_claim: "A named-pane hold remains an optimization: absent tmux or an unset session still reaches the existing direct-Popen restart path with identical argv and environment semantics, and the hold implementation has graph build-node or payload_ref coverage."
title: Named-pane hold degrades to direct restart safely
town: core
verdict: pending
---
<!-- BODY:BEGIN -->
# hypothesis:a00-0f73e63d-bdb2da

## Hypothesis

A named-pane hold must be an optimization, never a restart prerequisite: when the `tmux` executable is absent, the hold API cannot report a named session, or the pane/session lookup is unset, the same restart call must still launch the adapter command through the existing direct-`Popen` path with the adapter's prepared child environment. The durable tmux path and the hold implementation itself must also be covered by graph build nodes or `payload_ref` coverage, so their behavior has one inspectable version history.

## Test

Spawn an experiment under this hypothesis. A focused test may stub the tmux availability/session lookup as unavailable and spy on the direct process-launch seam.

**Proves it** if both unavailable-tmux and unset-session probes reach the direct launch seam with a non-empty pid/result, the same argv, and the same environment semantics as an ordinary spawn; and a grid coverage probe resolves a build node or `payload_ref` for the hold implementation.

**Disproves it** if either degraded-host case raises before launching, silently returns no pid, or substitutes a different argv/environment contract.

## Boundary

This hypothesis concerns safe degradation and version coverage only. The sibling goals own held-restart environment completeness and first-spawn pane founding; those must not be folded into this experiment or used to excuse a missing fallback here.

## Agent Notes
Framed a tight falsifiable claim that named-pane hold degrades to the existing direct-Popen restart path with identical argv/env, plus graph coverage; no implementation or measurement was performed.
