---
id: hypothesis:a00-1ade7043-d9c466
mint_id: 7c7ed8ae28e64b658e26fa5d07bfc018
type: hypothesis
parents:
  - goal:g10.1
next_edges: []
scaffold_hash: 3cad1bd09ce163e3
title: "LOD rendering of derivation chats: graduated depth-on-demand beats both full-verbatim and single-summary"
testable_claim: "An agent that accesses a derivation chat at graduated levels of detail (summary → key events → verbatim sections on demand) reaches correct conclusions in fewer tool calls than an agent given either the full verbatim chat or a single static summary."
confidence: 0.0
verdict: pending
tags:
  - hypothesis
  - g10.1
  - lod
  - chat-rendering
---

# hypothesis:a00-1ade7043-d9c466

## Hypothesis

### Testable claim

G10.1 asserts chats are "viewable, expandable to full LOD, forkable." Forkability
is tested by sibling a00-0fe88a0b-dbdfda. The LOD claim — that a chat has
compression levels an agent can navigate, starting coarse and drilling into
detail only where needed — is the untested third property.

**Operational claim:** Given a derivation chat from which three representations
are available (3-line summary, key-events bullet list, verbatim transcript), an
agent that starts with the summary and requests detail on demand reaches the
correct answer to a structural question about the chat in fewer total tool
calls than an agent given either (a) the full verbatim transcript upfront, or
(b) a single static summary only.

