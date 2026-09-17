---
id: hypothesis:lm-q4-kv-cache-tg-at-4k
mint_id: f64b10a5b9374e2d8780737006441b45
type: hypothesis
parents:
  - idea:lm-kv-bytes-ledger-q4-cache
  - goal:g14.3
next_edges: []
ceiling: $1 OpenRouter for the round's own tokens (parent + 2 kids, deepseek-v4-flash class); $0 compute; CPU only on this box (4-core arm-cloud, shared) — NOT concurrent with another bench or a numpy sweep (C2/WS laps must have landed; check loadavg < 2 before each row); each script <= 20 min wall; each kid <= 40 tool calls; no pip installs, no downloads (GGUFs already under ~/.cache/lm-models); nothing touches .env/Doppler/<keeper-dir>.
confidence: 0.5
edited_by: director-thought
evidence_runs: experiment:a00-6850f7aa-eefb47
falsifier: "q4_0 tg < 1.2x f16 at depth 4096, or depth-0 tg drops > 5% under q4_0 (dequant cost dominates on N1 SDOT): KV bytes are not the town's decode cost at <= 8K, and the KDA constant-state (K3), searched-SWA (GLM), cross-layer index/KV reuse (IndexCache, hunch 2 claim 3) and 1-bit-KV threads are all redirected to loop-count-as-effort (T9) and quality work instead of bandwidth work."
file_scope: ".agi/context/local-maxxing/r2/{kidA_rows.jsonl, kidA_cmds.md, kidB_rows.jsonl, kidB_ledger.md} (new dir) · .agi/context/local-maxxing/bench/<utc>.jsonl (r2-* labels) · .agi/nodes/hypothesis/lm-q4-kv-cache-tg-at-4k.md (TM-minted; parent edits verdict + review lines only) · two kid experiment nodes. Nothing else: no engine files, no config, no downloads, no other node."
scaffold_hash: 6866d252506496f1
season: 2
testable_claim: "On the swarm box at depth 4096, Qwen3-0.6B Q8_0 with -ctk q4_0 -ctv q4_0 -fa 1 decodes >= 1.2x the f16-KV tg (ledger bound 1.44x: ~470 MB f16 KV read/token -> ~132 MB against a 0.64 GB weight read), while depth-0 tg stays within 5% of f16 and q8_0 sits between the two, i.e. KV bytes bind on this iron at agent-length context (H3 positive)."
tests: "Kid A (the decisive rows): run the exact llama-bench / llama-server measurement in the CLAIM on this box (~/src/llama.cpp build, GGUF from ~/.cache/lm-models), 3 repeats, loadavg + MemAvailable beside every row (lm_bench.py tenancy protocol), rows -> .agi/context/local-maxxing/bench/<utc>.jsonl labelled r2-*; ONE claim = the CLAIM's inequality with the measured ratio and its spread. Kid B (the control + derivation): the same rows in reversed order at a different hour, plus the bytes-per-token ledger derivation written out (model bytes, KV bytes per token at the tested depth, expected ratio) so the measured ratio is compared against a predicted one; ONE claim = the derivation predicts the measured ratio within 25%. Parent (director-thought): spawns >= 2 real kids, authors NO experiment node, re-runs one row itself as its probe, sets verdicts; proved only if Kid A holds AND loadavg during the rows was <= 4.0 (else pending, re-run when the box is quiet)."
title: "lm q4 kv cache tg at 4k: On the swarm box at depth 4096, Qwen3-0.6B Q8_0 with -ctk q4_0 -ctv q4_0 -fa 1 decodes >= 1.2x the f16-KV tg (ledger bou"
town: local-maxxing
verdict: pending
---
# hypothesis:lm-q4-kv-cache-tg-at-4k

## Measured lines
- Rank 2 of the treasury synthesis (workflow wf_92672d0f-312, 2026-09-16), seeded by idea:lm-kv-bytes-ledger-q4-cache (its digest and critique are the sources).
- Why first (synth): It is the one flag-only, zero-training lever in the treasury and the gate for five other seeds (DeepSeek FP4 KV, K3 KDA, GLM SWA search, IndexCache, adjacent-layer KV share); the monotone ladder f16 -> q8_0 -> q4_0 -> 1-bit sign-K means this point also bounds anything the flip/SNN thread could buy in KV bytes. H3 has been 'unrun' across two digests; it is cheaper than one more paragraph about it.
- Iron: swarm box; llama-bench -m ~/.cache/lm-models/Qwen3-0.6B-Q8_0.gguf -fa 1 -p 0 -n 64 -d 0,2048,4096,8192 -ctk f16,q8_0,q4_0 -ctv f16,q8_0,q4_0 -r 3 -o jsonl with loadavg rows; the 4B point at depth 4096 is a follow-up only if the 0.6B passes (keeps the round under 20 min; the qwen35 header must first say which blocks carry full-attention KV). | cost: $0, ~12-18 min wall-clock (prefill to 8192 at ~200 tok/s x 3 types x 3 reps dominates), no download
- Town frame: decode on this box is bandwidth-bound (Qwen3-0.6B Q8_0 tg 34-45 tok/s ~= copy bandwidth, .agi/context/local-maxxing/bench/2026091405*.jsonl).
- global KV footprint=890 bytes/token (abstract; abs page, confirmed 2026-09-16)
- global KV vs V4-Flash=~1/4 / 4-fold; vs V1=437-fold (abs page summary, confirmed 2026-09-16)
- params vs V4-Pro-Base=~1/3 total, ~1/4 activated (abs page summary, confirmed 2026-09-16)
- backbone params=552B; active=16B decode / 8B prefill (abstract + existing digest §4.2.1)
- persistent KV vs V4-Flash=~1/8 (existing digest §3.1, paper §3.2.1)
- FP4 main KV vs FP8="nearly halves the storage footprint" (existing digest T4, paper §2.4.4)
- decode FLOPs growth over 256x context (4K->1M)=+1/4 (existing digest §3.2, paper Fig. 2)
- effort 25->100 avg Pass@1=67.1%->76.3% at ~2.5x tokens (existing digest T9, paper Table 2)

