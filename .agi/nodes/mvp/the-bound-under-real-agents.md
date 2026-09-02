---
id: mvp:the-bound-under-real-agents
mint_id: e416f8f0d8ec4379a5f79bfbe0bcca2b
type: mvp
title: goal:g4.8's remaining three falsifier clauses, at the cap the owner set
parents:
  - verdict:the-bound-is-structural-now
next_edges: []
scaffold_hash: 5f53b803a0d34926
status: open
confidence: 0.75
---

# mvp:the-bound-under-real-agents

## What this must satisfy

`verdict:the-bound-is-structural-now` closed **clause 2 only** of
`goal:g4.8`'s four-clause falsifier, against sleeping interpreters. Three
clauses are untouched and they are the ones about a loop rather than a counter.

### The three clauses still open

1. **No kid's node is lost or overwritten by another loop's kid.** The manifest
   race is fixed and verified at 8 concurrent agents; 25 is three times that,
   and `goal:s28`'s whole lesson is that a read-merge-write cycle can look
   correct and lose 6 of 8 under load.
2. **Each parent's review gate demotes at least one unevidenced verdict
   without the delegator intervening.** Never observed. This is the clause that
   distinguishes a parent tier from a spawn fan-out, and if it fails the tier
   is decorative.
3. **The delegator's own token spend is sub-linear in the number of loops.**
   The whole economic case for the tier. Measured by comparing delegator tokens
   across a 1-parent and a 5-parent iteration.

Model tiering is verified **by inspecting the spawned commands**, not assumed —
a parent silently running on the kid model would pass every other clause.

### The invariants

1. **The live population never exceeds `spawn.max_live`.** Proved
   synthetically; here it must hold with real agents that start slowly, die in
   more ways, and can be stopped rather than killed.
2. **An unadmitted slot appears in `manifest.unadmitted` and nowhere else.**
   Nothing that polls `agents` for liveness may find it.
3. **A parent that gets fewer kids than it asked for says so** rather than
   proceeding as if it had them.

### The falsifier

One iteration, 5 parents, real kids, at cap 25. All four `goal:g4.8` clauses
hold simultaneously. Node count grows by exactly the number of kid nodes
written; the manifest lists every spawned agent; `spawn_budget.py status`
peaks at or below 25 throughout.

### Sequencing

This should run **after** `mvp:a-live-loop-on-minted-keys`, not with it. Both
are live runs at cap 25 and both have unmeasured failure modes; running them
together means a failure cannot be attributed to either.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Clause 2 — a parent demoting an unevidenced verdict on its own — is the one I
would most expect to fail, and it is worth saying so before the run rather
than after. Everything the parent tier has demonstrated so far is spawning;
reviewing is the part that justifies the tier existing, and it has never been
observed happening without a human in the loop.

The sequencing note is the only design decision in this node. Two live runs at
an untested concurrency, sharing a novel credential path, would produce a
failure nobody could attribute. Separating them costs one iteration and buys
the ability to read the result.
<!-- THOUGHT:END -->
