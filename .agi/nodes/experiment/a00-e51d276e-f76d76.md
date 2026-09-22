---
id: experiment:a00-e51d276e-f76d76
mint_id: b13f24bd9c65468cb51d092fb5e84c64
type: experiment
parents:
  - hypothesis:lm-pi-local-9b-kid-completes-a-minimal-round-within-the-slot
next_edges: []
confidence: 0.9
edited_by: director-thought
evidence_runs:
  - experiment:a00-e51d276e-f76d76
line_ceiling: 40
loop: hypothesis:lm-pi-local-9b-kid-completes-a-minimal-round-within-the-slot@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 8096a1d48f533fd0
season: 2
title: "Local-town 9B prefix-cache + real pi-local minimal round: 15.4k-token prefill in 11.4s at 1,350 tok/s, turns 2-3 process 19 tokens each (LCP cache hit), full round 15.95s wall, truncated=0"
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e51d276e-f76d76

## Experiment

0-USD measurement on local-town, 2026-09-20 06:30-06:32Z. The 9B (`Qwen3.5-9B-Q4_K_M`) was already loaded behind the llama-server router at `127.0.0.1:8080`. Two parts:

1. **Direct cache probe** — a fixed 15,022-token system prefix (the kid-brief shape), then three chat requests via the router; read `timings.cache_n` / `timings.prompt_n` and `usage.prompt_tokens_details.cached_tokens`. Script: `.agi/sessions/iter-PL0.01/a00-e51d276e/prefix_cache_probe.py`.
2. **Real harness round** — `pi -p --provider local-town --model Qwen3.5-9B-Q4_K_M --thinking off --no-session "Create out.txt ... run wc -c out.txt ... reply DONE"` in a scratch dir, wall timed with `/usr/bin/time`. Server-side per-request numbers read from `docker logs llama-server`.

## Results

Probe (3 requests, same prefix):

| req | prompt tokens | cached (`cache_n`) | processed (`prompt_n`) | prefill | wall |
|---|---|---|---|---|---|
| 1 cold | 15,047 | 0 | 15,047 | 11,239 ms (1,339 tok/s) | 11.54 s |
| 2 extended | 15,069 | 15,043 | 26 | 143 ms | 0.34 s |
| 3 diverging | 15,044 | 15,026 | 18 | 117 ms | 0.30 s |

Real `pi -p` round: **wall 15.95 s**, exit 0, `out.txt` = `hello` (5 bytes), stdout `DONE`. The server log shows exactly 3 requests for the whole round:

- task 1643 (turn 1): `prompt eval time = 11391.26 ms / 15378 tokens` = 1,350 tok/s; eval 87 tokens; `n_tokens = 15464`.
- task 1741 (turn 2): `selected slot by LCP similarity, f_sim_best = 0.999`; `prompt eval time = 95.71 ms / 19 tokens`; eval 52.
- task 1795 (turn 3): same LCP selection; `prompt eval time = 95.58 ms / 19 tokens`; eval 32.
- Every `release` line: `truncated = 0`. Max context used 15,584 of 48,640 (32% of slot).

## Falsifier check

- No `done` in 20 min → false: 15.95 s.
- Slot overflow / truncation → false: `truncated = 0` on every task, peak 15,584 / 48,640.
- Turns 2+ re-prefill the whole prefix → false: turns 2-3 processed 19 prompt tokens each (LCP-cache hits).
- First-turn prefill ≈ 46.7 s at 330 tok/s (box-facts estimate) → **corrected**: measured 11.4 s at ~1,350 tok/s for a 15.4k-token prompt.

## Evidence

- Probe output: `.agi/sessions/iter-PL0.01/a00-e51d276e/probe.out`
- Server log excerpt: `.agi/sessions/iter-PL0.01/a00-e51d276e/server_log_excerpt.txt`
- Round stdout (`DONE`) and product (`hello`): `.agi/sessions/iter-PL0.01/a00-e51d276e/pi_done.txt`, `.../out.txt`
- Commands: `python3 .agi/sessions/iter-PL0.01/a00-e51d276e/prefix_cache_probe.py`; `pi -p --provider local-town --model Qwen3.5-9B-Q4_K_M --thinking off --no-session '...'`

## Caveat

This round was a direct `pi -p`, not an engine `--harness pi-local` dispatch, and it stopped one step short of the full typed round (no experiment-node record / `cli.py done`). Engine dispatch adds the node brief + adapter segments; the slot still has 33,056 tokens of headroom, so a brief 2-3x larger than this one still fits and the prefill/cache behaviour measured here is what that brief will meet.

## Agent Notes
Direct pi-local 9B minimal round: 15.4k-token prefill 11.4s @1,350 tok/s, turns 2-3 process 19 tokens each via LCP prefix-cache hit, round wall 15.95s, truncated=0, out.txt+DONE; all three named falsifiers clear; caveat: direct pi -p not engine --harness pi-local dispatch.

## Agent Notes
Direct pi -p round: 15.4k prefill 11.4s @1,350 tok/s, turns 2-3 show LCP cache hits (19 tokens each), 32% slot usage, truncated=0

PL0.02 real-dispatch measurement (director-thought, docker log 06:24:38-06:36:43Z, wall 725s): the PARENT a00-d28852cf own turns (not the kids separate probe, which shares the same server log and is excluded by task id/n_tokens discontinuity) are the real --harness pi-local engine-dispatch evidence. First turn (task 15): prompt_n=24128, prompt eval 19362.97ms (1246 tok/s), context after=24257/48640 (24383 headroom, well over the 10k bar). 20 parent turns total (19 with captured timing + 1 in flight at window edge), every one a cache hit -- no turn reprocessed anywhere near the full context even though the conversation kept growing from tool output (per-turn new-token counts ranged 45-2973, never a full re-prefill). Zero truncation on all 26 completed turns anywhere in the window (kid included). Peak parent context (last fully-captured turn, task 2563) = 39884/48640 = 82pct, headroom 8756 -- tighter than the kids isolated 32pct-peak toy measurement, and the more realistic number for capacity planning; the true final peak (task 2657) is not in the captured window, flagged as the one number I could not close. Wall spawn-to-dispatch-complete (manifest): 725s = 12.08min, well under the 20min bar. All three of thought-masters named proved-conditions hold with margin: first-turn headroom, cache hits on 2+, done well under 20min.
