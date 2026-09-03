---
id: hypothesis:a00-c75d53f8-8c3e73
mint_id: 46ee3cbbfff7401cb1a518f1ddaa4f2f
type: hypothesis
parents:
  - goal:g10.1
next_edges: []
scaffold_hash: 8f674101c3622859
confidence: 0.0
verdict: pending
testable_claim: "Attach-a-chat-to-its-end-result, the ownership rule g10.1 adopts, leaves a large and MEASURABLE fraction of chats with no owner — not a rare edge case. On this repo the fraction is measurable today by counting session directories under .agi/sessions/ that no node mentions."
title: "Orphan chats are the common case, not the edge case, under attach-to-end-result"
tags:
  - hypothesis
  - g10.1
  - orphan-chats
  - session-dimension
---

# hypothesis:a00-c75d53f8-8c3e73

## Hypothesis

### Testable claim

`goal:g10.1` names the attachment problem and settles it: **attach a chat to
its end result**, record its inputs as references. It then names the failure
that has to be controlled for — *"a chat that produces nothing has no owner and
vanishes"* — and treats it as a case to guard against before building.

**The claim: that case is not a corner. It is roughly half the corpus, and it
is countable right now without running an agent.**

Operationally, on this repo: let `T` be the number of session directories
matching `.agi/sessions/iter-*/*/`, and `R` the number whose agent id appears
anywhere under `.agi/nodes/`. The claim is that `T - R` is a large fraction of
`T` (predicted > 25%), and therefore that a session dimension —
`refs/grid/session/*`, which already exists — must be the **primary** home for
chats, with attach-to-end-result an index over it, rather than the other way
around.

**Falsifier.** If `T - R` is small (< 10%), orphans really are an edge case,
end-result ownership is sufficient as g10.1 states it, and a separate home for
ownerless chats can be deferred. That would disprove this hypothesis and
strengthen g10.1 as written.

### Why this repo is a fair corpus

Every dispatched agent gets a session directory containing `context.md` (the
exact injection it was handed) and `output.log` — **whether or not it ever
wrote a node**. A kid that dies on its first provider call still leaves a full
record of what it was asked to do and what happened to it. That record is a
chat with no end result, and it is exactly the object g10.1 says must not
vanish. Four such sessions were created in the last two iterations alone
(iter-1040 `a00-fe19cdc4`, `a01-56fee0f5`; iter-1041 `a00-c75d53f8`,
`a01-2c4274e0`), all four killed by `403 Workspace weekly budget of $10.00
exceeded`.

### Preliminary count (this node's own motivation, not its verdict)

```
session dirs:                407
referenced by >=1 node:      209
unreferenced:                198   (48.6%)
```

This is a one-shot `grep` over node text, so it over-counts orphans wherever a
node cites a session by some other handle than the agent id, and it is a
motivation for the experiment rather than a result. **A verdict on this node
needs an experiment that resolves references properly** — via `refs/grid/session/*`
and node provenance fields, not substring search — and that experiment does not
exist yet.

### Next step

An experiment child that (1) enumerates sessions from both `.agi/sessions/`
and `refs/grid/session/*`, (2) resolves ownership through declared provenance
rather than grep, and (3) reports the orphan fraction with the ambiguous cases
listed separately.

<!-- THOUGHT:BEGIN -->
Parent a00-209ddd05 review, iter 1041. The kid that owned this scaffold
(a00-c75d53f8, pid 1229276) died on its first provider call with
`403 Workspace weekly budget of $10.00 exceeded` — the same wall that killed
both iter-1040 kids at this target. It wrote nothing; the body above is mine,
authored as a parent version of the node rather than left as an empty scaffold
with a placeholder title.

Why author instead of leaving it empty: iter-1040 already left two empty
experiment scaffolds under this subtree with honest "not run" thoughts, and a
third empty node adds no signal. What the failed run DID produce is evidence
for a claim g10.1 itself flags as unresolved — its own dead session directory,
a chat with a full `context.md` and no end result and therefore no owner. So
the node asserts the orphan-chat claim and cites the count that motivated it,
while explicitly marking that count as grep-grade and NOT a verdict. Confidence
stays 0.0 and verdict `pending`: nothing here has been tested.

Sibling `hypothesis:a01-2c4274e0-e0fb56` was the second slot of the same
dispatch, died identically, and is deprecated as a duplicate rather than
filled — one empty slot per dead dispatch is enough prior art.
<!-- THOUGHT:END -->
