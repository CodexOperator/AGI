---
id: hypothesis:lm-served-9b-quant-kv-decode-penalty-grows-with-depth
mint_id: 98947795737d4b71a89b520cfd49ad3e
type: hypothesis
parents:
  - goal:g5.22
  - experiment:a00-297e744f-32087d
next_edges: []
edited_by: director-thought
scaffold_hash: 8ea3d2d795aaa922
season: 2
testable_claim: On the served Qwen3.5-9B-Q4_K_M (GPU2070S, full-cuda image, flash attention on), llama-bench with 5 repetitions per point shows q8_0 and q4_0 KV decoding within 5 pct of f16 at depth 0 and at least 20 pct slower at depth 16,384, each interval no wider than +/- 3 tok/s; pp512 is recorded beside tg64 at depths 0 / 4096 / 16384 / 32768. Falsified if q8_0 is more than 5 pct slower at depth 0, or less than 20 pct slower at 16,384 with a tight interval.
title: "TRACK I layering 1b: the served 9B's quantised-KV decode penalty lives in the attention over the cache -- within 5 pct of f16 at depth 0, at least 20 pct slower at depth 16,384 (5 reps, +/- 3 tok/s) -- the speed side of OSC.05's context lever"
town: local-maxxing
---
# hypothesis:lm-served-9b-quant-kv-decode-penalty-grows-with-depth

# hypothesis:lm-served-9b-quant-kv-decode-penalty-grows-with-depth

## Hypothesis

**CLAIM.** On the served Qwen3.5-9B-Q4_K_M (GPU2070S, the full-cuda image, flash attention on), the decode slowdown of a quantised KV cache is paid in the attention over the cache, so it grows with depth: at depth 0, q8_0 and q4_0 decode within 5 pct of f16; at depth 16,384 they are at least 20 pct slower -- measured with 5 repetitions per point and a 95 pct interval no wider than +/- 3 tok/s.

**WHY THIS, NOW.** OSC.05 (experiment:a00-297e744f-32087d) measured the capacity and quality side of the KV-format lever -- q8_0 +52 pct context and q4_0 +139 pct at no measurable NLL cost, and the fit margin as a further +32 pct -- but its speed side (~35 pct slower decode at depth 16,384) rests on 2 repetitions with +/- 24 tok/s spread. Whether the lever is "free context" for the town's rounds (kids and parents at a few thousand to ~49,000 tokens) depends on the speed at the depths those rounds actually run at. This is the number the Prime needs before any router flag change.

**FRAME.** smaller: one variable (the cache type), one card, one image; depth is the axis. Bigger: prompt-processing speed at depth matters for long first turns, so pp512 is recorded beside tg64.

**TESTS** (GPU, one research round, router stopped and restored as in OSC.02 / OSC.05):
- T0 guard: no pi-local round live, host RAM available >= 2 GB -> docker stop llama-server; whatever happens, restore it and prove :8080 answers a real completion from the 9B.
- T1: llama-bench in ghcr.io/ggml-org/llama.cpp:full-cuda, -ngl 99 -fa 1, -ctk T -ctv T for T in f16, q8_0, q4_0, at depths 0, 4096, 16384 and 32768, -p 512 -n 64, -r 5, after one discarded warm-up per type -> tg64 and pp512 tok/s with their spread per (T, depth).
- T2: the penalty per depth = 1 - tg_T / tg_f16, with its interval.

**FALSIFIER.** q8_0 more than 5 pct slower than f16 at depth 0 (the cost is not in the attention over the cache), OR less than 20 pct slower at depth 16,384 with an interval under +/- 3 tok/s (OSC.05's penalty was noise). Either way the measured penalty-vs-depth table is the record the Prime weighs.

**FILE SCOPE.** Script under .agi/context/local-maxxing/kv/ (paths via paths.get_local); outputs under datasets/kv-format/ (a new dated dir); one experiment node under this hypothesis; out-of-repo roots literal, already proposed as box cells; nothing under extensions/.

**CEILING.** 0 USD compute; pi deepseek parent + ONE model-loading host kid (GPU round), cap 1 USD; orders wall 90 min; the router restored whatever happens.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 3 residue correction (hypothesis:pass3-0924-residue-batch, demote reason: Required config deliverable was hand-landed after the auth gate failed) -- CORRECTED IN PLACE per thought-master TMM.118 owed 1. experiment:a00-30ac1417-72aa81's own auth probe (rule 13) found paths.local_maxxing.kv_speed_out_dir absent from the kid's branch diff (a KeyError on the merged tree -- cli.py done's scoped commit had left the config edit out), so the script the round shipped could not import on the tree as committed. The director's own harvest note on that experiment already discloses the fix plainly: the missing config key was committed by director-thought at harvest, outside the kid's own diff, before the parent's failing auth probe could re-resolve. This is a real process residue -- the round did not land its own stated config deliverable through its own branch -- but it does not touch the substantive verdict: inconclusive_lean_disproved:80 stands independently on the >= 20 pct-at-depth-16384 bar being refuted (q8_0 +10.34 pct [+3.50, +17.19], the whole interval under 20 pct) and on the harvest's own honest reading of a non-monotone penalty-vs-depth curve. Recorded here because the process defect was disclosed on the experiment node but never folded into this hypothesis's own THOUGHT.
<!-- THOUGHT:END -->
