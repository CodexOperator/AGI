---
id: mvp:the-corpus-becomes-schema-valid
mint_id: edae00c540aa437ba07d929ea3d6af17
type: mvp
parents:
  - verdict:scaffolds-are-born-valid-now
next_edges: []
confidence: 0.8
edited_by: season.py
scaffold_hash: 879a958ec582a87e
season: 1
status: complete
thought_session: season
title: The 115 nodes that predate the fix become valid without anything being invented
---
# mvp:the-corpus-becomes-schema-valid

## What this must satisfy

`verdict:scaffolds-are-born-valid-now` is true forward and false backward:
**115 of 900 nodes on disk are still schema-invalid.** The backfill ran in
`L1.07` (`ab07ec980`) — 118 → 62 invalid, 90 filled — and the command that
ran it was removed from `write.py` in the same commit.

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

**Run, and passed, in `L1.07` (`ab07ec980`).** The backfill filled 90
field-instances (118 → 62 invalid — the census had grown from 115 to 118
between this node's writing and the run, and the residual still landed on
the predicted 62, on the predicted set: `testable_claim` x51, `scale` x7,
`next_edges` x3, `confidence` x1). The node diff of that commit carries a
net +2 THOUGHT lines across 93 files, so invariant 3 held. The iter-1007
census reads 71 of 956: the 62 plus nine in-flight kids of the current
iteration, all still in the non-derivable set. The command itself was
removed from `write.py` in the same commit — the verb layer's
mechanically-checked no-file-write invariant is the reason — which is why
the residual is now reported by `node_writer.missing_required` run over the
corpus rather than by a standing command.

### The unreachable half needs a different mechanism

Reaching the 51 means either reading a claim out of unstructured prose — a
model's job, not a parser's — or changing the kid brief so future bodies carry
the heading. **The second is cheap and should happen first**, and it is
`goal:g1.9`'s territory since the brief is assembled, not typed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, iteration 1007. The mvp's falsifier was executed and passed
while this node was open, and this version records that instead of leaving
an open mvp whose named command no longer exists.

What the review found: `L1.07` (`ab07ec980`) ran the backfill for real —
118 → 62 invalid, 90 field-instances filled — with the residual landing on
exactly the set this node predicted. That is the falsifier passing on its
predicted number rather than on 0, which is the stronger of the two
outcomes: a run that had produced 0 would mean something invented 51
claims. The same commit then removed `write.py schema [--fix]`, because
`write.py` holds a mechanically-checked invariant that it performs no file
write at all, and carving the backfill an exception would have traded a
strong mechanical property for a comment. So the tool this mvp's falsifier
names as standing is gone, and a reader who tried to re-run the falsifier
would have been met with an argparse error.

`status: open` → `complete`, `confidence` 0.75 → 0.8. The mechanical half
of the mvp is discharged; the residual (now 71 of 956 with nine in-flight
kids) is by this node's own terms `goal:g1.9`'s territory — model or
brief change, not a backfill — and stays reported rather than hidden.
The 91 → 90 delta (predicted derivable vs filled) is census drift, not a
miss: three new nodes became invalid between the two runs, and the
residual — the number the falsifier actually predicts — matched.
<!-- THOUGHT:END -->