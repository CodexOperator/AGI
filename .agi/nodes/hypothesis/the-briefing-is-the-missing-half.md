---
id: hypothesis:the-briefing-is-the-missing-half
mint_id: 77f7cb183055488ca9884b61a27e9a70
type: hypothesis
parents:
  - goal:g9.7
next_edges:
  - experiment:the-viewport-reaches-parity
scaffold_hash: aff24ef94a0a1ff5
title: "What kept the viewport from replacing the renderer was never the tree — it was the nine sections around it"
testable_claim: "The gap between `viewport.py --emit llm` and `INJECTION.md` is entirely non-frame briefing material, so extracting that material into one module both call closes the gap without either renderer changing what it draws"
verdict: pending
confidence: 0.0
---

# hypothesis:the-briefing-is-the-missing-half

## Hypothesis

`goal:g9.7` holds **one render, two readers** and `viewport.py` delivers it —
for *frames*. The banked question "should the viewport replace `INJECTION.md`'s
renderer?" has sat open across two sessions on the assumption that answering it
means reconciling two tree renderers.

**It does not.** The tree was never the disagreement.

### Testable claim

The 226-line gap between `viewport.py --emit llm` (45 lines) and
`INJECTION.md` (271) is **entirely non-frame material**: the graph snapshot,
the primary metric and its gameability warning, chain diagnostics, the
attractor list, the big-vs-small split, the verdict taxonomy, the chain rules,
pending tasks, and the declared command table.

If that is true, then extracting those nine sections into a module both
renderers call:

1. closes the parity gap without either renderer changing what it *draws*;
2. leaves `INJECTION.md` **byte-identical**, which is the proof the extraction
   was a move rather than a rewrite; and
3. makes deleting `render-context.py` a deletion rather than a migration,
   because the contract no longer lives inside it.

### What would disprove it

- A section of `INJECTION.md` that cannot be computed without the ASCII
  renderer's own traversal — i.e. real coupling between briefing and tree.
- `INJECTION.md` changing by even one non-timestamp byte after the extraction.
- The viewport needing to reach back into the graph for something the
  `Briefing` does not carry, which would put a second computation back.

### Why it matters beyond tidiness

`render-context.py` held the **only** copy of the chain rules and the verdict
taxonomy as literal text in a line list. Anything else wanting to show an
agent the rules had to restate them — and `goal:g1.10` already measured what
restatement costs, finding four prose copies of the command table of which one
had been wrong for months. The rules an agent is judged against are exactly
the text that must not have two owners.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Written after the work rather than before it, and labelled as such: this is a claim I formed while reading the two outputs side by side, not a prediction I risked anything on. It is minted because the *next* reader deserves the framing that made the banked question easy — the question had been carried across two sessions as "reconcile two tree renderers", which is hard, when it was actually "one file owns the rules", which is one extraction.

Verdict stays `pending`. The experiment beneath it carries the evidence and the verdict; recording `proved` here on the strength of the same run would be counting one result twice.
<!-- THOUGHT:END -->
