---
id: hypothesis:born-valid-without-touching-frontmatter
mint_id: 3dd69140a6b54dea81b410193c611bd5
type: hypothesis
title: Born valid without touching frontmatter
parents:
  - goal:s31
next_edges:
  - experiment:the-falsifier-and-the-corpus-census
scaffold_hash: 2b25f5e175a1dd7f
verdict: pending
confidence: 0.85
---

# hypothesis:born-valid-without-touching-frontmatter

## Hypothesis

`goal:s31`'s vice is that two individually correct rules compose into a
contradiction: the scaffold owns frontmatter, and the kid is told to leave
frontmatter alone — so a schema-required field the writer does not supply
**cannot be added by anyone doing their job as briefed**.

### Testable claim

A scaffold can be born schema-valid without any agent touching frontmatter, by
splitting the required fields into two populations: those the **engine can
derive** at write time, seeded before the file is written; and those only the
**kid holds**, written by the kid into the *body* under the heading its brief
asks for and lifted into frontmatter at completion by the gated write path.
Nothing is invented for a field in neither population — it stays absent and
stays reported.

### What would prove it

`goal:s31`'s falsifier exactly:

- Scaffold a hypothesis through the normal path, validate against
  `[hypothesis].md`'s `required` list with **no parent intervention** — it
  passes once the kid has written its body.
- `completion.is_complete` still distinguishes an untouched scaffold from a
  filled one, **before and after** the fill. The fix must not buy validity
  with the completion check.
- Seeding frontmatter leaves `scaffold_hash` byte-identical, which is *why*
  the previous clause can hold: the hash is over the **body**.

### What would disprove it

- Any field filled with a placeholder. `goal:g2.10` is the standing proof that
  a declared-but-unfilled field attracts `TODO(model)`, and a corpus of
  placeholders is worse than a corpus of absences because it looks answered.
- A fix that requires the kid to write frontmatter, which trades a silent
  invalid node for a silently broken completion check — strictly worse, and
  the trade the goal explicitly forbids.
- The required list being read from anywhere but the schema registry. The
  goal's objection to patching `node_writer` was that it would add "one more
  caller that agrees with the schema by convention"; a hand-kept list here
  would be that objection coming true.

### The corpus is a separate population

Nodes written before this fix are not made valid by it. Counting them is part
of the experiment; **repairing them is a distinct, larger action** and is not
claimed here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The two-populations framing is what makes this tractable. `goal:s31` listed
three candidate shapes as alternatives — seed at scaffold time, derive from the
body at completion, or validate loudly — and the useful move was to notice they
are not alternatives at all: each handles a different class of field, and all
three together are what "born valid" requires. Seeding alone cannot supply a
testable claim; body-derivation alone cannot run at scaffold time; validation
alone fixes nothing, which the goal itself says.

The disproof clauses are the ones worth defending. Placeholders are the failure
that would look most like success here — every required field present, every
schema satisfied, and a corpus of `TODO(model)`. The goal's own scar tissue
(8,034 fields) is why "invents nothing" is a disproof condition rather than a
nicety.

The last section exists because the corpus number is going to be large and
quotable, and a hypothesis that quietly let "scaffolds are born valid" be read
as "the corpus is valid" would be doing the misreading's work for it.
<!-- THOUGHT:END -->