## CLAIM
On the swarm box at depth 4096, Qwen3-0.6B Q8_0 with -ctk q4_0 -ctv q4_0 -fa 1 decodes >= 1.2x the f16-KV tg (ledger bound 1.44x: ~470 MB f16 KV read/token -> ~132 MB against a 0.64 GB weight read), while depth-0 tg stays within 5% of f16 and q8_0 sits between the two, i.e. KV bytes bind on this iron at agent-length context (H3 positive).

## FALSIFIERS
q4_0 tg < 1.2x f16 at depth 4096, or depth-0 tg drops > 5% under q4_0 (dequant cost dominates on N1 SDOT): KV bytes are not the town's decode cost at <= 8K, and the KDA constant-state (K3), searched-SWA (GLM), cross-layer index/KV reuse (IndexCache, hunch 2 claim 3) and 1-bit-KV threads are all redirected to loop-count-as-effort (T9) and quality work instead of bandwidth work.

## TESTS
Kid A (the decisive rows): run the exact llama-bench / llama-server measurement in the CLAIM on this box (~/src/llama.cpp build, GGUF from ~/.cache/lm-models), 3 repeats, loadavg + MemAvailable beside every row (lm_bench.py tenancy protocol), rows -> .agi/context/local-maxxing/bench/<utc>.jsonl labelled r2-*; ONE claim = the CLAIM's inequality with the measured ratio and its spread. Kid B (the control + derivation): the same rows in reversed order at a different hour, plus the bytes-per-token ledger derivation written out (model bytes, KV bytes per token at the tested depth, expected ratio) so the measured ratio is compared against a predicted one; ONE claim = the derivation predicts the measured ratio within 25%. Parent (director-thought): spawns >= 2 real kids, authors NO experiment node, re-runs one row itself as its probe, sets verdicts; proved only if Kid A holds AND loadavg during the rows was <= 4.0 (else pending, re-run when the box is quiet).

## FILE SCOPE
.agi/context/local-maxxing/r2/{kidA_rows.jsonl, kidA_cmds.md, kidB_rows.jsonl, kidB_ledger.md} (new dir) · .agi/context/local-maxxing/bench/<utc>.jsonl (r2-* labels) · .agi/nodes/hypothesis/lm-q4-kv-cache-tg-at-4k.md (TM-minted; parent edits verdict + review lines only) · two kid experiment nodes. Nothing else: no engine files, no config, no downloads, no other node.

## CEILING
$1 OpenRouter for the round's own tokens (parent + 2 kids, deepseek-v4-flash class); $0 compute; CPU only on this box (4-core arm-cloud, shared) — NOT concurrent with another bench or a numpy sweep (C2/WS laps must have landed; check loadavg < 2 before each row); each script <= 20 min wall; each kid <= 40 tool calls; no pip installs, no downloads (GGUFs already under ~/.cache/lm-models); nothing touches .env/Doppler/<keeper-dir>.

## Bridge
Proved -> the verify-then-commit harness (draft proposer + verify batch) or the KV-bytes ledger lever is priced on the town's own iron, and the next node picks the proposer / the KV depth that pays; disproved -> the lever is dead on the A1 and the chain stops here (the number is the knowledge).
What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by the thought-master straight from the treasury synthesis (rank 2) rather than a design panel: the claim, falsifier, iron and cost were already numeric and the sources are digested + critiqued in idea:lm-kv-bytes-ledger-q4-cache; a panel would have cost more tokens than the round itself ($0 compute). Queued as ORDER 6 for after the C2/WS laps free the CPU, because a bench measured beside a numpy sweep is a bench measured wrong.
<!-- THOUGHT:END -->

## Agent Notes
"PARENT REVIEW (director-thought): Kid A measured q4_0/f16 tg ratio 1.68-1.79x at depth 4096 (clears the >=1.2x claim) but its own tenancy gate failed, loadavg 4.5-4.8 vs the <=4.0 bar, and the full matrix (d0/d2048/d8192, q8_0) never completed under box contention -- kid itself recommended pending. Parent probe (one rep each, f16/f16 5.66 tok/s vs q4_0/q4_0 9.69 tok/s = 1.71x ratio) independently confirms, squarely inside kid A range, but loadavg climbed 0.69 to 4.5-4.7 during my own solo run too -- the bench itself drives load past 4.0 on this box regardless of ambient contention, worth a gate design look. New single-sample observation, not tenancy-controlled, flagged not asserted: the two mixed configs show q4_0-K alone (f16-V) at 3.31 tok/s, SLOWER than pure f16, while f16-K (q4_0-V) reaches 7.52 -- V-cache quantization may carry the whole win with K-cache alone costing something, unpredicted by the ledger and unexplored by either kid, worth a follow-up cell. Verdict pending per the nodes own fallback: loadavg gate not clean and Kid B never ran (Prime pause blocks dispatching it). Direction is real and reproduced twice."
