---
id: exp:a00-derivation-chat-event-density-r1
mint_id: 7a2e4c9d1b6f4a3e9c0d5f8b3a1e6c72
type: experiment
parents:
  - hypothesis:a00-160ca279-56d211
next_edges: []
confidence: 0.55
edited_by: season.py
evidence_runs: 1
season: 1
tags:
  - g10.1
  - derivation-chats
testable_claim: A zero-model-call parser over structured JSONL session logs (message.role, content[].type) recovers per-chat event counts (tool calls, tool errors, thinking blocks) that are not sparse (≫2/chat), addressing one of the hypothesis's two named disproof conditions.
thought_session: season
title: Zero-LLM field extraction on 8 raw derivation-chat JSONL logs
verdict: inconclusive_lean_proved:55
---
# exp:a00-derivation-chat-event-density-r1

## What ran

8 raw derivation-chat logs (`sessions/*.jsonl`, pi-harness format, a
different project's autoresearch run — not this repo's own chats, sampled
because they were on-disk and structurally identical: `message.role` in
{`user`,`assistant`,`toolResult`}, `content[].type` in {`text`,`thinking`,
`toolCall`}). A ~30-line Python script, **zero model calls**, walked each
line as JSON and counted `toolCall` content blocks, `toolResult` messages
(with `isError`), and `thinking` blocks per chat. No regex needed — the
harness already emits structured fields, which is stronger than the
hypothesis required (it only demanded regex/pattern matching).

## Output

| file (truncated) | toolcalls | results | errors | thinking |
|---|---|---|---|---|
| 06-24-27 | 10 | 10 | 1 | 8 |
| 06-28-50 | 8 | 8 | 0 | 8 |
| 06-34-54 | 33 | 33 | 3 | 30 |
| 06-43-59 | 9 | 9 | 0 | 8 |
| 06-49-28 | 73 | 73 | 3 | 70 |
| 06-58-33 | 62 | 62 | 2 | 59 |
| 07-07-38 | 24 | 24 | 2 | 22 |
| 07-14-57 | 12 | 12 | 1 | 10 |

A first pass that tried to match node-id references (`idea:`, `goal:`, ...)
via regex against `content` found 0 in all 8 files — expected, since this
sample project doesn't use this repo's node-id scheme, not a defect in the
extractor.

## Reading against the hypothesis

**Addresses one disproof condition directly:** "the extracted subgraph has
so few edges (≤2 per chat on average) that it adds nothing" — false here.
Every chat produced 8-73 mechanically-recoverable events, an order of
magnitude above the ≤2 floor. Tool-error events (6/8 chats had ≥1) are a
plausible zero-cost proxy for "dead-end attempt" without needing to inspect
tool output content.

**Does not address the other two disproof conditions:**
- Whether >50% of structurally significant events are *implicit* (a
  "decision branch" the agent took inside a `thinking` block with no tool
  call) is still untested — this run counted thinking blocks but did not
  classify their content, which is exactly the classification the
  hypothesis's own "what would prove it" section requires validating
  against a 20-chat hand-annotated gold set.
- No cross-check against a different agent harness's log format (the
  circularity failure mode the hypothesis pre-registered) — all 8 samples
  are one harness (pi).

## Verdict lean

Not proved: the gold-set classification step (event class ≥90% recovery)
is the actual bar the hypothesis sets, and this run is a pilot on raw
counts, not classified events. But the sparsity disproof condition is
now concretely ruled out on this sample, which is evidence in the
hypothesis's favor, not neutral. Lean proved, low-moderate confidence.

## Agent Notes
Zero-LLM field parse of 8 raw pi-harness session JSONL logs: 8-73 tool-call/thinking events per chat, ruling out the sparsity disproof condition on this sample; gold-set event-classification (decision-branch vs routine thinking) still untested.