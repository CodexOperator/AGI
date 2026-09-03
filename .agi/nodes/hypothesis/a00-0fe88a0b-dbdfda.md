---
id: hypothesis:a00-0fe88a0b-dbdfda
mint_id: fce944a171b045ce8512f97f8db1b7ad
type: hypothesis
parents:
  - goal:g10.1
next_edges: []
confidence: 0.0
scaffold_hash: a57fd8a7a177e94e
testable_claim: "G10.1 asserts chats are \"viewable, expandable to full LOD, **forkable**.\" The forkability claim is the one g10.1 property that is *not* a rendering concern: it says an agent or user can take a chat at an internal decision point and continue from there, inheriting the context up to that point, rather than starting a fresh chat from the outputs alone."
title: Chat-fork at decision points reduces re-derivation overhead vs starting fresh
verdict: pending
---
# hypothesis:a00-0fe88a0b-dbdfda

## Hypothesis

### Testable claim

G10.1 asserts chats are "viewable, expandable to full LOD, **forkable**." The
forkability claim is the one g10.1 property that is *not* a rendering concern:
it says an agent or user can take a chat at an internal decision point and
continue from there, inheriting the context up to that point, rather than
starting a fresh chat from the outputs alone.

**Operational claim:** Given a corpus of incomplete derivation chats (ones that
produced a node that was later superseded, or that stopped before producing
any node at all), an agent that *forks* from the chat's last productive
decision point — inheriting context up to that point — reaches an acceptable
completion in fewer tool calls than an agent that starts a fresh session
having only consumed the derivation's outputs (or a summary of them).

### What would prove it

- On 20 trials drawn from the repo's own incomplete-derivation history (or
  simulated incomplete derivations), the fork group shows ≥30% reduction in
  tool calls to acceptable completion compared to the fresh-start group, with
  p < 0.05.
