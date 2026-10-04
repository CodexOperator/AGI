---
id: hypothesis:born-valid-without-touching-frontmatter
mint_id: 3dd69140a6b54dea81b410193c611bd5
type: hypothesis
parents:
  - goal:g7.33.10.1
next_edges:
  - experiment:the-falsifier-and-the-corpus-census
confidence: 0.85
edited_by: belam
evidence_runs:
  - experiment:dg2close-born-valid-without-touching-frontmatter-check
scaffold_hash: 2b25f5e175a1dd7f
season: 1
testable_claim: "A scaffold can be born schema-valid without any agent touching frontmatter, by splitting the required fields into two populations: those the **engine can derive** at write time, seeded before the file is written; and those only the **kid holds**, written by the kid into the *body* under the heading its brief asks for and lifted into frontmatter at completion by the gated write path. Nothing is invented for a field in neither population — it stays absent and stays reported."
thought_session: season
title: Born valid without touching frontmatter
verdict: proved
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
Moved from goal:s31 to goal:g7.33.10.1 because its proved two-populations claim (engine-derivable fields seeded, kid-held fields lifted from the body, nothing invented) is exactly g7.33.10.1's backfill invariant: a value comes from the node's own bytes or stays missing with a named finding. goal:g7.33.10.1 is the live leaf the council re-homed retired s31 into, and its body cites this node by id. Owner, verbatim: "Move all hypotheses under all retired s goals to be patented by appropriate nested g-goals". Parenthood only (owner: "The regime doesn't need a goal. We're just adjusting parenthood"): mint_id, body and verdict unchanged.
<!-- THOUGHT:END -->
