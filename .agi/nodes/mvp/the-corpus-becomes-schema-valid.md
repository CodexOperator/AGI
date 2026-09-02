---
id: mvp:the-corpus-becomes-schema-valid
mint_id: edae00c540aa437ba07d929ea3d6af17
type: mvp
title: The 115 nodes that predate the fix become valid without anything being invented
parents:
  - verdict:scaffolds-are-born-valid-now
next_edges: []
scaffold_hash: 879a958ec582a87e
status: open
confidence: 0.75
---

# mvp:the-corpus-becomes-schema-valid

## What this must satisfy

`verdict:scaffolds-are-born-valid-now` is true forward and false backward:
**115 of 900 nodes on disk are still schema-invalid.** `write.py schema --fix`
exists and has only ever run dry.

### The two populations, and only one is mechanical

- **91 field-instances are derivable** — `title` x86 from each node's own
  address, `testable_claim` x5 from bodies that already state one under a
  heading. This half is one command, reversible through git and the grid.
- **62 are not** — `testable_claim` x51, `scale` x7, `next_edges` x3,
  `confidence` x1. **51 of 56 missing claims are bodies that state the claim in
  prose without the heading `_section_text` looks for.** No mechanical fix
  reaches them, and inventing them would put exactly the `TODO(model)`
  placeholder into the corpus that `goal:g2.10` spent 8,034 fields teaching
  this project to fear.

### The invariants

1. **Nothing is invented.** A field with no derivable value stays absent and
   stays counted. This is the invariant, not a limitation of the current
   implementation.
2. **`active_node_count` + `deprecated_node_count` does not move.** A backfill
   edits; it never creates or removes.
3. **An authored `THOUGHT` survives every rewrite.** Guaranteed by
   `update_node`, and 91 nodes is the largest single exercise of that
   guarantee so far.
4. **The residual is reported, not hidden.** After the backfill,
   `write.py schema` still names what remains, and the number is expected to be
   62 rather than 0.

### The falsifier

Run `write.py schema --fix`. `write.py schema` afterwards reports exactly the
predicted residual — 62 field-instances, no more and no fewer. Node counts are
unchanged. Every node that carried a `THOUGHT` before still carries the same
one, byte-identical. `grid.py commit --all` mints a version for each changed
node and none for the rest.

### The unreachable half needs a different mechanism

Reaching the 51 means either reading a claim out of unstructured prose — a
model's job, not a parser's — or changing the kid brief so future bodies carry
the heading. **The second is cheap and should happen first**, and it is
`goal:g1.9`'s territory since the brief is assembled, not typed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The falsifier predicts a specific residual rather than success, because "the
backfill worked" and "the backfill filled everything" are different claims and
only the first is wanted. A run that produced 0 remaining would mean something
invented 51 claims.

The last section is the actually useful finding buried in this mvp: the
mechanical fix is the small half. Most of the invalidity is bodies that never
carried the structure the frontmatter needed, and the durable fix is upstream
in the brief rather than downstream in a backfill. Recording that here stops
the backfill from being mistaken for the solution.
<!-- THOUGHT:END -->