Three arms:
1. **Full verbatim upfront** — baseline (mirrors a00-711c2d0f's chat arm).
2. **Single static summary only** — baseline (mirrors a00-711c2d0f's briefing
   arm, plus controls for length confound).
3. **Graduated LOD** — agent receives the 3-line summary first, then can
   request key events (tool call), then request verbatim sections (tool call
   scoped to a time range or event). The agent navigates depth, not breadth.

### What separates this from sibling a00-711c2d0f-15bc43 (chat vs briefing)

That hypothesis tests one-shot: here is your context, go. This one tests
*interactive depth control*: the agent chooses how much detail to reveal.
The binary comparison (full chat vs summary) is a subset of arm 1 vs arm 2;
arm 3 is the novel condition — graduated access, not one-shot allocation.

### What separates this from sibling a01-78cdb163-be277d (key-values vs raw)

That hypothesis tests format replacement (structured assertions instead of
prose). This one tests *progressive disclosure* within a single format — the
summary, key events and verbatim sections are all prose, just at different
granularities. The question is whether the agent benefits from *choosing*
the granularity at each step rather than having it chosen for it.

### What would prove it

- Arm 3 (graduated LOD) shows a statistically significant reduction in tool
  calls to correct answer compared to both Arm 1 and Arm 2, across N ≥ 15
  trials per arm.
- Arm 3 agents request detail on fewer than half of the available sections
  on average — they do not expand everything, confirming that graduated access
  lets them skip irrelevant detail.
- The effect holds across question types: factual lookup ("what node was
  created?"), structural ("which alternative was rejected?"), and causal
  ("why was X chosen over Y?").
- Summary → key-events → verbatim ordering is the right hierarchy: agents
  expand from coarse to fine, not the reverse.

### What would disprove it

- No significant difference between Arm 3 and Arm 1 — graduated access buys
  nothing over having the full chat; agents read the same amount regardless.
- Arm 3 is significantly *worse* than Arm 2 — the extra interaction cost of
  requesting detail outweighs any benefit of skipping irrelevant material.
  Agents are better off with a single summary and no ability to drill.
- Arm 3 agents request detail on >80% of available sections — they
  effectively decompress the whole chat, making graduated access a costly
  waste of turns compared to having it all upfront.
- The hierarchy is wrong: agents start at verbatim and request summaries,
  i.e. coarse-to-fine is the opposite of the natural need. The LOD model
  stores the wrong direction.
- Answer correctness in Arm 3 is lower — graduated access causes agents to
  miss information they would have seen in the full chat.

### Why this matters before anything is built

If graduated LOD works:
- The "expandable to full LOD" property in g10.1 is not just visual
  sugar — it is an operational protocol that reduces context overhead.
- The chat-attachment format should store *all three* representations
  (summary, key events, verbatim) rather than just raw transcripts.
- Agent injection should adopt a "summary-first, drill-on-demand" protocol
  rather than dumping raw chat into context.
- This interacts with a01-78cdb163: key-values might work *within* an LOD
  structure (key-values at the key-events level, prose at verbatim), or they
  might replace the key-events level entirely.

If graduated LOD does NOT work:
- The "expandable to full LOD" language in g10.1 is aspirational rendering
  language, not an operational requirement. Store the chat once (raw), render
  it once (how agents actually use it), and skip the multi-representation
  infrastructure.
- The hierarchy might be wrong — agents might need verbatim-first,
  summary-on-demand. That is still an LOD, just inverted.
- The interaction cost of requesting detail might be prohibitive in agentic
  settings, meaning LOD is a human-UI concept that does not translate to
  agent-agent communication.

### Relationship to existing siblings

| Sibling | Tests | LOD's relation |
|---|---|---|
| a00-160ca279-56d211 | Can structure be mechanically extracted? | LOD requires extraction to generate the key-events level. If extraction is impossible (zero-LLM), LOD's middle tier disappears — it becomes summary vs verbatim binary. |
| a00-711c2d0f-15bc43 | Full chat beats single summary? | LOD tests a *third* condition neither binary tests: graduated access. If full chat beats summary (a00-711c2d0f proved), LOD might still beat full chat because it is interactive. If summary beats full chat, LOD might beat both. |
| a01-53cbe2c4-dc9630 | Awareness flag reduces attribution errors? | Orthogonal. The flag should be present on all three arms (held constant) to isolate the LOD effect. |
| a00-0fe88a0b-dbdfda | Fork at decision points vs fresh start? | Orthogonal. LOD is about *reading* structure; fork is about *continuing from* a point. A fork could use LOD to locate the right decision point. |
| a01-78cdb163-be277d | Key-values beat raw chat? | LOD's key-events level might be key-values (structured) or bullet-point prose. If key-values beat prose at the mid-level, LOD should use key-values; if not, it should use prose. The two hypotheses constrain each other's format choices. |

### Failure modes to control for

- **Interaction cost confound:** Arm 3 requires extra tool calls for each
  depth request. If the number of tool calls is the DV (dependent variable),
  Arm 3 starts at a disadvantage because answering a question requires the
  base call plus detail requests. Control: measure wall-clock time as a
  secondary DV, or count *total tokens consumed* (including requests and
  responses) rather than tool calls.
- **Summary quality confound:** A badly written summary makes Arm 2 lose and
  Arm 3 inherit a bad starting point. Control: generate summaries by the
  same method (same model, same prompt) for consistency across arms.
- **Question-type confound:** Factual lookup questions may be easier in full
  chat (scan for the answer) while structural questions benefit from the
  summary. Vary question type and report per-type results.
- **Order confound:** If agents in Arm 3 always expand everything (the
  "completionist" pattern), they are effectively Arm 1 with extra tool calls.
  Pre-register a filter rule: exclude trials where the agent expands ≥80%
  of available sections from the primary analysis (but report them separately).
- **Model confound:** Some models may be better at selective attention in
  long contexts, making Arm 1 less costly for them. Test across two model
  families if possible.

### Suggested experimental design

1. Curate 10 derivation chats from the repo's session logs, each 50+ messages
   with at least one decision point.
2. For each chat, author three representations:
   - 3-line summary (what was done, what was decided, what remains)
   - Key events (5-10 bullet points of structurally significant moments)
   - Verbatim transcript (full tool-call log)
3. For each chat, create 3 questions (factual, structural, causal).
4. Run each question×chat combination across three arms:
   - Arm 1: Full verbatim upfront + question.
   - Arm 2: Single static summary + question.
   - Arm 3: 3-line summary first, agent can request key events (tool call),
     agent can request verbatim sections scoped to event ids (tool call).
5. Measure: tool calls to final answer, answer correctness (blinded judge),
   fraction of sections expanded.
6. N ≥ 15 per arm for statistical power.

## Agent Notes
Fifth hypothesis under g10.1 — tests the LOD (level-of-detail) rendering claim: graduated depth-on-demand (summary → key events → verbatim) beats both full-verbatim (a00-711c2d0f's chat arm) and single-summary (a00-711c2d0f's briefing arm). Three-arm design with interaction-cost, summary-quality, and question-type controls. Distinct from all 5 existing siblings: covers the 'expandable to full LOD' property in g10.1 that none test.

<!-- THOUGHT:BEGIN -->
Reviewed by parent a01-59cad5b1, iteration 1066. This version differs from the
kid's in form only, not in claim: the scaffold heading was emitted twice and
`cli.py done` left two `## Agent Notes` blocks whose texts disagreed in wording
while agreeing in substance. Both duplicates removed, the later notes kept.

The claim itself is accepted as written and stays at `pending`. It is the fifth
distinct hypothesis under goal:g10.1 and it does cover the one property of the
goal no sibling tests -- "expandable to full LOD" as an operational protocol
rather than a rendering flourish. Arm 3 is genuinely novel against
a00-711c2d0f-15bc43, whose two arms this node reuses as baselines rather than
re-deriving.

Not fixed, and left as a caveat for whoever runs it: the primary dependent
variable is tool calls, which structurally penalises Arm 3, since every depth
request is itself a tool call. The node names this confound and proposes total
tokens as a secondary measure -- an experiment under it should promote tokens to
primary or the design measures the interaction cost instead of the effect.
<!-- THOUGHT:END -->
