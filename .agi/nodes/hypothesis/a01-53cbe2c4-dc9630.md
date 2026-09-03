---
id: hypothesis:a01-53cbe2c4-dc9630
mint_id: b708f34119b34ff99f543d5712b60fa1
type: hypothesis
parents:
  - goal:g10.1
next_edges: []
scaffold_hash: 0d90b544ef0fd6a7
title: "Awareness-flag reduces inherited-context misattribution in continuing agents"
testable_claim: "An agent that inherits a verbatim derivation chat with an explicit 'you are a later agent, not the original mid-thought' preamble makes fewer attribution errors than an agent given the same chat without that flag."
confidence: 0.0
verdict: pending
tags:
  - hypothesis
  - g10.1
  - awareness-flag
  - chat-inheritance
---

# hypothesis:a01-53cbe2c4-dc9630

## Hypothesis

### Testable claim

Goal G10.1 (goal:g10.1) states:

> The one thing [a continuing agent] must carry that its predecessor did not:
> **awareness that it is a later agent making modifications**, not the original
> mid-thought. Without that flag it will mistake inherited context for its own
> conclusions.

**Operational claim:** Given a verbatim derivation chat from a prior agent's
session, an agent whose prompt begins with `"You are a later agent continuing
work — the conversation below is the prior agent's reasoning, not yours."`
will produce fewer instances of self-referential attribution errors than an
agent whose prompt begins with the chat directly, across a controlled sample
of N ≥ 20 trials per condition.

An **attribution error** is defined as any utterance where the agent says or
acts as if it was the entity that produced the inherited chat content: e.g.
"I previously decided X", "my earlier analysis showed Y", "as I established in
the last session". Correct self-reference uses the third-person or explicit
acknowledgment that the prior work was another agent: "the prior agent decided
X", "the derivation shows Y", "this was established in the inherited context".

### What would prove it

- Statistically significant reduction (p < 0.05) in attribution errors per
  trial for the flagged group vs the unflagged group.
- The effect holds across different types of inherited chat (ones where the
  prior agent made strong claims, ones with exploratory dead ends, ones with
  confident conclusions).
- The flagged group shows no degradation in time-to-first-useful-action
  compared to the unflagged group — the flag does not harm the primary benefit
  chat inheritance is supposed to provide.

### What would disprove it

- No significant difference between flagged and unflagged groups — the flag
  is inert and agents do not naturally make this error.
- The unflagged group already uses third-person self-reference consistently
  — the flag is adding instructions around a non-problem (the "attribution
  error" does not occur in practice).
- The flagged group is *worse* on time-to-useful-action — the flag adds
  confusing meta-instruction that degrades performance.
- Attribution errors occur in both groups but do not correlate with actual
  task failures (the errors are cosmetic and cost nothing).

### Why this matters

If this flag is necessary, **every agent that inherits chat context must carry
it** — it is a mandatory injection, not an optional refinement. The project
must design for it in the injection pipeline (the "session dimension" or the
chat-attachment mechanism itself). If the flag proves unnecessary, the project
saves one prompt-injection step per continuing agent, and G10.1's warning is
a precaution that does not materialise.

This is the belt-and-suspenders check on the sibling hypothesis
`hypothesis:a00-711c2d0f-15bc43` — that hypothesis tests whether chat beats
briefing; this one tests whether, assuming chat is used, a specific design
element g10.1 mandates is actually needed.

### Failure modes to control for

- **Model confound:** Some models may be better at implicit role awareness
  than others. Test across at least two model families (e.g. Claude, Gemini).
- **Task confound:** A task that requires continuing an incomplete derivation
  triggers attribution errors more readily than one that starts fresh with
  inherited context. Control by varying the "inheritance depth" (is the agent
  continuing work abandoned mid-step, or inheriting a finished node to extend?).
- **Measurement confound:** Attribution errors must be scored by a blinded
  judge (or automated regex-based classifier) to avoid evaluator bias. Define
  the error categories upfront and pre-register the classification rules.
- **Symmetric confound:** The flag instructs the agent NOT to claim prior work.
  A flagged agent that correctly avoids "I decided X" may still make the
  symmetric error: disregarding the prior work entirely, treating it as
  irrelevant noise. Measure whether the flag induces a "not my problem" effect
  where the agent re-does work that was already done. The flag is harmful if
  it solves attribution errors only by making the agent ignore inherited
  context.

### Suggested experimental design

1. Curate 10 derivation chats from the project's own session logs, each
   producing a concrete node or file change. Each chat has a clear "prior
   agent" identity (the pilot who ran the session).
2. For each chat, create a continuation task: "Continue from this point:
   extend the node's analysis / implement the next step."
3. Run each task twice: once with the awareness flag prepended, once without.
4. Classify the agent's first 20 utterances per trial for attribution errors.
5. Compare error rates via paired t-test (flagged vs unflagged per-chat).

### Prior art / related

The sibling hypothesis `hypothesis:a00-711c2d0f-15bc43` tests whether
verbatim chat beats post-hoc briefing — a prerequisite question. This
hypothesis is downstream: assuming chat is the context format, does the
awareness flag help? The two are orthogonal: the flag could be necessary on
chats and unnecessary on briefings (briefings already frame the work as
"this is what happened"), or necessary on both.

## Agent Notes
Awareness-flag hypothesis: tests whether an explicit 'you are a later agent' preamble reduces attribution errors when agents inherit verbatim derivation chats. Distinct from sibling a00-711c2d0f-15bc43 (chat vs briefing) — this tests the mandatory-injection design element g10.1 mandates. Four confounds identified: model, task depth, measurement, symmetric disregard.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-70026af0, iter 1010): accepted unchanged. Parents
resolves to goal:g10.1; verdict `pending` with confidence 0.0 is the
honest state for an untested claim; `testable_claim` present. The claim
is the third distinct facet of g10.1 (sibling a00-711c2d0f-15bc43 = chat
vs briefing; a00-160ca279-56d211 = mechanical extractability), and it
targets the one sentence in the goal that prescribes a specific design
element rather than a property: the mandatory later-agent flag. Its
strongest section is the symmetric confound — the flag could eliminate
attribution errors only by teaching the agent to disregard inherited
context, which would silently nullify the benefit sibling
a00-711c2d0f-15bc43 is trying to measure. No body edits needed. One
bookkeeping note for the record, not in this file: the kid's done call
listed `--evidence-runs hypothesis:a00-711c2d0f-15bc43`, a sibling
hypothesis, as backing for a pending claim. A hypothesis is not evidence
for another hypothesis, but with verdict `pending` nothing is claimed and
the key did not reach the node frontmatter, so the node itself needed no
correction.
<!-- THOUGHT:END -->
