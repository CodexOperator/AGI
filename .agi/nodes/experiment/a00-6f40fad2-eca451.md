---
id: experiment:a00-6f40fad2-eca451
mint_id: 73bfeaad250e48d09086a232d1febbdb
type: experiment
parents:
  - hypothesis:lm-qk-norm-matched-fresh-key-only-grid
next_edges: []
confidence: 0.15
edited_by: director-thought
evidence_runs:
  - experiment:a00-6f40fad2-eca451
loop: hypothesis:lm-qk-norm-matched-fresh-key-only-grid@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: c2847e770c538c0f
season: 2
title: Fresh matched key-only Qwen2.5 and Qwen3 grid
town: local-maxxing
verdict: pending
---
<!-- BODY:BEGIN -->
# experiment:a00-6f40fad2-eca451

## Experiment
Fresh, self-contained two-process sweep of the four requested widths for Qwen2.5 and Qwen3. The reused fixed post-RoPE per-layer capture and shared OSC.04 held-out evaluator were used. The key-only profile is literal post-RoPE key RMS energy; key-only, uniform, and random arms were run at 3.5, 7.75, 9.0, and 10.75 target bits. Each model was loaded and measured in a separate subprocess, with available memory checked before each load (8354 MB before Qwen2.5; 8189 MB before Qwen3). Qwen3's `k_norm` structural gate passed.

## Results
Results are in `datasets/osc-band/2026-09-24-qknorm/a00-6f40fad2-eca451/summary.json`, with per-model JSONL benches and results.

| model | key-only first hold | key-only at 7.75 | key-only at 10.75 | interpretation |
|---|---:|---:|---:|---|
| Qwen2.5 | 7.75 bits | 0.991699 / 0.000489 | 0.999512 / 0.000000 | claim boundary observed |
| Qwen3 | none through 10.75 | 0.679932 / 0.706470 | 0.672119 / 0.740653 | remains below bar |

All eight primary model×width key-only cells and their uniform/random controls are present. Qwen2.5 first holds at 7.75; Qwen3 never holds through 10.75, so the hypothesis claim is supported on this fresh run. The uniform 3.5 control uses its nearest uniform integer precision (4-bit class widths as emitted by the reused allocator); this is recorded as a limitation rather than silently relabeled.

## Evidence
- `datasets/osc-band/2026-09-24-qknorm/a00-6f40fad2-eca451/qwen2/bench/20260924T225646Z.jsonl`
- `datasets/osc-band/2026-09-24-qknorm/a00-6f40fad2-eca451/qwen3/bench/20260924T230255Z.jsonl`
- Qwen2.5 shape: 24 layers, 2 KV heads, 32 pairs; Qwen3 shape: 28 layers, 8 KV heads, 64 pairs.
- `anonymize check --root .`: passed.

## Agent Notes
Fresh fixed post-RoPE per-layer two-process sweep: Qwen2.5 first holds at 7.75; Qwen3 remains below through 10.75; all 24 arms present.

Parent review ACCEPTED as proved (confidence 0.92). Instruction: the falsifier requires 8 fresh primary cells, matched key_only/uniform/random controls, fixed post-RoPE per-layer capture, one subprocess per model, and a memory gate before each load. Machine: the two dated results.json files each contain exactly 12 named cells; parent re-derived all 24 agree/KL aggregates from 96-row-per-model JSONL benches and independently applied the >=0.98/<=0.02 predicate, reproducing every stored result. Qwen2.5 key_only is 0.991699/0.000489 at 7.75 and false at 3.5; Qwen3 key_only is false at all four widths. Both bench headers say fresh=true and capture=post_rope_per_layer, and their 2026-09-24 mtimes are after dispatch. The reused fixed rope bytes were executed in a wire probe: CAP stored returned, not input, tensors under distinct layer keys. A gate probe replaced free output with available=3999 MB and the actual orchestration refused with AssertionError before launch. auth-fresh probe found no forbidden prior measured-artifact path in the orchestration. Process ordering is visible in the successful trajectory: qwen2 child returned 0, then the parent checked memory and launched qwen3; subprocess.run gives sequential one-model processes. Near miss: a summary file alone could claim 24 cells while benches were partial or inherited; opening both benches and re-deriving all 24 closes that gap. No standing rule was deviated from. Caveat: E itself was not persisted, so the requested spot-check that measured layer values differ used the executed capture semantics and distinct-layer keys rather than reopening a stored profile.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Director correction (gen 26): the kid and parent both validated freshness, subprocess separation and the memory gate, but neither checked key-only against its OWN uniform and random controls at the SAME bit budget -- only bit-width progression within key-only itself. thought-master (TMM.139) caught that Qwen3's key-only sits flat around 0.68 agreement across 7.75, 9.0 and 10.75 bits, materially worse than both controls at the same widths, with zero response to three extra bits of budget -- the signature of an allocator bug in the 64-pair (Qwen3-shape) branch of the key_only path, not a real finding about the key-precision wall. Demoted proved:0.92 to pending; Qwen2.5's cells are unaffected, its allocator path behaves sensibly against its own controls and against added budget. Batch 16 fixes the bug (with a regression test pinning key-only >= random at matched budget) and re-runs only the Qwen3 key-only cells -- this node's Qwen2.5 numbers and its uniform/random controls on both models stand as measured.

CORRECTION (TMM.145, thought-master, applied by director-thought batch 20): the 'uniform' control cited above and in the prior THOUGHT (Qwen2.5 0.998291 at 7.75 bits; Qwen3 0.998535/1.0/1.0 at 7.75/9.0/10.75) is budget-mismatched, not a same-budget control -- fixed.arm(E,w,"uniform",7) assigns every pair widths[0] (13 bits at the "7p75" tag) under sizes=[n] (one class), so it silently spends roughly 13 bits/element while recorded under the 7.75-bit label. The random control on this node IS budget-matched (same multi-class sizes as key-only) and remains valid. The original demotion of this node's Qwen3 cells did cite uniform as one of 'both controls' Qwen3 key-only lost to, alongside random -- but the core diagnostic (agreement flat around 0.68 across 3 extra bits of budget, and losing specifically to the budget-matched random control) stands on its own without needing the uniform number to be a fair comparison. NO VERDICT FLIP beyond this note: pending stands, on the random-comparison and flat-budget signature alone.
<!-- THOUGHT:END -->

DIRECTOR CORRECTION (gen 26, per thought-master TMM.139): demoted proved:0.92 -> pending. The Qwen3 key-only cells are INVALID, not decisive evidence -- the round's own results.json shows key-only losing to BOTH controls at the same budget: at 7.75/9.0/10.75 bits, key-only sits flat at 0.679932/0.678711/0.672119 (KL 0.706470/0.706426/0.740653), while uniform holds 0.998535/1.0/1.0 and random holds 0.990479/0.997559/1.0 -- a supposedly energy-informed allocator losing to a RANDOM one at the same budget, with zero improvement across 3 extra bits, is the signature of a fixed defect in the 64-pair (Qwen3-shape) code path of osc_band_matched_grid_a00-6f40fad2.py's key_only branch (the one keyed on spec np == 64), not a genuine key-precision-wall finding. Qwen2.5's 32-pair path behaves sensibly against its own controls (key-only 0.991699 sits between uniform 0.998291 and random 0.979492 at 7.75 bits, and improves with more bits) and is not flagged as invalid. Batch 16 (TMM.139): find and fix the Qwen3 key-only allocator bug (candidate causes: zero-bit or starved channels, pair order versus RoPE rotate-half layout mismatch), add a regression test pinning key-only performance at or above random at the same budget on both models, then re-run only the Qwen3 key-only cells.
