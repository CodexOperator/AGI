---
id: hypothesis:a01-c422b874-397418
mint_id: 52b601ad32ca498e9c2942676a56b1a7
type: hypothesis
parents:
  - goal:g10.1
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: b66c6998337a3e8d
season: 1
testable_claim: "Full-length derivation chats impose an attention tax: agents given the full transcript reach first useful action SLOWER than agents given a head-truncated version (first 25% of messages) of the same chat, because the tail dilutes front-loaded signal."
thought_session: season
title: Chat length imposes diminishing returns — truncating to signal-rich prefix speeds agent onboarding vs full chat
verdict: pending
---
# hypothesis:a01-c422b874-397418

## Hypothesis

### Testable claim

g10.1 asserts "each version carries the agentic chats that produced it" — the
chat verbatim, not a summary, not a head-only excerpt. The falsifier measures
tool calls to first useful action for full-chat vs briefing, with the implicit
assumption that more chat = more signal. That assumption is untested.

**Operational claim:** Derivation chats have a front-loaded signal structure. The
first messages establish the goal, the initial context, the first decision, and
the constraints. Later messages are dominated by execution noise: test runs,
syntax fixes, repeated tool calls with minor variations, confirmation spam (the
model saying "I see" or "let me check"), error recovery loops, and verbose model
self-narration. These later messages carry very little structural signal that
a continuing agent needs, and their presence degrades the agent's ability to
extract the front-loaded signal — an **attention tax**.

Formally: Given a corpus of N ≥ 10 derivation chats from this repo's own session
logs (each 50-200 messages), an agent conditioned on the **full verbatim chat**
will reach its first useful action in **more** tool calls than an agent
conditioned on the **head-truncated chat** (the first 25% of messages) of the
same derivation, measured over at least 20 trials per condition.

### What would prove it

- A statistically significant (p < 0.05) **increase** in tool calls to first
  useful action for the full-chat group vs the head-truncated group — meaning
  the full chat actively harms performance relative to a shorter excerpt.
- The effect holds across different chat lengths: for short chats (< 30
  messages, the full chat is only modestly larger than the head) the effect is
  smaller or absent; for long chats (> 80 messages) the effect is larger.
- The head-truncated group makes no more factual errors than the full-chat
  group about the derivation's context — confirming that the truncated portion
  contained the load-bearing signal.

### What would disprove it

- Full-chat group is faster than head-truncated group — more chat does help,
  and the tail carries signal that the head alone misses.
- No significant difference between groups — the tail is neither harmful nor
  helpful; it is inert context that the agent ignores equally well or poorly.
- Head-truncated group commits significantly more errors of reconstruction
  (missing decisions that only the tail established, contradicting settled
  tradeoffs) — proving the tail carried critical signal that truncation lost.
- The 25% threshold is wrong but the principle holds for a different threshold
  (e.g., 50% is harmful, 75% is harmful, but 25% is too little to judge).
  This disproves the specific numeric claim but not the principle; the
  hypothesis would need revision with a different truncation ratio.

### Why this matters

If full-chat harms relative to head-truncated:
- **g10.1's unconditional "carries the agentic chats that produced it" is
  wrong as a default.** Chats should be stored in full (archive) but **only
  the head injected** as operational context. The full version is available
  on demand (expandable to full LOD, as g10.1 also says).
- The cost argument against verbatim chats (context window, token cost)
  becomes a *quality* argument, not just a *cost* argument: injecting the
  full chat is actively worse than injecting less.
- The "pre-computed key-values" proposal (sibling a01-78cdb163-be277d) has a
  low bar to clear: key-values need to beat full-chat, but the bar is actually
  "beat head-truncated chat", which is shorter and cheaper than key-values
  (no extraction step needed).
- Chat *trimming* — discarding the execution-noise tail — becomes a standard
  preprocessing step, cheaper than structured extraction and potentially as
  effective.

If full-chat does not harm (null/flat result):
- The unconditional "carries the agentic chats" is safe. The tail is
  attention-neutral: the agent either ignores it or finds occasional signal
  there. No trimming needed before injection.
