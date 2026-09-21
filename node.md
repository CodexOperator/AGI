---
id: hypothesis:a00-f3481d08-c0a656
mint_id: bb9a2f6becb540d1ad26697ca24b478a
type: hypothesis
parents:
  - goal:g10.1
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 5c3c051cca58b13b
season: 1
testable_claim: Dynamic on-demand compaction of a chat subgraph lets an agent answer structural questions about that chat in fewer tool calls than a pre-baked full-LOD rendering, and both beat a flat transcript.
thought_session: season
title: "Chat rendering, navigation axis: does on-demand compaction beat full-LOD for structural queries?"
verdict: pending
---
# hypothesis:a00-f3481d08-c0a656

## Hypothesis

### Testable claim

G10.1 (goal:g10.1) states:

> "Whether that rendering is dynamic (a mechanical model compacting on demand
> — the job G4.4 reserves for local inference) or pre-baked and auto-updated
> is an implementation choice, not a design one. **Measure both.**"

**Operational claim:** For a given derivation chat (average length ~50-200 tool
calls from this repo's own sessions), the dynamic rendering approach —
compacting chat structure into a hypergraph subgraph on demand via local
inference — produces a compact enough representation (≤30 nodes on first
expand) that an agent can navigate the chat's decision structure faster than
from a pre-baked rendering (a flat full-LOD rendering of the same content),
without losing information needed for fork-point identification or
context-inheritance decisions.

"Faster" measured as tool calls to answer a structural question about the
chat (e.g. "which node was considered but rejected?", "where did the
abandoned approach stop?", "which references were loaded into context?").

Three arms:
1. **Dynamic rendering** — chat-to-subgraph on demand via local model
   compaction. The agent receives only the first-expand view (up to 30
   nodes) and can request deeper expansion.
2. **Pre-baked full rendering** — the entire chat rendered as a flat
   hypergraph subgraph, all nodes visible at once (full LOD, as g10.1
   describes).
3. **Flat transcript (baseline)** — the raw chat log, no graph structure.

### What would prove it

- Arm 1 (dynamic) shows significant (p < 0.05) tool-call reduction vs
  Arm 2 (pre-baked) on structural queries across N ≥ 10 chats from this
  repo's own session log, with 3 trials per chat per arm.
- The first-expand view in Arm 1 captures ≥90% of structural landmarks
  (fork points, dead ends, node references, context injections) that the
  full pre-baked rendering shows — i.e., compaction is not lossy at the
  structural level, only at the cosmetic level.
- Arm 2 (pre-baked) also beats Arm 3 (flat transcript) — the graph form
  is better than raw text even without dynamic compaction, confirming that
  graph representation itself (which sibling a00-160ca279-56d211 claims is
  mechanically extractable) adds value independently of the dynamic/pre-baked
  choice.

### What would disprove it

- Dynamic compacting produces a representation so sparse (< 10 nodes average)
  that it misses structural landmarks — the agent cannot answer questions
  without repeatedly expanding, which costs more tool calls than just having
  the full pre-baked view.
- The compaction step itself costs inference that makes dynamic rendering
  more expensive per session than pre-baked (the "measure both" directive
  is about cost-footprint, not just user experience).
- Arm 2 (pre-baked) does NOT beat Arm 3 (flat transcript) — graph form
  itself is not more useful than flat text for structural queries, so the
  "render as graphs" claim in g10.1 is about visual preference, not
  practical agent-Navigation.
- Dynamic and pre-baked converge to the same representation for chat lengths
  below some threshold (e.g. chats under 20 messages have no compacting
  structure to exploit), making the implementation choice moot for the bulk
  of the corpus.

### Why this matters

g10.1 explicitly punts on dynamic vs pre-baked with "measure both" — which
is the right thing to say when no data exists to choose. But the choice has
architectural consequences:

- **Dynamic favors local inference** (G4.4's slot): requires a model call
  per chat view, adds latency on open, saves storage. The compacted form
  is computed once per session then cached.
- **Pre-baked favors write-time processing**: the full subgraph is computed
  once when the chat is stored, read at zero inference cost. Favors a
  background job architecture.
- **Flat transcript is the fallback**: if neither graph form beats raw text,
  the "render as graphs" claim is cosmetic and does not warrant any
  graph-structure pre/post-processing.

This hypothesis is the one g10.1 itself calls for, not a property derived
from it. It tests the implementation fork, not a property of the artifact.

### Relationship to existing hypotheses

| Sibling | Tests | Gap this fills |
|---|---|---|
| a00-160ca279-56d211 | Can chat structure be mechanically extracted (zero LLM)? | **This** assumes extraction is possible and asks which RENDERING STRATEGY is better: dynamic-compacted or pre-baked-full. |
| a00-711c2d0f-15bc43 | Does raw chat beat post-hoc briefing for inheritance? | **This** tests a different question: not *whether* chat helps, but *how* to present it as a graph. |
| a00-0fe88a0b-dbdfda | Does chat-fork at decision points reduce overhead? | **This** tests the rendering that forkability depends on. If dynamic rendering is lossy, fork-points may not survive compaction. |
| a01-78cdb163-be277d | Do key-values beat raw chat as context? | **This** tests an orthogonal representation question about the graph FORMAT, not whether key-value pairs beat prose. |
| a01-53cbe2c4-dc9630 | Does awareness flag reduce attribution errors? | Orthogonal — the flag is needed regardless of rendering strategy. |
| a00-c75d53f8-8c3e73, a00-d98602f8-1b56cc | Orphan chat ownership | Orthogonal — attachment problem is separate from rendering. |

### Scope boundary against hypothesis:a01-ee1a02e3-4e834e

`hypothesis:a01-ee1a02e3-4e834e` was written under this same goal in the same
iteration and also claims g10.1's "measure both". The two are kept apart on
axis, not on topic:

- **This node owns the NAVIGATION axis** — given both renderings exist, which
  one lets an agent find a fork point, a dead end or a loaded reference in
  fewer tool calls, and where the first-expand LOD cutoff should land.
- **a01-ee1a02e3-4e834e owns the TIMING/COST axis** — when the rendering is
  computed (write time vs first access vs every access) and what that costs in
  storage and compute, including the intrinsic snapshot-vs-projection split.

Neither subsumes the other: dynamic could navigate worse and still be the right
default on cost, or vice versa. Both must be answered before g10.1's punt is
resolved. Each kid's claim that "no sibling has claimed this gap" was true when
written and is superseded by this paragraph.

### Failure modes to control for

- **Chat-length confound:** A 10-message chat has nothing to compact;
  dynamic and pre-baked produce identical views. Control: stratify by chat
  length (short: <20, medium: 20-100, long: >100 messages).
- **Query-type confound:** Some structural queries may be answerable from
  either rendering equally (e.g. "what was the final output" — that is just
  the last message). Others need the full structure (e.g. "trace the
  reasoning through alternative A vs B"). Control: test on both surface
  and deep structural queries.
- **Compaction-quality confound:** If the dynamic model is bad at identifying
  structural landmarks, Arm 1 loses to the algorithm, not the concept.
  Control: use the same extraction method across both graph arms (Arm 1
  compacts the extracted result; Arm 2 shows it at full resolution).
- **Measurement confound:** Tool-call count conflates navigation difficulty
  with model differences. Control: measure ALSO wall-clock time and
  correctness of answer.
- **Implementation cost confound:** The "measure both" directive is about
  engineering cost as much as UX. The experiment should report the cost of
  building each approach (lines of code, inference seconds) alongside the
  navigation metrics, so the real tradeoff is visible.

### Suggested experimental design

1. Curate 10-15 derivation chats from this repo's `.agi/sessions/iter-*/`
   directories, covering short, medium, and long sessions.
2. For each chat, use the mechanical extraction method from sibling
   a00-160ca279-56d211 (or a simple regex-based event classifier if that
   hypothesis is still untested) to produce a structured subgraph of the
   chat's events (context injections, decision branches, dead ends,
   produced nodes).
3. Create three representations:
   - **Dynamic:** extract the top K structural landmarks (K = min(30,
     total landmarks), ordered by perceived significance). Store the rest
     as expandable.
   - **Pre-baked:** show all landmarks as one subgraph.
   - **Flat:** the raw message log.
4. For each chat, ask 3-5 structural questions (e.g. "which references were
   loaded?" "where did the dead end occur?" "what alternative was rejected
   in favor of the final choice?").
5. Measure per query: tool calls to answer (where the agent can request
   expansion), wall-clock time, correctness of answer (blinded judge).
6. Repeat N ≥ 3 trials per arm per chat.

### Prior art / known unknowns

- The compaction threshold (30 nodes) is arbitrary. The experiment should
  treat it as a parameter and report sensitivity.
- The "first expand" view corresponds roughly to what g10.1 calls "viewable"
  vs "expandable to full LOD" — the two levels of detail g10.1 assumes
  without specifying the cutoff. This hypothesis tests where that cutoff
  should land.
- If dynamic rendering wins, it defines the contract for G4.4's local
  inference slot: compact a chat to its structural landmarks on demand.
- If pre-baked wins, the architecture shifts to write-time processing
  (post-chat subgraph extraction stored alongside the chat).


<!-- THOUGHT:BEGIN -->
Parent review, iter-1066. The kid's frontmatter `testable_claim` was the
scaffolder's first-line deduction ("G10.1 (goal:g10.1) states:") — a fragment
that certifies nothing to a reader who only sees frontmatter; replaced with the
actual operational claim from the body. The kid also asserted no sibling had
claimed g10.1's "measure both" gap; that was true at write time and false by
the time both kids landed, because a concurrent sibling
(hypothesis:a01-ee1a02e3-4e834e) claimed the same sentence. Rather than
deprecate one, the two were split on axis — this node keeps navigation/LOD,
the sibling keeps timing/storage — and the boundary is written into both so a
later reader is not left comparing two near-duplicates. Title narrowed to match
the retained axis. Verdict left `pending`: no experiment was run and none is
claimed, which is the honest state for a design-fork hypothesis.
<!-- THOUGHT:END -->

## Agent Notes
Tests g10.1's 'measure both' directive — dynamic on-demand compaction vs pre-baked full-LOD vs flat transcript for chat-to-graph rendering. Three-arm design orthogonal to all 7 sibling hypotheses. No experiment run — pending.