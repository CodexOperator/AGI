---
id: hyp:spawn-check-on-writer-path
mint_id: 35f11042d4114652a71dc3d8e6697b65
type: hypothesis
parents:
  - idea:schema-declared-spawn-gate
next_edges:
  - exp:node-type-corpus-survey
  - exp:spawn-gate-falsifier
confidence: 0.8
edited_by: season.py
season: 1
subgraph: false
tags:
  - s17
  - schema
  - gate
testable_claim: A spawn rule read from context/schemas/[<type>].md and applied inside cli.py/post_wire.py will (a) refuse to write a verdict with no parent and a task with three parents, each time naming the violated rule AND the schema file it came from, (b) print an explicit approval naming the schema on a legal spawn, and (c) leave every one of the 53 existing rule-violating nodes in place.
thought_session: season
title: A schema-declared spawn rule, enforced on the writer path, rejects by name and approves out loud
---
# hyp:spawn-check-on-writer-path

## The testable claim

A spawn rule that lives in `context/schemas/[<type>].md` and is applied
**inside the writer path** will:

- **(a) reject** a `verdict` with no parent and a `task` with three parents,
  each rejection naming the violated rule *and* the schema file it came from,
  and writing no file;
- **(b) approve out loud** — a legal spawn produces an explicit line saying
  what it was checked against, so "approved" and "not checked" cannot be
  confused;
- **(c) change nothing historical** — all 53 nodes that violate the new rule
  keep their place, and `node_count` does not drop.

## What would prove it

All three, observed in real terminal output from the real writer path, on a
rule that was transcribed from the corpus rather than invented. (c) is checked
by counting nodes before and after.

## What would disprove it

Any one of the three going silent. Specifically:

- a rejection that says "invalid" without naming the rule or the file — that
  is a code control that teaches like a prose one;
- an approval that prints nothing, because then the gate is indistinguishable
  from a gate that is not installed;
- any drop in `node_count`, which would mean the rule was applied
  retroactively — a purge, not a report (G7's first invariant).

A **partial** result is a real outcome and must be reported as
`inconclusive_lean_*`, not rounded up.

## The three sub-claims that could each fail independently

1. **The rule is derivable.** Is the corpus consistent enough that a rule read
   off it is meaningful, or is it noise? Tested by re-running the survey
   independently of the table in `GOALS.md` §S17 and checking it reproduces.
2. **The rule is expressible.** `goal` is one `type:` with three shapes
   (`long-term`, `short-term`, `subgoal`), two of which may be parentless and
   one of which may not. A flat per-type rule cannot say that; it would
   license all 48 subgoals to float free.
3. **The rule is enforceable at the right moment.** The check has to run
   before the file is written, or a rejection leaves a half-node behind.

## Explicitly out of scope

Whether the rule table is *correct* in some absolute sense. It is transcribed
from what 778 nodes actually do. If the corpus is wrong, the table inherits
that — and the 53 violations are evidence that corpus and rule already
disagree. Reconciling them is not this hypothesis; **reporting them is.**