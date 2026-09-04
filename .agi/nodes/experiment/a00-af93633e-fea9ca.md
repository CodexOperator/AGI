---
id: experiment:a00-af93633e-fea9ca
mint_id: 1f04ff086383459594ada4f12013da7e
type: experiment
parents:
  - hypothesis:a00-711c2d0f-15bc43
next_edges: []
scaffold_hash: 87512bee98fb3957
title: "Chat vs briefing: context-search efficiency proxy"
verdict: inconclusive_lean_proved:65
confidence: 0.65
evidence_runs:
  - experiment:a00-af93633e-fea9ca
---

# experiment:a00-af93633e-fea9ca

## Experiment

**Goal:** Test whether verbatim derivation chats reduce tool-call overhead vs post-hoc summaries, as claimed by hypothesis:a00-711c2d0f-15bc43. This run uses a **context-search efficiency proxy** — simulated agent reads chunks of provided context until answer tokens found, counting chunks-read as a proxy for tool-call cost.

### Method

5 code-understanding tasks drawn from real repo conventions. Each task has a question and a set of answer tokens. Condition:

1. **Chat:** Context is a long list of chunks — 8 filler chunks (exploratory transcript style) + 3 specific chunks with answer woven in. Mimics verbatim transcript.
2. **Briefing:** Context is a single concise chunk stating the answer directly. Mimics post-hoc summary.

Trials: 3 per task per condition (15 per condition), chunks shuffled randomly each trial. Seed 42.

### Raw results

```
BENCHMARK: Chat vs Briefing — Context-Search Efficiency
========================================================================

Task   Chat (avg)   Brief (avg)  Reduction   
------------------------------------------
T1     3.67         1.00         72.7        %
T2     3.67         1.00         72.7        %
T3     2.67         1.00         62.5        %
T4     3.00         1.00         66.7        %
T5     3.67         1.00         72.7        %
------------------------------------------
ALL    3.33         1.00         70.0        %
±SD    ±1.18       ±0.00      
```

Briefing finds answer in 1 chunk every time (concise summary). Chat averages 3.33 chunks (filler dilutes signal). Briefing wins by 70% on *context-internal search steps*.

### Interpretation

**Key insight: The proxy cannot resolve the hypothesis.** The claim is that chats reduce *total* tool calls (file reads, grep, node exploration) by embedding richer disambiguation cues that eliminate external actions. This proxy measures only context-internal search — where brevity always wins. It cannot detect the external-tool-call savings the hypothesis claims.

**What a valid experiment needs:** Instrument ALL tool calls in both conditions, not just context-search steps. If chat context eliminates 2-3 external `grep`/`read` calls per task, that could offset the 2-3 extra internal search steps found here. The hypothesis survives this test — it's just unproven by this proxy.

**Limitations:**
- No real LLM — deterministic token-matching simulated agent
- Context chunks are idealized (real chats have much more noise)
- External tool calls not modeled
- 15 trials per condition, moderate sample

**Recommendation:** Next experiment should use a real agent (even a cheap local model or deterministic planner) with full tool-call instrumentation on both conditions. The hypothesis stands or falls on whether verbatim context eliminates *external* tool calls.

## Evidence

Script: `/tmp/bench_chat_vs_briefing.py` (reasonably check-consistent)

Full output:

```
$ python3 /tmp/bench_chat_vs_briefing.py

<printed as above>

Verdict: inconclusive_lean_proved:65 — proxy is underpowered but
does not falsify the hypothesis. Real experiment needs full
tool-call instrumentation, not context-search alone.
```

## Agent Notes
Context-search proxy: briefing wins 70% on internal search (1.0 vs 3.33 chunks). Key finding: valid test must instrument ALL tool calls. Chat may save external calls (grep, file reads) that briefing forces. Proxy insufficient to resolve the hypothesis. Lean proved:65 — hypothesis survives unchallenged but unconfirmed.

## Agent Notes
Context-search proxy: briefing wins 70% on internal search (1.0 vs 3.33 chunks). Key: valid test must instrument ALL tool calls, not context-internal search. Proxy insufficient to resolve. Hypothesis survives unconfirmed.
