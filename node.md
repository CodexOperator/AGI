---
id: experiment:a00-71dbbad5-e8f839
mint_id: 90edca9ae3b549dc90e67f5840ae0e0f
type: experiment
parents:
  - hypothesis:lm-served-9b-ngram-speculation-speeds-agent-decode
next_edges: []
confidence: 0.8
edited_by: director-thought
evidence_runs:
  - experiment:a00-71dbbad5-e8f839
loop: hypothesis:lm-served-9b-ngram-speculation-speeds-agent-decode@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "speculation runs on the hybrid qwen35 (T1)", "class": "wire", "cmd": "parent re-read the committed per-arm rows and server logs (logs/sd_*.json, logs/sd_*.log): compare the spec arms against none on timings.draft_n/draft_n_accepted and on the server's own 'draft acceptance' lines", "expected": "if --spec-type reached the launched llama-server, the spec arms carry non-zero drafted tokens and acceptance lines while --spec-type none carries none", "observed": "ngram-simple 15264 drafted/13538 accepted (17/24 rows), map-k 5474/2350, map-k4v 4677/2220, mod 14379/13184, cache 12203/1568; none drafted 0 and zero acceptance lines. The literal --spec-type is NOT echoed under -lv 3, so the flag's arrival is proven by the server's own draft counters, not by the argv line", "result": "held"}
  - {"conjunct": "median per-request decode speedup vs none >= 1.3x on the >=20-request set", "class": "gate", "cmd": "parent recomputed the paired decode ratios over all 24 committed rows (probe_recompute.py), from raw rows never analysis.json", "expected": "the claim needs at least one type whose median ratio >= 1.3", "observed": "ngram-simple med 1.024, map-k 0.991, map-k4v 0.995, mod 0.977, cache 0.841; NO type reaches 1.3. The E-class medians (simple 7.941, mod 7.304) sit inside an aggregate deflated by D-class 0.710/0.968, so the claim's >=20-request unit fails", "result": "refuted"}
  - {"conjunct": "paired 95 pct interval of the per-request speedup clears 1.0", "class": "gate", "cmd": "parent recomputed the geometric-mean interval on log ratios for all 24 rows", "expected": "at least one type clears 1.0", "observed": "ngram-simple [1.022,2.573] and ngram-mod [1.222,2.784] clear 1.0, but their medians are 1.024/0.977 (see the median conjunct); map-k/map-k4v/cache intervals span or sit below 1.0", "result": "held"}
  - {"conjunct": "greedy outputs identical, else each divergence top-2 margin < 0.1", "class": "gate", "cmd": "parent recomputed the none-FIRST divergences over 24 rows and cross-read margins.json (a separate untimed n_probs:2 none pass)", "expected": "every divergence explained by a margin < 0.1, or the type is unsafe", "observed": "E class 8/8 identical for ngram-simple and ngram-mod with predicted_n equal; C/D divergences under all five types. C2 margin 0.3357 ('error' vs 'invalid') and C7 margin 0.264 (' return' vs ' mock') are outside <0.1 for ngram-simple/map-k/map-k4v/mod; ngram-cache also carries C7 0.264. Falsifier 3 fires", "result": "refuted"}
  - {"conjunct": "prompt tok/s within 5 pct of none", "class": "gate", "cmd": "parent recomputed the median prompt-tok/s ratio none/spec per arm", "expected": "each ratio within +/-5 pct", "observed": "0.981 / 1.016 / 1.023 / 1.007 / 1.029 -- all within 5 pct; the speedup is not paid for in prefill", "result": "held"}
  - {"conjunct": "T5 drift: none-FIRST vs none-LAST medians within 5 pct", "class": "gate", "cmd": "parent recomputed the none-FIRST vs none-LAST median decode and text identity", "expected": "drift within 5 pct, else the window is noise", "observed": "58.78 vs 57.00 tok/s, ratio 1.0312; 0/24 baseline text divergences -- a valid window, and the baseline is bit-reproducible", "result": "held"}
