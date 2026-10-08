---
id: idea:a00-dec86d5d-735de8
mint_id: dcad3a14fb1442279ad8c39cf34d09d1
type: idea
parents: []
confidence: 0.5
edited_by: season.py
evidence_runs: 0
season: 1
thought_session: season
title: A00 dec86d5d 735de8
verdict: pending
wired_at: 1788197591
wired_from: a00-dec86d5d
---

# idea:a00-dec86d5d-735de8

## Idea

`scale:` big — new chain, fresh domain.

**domain-grid-changelog**: use the grid's per-node version history (`refs/grid/*` + THOUGHT blocks, which `grid.py diff` already renders as a reasoning changelog) as a **work-selection signal** for agent dispatch.

Today dispatch picks attractive nodes by descendant count (`outcome_coverage` goal-attributable). That signal says where work has *accumulated*, not where work *stalled*. The grid history says where work *stopped and why*: a chain whose last N grid versions are verdicts with no MVP spawned, or whose THOUGHT deltas repeatedly say "deferred", is stalled work that no descendant-count heuristic can see.

Testable consequences:
- H1: a stalled-chain detector over grid history (last version type per node, recency, verdict-without-successor pattern) identifies chains better than descendant count at predicting which dispatch target raises `outcome_coverage` next iteration.
- H2: injecting the 5 most recent THOUGHT deltas of a dispatch target into the zoom context reduces repeated/aborted approaches per agent (fewer `pending` verdicts).

Concrete first step: hypothesis node claiming H1, with an experiment that backfills "stalled" labels from existing 826-node graph + grid refs and compares against where outcome_coverage gains actually happened historically.

Success = the detector ranks at least one truly stalled chain in the top 5 that descendant-count ranking misses entirely. Failure = top-5 overlap with descendant-count ranking (no new signal).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. -->
Descendant count measures where the web is dense; grid history measures where a thread was cut mid-weave. The graph already pays the storage cost of per-node versioning — this idea spends it on selection, which nothing currently does. Started fresh (no parent domain) because it sits between grid and chain-engine and belongs to neither.
<!-- THOUGHT:END -->

seeded big idea domain-grid-changelog: stalled-chain detector from grid version history as dispatch signal; H1/H2 stated, first experiment defined