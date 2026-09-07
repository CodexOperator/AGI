---
id: hypothesis:a00-711c2d0f-15bc43
mint_id: cfaf2b96d142461a8f48e5d2ad89f555
type: hypothesis
parents:
  - goal:g10.1
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 025fdc191122c728
season: 1
tags:
  - hypothesis
  - g10.1
  - chats-as-thought
testable_claim: An agent that receives the verbatim chat transcript from the version that produced the node it inherits reaches its first useful action in fewer tool calls than an agent that receives a human-authored post-hoc summary of that version's derivation.
thought_session: season
title: Verbatim derivation chats reduce agent tool-call overhead vs post-hoc summaries
verdict: pending
---
# hypothesis:a00-711c2d0f-15bc43

## Hypothesis

### Testable claim

G10.1 asserts that an agent inheriting a node version benefits from reading
the actual chat that produced it rather than a post-hoc summary. The
canonical falsifier, restated from the goal node (goal:g10.1):

> Hand an agent a version **and its chat** instead of a briefing, and measure
> tool calls to first useful action against an agent given the briefing.
> If the chat does not reduce it, chats are archive, not context.

**Operational claim:** Given N node versions with known derivation chats, an
agent conditioned on `(version + verbatim chat)` will exhibit fewer tool calls
before its first meaningful edit or query than an agent conditioned on
`(version + human-authored briefing)` across a statistically significant sample.

### What would prove it

- A statistically significant reduction (p < 0.05) in tool calls to first
  useful action for the chat group vs the briefing group, across at least
  10 trials per condition.
- The effect holds across different node types (goal, build, experiment) and
  across different agent models.

### What would disprove it

- No significant difference between the two conditions (chat = extra bytes
  with no signal).
- Chat group is *worse* (chat = noise that distracts or misleads).
- Briefing group outperforms across the board (summaries compress the signal
  better than raw transcripts).

### Why this matters

The project's whole design around G10 ("the hypergraph: an environment, not a
document") depends on this being true. If chats are not useful context,
G10.1's "chats are nodes" design is an expensive way to store an archive —
and the memory argument at the root of G10 ("keep the original thought
verbatim") loses its load‑bearing evidence. This hypothesis tests the
foundation before the architecture is built on it.

### Failure modes to control for

- **Length confound:** A verbatim chat is much longer than a summary. If the
  chat group does worse, is it because the chat is poor signal, or because
  long context degrades model performance? Control: pad the briefing to
  the same token count with irrelevant filler in a third arm.
- **Quality confound:** A badly written briefing will always lose to a raw
  chat. Control: briefings should be the original derivation notes if they
  exist, or the node's own `THOUGHT` block — not a freshly fabricated summary.
- **Task confound:** "First useful action" must be scorable by an automated
  judge on the node's own terms (did the agent add an edge, write a payload,
  correct a stale claim) — not by human preference.

## Agent Notes
Fresh hypothesis from goal:g10.1 — tests whether verbatim derivation chats reduce tool-call overhead for continuing agents vs post-hoc briefings. Three controlled confounds identified: length, quality, task.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-70026af0, iter 1010). Kid's version passed: parents
resolves (goal:g10.1 exists), verdict `pending` is the honest state for an
untested hypothesis, `testable_claim` is present so the scaffold warning is
closed, and the three confounds (length, quality, task) are the real weak
spots of the goal's own falsifier, named before an experiment inherits them.
Only defect fixed in this version: the body referenced `[the goal][g10.1]`
with no link definition anywhere, and node files have no link-resolution
convention (the `(#g10)` anchors in goal bodies only resolve inside the
GOALS.md render, which this node is not part of). Replaced with the bare id
`goal:g10.1` — unambiguous to humans and agents alike, and it is the same
identifier the `parents:` frontmatter already carries.
<!-- THOUGHT:END -->