---
id: hypothesis:a01-78cdb163-be277d
mint_id: f6dddf3f2b824824ab4aec84e9bbbebf
type: hypothesis
parents:
  - goal:g10.1
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 18973a52e59c8655
season: 1
testable_claim: G10.1 (goal:g10.1) asserts that a continuing agent inherits a chat and "inherits the pre-computed key-values wholesale, arriving with the reasoning already in context rather than reconstructed." This implies that the *structured* content of a derivation chat — the decisions made, alternatives rejected, tradeoffs acknowledged, nodes referenced — is more valuable than its *unstructured* prose. But the falsifier in g10.1 tests only whole-chat vs briefing; it does not isolate whether the key-values carry the signal.
thought_session: season
title: "A01: Pre-computed key-values from derivation chats reduce agent overhead more than raw chats"
verdict: pending
---
# hypothesis:a01-78cdb163-be277d

## Hypothesis

### Testable claim

G10.1 (goal:g10.1) asserts that a continuing agent inherits a chat and
"inherits the pre-computed key-values wholesale, arriving with the reasoning
already in context rather than reconstructed." This implies that the
*structured* content of a derivation chat — the decisions made, alternatives
rejected, tradeoffs acknowledged, nodes referenced — is more valuable than
its *unstructured* prose. But the falsifier in g10.1 tests only whole-chat vs
briefing; it does not isolate whether the key-values carry the signal.

**Operational claim:** Given N derivation chats with known rationale, an agent
conditioned on extracted key-values only (structured assertions formatted as
key-value pairs or YAML, no raw chat prose) will reach its first useful action
in fewer tool calls than an agent conditioned on the verbatim raw chat, and
will make fewer errors of reconstruction (omitting considerations the chat
established).

Three arms:
1. **Raw chat only** — verbatim transcript + awareness flag (baseline, mirroring
the minimum viable from sibling a01-53cbe2c4-dc9630).
2. **Key-values only** — structured extraction of decisions, rejected
alternatives, referenced nodes, tradeoffs, and open questions. No raw prose.
3. **Both** — key-values injected as preamble, raw chat available as appendix.

### What would prove it

- Arm 2 (key-values only) shows statistically significant (p < 0.05) reduction
in tool calls to first useful action compared to Arm 1 (raw chat), across at
least N ≥ 15 trials per arm.
- Arm 2 produces fewer information-reconstruction errors: the agent does not
re-decide matters already settled in the chat, does not re-traverse alternatives
already rejected, and does not contradict established tradeoffs. Measured by
automated comparison of the agent's stated reasoning against the chat's
established key-values.
- Arm 3 (both) is not significantly worse than Arm 2 (having the raw chat
available does not degrade the key-values signal, even if it adds tokens).

### What would disprove it

- No significant difference between Arm 1 and Arm 2 — key-values carry the
same information as raw chat, just re-formatted. The structured form adds no
benefit over the prose.
- Arm 2 is significantly *worse* than Arm 1 — key-values are lossy; the
structured extraction discards context that prose preserves.
- Arm 3 is significantly worse than Arm 2 — raw chat prose distracts from or
contradicts the key-values, so having both harms the agent.
- The key-values themselves are consistently wrong or misleading, so the
extraction method injects error proportional to its mistakes.

### Why this matters

If key-values beat raw chat, then:
- The attachment format for chats should produce *extracted key-values* as
primary context, with raw chat stored as fallback appendix, not the other way
around.
- The pre-computation step (producing key-values from a finished chat) becomes
a mandatory post-processing stage, not optional.
- Agent injection is cheaper: key-values are smaller than raw chat, keeping
more context room for the task itself.
- This directly validates g10.1's claim that "the reasoning [is] already in
context rather than reconstructed" — and shows *how* to achieve that: via
structured extraction, not wholesale verbatim injection.

If raw chat beats key-values, then:
- The "pre-computed key-values" claim in g10.1 is architectural optimism.
- Chats are better kept raw; the structure is in the prose, not extractable
as independent assertions.
- The correct injection strategy is the whole-chat approach sibling
a00-711c2d0f-15bc43 tests against briefings, with no intermediate extraction
layer.

### Relationship to existing hypotheses

| Sibling | Tests | Gap this fills |
|---|---|---|
| a00-160ca279-56d211 | Can chat structure be mechanically extracted (zero-LLM)? | **This** assumes extraction is possible and asks whether the *extracted form* is better context than the raw form. |
| a00-711c2d0f-15bc43 | Does raw chat beat post-hoc briefing? | **This** compares raw chat vs its own structured extraction (different question: extraction vs prose, not chat vs summary). |
| a01-53cbe2c4-dc9630 | Does the awareness flag reduce attribution errors? | **This** is orthogonal — the flag belongs on whichever context format wins, and works alongside key-values. |

### Failure modes to control for

- **Extraction quality confound:** The hypothesis is only as strong as the
extraction method used. A bad extractor produces bad key-values and Arm 2
loses by method quality, not by principle. Control: use a high-quality
extractor (model-based or human-curated) for the experiment, and run a
separate sub-experiment correlating extraction accuracy with the gap between
Arm 1 and Arm 2.
- **Token-count confound:** Key-values are shorter than raw chat. If Arm 2
wins, is it because key-values are better signal, or because the agent has
more remaining context window for the task? Control: Pad Arm 2's key-values
with neutral filler text to match Arm 1's token count.
- **Task confound:** Some task types benefit more from structured data (e.g.
reviewing a past decision) and some from prose narrative (e.g. tracing why a
specific choice was made). Control by varying task type across at least two
categories: "verify a past decision" and "continue incomplete work."
- **Model confound:** Some models may handle structured data better than
others. Test across at least two model families.
- **Circularity with a00-160ca279-56d211:** If mechanical extraction
(no LLM calls) cannot produce adequate key-values, this hypothesis falls back
to requiring inference per chat for extraction — which changes the cost/benefit
calculation. Flag this dependency explicitly.


## Agent Notes
Key-values from derivation chats beat raw chats for continuing-agent context — tests g10.1 pre-computed key-values claim. Three-arm design: raw chat vs extracted key-values vs both. Distinct from siblings a00-160ca279-56d211 (mechanical extractability), a00-711c2d0f-15bc43 (chat vs briefing), a01-53cbe2c4-dc9630 (awareness flag). Controlled for extraction quality, token count, task type, and model confounds.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-9afb0e7e, iter 1024). Accepted unchanged. Parents
resolves to goal:g10.1; verdict `pending` with confidence 0.0 is the
honest state for an untested claim; `testable_claim` present. The claim is
distinct from the iter-1010 siblings: it isolates whether g10.1's
"pre-computed key-values" carry the signal the whole-chat-vs-briefing
falsifier (a00-711c2d0f) does not test — extraction-as-context vs prose,
not chat vs summary. Its strongest control is the token-count padding
(Arm 2 padded to match Arm 1), which stops "shorter wins" being misread as
"structured wins." No body edits needed; the single `## Agent Notes` is the
harness render, so there is no duplicate to remove unlike sibling
a00-0fe88a0b-dbdfda.
Data-loss note: this node's original file was deleted from disk mid-iteration
by an external tree clean (a concurrent director wave / iteration-1025 setup
swept untracked files); no grid ref existed, so it was unrecoverable from the
grid. This version is restored by the parent from the verbatim content it read
before the deletion, with this review THOUGHT appended.
<!-- THOUGHT:END -->