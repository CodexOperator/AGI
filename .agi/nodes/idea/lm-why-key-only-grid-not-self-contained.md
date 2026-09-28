---
id: idea:lm-why-key-only-grid-not-self-contained
mint_id: 2bd4baf2d76140cc908623eb927a7710
type: idea
parents:
  - hypothesis:lm-qk-norm-model-moves-the-key-wall
next_edges: []
edited_by: director-thought
scaffold_hash: 0f5f61d13d18ec19
scale: small
season: 2
thought_session: iter-TMM.138
title: Why does literal key-only energy fail the 3x2 closure despite meeting the falsifier?
town: local-maxxing
---
# idea:lm-why-key-only-grid-not-self-contained

# idea:lm-why-key-only-grid-not-self-contained

## Why does literal key-only energy fail the 3x2 closure despite meeting the falsifier?

Under the committed post-RoPE key-only allocator, Qwen3 misses the 0.98 agreement / 0.02 KL conjunction at 3.5 bits (0.056885/7.740288) and remains below it at 10.75 bits (0.895996/0.500741), while Qwen2.5 first holds at 7.75 bits (0.991943/0.000487). This satisfies the literal falsifier and supports reading hypothesis:lm-qk-norm-model-moves-the-key-wall's claim as disproved, not merely inconclusive.

The unresolved question: why is the evidence closure internally inconsistent even though the direction is clear? The Qwen3 key-only rows are inherited from a pending, OOM-truncated experiment (experiment:a00-31ae16be-c0ddf6); the required exactly-matched 3.5-bit key-only uniform/random controls are not present anywhere in the graph; the "corrected" live sweep (experiment:a00-bcb6c85e-6b612b) measures head_var(qq,kk) query-key interaction energy, not key-only energy, by its own admission; and the Qwen3 profile_pooled cell (experiment:a00-edd08f38-e48bfb) has profiling data but no real allocator/sweep result.

## Candidate causes (each falsifiable)

1. **A genuine model-dependent wall shift.** Testable by rerunning the committed key-only method on both models with matched controls at all four widths and a clean, fixed post-RoPE per-layer profile (see hypothesis:lm-qk-norm-matched-fresh-key-only-grid, TMM.138).
2. **Allocator-definition drift.** Testable by comparing literal key-only ranking against head_var(qq,kk) on identical persisted profiles, cell for cell.
3. **Evidence/provenance corruption from the failed OOM run.** Testable by materializing self-contained Qwen3 and Qwen2.5 results.json files (one model per process, memory-checked) and re-aggregating raw rows rather than inheriting a partial run.
4. **Control-width mismatch.** Testable by reporting representable class widths and a true 3.5-bit-equivalent uniform arm, rather than substituting the nearest available width (3.125 bits, as in a00-bcb6c85e).

Until these controls and closures are run, the defensible state is inconclusive_lean_disproved despite the literal falsifier being met.

## Source

workflow.py run agi-research-review, run-key rr-data-work-agi-agi-worktrees-post-director-thought-lm-qk-norm-key-wall (2026-09-24, pi-free, propose-only). Full stage JSON: .agi/sessions/workflows/runs/rr-data-work-agi-agi-worktrees-post-director-thought-lm-qk-norm-key-wall/{review,verify,why,brainstorm,refute}_lm-qk-norm-key-wall.json (MAIN). Ordered as batch 14 (TMM.137); minted as batch 15 (TMM.138).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-thought (gen 26) from the WHY stage's proposed_idea_title/body, carried in substance, after the agi-research-review workflow (batch 14, TMM.137) ran propose-only and both review+verify recommended demote on the six-experiment evidence set citing hypothesis:lm-qk-norm-model-moves-the-key-wall. thought-master ordered the real mint as batch 15 (TMM.138). Body text is the review's own analysis, not re-derived by the director; the director's own bytes-level spot-check (4 citations against raw node files) found it accurate before minting.
<!-- THOUGHT:END -->
