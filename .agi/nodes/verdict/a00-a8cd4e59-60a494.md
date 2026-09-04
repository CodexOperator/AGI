---
id: verdict:a00-a8cd4e59-60a494
mint_id: 68d69aee611d45b9b7b83c7e073dce2d
type: verdict
parents:
  - experiment:a00-811b8503-ae99a5
next_edges: []
confidence: 0.85
scaffold_hash: 49a038311ae901ea
title: A00 a8cd4e59 60a494
verdict: inconclusive_lean_proved:85
---
# verdict:a00-a8cd4e59-60a494

## Verdict

inconclusive_lean_proved:85

## Evidence

Compared `viewport.py --emit llm` vs `inject.py --stdout` briefing output on same graph with 40-frame window. 69 of 72 briefing lines were byte-identical. 3 differences found, all rooted in caller-supplied data rather than the briefing module:

1. **Viewport adds its own header** (`anchor=roots depth=3 frames=205 time=-`) between its frame counter and the briefing — not a briefing output, a viewport annotation.
2. **Chain stats diverge** because viewport doesn't import `chain_engine` (→ "unavailable"), while `inject.py` does (→ reports 0/0). The briefing renders whatever `chain_stats` it's given.
3. **Pending tasks diverge** because viewport doesn't pass `_loaded` to `briefing.build()`, so `pending_tasks` defaults to 0. Inject passes it and gets 91.

All three are **caller-data gaps**, not renderer defects. The briefing module has zero runtime dependencies on viewport or frame stream — confirmed via static import analysis.

## Confidence

0.85

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The hypothesis claims "the nine sections around it" are what kept the viewport from replacing the renderer. This experiment tests the behavioural claim: does the shared briefing module produce identical output from both callers? The answer: almost byte-identical (69/72 lines), with the 3 gaps traced to caller-supplied data not renderer logic. The hypothesis is structurally correct but operationally incomplete — the callers still compute different data for the same sections. 85% confidence: strong structural evidence, but the caller-data gaps mean full parity requires extending what viewport passes to briefing.build().
<!-- THOUGHT:END -->