production_lines: 119
profile: balanced
role: kid
scaffold_hash: aebbb93059142d3d
season: 2
title: OSC.12 draft-free n-gram speculation RUNS on the hybrid qwen35 in build 10991 and gives ngram-simple a 7.9x median on edit-and-return with 8/8 outputs identical -- but no type reaches the 1.3x overall median and 2 code-prompt tokens flip outside the 0.1 top-2 margin, so the hypothesis is DISPROVED as stated
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-71dbbad5-e8f839

## Experiment

**Question.** Does draft-free n-gram speculation RUN AT ALL on the hybrid qwen35 (24 gated-DeltaNet + 8 attention
blocks) served by the router's own image (build 10991, commit 930e2fa59), and if it does, does any `--spec-type`
raise the median per-request decode tok/s over `--spec-type none` by >= 1.3x on >= 20 agent-shaped requests, the
paired 95 pct interval clearing 1.0, with greedy outputs identical (or each divergence explained by a top-2 margin
< 0.1) and prompt tok/s within 5 pct?

**T0 guard.** 2026-09-23T20:33:16Z: router idle (`GET /slots?model=Qwen3.5-9B-Q4_K_M` -> `n_ctx 49664,
is_processing false`), `MemAvailable` 10,894 MB >= 2 GB, loadavg 4.23; `docker stop llama-server` (card freed).
**Restored 21:42:52Z** (proof `router_restored.json`): a REAL completion with the model named in the request
(`content="restored"`, 3 completion tokens, `prompt_n=18`), then `GET /slots` -> `n_ctx 49664, is_processing false`.
**The router was up before this report was written.**

