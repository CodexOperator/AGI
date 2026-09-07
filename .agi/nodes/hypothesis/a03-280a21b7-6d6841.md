---
id: hypothesis:a03-280a21b7-6d6841
mint_id: 9f10ee0a447b4c87a1350b3f96819d27
type: hypothesis
parents:
  - goal:g4.8
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 4a3d7d5cdf404654
season: 1
testable_claim: With the lease-bound mechanism capping concurrent agents, kids spawned by different parents into the same working tree can avoid node file collisions because each kid's node file path is derived from its unique mint_id (a UUID) and contains no shared counter, temp-name, or sequence number that another kid could alias — so two kids cannot write to the same path even if they target the same parent node.
thought_session: season
title: Parallel kids writing to the same working tree avoid node collisions through mint_id-scoped file paths
verdict: pending
---
# hypothesis:a03-280a21b7-6d6841

## Hypothesis

### Testable claim

With the lease-bound mechanism capping concurrent agents at the declared bound
(proved by `experiment:lease-bound-under-five-spawners`), kids spawned by
different parents into the same working tree avoid node file collisions
**because** each kid's node file path is derived from its unique `mint_id`
(a UUID) and contains no shared counter, temp-name, or sequence number that
another kid could alias. Two kids targeting the same parent node write to
different file paths — so they cannot overwrite each other even if they run
the same task at the same time.

### What would prove it

An experiment running 2 parents concurrently against `goal:g4.8`, each
spawning 2 kids, where:

- All 4 kids complete and write their node files to `.agi/nodes/hypothesis/`
- Each file has a distinct path (derived from unique mint_id)
- No file is truncated, partially written, or has another kid's content
  embedded in it (verified by `mint_id` in frontmatter matching the file's
  own node id)
- The total number of kid node files equals the number of kids spawned (4)
  — no overwrites, no orphans
- A negative control: 2 kids deliberately spawned with no mint_id
  scoping (mimicking pre-g4.8 behaviour) produces at least one collision
  or overwrite, so the test measures scoping rather than luck

### What would disprove it

- Any kid's node file contains another kid's frontmatter `id` or `mint_id`
  — the files collided
- Any kid's node file is truncated or has a zero-byte body — partial write
  from a concurrent writer
- Fewer than 4 distinct kid node files exist after all 4 kids complete
  — overwrite
- The negative control produces no collisions either — the test harness
  itself serializes writes, invalidating the entire comparison

### Relation to g4.8

Directly tests g4.8 falsifier **clause 1** — "no kid's node is lost or
overwritten by another loop's kid" — which g4.8 calls out as unfixed in
item 4: "Kids that do not collide. `goal:g4.1` — parallel kids share one
working tree. Unfixed, and it is the failure this goal multiplies rather
than introduces." This hypothesis is the claim that the failure **is not**
multiplied, because mint_id-scoped paths make collisions structurally
impossible regardless of concurrency.

### Why it is not a tautology

The claim would be a tautology only if file paths were guaranteed unique by
construction *and* the write were atomic. Python file writes are not atomic
at the OS level for multi-writer scenarios (no `O_EXCL` on the write path).
The hypothesis asserts that distinct paths + non-overlapping writes = no
collision, which holds if and only if:

1. Every kid indeed gets a unique mint_id before writing
2. The write path opens the file with `O_CREAT` (not `O_EXCL`) so a
   collision would silently append or truncate — but there is no collision
   because the paths are distinct
3. No external process renames or moves files between the write and the
   read-back

Conditions 1 and 3 are what the experiment tests. Condition 2 is structural
and can be verified by inspecting the node writer code.


## Agent Notes
Hypothesis: mint_id-scoped node file paths prevent collisions between parallel kids writing to same working tree. Targets g4.8 falsifier clause 1 (no kid node loss/overwrite) — the remaining unfixed clause. Builds on lease-bound proof for clause 2.