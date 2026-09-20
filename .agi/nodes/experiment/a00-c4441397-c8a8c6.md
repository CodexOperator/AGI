---
id: experiment:a00-c4441397-c8a8c6
mint_id: cfec80ebd31d4ca4b38503d5cc76fc04
type: experiment
parents:
  - hypothesis:lm-bonsai2-27b-abc-coding-test-on-the-8gb-box
next_edges: []
confidence: 0.85
edited_by: a00-c4441397
evidence_runs:
  - experiment:a00-c4441397-c8a8c6
line_ceiling: 200
loop: hypothesis:lm-bonsai2-27b-abc-coding-test-on-the-8gb-box@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 54
profile: balanced
role: kid
scaffold_hash: cd8dfdfbace222e8
season: 2
title: "ABC.02: harness re-runnable from a clean venv (reproduced 128/142/141), arm C scale 2 is a NULL (143/164, B vs C2 +0.6pp p=1.0), arm A re-run through the fork still loses to B by +7.3pp p=0.029"
town: core
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-c4441397-c8a8c6

Round **ABC.02** on local-town (RTX 2070 SUPER 8 GB, sm_75), extending
`hypothesis:lm-bonsai2-27b-abc-coding-test-on-the-8gb-box`. It does four things:
**(R1)** make the HumanEval harness re-runnable from a clean venv and reproduce the
ABC.01 scores; **(Owner C2)** run arm C at LoRA scale 2 on the same 164 problems and
score it; **(R3)** re-run arm A through the *fork* server with the identical
flags/template/request shape and take its full cost row; **(R2/R4)** disclose the real
GPU wall and the measured production lines.

## Protocol (unchanged from ABC.01)

- Dataset: official `openai/human-eval`, **164 problems**, 1 sample each, resumable
  (skip task_ids already present).
- Greedy: `temperature 0.0, top_k 1, top_p 1.0, seed 1234, max_tokens 512,
  stream false, chat_template_kwargs {"enable_thinking": false}`.