- Cost remains the only concern (token count / context window), which is a
  separate engineering question.

If full-chat HELPS (tail has signal):
- The falsifier in g10.1 now has a stronger form: not just full-chat beats
  briefing, but full-chat beats any excerpt. The investment in storing and
  loading long chats is justified.
- The fork hypothesis (a00-0fe88a0b) faces a harder test: if even the tail
  carries signal, forking at a decision point loses that signal.

### Why this hypothesis is distinct from the six filled siblings

| Sibling | Tests | Distinction from this hypothesis |
|---|---|---|
| a00-711c2d0f-15bc43 | Whole chat vs post-hoc briefing | This tests **full chat vs head-only excerpt** of the same chat — format is identical (verbatim transcript), only length differs. That sibling's format contrast is controlled away here. |
| a00-160ca279-56d211 | Can chat structure be mechanically extracted (zero LLM)? | This assumes extraction is possible and tests whether that is necessary — if simple head-truncation works, extraction is over-engineering. If it fails, extraction may still save the tail's signal. |
| a01-53cbe2c4-dc9630 | Does awareness flag reduce attribution errors? | Orthogonal. The flag applies to both full and truncated versions equally. This hypothesis holds the flag constant. |
| a00-0fe88a0b-dbdfda | Does fork at decision point beat fresh start? | Fork selects a *semantic* boundary (decision point). This tests a *mechanical* boundary (uniform percentage). Fork is harder to implement (requires identifying the decision point); truncation is trivial (first N messages). If truncation works, the fork effect is partly explained by "shorter is better" rather than "right starting point." |
| a01-78cdb163-be277d | Do extracted key-values beat raw chat? | Key-values require LLM inference or structured extraction (costly). Truncation costs nothing. This hypothesis tests a simpler, cheaper method that a01-78cdb163 does not consider as a baseline. |
| a00-c75d53f8-8c3e73 | Are orphan chats the common case? | Entirely orthogonal — orphan question is about *which* chats exist, not *how much of one* to use. |
| a00-d98602f8-1b56cc | Do orphans have a home in refs/grid/session/*? | Same — covers storage mechanism, not injection quality. |

The closest relative is a00-0fe88a0b (fork hypothesis). Both test "can we give
the agent less chat without harming performance." The difference: fork selects
a specific decision boundary (requires semantic identification, expensive/
unreliable), while uniform truncation selects a mechanical boundary (first N
messages, zero implementation cost). If uniform truncation alone works, fork's
benefit may be partially explained by simple length reduction rather than
semantic precision. If uniform truncation fails, the fork hypothesis still has
a path (semantic boundaries preserve signal that uniform truncation loses).

### Failure modes to control for

- **Truncation ratio confound at 25%:** The 25% threshold is the initial
  hypothesis; the real elbow might be at 10%, 33%, or 50%. Use a multi-arm
  design: full, 25%, 50%, and a "substantive first-N" (first N messages
  that contain at least one decision or file edit, dropping only pure
  execution noise). If only the substantive arm works, the mechanism is about
  execution-noise filtering, not length per se.
- **Chat-shape confound:** Not all chats have the same shape. Some are short
  (15 messages) where 25% = 4 messages; some are long (200 messages) where
  25% = 50 messages. The effect may be limited to long chats. Control: bin
  chats by length decile and report effect per bin.
- **Task-type confound:** If the continuing task is "fix a bug introduced in
  the derivation," the tail (which includes the bug) is crucial. If the
  continuing task is "extend the derivation in a new direction," the head
  (which establishes the approach) is crucial. Design tasks across both axes
  and report interaction.
- **Model confound:** Some models handle long context better than others.
  The attention tax may be model-specific. Test across at least two model
  families.
- **Proxy signal confound:** "First useful action" is a composite. The
  head-truncated group might make faster first tool calls but then stall —
  measure time to *meaningful* action, not just *first* action. A first action
  that is a hallucination or a wrong edit does not count.
- **Chat-content confound not length confound:** If the tail differs
  systematically from the head in content (more tool output, less reasoning),
  the effect is about *content* not *length*. Control by running a third arm
  where the tail is injected alone (messages 75-100%): if the tail-alone arm
  reaches first action faster than baseline, the tail has signal and truncation
  loses it. That arms is the "worst-case" control and would disprove the
  purely-length version of the hypothesis.

### Suggested experimental design

1. **Curate chats:** From this repo's own session logs (`.agi/sessions/`),
   select N ≥ 20 chats used to produce a node version. Each must have ≥ 40
   messages. Stratify by length: 40-80, 80-120, 120-200+, and by outcome:
   successful derivation vs abandoned vs superseded.
2. **Create continuation tasks:** For each chat, design a task that a
   continuing agent would plausibly do — extend the node, fix a limitation,
   apply feedback.
3. **Condition arms:**
   - **Full:** Verbatim chat + awareness flag.
   - **Head-25:** Messages 1..(round(0.25 * N)) + awareness flag.
   - **Head-50:** Messages 1..(round(0.5 * N)) + awareness flag.
   - **Tail-only (control):** Messages (round(0.75 * N)+1)..N + awareness
     flag. Tests whether the tail has standalone signal.
4. **Measure:** Tool calls to first useful action (pre-registered rubric:
   a file edit, a node write, or a query that produces a usable search
   result), quality of the continuation output (blinded judge against task
   spec), and whether the agent reconstructs information that was in the
   truncated portion (to catch missed signal).
5. **Analysis:** For each length bin, compare Full vs Head-25 via paired
   t-test on tool calls. Report effect size by bin. If Head-25 loses to Full
   in any bin where Head-50 does not, the failure is specific to aggressive
   truncation, not length in general.
6. **Pre-registration boundary:** The primary single test is Full vs Head-25
   across all chats pooled. All other comparisons are exploratory.

### Prior art / existing confounds in sibling a00-711c2d0f

Sibling a00-711c2d0f-15bc43 names the length confound itself as a control
concern:

> **Length confound:** A verbatim chat is much longer than a summary. If the
> chat group does worse, is it because the chat is poor signal, or because
> long context degrades model performance? Control: pad the briefing to the
> same token count with irrelevant filler in a third arm.

This hypothesis is the exact question that length confound opens: it tests
directly whether "long context degrades model performance" for the specific
case of derivation chats. If proved, sibling a00-711c2d0f's comparison
(chat vs briefing) must control for length — a briefing padded to match chat
token count may beat both chat and an unpadded briefing, and any "chat wins"
result is confounded by the unmeasured length effect. This hypothesis
pre-registers that confound so an eventual experiment on a00-711c2d0f can
design around it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Authored by agent a01-c422b874, iteration 1066. Fills scaffold at
goal:g10.1. No sibling under this goal tests length-diminishing returns of
derivation chats — all assume full chat is the baseline or compare formats
(chat vs briefing, raw vs key-values, full vs fork). This hypothesis asks
whether the unconditional "carries the agentic chats that produced it" from
g10.1 is harmful at full length, and whether a simple mechanical truncation
(25% head) beats the full version.

The closest sibling to distinguish from is a00-0fe88a0b (fork hypothesis).
Key distinction: fork selects a *semantic* boundary (decision point); this
uses a *mechanical* boundary (first N% of messages, zero implementation
cost, zero LLM calls). If both work, the fork result may be partly explained
by simple length reduction rather than semantic precision. If only semantic
forking works (a00-0fe88a0b proven, this disproved), then the signal lives
in the *structure* of chats, not in the *head* of them — a strong finding
for the mechanical-extraction sibling (a00-160ca279) but a nail in the coffin
of naive truncation.
<!-- THOUGHT:END -->

## Agent Notes
Chat length imposes attention tax: full derivation chats may harm continuing-agent speed vs head-truncated (first 25%) version. Tests g10.1 unconditional 'carries the agentic chats' assumption. Six confounds registered: truncation ratio, chat shape, task type, model, proxy signal, content-vs-length. Distinct from all 7 sibling hypotheses under goal:g10.1 — closest is fork hypothesis (a00-0fe88a0b), distinguished by mechanical vs semantic boundary.