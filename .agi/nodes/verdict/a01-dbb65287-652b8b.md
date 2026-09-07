---
id: verdict:a01-dbb65287-652b8b
mint_id: 199e9d6c7844492cb1b6995ec75bf111
type: verdict
parents:
  - experiment:a00-811b8503-ae99a5
next_edges: []
confidence: 0.85
edited_by: season.py
scaffold_hash: 8b052cb6a712b322
season: 1
thought_session: season
title: A01 dbb65287 652b8b
verdict: inconclusive_lean_proved:85
---
# verdict:a01-dbb65287-652b8b

## Verdict

inconclusive_lean_proved:85

## Evidence

Experiment `a00-811b8503-ae99a5` compared `viewport.py --emit llm` vs `inject.py --stdout` output (briefing sections only, 40-frame window, same graph). Of 72 briefing lines, 69 were byte-identical. The 3 differences were:

1. A viewport-specific header annotation (`anchor=roots ...`) — not part of the briefing module output, added by the viewport's own renderer.
2. Chain stats: viewport cannot import `chain_engine` → "unavailable"; inject can → reports 0/0. The divergence is in what each caller computes before calling `briefing.build()`.
3. Pending tasks: viewport passes no `loaded` → defaults to 0; inject passes loaded graph → reports 91.

The briefing module itself has zero runtime dependencies on viewport or frame stream — pure rendering library. This proves the **structural claim**: the nine sections can be extracted into a shared module both callers use, closing the renderer parity gap without either changing what it draws.

The **operational claim** (full byte-identical parity from both callers) is not yet met — but the remaining gaps are in data the callers choose to compute, not in how the briefing renders it. The abstraction is correct; the callers need to compute the same inputs.

The sibling experiments (`the-renderer-retired-and-what-it-took-with-it`, `the-viewport-reaches-parity`) proved the extraction and retirement were safe via coarse output equivalence. This experiment adds evidence at the briefing-module boundary: the abstraction works, the inputs are the gap.

## Confidence

0.85

## Agent Notes
Structural claim proved: briefing module produces 69/72 identical lines from both callers, 3 divergences all in caller-supplied data not the briefing itself. Abstraction is correct; inputs are the remaining gap.