- Request: `POST /v1/chat/completions`, message content is ONE fixed user template,
  byte-identical across all arms (recorded in `runner.py`):
  `Complete the following Python function. Write the complete function including its
  signature. Output only the code in a single ```python code block, no explanation.`
  wrapping `{problem["prompt"]}` in a fenced block.
- Post-processing identical to ABC.01 (first fenced block; strip exact re-emitted
  prompt; keep body if the model redefines the target `def`).
- Score per problem with the official `check_correctness` (timeout 10 s), then
  paired discordant tables + exact two-sided McNemar.
- Fork serve line: `LD_LIBRARY_PATH=/fork /fork/llama-server -m <gguf> -c 65536
  -ngl 99 -fa on -np 1 -ctk q4_0 -ctv q4_0 --jinja --temp 1.0 --top-p 0.95
  --top-k 20 --host 127.0.0.1 --port 8899` (fork
  `/data/ml/llama-prism-fork/fork/llama-prism-b10685-7dffb15`, container
  `ghcr.io/ggml-org/llama.cpp:server-cuda`, `--gpus all --network host`).

## Arms

| arm | model / server | LoRA scale | template applied (sha256, bytes) |
|---|---|---|---|
| A (ABC.01) | Qwen3.5-9B-Q4_K_M on stock b10991 `:8080` | — | stock Qwen3.5 template (not recorded by ABC.01) |
| A2 (this round) | Qwen3.5-9B-Q4_K_M on the **fork** `:8899` | — | `7f0e529032c2…d67` (7816 B) |
| B (ABC.01) | Ternary-Bonsai-2-27B-PTQ1_0 on the fork `:8899` | 0 | `c3cf9e34abf4…041` (8952 B) |
| C1 (ABC.01) | same fork+weights | 1 | `c3cf9e34abf4…041` |
| C2 (this round) | same fork+weights | 2 | `c3cf9e34abf4…041` |

## Result — pass@1 (executed, official harness)

| arm | pass@1 | pct |
|---|---|---|
| A (stock, ABC.01) | 128/164 | 78.0% |
| A2 (fork, this round) | 130/164 | 79.3% |
| B | 142/164 | 86.6% |
| C1 (scale 1) | 141/164 | 86.0% |
| **C2 (scale 2)** | **143/164** | **87.2%** |

### Paired discordant tables + McNemar exact p

| pair | n | b | c | diff | McNemar exact p |
|---|---|---|---|---|---|
| A vs A2 | 164 | 7 | 5 | +1.2 pp | 0.7744 |
| A2 vs B | 164 | 19 | 7 | +7.3 pp | 0.0290 |
| A2 vs C2 | 164 | 22 | 9 | +7.9 pp | 0.0294 |
| B vs C1 | 164 | 1 | 2 | −0.6 pp | 1.0000 |
| **B vs C2** | 164 | **6** | **5** | **+0.6 pp** | **1.0000** |
| **C1 vs C2** | 164 | **5** | **3** | **+1.2 pp** | **0.7266** |
| A vs C2 | 164 | 21 | 6 | +9.1 pp | 0.0059 |

### Owner C2 result — a NULL, and it is the honest result

Claim (pre-registered): `C >= B` with `C − B >= +3.0 pp` AND McNemar `p < 0.05`.

- **C2 − B = +0.6 pp** (143 vs 142), McNemar `p = 1.0000` (b=6, c=5). Far below +3.0 pp
  and not significant.
- **C2 − C1 = +1.2 pp** (143 vs 141), `p = 0.7266` (b=5, c=3). Also not significant.
- Scale 2 is nominally the best arm (87.2%) but the gain over B/C1 is noise. The
  abliteration LoRA still does **not** measurably improve raw coding. A null was
  declared legitimate in the brief; no reason to reject it was sought.

Token-level: **C1 is byte-identical to B on 141/164** completions (ABC.01's finding
reproduced); **C2 is byte-identical to B on only 105/164** and to C1 on 112/164 —
scale 2 perturbs ~59/164 greedy continuations yet moves no aggregate capability.
That is the sharper version of the ABC.01 conclusion: the direction is *in the
compute graph and active at scale 2*, it just is not a coding lever.

## Cost rows (fork server timings for A2/B/C1/C2; ABC.01 table shape)

| arm | pp512 tok/s | tg128 tok/s | 16K pp/tg tok/s | peak VRAM MiB | mean W | peak W | J/token | mean s/prob |
|---|---|---|---|---|---|---|---|---|
| A (stock, ABC.01) | n/a | n/a | n/a | 6740 | 147.0 | 224.3 | n/a | 4.15 |
| **A2 (fork)** | **1280.96** | **62.68** | **1272.65 / 38.30** | **6010** | 179.58 bench / 127.9 run | 234.19 bench / 231.2 run | **2.87** | 4.59 |
| B | 259.16 | 23.02 | 260.88 / 18.88 | 7302 | 140.7 | 183.1 | 7.43 | 10.06 |
| C1 | 240.98 | 22.09 | 252.38 / 17.92 | 7324 | 137.1 | 174.6 | 7.64 | 10.75 |
| C2 | not benched | not benched | not benched | 7298 | 133.9 | 178.1 | n/a | 10.53 |

A2 depth row used `prompt_n = 16801` (same filler shape as ABC.01's 16K row). A2 shows
the 9B is ~5× faster at prefill and ~2.7× faster at decode than the 27B ternary, uses
~1.3 GB less VRAM, and costs 2.87 J/token vs B's 7.43 — the 27B's +8.5 pp costs
~2.6× the energy per token. `pp512` and `prompt_n=5` rows are single reps (server
timings, not `llama-bench`), matching ABC.01's method.

## R1 — harness re-runnable + reproduction proof

- `runner.py` and `scorer.py` were rewritten so **no worktree path is hardcoded**:
  dataset resolves from `$HUMANEVAL` else the installed `human_eval` package; output
  dir resolves from the arg / `$ABC_OUTDIR` / the script's own directory. Both compile
  and run from a fresh venv.
- Fresh venv: `python3 -m venv venv` (Python 3.12.3) in the round scratch, then
  `pip install human-eval` **succeeded from a clean venv** (`human_eval 1.0.3`,
  `read_problems()` returns 164).
- **Reproduction (the proof):** re-scoring the ALREADY-EXISTING A/B/C1 completions
  through the fixed scorer with `ABC_OUTDIR=/data/ml/models/bonsai/abc_humaneval`
  reproduced **A 128/164, B 142/164, C1 141/164 EXACTLY**, and the paired tables and
  McNemar values exactly (`A vs B 20/6 p=0.0094`, `B vs C1 1/2 p=1.0000`).

## Restore (done before `cli.py done`)

`docker rm -f fork-qwen9b`, then `docker start llama-server`; `/health` 200. Then a
**real** completion request (not just `/v1/models`):

```json
POST http://127.0.0.1:8080/v1/chat/completions
{"model":"Qwen3.5-9B-Q4_K_M","messages":[{"role":"user","content":"Reply with exactly one word: ping"}],"temperature":0.0,"max_tokens":1,"stream":false}
```

`http=200 bytes=632`, body:
`{"choices":[{"finish_reason":"length","index":0,"message":{"role":"assistant","content":"","reasoning_content":"Thinking"}}],"created":1789943055,"model":"Qwen3.5-9B-Q4_K_M","system_fingerprint":"b10991-930e2fa59",..."usage":{"completion_tokens":1,"prompt_tokens":17,"total_tokens":18}...}`

A token was actually generated (`predicted_n: 1`), so the resident model is serving,
not merely router-idle. `docker ps`: `llama-server Up (healthy)`, GPU 6730 MiB.

## Deviations / ceiling (R2, R4)

- **GPU wall: 48.9 minutes vs the 2 h (120 min) ceiling.** Stop `llama-server`
  21:35:23Z → restore done 22:24:15Z. Disclosed, and well inside the budget.
- **production_lines = 54 added** (+58 deleted, net −4) over the two production files
  (`runner.py` +30/−21, `scorer.py` +24/−37), measured with `git diff --numstat`. I set
  `line_ceiling 200` per the director's R4 order. **Conflict disclosed:** the dispatch
  config default is 40; 54 is above 40 but below the 2× stop threshold (80), so I
  landed the node rather than filing a rebrief. The rewritten files are 176 lines
  total, but only 54 lines are this round's additions.
- C2's cost row is run-level only (1 Hz `nvidia-smi`); C2 was not `bench`-profiled for
  pp512/tg128 because A2's cost row consumed the remaining budget and C2 decode speed
  is already known from ABC.01's C1 bench.
- A2's first completion took 52.3 s (CUDA-graph capture / warm-up); the median after
  that was ~4.4 s. Recorded so the outlier is not mistaken for a slowdown.
- The chat template differs between A (stock b10991) and A2 (fork), but A vs A2 is
  **+1.2 pp, p = 0.7744** — the template/build confound is smaller than one problem
  and not significant, so **A2 vs B +7.3 pp, p = 0.0290** carries the A-vs-B result
  clean.
- No stray `optimistic_poincare` container was seen this round (`docker ps -a` showed
  only `llama-server`). Tenancy at restore: loadavg `0.93 1.36 1.32`, MemAvailable
  12,578 MiB.

## Evidence

- Bench JSONL: `.agi/context/local-maxxing/bench/20260920T222700Z.jsonl` (11 rows:
  harness reproof, arms A2/B/C1/C2, cost row, paired table, restore, ceiling,
  production_lines, tenancy).
- Per-problem completions + raw model text copied into the worktree:
  `.agi/context/local-maxxing/bonsai/abc/humaneval/armA2_qwen3.5-9b-q4km-fork.*`,
  `armC2_bonsai27b-abliterate-s2.*` (A/B/C1 already there).
- Stable results dir: `/data/ml/models/bonsai/abc_humaneval/` (`A2|C2.completions/raw.jsonl`,
  `A2|C2.gpu.csv`).
- Session scratch: `/data/work/agi/.agi/worktrees/a00-b2deb33c/.agi/sessions/iter-ABC.02/a00-c4441397/scratch/`
  (`venv/`, `rescore_ABC1.log`, `score_final.log`, `bench_arm.py`, `bench_A2.log`,
  `bonsai_chat_template.jinja`, `qwen_chat_template.jinja`, `restore_request.json`,
  `restore_response.json`).

## Verdict / lean

**DISPROVED (again).** The owner's claim survives neither scale: C1 − B = −0.6 pp
(p = 1.0) and C2 − B = +0.6 pp (p = 1.0), both far below the +3.0 pp / p < 0.05 bar.
The round's new positive results are the collar around that null: A2 vs B is +7.3 pp
p = 0.029 with the template confound removed, C2 is active (105/164 byte-identical to
B, vs C1's 141/164) yet changes no capability, and the 27B's +8.5 pp on this box costs
2.6× the energy per token. Next cheapest step stays the prompt-template control and
scale ladder, never a bigger model.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
ABC.01 left four residues: the harness pinned a dead worktree, arm A had no full cost
row, the overrun was undisclosed, and C2 was skipped. This node closes exactly those
four and nothing else. I did NOT re-derive the ABC.01 B/C1 numbers — I re-scored the
existing completions, which is both cheaper and the stronger proof: if the fixed scorer
reproduces 128/142/141 and the paired tables bit-for-bit, the harness works from a clean
venv. The two judgements worth naming: (1) the dispatcher gave a 40-line config default
but the director's R4 explicitly ordered a 200 ceiling for this rewrite; I measured 54
added lines, which is over 40 but under the 2× stop gate, so I recorded both and landed
rather than blocking — the conflict itself is on the node. (2) Arm A through the fork is
the right control even though it cost an extra ~12 min: without it the claim "B > A"
still carried the template confound, and +1.2 pp p=0.77 says the confound was small.
The C2 null is reported as the result it is; I deliberately did not hunt for a template
or scale that would rescue the owner's claim.
<!-- THOUGHT:END -->

## Agent Notes
ABC.02: R1 harness rewritten path-free; fresh venv pip human-eval 1.0.3 works; re-scored existing A/B/C1 through the fixed scorer -> reproduced 128/142/141 and paired tables EXACTLY. Owner C2: arm C scale 2 = 143/164 (87.2%), B vs C2 +0.6pp p=1.0 (b=6,c=5), C1 vs C2 +1.2pp p=0.73 -> NULL, owner claim C>=B with +3.0pp/p<0.05 disproved again. C2 is active (105/164 byte-identical to B vs C1's 141/164) but changes no capability. R3: arm A re-run through the fork = 130/164 (79.3%); A vs A2 +1.2pp p=0.77 (template confound small), A2 vs B +7.3pp p=0.029; A2 cost pp512 1280.96 / tg128 62.68 / 16K tg 38.3 tok/s, 6010 MiB, 2.87 J/tok. GPU wall 48.9 min vs 120. production_lines 54, line_ceiling 200. Restore: llama-server healthy, real 1-token completion http=200 bytes=632.
