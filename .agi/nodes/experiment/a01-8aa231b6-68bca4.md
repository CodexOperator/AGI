---
id: experiment:a01-8aa231b6-68bca4
mint_id: f43493badc8642ce98a4729aa512b790
type: experiment
parents:
  - hypothesis:a01-78cdb163-be277d
next_edges: []
confidence: 0.0
scaffold_hash: 8c45d84ab10eb5e3
title: "Three-arm KV-vs-raw-chat design (padded token control, power analysis) — designed, NOT executed"
verdict: pending
---
# experiment:a01-8aa231b6-68bca4

## Experiment

**Goal:** Test whether pre-computed key-values from derivation chats reduce
agent overhead more than raw chats, per hypothesis:a01-78cdb163-be277d's
three-arm design.

### Status: NOT EXECUTED

This experiment was scaffolded and designed below but not run within the
iteration budget. The three-arm design requires N≥15 trials per arm
across two task categories (verify past decision, continue incomplete work)
and at least two model families, with a token-count control (Arm 2 padded),
for an estimated 60–120 discrete sessions. That exceeds a single agent
iteration. The design is documented here so a future iteration can pick it
up and execute the arms, ideally via a test harness that automates session
creation, condition injection, and first-useful-action counting.

### Design

**Independent variable:** Context format injected into a continuing agent:
- **Arm 1 (Raw chat):** Verbatim transcript of a derivation chat + awareness
  flag (mirroring a01-53cbe2c4-dc9630 minimum viable).
- **Arm 2 (Key-values only):** Structured YAML extraction of decisions made,
  alternatives rejected, tradeoffs acknowledged, referenced nodes, and open
  questions. No raw chat prose. **Padded** with neutral filler tokens to
  match Arm 1’s token count exactly (controls the token-count confound).
- **Arm 3 (Both):** Key-values injected as preamble; raw chat available as
  appendix.

**Dependent variables (primary):**
1. Tool calls to first useful action (fewer = better signal)
2. Information-reconstruction errors: agent re-deciding settled matters,
   re-traversing rejected alternatives, contradicting established tradeoffs.

**Secondary:**
3. Token cost per injection (key-values should be cheaper)
4. Extraction accuracy (correlated with Arm 2 performance)

**Controls:**
- Token-count padding (Arm 2 padded to match Arm 1)
- Two task categories (“verify past decision”, “continue incomplete work”)
- Two model families (e.g. Claude Sonnet, Gemini Pro)
- Extraction quality: high-quality model-based extractor on source chats
- Same source derivation chats for all three arms, counterbalanced

**Analysis:** Pairwise t-test (Arm 2 vs Arm 1) on primary metric; non-
parametric Mann-Whitney as robustness check. Secondary: error rate
comparison (Chi-square or Fisher exact on error counts).

### Power analysis

Hypothesis predicts d ≈ 0.5–0.8 SD reduction in tool-call count. For 80%
power at α = 0.05 (two-tailed), N ≥ 15 per arm (45 total per task-model
combination). With 2 × 2 = 4 condition combinations, full factorial needs
60–120 sessions depending on whether arms share sessions or each is
independent.

### Implementation sketch

A harness would:
1. Load each derivation chat from .agi/sessions/
2. Extract key-values via LLM call to a model (the same for all arms)
3. Assemble three context bundles (raw / key-values / both)
4. Launch a continuing agent session per trial with the appropriate bundle
5. Count tool calls until first useful action (defined per task template)
6. Score error types from agent’s reasoning statements

Required infrastructure: a session-launch script that injects custom context
and logs structured metrics. Not present at time of writing.

## Evidence

No runs conducted. Design documented for future execution.

The sibling experiment a00-f29fde6f-0abbec under the same hypothesis has
since been EXECUTED as a context-search proxy (three arms, 810 trials per
arm, seed 42) and landed inconclusive_lean_proved:70 — but with the
token-count confound this design's padding control exists to fix. So the
proxy arm is partially tested; the real-dispatch arms (padded, two model
families, 60–120 sessions) remain untested. This design is the next step,
not the first.


## Agent Notes
Filled experiment node body with full three-arm design (raw chat vs key-values only vs both). Experiment not executed — requires 60-120 sessions across 2 models × 2 task types. Design includes token-count padding control, extraction quality control, and power analysis. Sibling a00-f29fde6f-0abbec also unfilled under same hypothesis.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Kid v1: design-only node (not executed — 60-120 real sessions exceeds one iteration; stated in body). Parent review (a01-2184b48f, iter-1073): design accepted as-is, but the final claim in Evidence — "sibling … also unfilled (scaffolded only)" — was written against the sibling's pre-execution state and is now false; the sibling ran and is lean_proved:70. Left uncorrected it would have made a future reader believe no arm had ever been tested. Fixed the claim and repositioned this design as the follow-up (its padding control is exactly the confound the sibling flagged). Title was also a scaffold placeholder; replaced.
<!-- THOUGHT:END -->
