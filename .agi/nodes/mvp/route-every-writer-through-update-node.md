---
id: mvp:route-every-writer-through-update-node
mint_id: 619f50cb65f7403795654f49c637c3c9
type: mvp
title: Every in-place node edit goes through one gated routine
parents:
  - verdict:the-write-half-has-a-floor
next_edges: []
scaffold_hash: d095dad2f7592a30
status: open
confidence: 0.8
---

# mvp:route-every-writer-through-update-node

## What this must satisfy

`verdict:the-write-half-has-a-floor` proved the routine exists and is safe to
route edits through. Its first limit is that **nothing routes through it**:
`update_node` has no production caller beyond `write.set_link`. A gated write
path with no callers is a convention with a test suite.

### The interfaces

- `post_wire.py`'s `_write_node` and `cli.py`'s `_append_verdict_to_node` both
  read frontmatter, mutate it and rewrite the file by hand. Both become
  `node_writer.update_node` calls.
- The three generators — `snapshot-goals.py`, `snapshot-build-site.py`,
  `level3.py` — stay outside, deliberately. They own their own frontmatter keys
  and a `preserve=` merge `update_node` has no notion of, and `goal:g13`
  already records that exemption. **Do not "unify" them.**

### The invariants

1. **No caller may lose an authored `THOUGHT`.** The routine guarantees it;
   the point of routing through it is that callers inherit the guarantee
   instead of each re-earning it.
2. **A no-op edit stays a no-op.** `post_wire` runs on every completion; if
   routing it through `update_node` makes it rewrite unchanged files, the grid
   gains a version per node per iteration and *versions record change, not
   time* stops being true.
3. **`scaffold_hash` never moves on a frontmatter-only edit.** Already
   asserted; it becomes load-bearing once the completion path uses it.

### The falsifier

Run one full iteration. Every node written or updated in it passed through
`update_node` — verified by instrumenting the routine and asserting no other
code path opened a node file for writing. `grid.py commit --all` afterwards
mints versions only for nodes that actually changed. The suite stays green,
including the four writer-path tests that predate this change.

### What is deliberately out of scope

Making a node body a *marker*. That is `goal:g13`'s load-bearing claim and it
is untouched by this mvp — 685 nodes still resolve `self` by default and none
declares a link. Routing writers is the prerequisite, not the migration.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted from the parent verdict's own first limit rather than from an idea.
That is the shape an mvp should have here: the verdict said what it did not
prove, and the smallest thing that would discharge it is exactly that gap.

Invariant 2 is the one most likely to be skipped and is the one that would do
real damage. `post_wire` touches every completed node every iteration; a
routing change that turns "read, decide nothing changed, leave it" into "read,
rewrite identically" is invisible in tests and shows up as a grid that records
time instead of change. The `UNCHANGED` status exists for this and the
falsifier checks it explicitly.

The out-of-scope paragraph is here because "route every writer through the one
path" sounds like it finishes g13, and it does not. It finishes the floor.
<!-- THOUGHT:END -->
