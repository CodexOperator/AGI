---
id: hypothesis:shared-lease-bounds-the-tree
mint_id: c7947bc03cd24c62bfa87b709f71d96f
type: hypothesis
parents:
  - goal:g4.8
next_edges:
  - experiment:lease-bound-under-five-spawners
confidence: 0.9
edited_by: season.py
scaffold_hash: de6312a4a1ec2849
season: 1
testable_claim: With a per-tree lease taken under a lock at the spawn site, N independent spawners each opening M slots keep the live population <= the declared cap, where the same topology under `spawn.parallel` alone reaches N*M.
thought_session: season
title: A bound lives in shared state, not in a number each spawner reads
verdict: pending
---
# hypothesis:shared-lease-bounds-the-tree

## Hypothesis

`hypothesis:a00-8d238338-ec4dff` asked whether a parent *enforcing*
`spawn.parallel` could hold a global bound, and `experiment:a00-5f927203-8a66a2`
**disproved** it. This hypothesis is the next step after that disproof, not a
retry of it: the failure was not that parents enforce the limit badly, it is
that **a limit expressed as a number cannot be global**, because every spawner
reads its own copy and none of them can see the others.

### Testable claim

A bound enforced through **shared state mutated at the spawn site** — one lease
file per live agent, created under an exclusive lock over the whole lease
directory, immediately before the process is created — holds the live
population at or below the declared cap for `N` independent spawners opening
`M` slots each, at every sample, for any cap.

### What would prove it

Five independent OS processes (the shape of five parents, each running
`dispatch.py` for itself) racing through one lease directory, five slots each —
25 would-be agents. At caps of 1, 3 and 5:

- the peak live count never exceeds the cap, at every sample;
- the peak actually *reaches* the cap, so the run is at the boundary rather
  than passing because everything was refused;
- a negative control at a cap that does not bind admits all 25 and peaks far
  above 5, so the assertion is measuring the bound and not the harness.

### What would disprove it

- Any sample above the cap — the read-count-write cycle is not atomic and the
  hole is still open.
- The bound holds only because slots are never returned, i.e. a killed agent
  keeps its lease and the budget shrinks monotonically toward zero. A safety
  rail that degrades into an outage has not proved the claim, it has replaced
  one failure with a worse one.
- Admission blocks rather than refusing, producing the deadlock this topology
  invites: parents holding every lease, each waiting on a kid that can never
  be admitted until a parent finishes.

### Why the mechanism has to sit at the spawn site

`goal:g4.8` item 3's own words — the limit has to be enforced where spawning
happens rather than stated in a brief a parent may ignore. A parent gets its
kids by running `dispatch.py` again, so the second invocation passing through
the same admission path is the entire mechanism: **there is no separate
grandchild code path to bound, only the same one entered twice.**

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted after `experiment:a00-5f927203-8a66a2` disproved the previous
hypothesis, and deliberately as a new hypothesis rather than an edit to that
one. The disproof is a real result about a real design and it keeps its
verdict; what changed is the design, not the measurement.

The claim is stated about *shared state* rather than about a lease directory
specifically, because the lease directory is one implementation and the falsifier
should not be satisfiable only by it. What must not survive is the class of
answer the previous hypothesis tried: a number that each spawner reads for
itself, however carefully each one then behaves.

The second and third proof clauses were added after drafting the first, on the
grounds that a bound test which passes because nothing was admitted is the
cheapest possible false green — and this project has already recorded one
smoke check that passed on a traceback because absent output and a crash look
identical to `grep`.
<!-- THOUGHT:END -->