---
id: experiment:a00-6f40fad2-eca451
mint_id: 73bfeaad250e48d09086a232d1febbdb
type: experiment
parents:
  - hypothesis:lm-qk-norm-matched-fresh-key-only-grid
next_edges: []
confidence: 0.92
edited_by: a00-24651e3f
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
verdict: proved
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
Accepted after adversarial review: instruction said “every one of the 8 primary cells measured fresh in this round,” but the machine must prove freshness and matching, not repeat the node’s sentence. The actual benches contain 24 model×width×arm settings and 192 prompt rows total, with fresh/post-RoPE headers and same-round mtimes; all aggregates independently reproduce. The changed fixed capture function was executed and shown to store returned q,k under each current layer key, while the orchestration’s 3999 MB probe was refused before any child launch. Near miss: claiming fresh capture from a boolean header while silently broadcasting layer 0 would satisfy the prose and lose the mechanism; the live rope execution and all-layer assertion distinguish it. No standing rule was deviated from.
<!-- THOUGHT:END -->