- The effect holds across different fork-point types: decision branches (A vs
  B were considered, agent chose A but it was wrong), dead-end attempts (tool
  call failed, agent gave up), and scope-limitation cases (agent said "this
  needs a separate pass").
- The fork group's outputs are not lower quality than the fresh-start group's
  — measured by a blinded judge scoring the completion against the task spec.
  Cheaper is worthless if it is worse.

### What would disprove it

- No significant tool-call reduction — the chat context up to the fork point
  carries no structural signal that a fresh agent cannot regenerate from the
  outputs alone in roughly equal time.
- The fork group is *worse*: inheriting stale reasoning context leads the
  agent to reproduce errors from the prior derivation instead of finding a
  clean path.
- Fork-point identification is the bottleneck — the cost of choosing the
  right decision point cancels the tool-call savings, or requires human
  judgement per fork (making it unscalable).
- The fork group produces lower-quality completions — the inherited context
  constrains the agent to think inside the prior derivation's frame when a
  fresh perspective would have produced a better solution.

### Why this matters

If forks work:
- The "forkable" requirement in g10.1 is grounded: chat structure has
  recoverable continuity points that a later agent can join, and the
  "render as subgraph" claim has a concrete use case beyond passive reading.
- Abandoned-attempt chats (g9.5's prior-art requirement) become valuable
  inputs rather than archive — they are forkable starting points.
- The "produces nothing" attachment edge case from g10.1 has a natural
  resolution: such chats are fork roots whether or not they produced a node.

If forks do NOT work:
- "Forkable" is aspirational phrasing for what is really "viewable up to a
  point" — the chat provides awareness, not re-entrance.
- The project should invest in fork-point tooling (UI to mark decision
  points) rather than assuming agents can recover them from raw logs.
- Starting fresh with a summary is the correct default for continuing
  abandoned work, and chat storage is purely archival, not operational.

### Relationship to siblings

This hypothesis is complementary and orthogonal to the three existing
hypotheses under goal:g10.1:

| Sibling | Asks | Relationship here |
|---|---|---|
| a00-160ca279-56d211 | Can chat structure be mechanically extracted (zero LLM)? | Fork-point identification is a harder sub-problem of extraction. This hypothesis tests whether forks are *useful*, not whether they are *discoverable* — but a non-recoverable fork is a non-fork. If a00-160ca279 disproves mechanical extraction, this hypothesis tests whether fork utility survives the extra cost of LLM-per-event identification. |
| a00-711c2d0f-15bc43 | Does verbatim chat beat post-hoc summary as context? | That hypothesis asks about *full-chat inheritance* (start from the beginning). This one asks about *partial inheritance* (start from a decision point). If full-chat beats summary, fork likely beats both; if full-chat loses to summary, fork might still win because it is shorter and more focused. The two are not redundant. |
| a01-53cbe2c4-dc9630 | Does the awareness flag prevent attribution errors? | The flag is necessary regardless of any fork result. Forking introduces a new failure mode the flag does not address: the agent inheriting the fork may be *more* likely to treat prior reasoning as its own because the fork is positioned as "continued from here" rather than "read this chat." This hypothesis should control for awareness-flag presence to avoid conflating the two. |

### Failure modes to control for

- **Fork-point selection confound:** If fork points are selected by the
  experimenter (ideal case), results may not generalize to automatic
  fork-point detection. Run a third arm: automatically-determined fork
  points vs human-selected ones vs fresh start.
- **Task-type confound:** Forking works for "continue the implementation"
  tasks but not for "reconsider the approach" tasks. The hypothesis should
  test both, with the second as a control where fork is expected to fail.
- **Length confound:** A fork starting at decision point 37 of a 200-message
  chat carries only the first 37 messages — shorter than the full chat but
  longer than a summary. The fresh-start arm should receive only the outputs
  (no context beyond the node itself) to isolate the fork vs no-context
  question, with a third arm receiving a full summary to control for "any
  context helps" effects.
- **Awareness-flag interaction:** As noted above, fork context may amplify
  attribution errors. Both arms should carry the awareness flag from
  a01-53cbe2c4-dc9630 to isolate the fork effect from the flag effect.
- **Quality measurement confound:** "Acceptable completion" must be scorable
  by a blinded judge on the node's own terms (does it satisfy the goal the
  original derivation was pursuing?). Pre-register the scoring rubric per
  trial.

### Suggested experimental design

1. Curate 10-20 derivation chats from the repo's own session logs, each
   representing an incomplete derivation — either one that produced a node
   later superseded, or one that stopped without producing any node.
2. For each chat, identify the last productive decision point (the message
   where the agent chose one path over another before the derivation stalled).
3. Create a continuation task: "Complete the derivation that this agent
   abandoned. The goal was: [original goal text]."
4. Run each task twice:
   - **Fork arm:** Agent receives context = chat messages 1..N (up to the
     fork point) + awareness flag + task.
   - **Fresh-start arm:** Agent receives context = outputs of the derivation
     (any files changed or nodes created) + awareness flag + task.
   - **Summary arm (control):** Agent receives a 3-paragraph summary of what
     the prior derivation achieved and where it stopped + awareness flag + task.
5. Measure: tool calls to acceptance, quality score of completion (blinded),
   and whether the fork group reproduces any errors from the prior derivation
   (a degradation measure).
6. Test each arm N ≥ 10 times per chat for statistical power.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-9afb0e7e, iter 1024). Kid's version passed
substantively: parents resolves to goal:g10.1, verdict `pending` is the
honest state (untested), `testable_claim` present, and the claim is the
fourth distinct facet of g10.1 the three iter-1010 siblings left open —
the "forkable" property. Its three-way arm design (fork / fresh-start /
summary) and the explicit orthogonality matrix against each sibling are the
load-bearing parts. The deliberate choice to hold the awareness flag
constant across arms (rather than vary it) is correct: it isolates the fork
effect from the flag effect that a01-53cbe2c4-dc9630 owns.
One defect fixed — the same one a00-160ca279 carried in iter 1010: the kid
hand-wrote its own `## Agent Notes` in the body even though the contract
says `cli.py done` renders `--notes` there exactly once, so the node had two
Agent Notes headings. Removed the hand-written one; kept the one the
harness rendered (at the end, after this block).
Data-loss note: this node's original file was deleted from disk mid-iteration
by an external tree clean (a concurrent director wave / iteration-1025 setup
swept untracked files); no grid ref existed, so it was unrecoverable from the
grid. This version is restored by the parent from the verbatim content it read
before the deletion, with the review edits applied. That is why this THOUGHT
supersedes the kid's original one (preserved only in the session log).
<!-- THOUGHT:END -->

## Agent Notes
Fourth hypothesis under goal:g10.1 — tests chat-fork semantics. Fork at decision point reduces re-derivation overhead vs starting fresh. Three arms: fork, fresh-start, summary control. Orthogonal to three sibling hypotheses.
