# recurrent-looped-transformer-rlt — RLT, TEMPORAL recurrence (owner paper) — reading digest
READ-ONLY. MEASURED = quoted from a page read today; ESTIMATE = inferred, arithmetic shown.

## PAGE 1 — alphaXiv (fetched 2026-09-18)
URL: https://www.alphaxiv.org/abs/2609.recurrent-looped-transformer
- TITLE (MEASURED): "Recurrent Looped Transformer" (RLT).
- AUTHOR / DATE (MEASURED): Yifan Zhang (Princeton); technical report 2026-09-12 (coverage dated
  2026-09-13). The owner's id "2609.recurrent-looped-transformer" is the alphaXiv id (not an arXiv
  numeric id in this slice).
- MECHANISM (2 lines, MEASURED): a causal encoder builds prefix-restricted key-value memory; a
  recurrent decoder carries its FINAL HIDDEN STATE plus a layerwise sliding-window attention (SWA)
  cache across every prompt and response token. Each token runs the same state transition
  `H_t = D_theta(merge(e_t, s_{t-1}), M_{<=t}, C^D_{t-1})`; encoder work is parallel, decoder work
  is sequential in token order.

## THE EXPLICIT DIFFERENCE: TEMPORAL vs DEPTH RECURRENCE (MEASURED)
- DEPTH recurrence (Huginn, Ouro, MoR, UT, Giannou/Yang): the SAME position's hidden state is
  iterated by re-applying a weight-tied block. Effective depth = block depth x loops; the loop is a
  per-position compute dial; state does not (beyond ordinary attention) cross token boundaries.
- TEMPORAL recurrence (RLT): the recurrence runs ACROSS SEQUENCE POSITIONS — the decoder's final
  output state for token t is fed into the computation for token t+1, and the loop continues through
  the prompt/response boundary. The paper: "RLT differs from Universal Transformer-style systems
  because its recurrence is organized across sequence positions rather than primarily as repeated
  depth iterations at one position." Effective path length = tokens x decoder depth (unbounded as the
  sequence extends), with a FIXED number of blocks per token.
- Consequence (MEASURED): "RLT does not claim to reduce total arithmetic or latency relative to a
  standard Transformer. Prompt processing still contains a sequential decoder component." This is the
  opposite of the depth-recurrence pitch, where depth is a compute dial you can turn DOWN.

## UNIQUE PARAMS vs EFFECTIVE DEPTH (MEASURED)
- "A conventional Transformer has a fixed number of physical layers. RLT also uses a fixed decoder
  depth, but it repeatedly applies those layers across successive tokens. If the decoder has depth
  L_D, then processing t tokens creates a recurrent path containing t x L_D decoder-block evaluations."
  So: unique params ~ encoder + decoder (optionally tied); effective depth grows with SEQUENCE LENGTH,
  not with a loop dial. No numeric parameter count is given.

## RELEASED WEIGHTS / CODE (MEASURED)
- NONE. The page states the report is "an architectural and execution specification rather than a
  completed empirical system" and "does not report benchmark results, measured throughput, latency,
  memory consumption, or comparisons with trained baselines." No HF id, no repo, no GGUF.
- Related code cited: a Prefill-Decode kernel-mismatch technical report (github.com/yifanzhang-pro/
  Pretraining-RL-Science) — a companion, not the RLT implementation.

## CPU RUNNABILITY
- Not applicable today: no weights. Architecturally it is WORSE for the box than depth recurrence,
  because the decoder is sequential over every prompt token (ESTIMATE from the stated contract).

## QUALITY / TRAINING COST
- No quality numbers, no throughput numbers, no training cost reported (MEASURED: explicitly
  analytical). Do NOT cite RLT as evidence. Its value to the town is the design idea (one recurrent
  state transition across prompt and response; encoder memory vs decoder SWA cache separated;
  exact current-policy replay for RL) and its explicit contrast with depth recurrence.

## WHY IT MATTERS HERE
- It names the fork in the road: the town's CPU-first interest is DEPTH recurrence (turn compute down
  per token) — RLT is the TEMPORAL alternative (compute grows with sequence length, but latent state
  persists across tokens). Any town hypothesis that says "recurrence" must state which one; mixing
  them is a category error. If RLT ever ships weights, the fair CPU test is short sequences only.