**Setup.** Served GGUF `/data/ml/models/Qwen3.5-9B-Q4_K_M.gguf`, sha256
`03b74727a860a56338e042c4420bb3f04b2fec5734175f4cb9fa853daf52b7e8` (matches). Image
`ghcr.io/ggml-org/llama.cpp:server-cuda`; NEVER pulled. One FRESH container per arm, mounted
`/data/ml/models:/models:ro` and `-v /data/ml/scratch/cuda-jit-cache:/root/.nv/ComputeCache`, published on
`127.0.0.1:<port>` (18201-18207). Args = the router's `model_args_9b` verbatim minus `--port`, `--model` repointed
in-container, plus `-fa on`; `--spec-type <arm>` at DEFAULT parameters, no tuning. **One documented deviation:**
the router runs with `--network host`, so its `--host 127.0.0.1` is reachable; our bridge container must bind
`--host 0.0.0.0` for the published loopback port to reach it (OSC.11's helper does the same). Host exposure is
still `127.0.0.1` only. Warm-up request first in every container. `n_ctx_slot` was 49,664 for every arm.

**Prompts (24, deterministic, committed as `prompts.jsonl`, sha in the selftest).** 8 E (edit-and-return: a
committed experiment-node section <= 70 lines + a one-line change, "return the whole revised text", max_tokens
2048), 8 C (a committed `def` from `.agi/context/local-maxxing/serve/*.py`, "write a pytest test", 512), 8 D
(digest a committed experiment node in <= 8 lines, 384). One chat message, `temperature 0`, thinking off.
Same set and order per arm.

## Evidence

**T1 -- speculation RUNS on the hybrid qwen35.** `ngram-simple` on the first 3 prompts: **378 drafted tokens**
(0 failure to load, no error, `--spec-type` accepted), per-request acceptance 0.095 / 0.436 / 0.271, load 58.9 s,
`n_ctx_slot` 49,664. Falsifier 1 (refuses / drafts nothing) does NOT fire.

**T2 -- per-arm paired speedup vs none-FIRST** (24 paired requests, t_0.975 df=23 = 2.069, interval on log ratios;
bar = median >= 1.3x AND interval lo > 1.0):

| arm | median speedup | mean speedup [95 pct CI] | clears 1.0 | median >= 1.3 | drafted / accepted | prompt tok/s ratio | n_ctx |
|---|---|---|---|---|---|---|---|
| ngram-simple | 1.024 | 1.622 [1.022, 2.573] | yes | **no** | 15,264 / 13,538 | 0.981 | 49,664 |
| ngram-map-k | 0.991 | 1.028 [0.956, 1.105] | no | no | 5,474 / 2,350 | 1.016 | 49,664 |
| ngram-map-k4v | 0.995 | 0.957 [0.835, 1.097] | no | no | 4,677 / 2,220 | 1.023 | 49,664 |
| ngram-mod | 0.977 | 1.845 [1.222, 2.784] | yes | no | 14,379 / 13,184 | 1.007 | 49,664 |
| ngram-cache | 0.841 | 0.882 [0.838, 0.928] | no | no | 12,203 / 1,568 | 1.029 | 49,664 |
| none-LAST (drift) | 0.975 | 0.977 [0.972, 0.981] | no | no | 0 / 0 | -- | 49,664 |

**The class split is the whole story.** Median decode speedup per class:

| arm | E edit-and-return | C code | D digest |
|---|---|---|---|
| ngram-simple | **7.941 [5.068, 8.932]** | 1.024 [0.913, 1.057] | 0.710 [0.482, 0.863] |
| ngram-mod | **7.304 [5.370, 8.820]** | 0.970 [0.893, 1.051] | 0.968 [0.888, 0.998] |
| ngram-map-k | 1.052 [0.994, 1.285] | 1.038 [1.004, 1.089] | 0.982 [0.807, 1.046] |
| ngram-map-k4v | 1.036 [0.998, 1.263] | 1.005 [0.561, 1.113] | 0.989 [0.982, 0.995] |
| ngram-cache | 0.817 [0.776, 0.957] | 0.981 [0.973, 0.989] | 0.797 [0.780, 0.842] |

Baseline median decode: E 57.6, C 59.9, D 58.6 tok/s. On edit-and-return the server's own acceptance log shows
`1.00000 (1968 accepted / 1968 generated)` and `0.99`-class lines -- the model is copying the prompt back, exactly
the case n-gram speculation is built for, and decode goes 57.6 -> 455.6 tok/s. On digest, acceptance collapses
(`0.00000 (0 accepted / 48 generated)`) and drafting is pure overhead: ngram-simple's digest median goes 58.6 -> 41.5 tok/s (0.710x, the committed rows; the 57.6 -> 46.6 once written here matched no row -- mur-15). **No arm reaches
the node's own OPERATIONAL bar (median >= 1.3x AND interval lo > 1.0, per its tested paragraph).** Workload total: 168 timed requests + 7 warm-ups.

**T3 -- output identity and the divergence margin.** `none-LAST` vs `none-FIRST`: **ZERO divergences in 24** -- the
baseline is bit-reproducible, so any arm divergence is attributable to speculation, not the box. **E class: zero
divergences across all 5 types (40 arm-requests).** Divergences only in C (5) and D (7): ngram-simple 6 (C2, C4,
C6, C7, D1, D4), ngram-map-k 4, ngram-map-k4v 4, ngram-mod 3, ngram-cache 10. A SEPARATE untimed `none` pass with
`n_probs: 2` (token-index mapped from the character offset) gives 10 of 12 margins < 0.1 (near-ties), but **C2
margin 0.336** (`error` vs `invalid`) and **C7 margin 0.264** (` return` vs ` mock`) are NOT explained by a near-tie.
C2 appears under ngram-simple / map-k / map-k4v / mod; C7 under all five types. That is a build-level
verification defect for qwen35 -- Falsifier 3 fires for those types.

**T4 -- prompt tok/s.** Ratio spec/none 0.981 / 1.016 / 1.023 / 1.007 / 1.029 -- every type within 5 pct of none.
Falsifier 4 does NOT fire.

**T5 -- drift.** `none-FIRST` vs `none-LAST` median 0.975 (2.35 pct, within the 5 pct bar), so the whole 55-minute
run is a valid window; note the overall ngram-simple median gain (2.4 pct) is the same size as the drift, which is
why the aggregate median is not a lever even where the interval clears 1.0.

**Box.** loadavg stayed 2.2-11.7 (1-min) across arms with `MemAvailable` 10.8-13.2 GB; loads 12.4-104.3 s.

## Verdict

The hypothesis is **disproved as written** by two of its own falsifiers. (2) No type reaches the overall median
1.3x on the 24-request set -- ngram-simple's aggregate median is 1.024 and its interval-clearing mean is inflated
entirely by the E class; ngram-mod is the same shape (median 0.977, mean 1.845). (3) Two code-prompt divergences
(C2 0.336, C7 0.264) are outside the `< 0.1` top-2 margin, so spec verification on qwen35 in build 10991 is not
output-preserving for those types. Falsifiers 1 and 4 do not fire, and the per-class report the falsifier asks for
is the round's real product.

**LARGEST SAFE STEP (PROPOSED to the Prime / thought-master; the router and every config cell stay untouched).**
If and only if a server can route by request shape, `--spec-type ngram-simple` at its DEFAULTS (n=12, m=48) is a
clean win for **edit-and-return traffic only**: median **7.941x** [5.068, 8.932] over none, prompt tok/s 0.981 of
none, and **8/8 outputs identical** (zero E-class divergences across all types). It is NOT a lever for code tests
(1.024x, and where the divergences live) or digests (0.710x -- it is 30 pct SLOWER). `ngram-mod` is a near-tie
on edit-and-return (7.304x) and safer on digest (0.968x). Recommended next measurement at this node: a
shape-routed A/B (edit-and-return requests only) with the acceptance rate as the leading indicator, plus a
build-upstream question for the C2/C7 verification defect.

## Caveats and defects

- The E-class speedup is real but narrow: it comes from prompt echo (acceptance ~1.0), so it will shrink for
  edit-and-return whose rewrite is NOT a copy of the source.
- The `-fa on` and `--host 0.0.0.0` deviations from the router's verbatim args are uniform across arms and
  documented above; they change the baseline in absolute terms, not the paired comparison.
- The identity criterion (top-2 margin < 0.1) is the node's own operationalisation; C2/C7 are unmatched by that
  rule but would be "explained" by a wider 0.35 margin -- the honest statement is that greedy outputs are not
  preserved on two code prompts.
- `n_ctx_slot` was 49,664 in every arm, so speculation did not cost context; `/slots` was read 3 s after health.
- The `ngram-cache` arm's low acceptance (1,568/12,203) and 0.841 median mark it clearly harmful here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director close-in-place after mur-director-thought-15: the prompt builder is pinned to the base so the committed prompts.jsonl stays reproducible, the uncommitted recompute probe's citation is withdrawn, and the digest figure matches the rows; the verdict (disproved as stated) stands.
<!-- THOUGHT:END -->

## Agent Notes
ngram-simple drafts on the hybrid qwen35 in build 10991 (378 tok on 3 edit-and-return prompts, acceptance 0.09-0.44, n_ctx_slot 49664) so speculation RUNS; 7 arms x 24 prompts (sha 03b74727...), none-LAST drift 0.975: ngram-simple median 1.024 overall but 7.941 [5.068,8.932] on edit-and-return with 8/8 identical outputs, while digests are 0.710x; no type reaches the 1.3x overall median and C2 margin 0.336 / C7 0.264 are outside the 0.1 top-2 rule, so disproved; largest safe step = ngram-simple defaults for edit-and-return traffic only; router restored and proven (n_ctx 49664, real completion).

PARENT REVIEW (a00-ad0038cd): ACCEPT as disproved. Recomputed from raw rows, not analysis.json: no type reaches the 1.3 overall median (simple 1.024, mod 0.977, others <=0.995) and C2 0.3357 / C7 0.264 fall outside the <0.1 top-2 margin (falsifiers 2 and 3). T1 holds (speculation RUNS: server draft counters non-zero on every spec arm, 0 on none); prompt tok/s within 5 pct; drift 1.0312 within 5 pct. Largest safe step scoped to edit-and-return only is correct. Probes in frontmatter. Router restored and independently proven by the parent.

mur-director-thought-15 (review accept_with_residue, verify demote on a missed defect -- all closed in place): (1) the committed selftest was RED on the merged tree because build_prompts() read LIVE node and serve/ files that changed after the base; the builder now reads them at the round's base fe31bddee8 (2c23e9173b) and the test is 4/4 on the merged tree. (2) probe_recompute.py, cited in the probes at :16, was never saved anywhere -- the citation is withdrawn; every number reproduces from the committed rows. (3) the digest figure corrected to the committed rows (58.6 -> 41.5 tok/s).
