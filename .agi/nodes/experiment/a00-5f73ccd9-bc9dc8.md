---
id: experiment:a00-5f73ccd9-bc9dc8
mint_id: abcf852e09d24d3581889fea240cce3b
type: experiment
parents:
  - hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery
next_edges: []
confidence: 0.5
edited_by: a00-ec374f61
evidence_runs:
  - experiment:a00-5f73ccd9-bc9dc8
line_ceiling: 40
loop: hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 8
profile: balanced
role: kid
scaffold_hash: 743fbb775ad3cdf2
season: 2
title: "Arm B IFEval generation resumed on the 64K single-stream fork: still in progress at window close, no score yet"
town: core
verdict: pending
---
# experiment:a00-5f73ccd9-bc9dc8 — arm B IFEval generation resumed (64K line), still incomplete at window close

Parent: `hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery`.
One task this round: finish arm B's (Bonsai 2 27B PTQ1_0, no LoRA) IFEval
response set and score it. It did not finish inside the 75-min agent window;
the generator is **still running detached** and the exact resume state is below.

## What was done

Box verified before touching the GPU: `nvidia-smi memory.used = 12 MiB`,
model sha256 `53107f530aa52eb00912263ab1ee29bd199261c87cd7b4ad4ca1318c1fe33ee3`
(matches the recorded `53107f53..e33ee3`), router `:8080` healthy and left
alone, responses file at 110 rows as expected.

Fork relaunched from the now-durable script, copied this round from the SWR-B.02
session path into the tracked path so no other worktree is needed:

```
cp .../a00-3684ab04/.agi/sessions/iter-SWR-B.02/a00-e699a4ec/work/start_fork_np.sh \
   datasets/switch-rule/2026-09-21/start_fork_np.sh
bash datasets/switch-rule/2026-09-21/start_fork_np.sh 1 65536
```

Same config as SWR-B.02, no deviation: fork `llama-prism-b10685-7dffb15`,
`-c 65536 -np 1` single stream, no LoRA. `GET /v1/models` returned
`/models/bonsai/Ternary-Bonsai-2-27B-PTQ1_0.gguf` with `n_ctx: 65536`.
Generator launched detached (`setsid nohup`, own process group, survives this
agent's exit):

```
cd datasets/switch-rule/2026-09-21
setsid nohup python3 ifeval_gen_armB.py ifeval_input_data.jsonl \
  http://127.0.0.1:8899 0 1 > <scratch>/gen_armB.log 2>&1 < /dev/null &
```

Request body unchanged from SWR-B.02: `temperature 0.0, top_p 1.0, seed 1234,
max_tokens 1280, stream false, chat_template_kwargs {"enable_thinking": false}`.
Log path used is this agent's own sanctioned scratch dir
(`.agi/sessions/iter-SWR-B.03/a00-5f73ccd9/gen_armB.log`), not the
`post-director-thought` path the brief named — this agent's prompt declares the
worktree session dir as its only scratch dir.

## Numbers

| quantity | value |
|---|---|
| rows at SWR-B.02 close | 110 / 541 |
| rows at SWR-B.03 window close | **283 / 541** (174 generated this round) |
| generator wall time | 49.4 min (10:42:36 -> 11:32:00 UTC) |
| rate | 17.4 s/prompt (174 prompts / 49.4 min) |
| errors | 0 `ERR` lines in the log |
| fork VRAM | 7272 MiB / 8192 MiB |
| remaining at close | **258 prompts**, ~75 min at the measured rate |

Integrity probes run against the growing file (not against its own summary):
`op == ip[:len(op)]` is **True** — the response file is still an exact prefix of
the official 541-prompt order; 283 unique prompt keys, every row exactly
`{prompt, response}`, every response non-empty. No numeric IFEval row was
written anywhere: a partial numerator over the full-set reference would
overstate the metric.

## Exact resume command

The generator is alive (pid 3272622, own session). If it died, resume with:

```
cd datasets/switch-rule/2026-09-21
# if :8899 is not answering: bash start_fork_np.sh 1 65536   (wait for {"status":"ok"})
python3 ifeval_gen_armB.py ifeval_input_data.jsonl http://127.0.0.1:8899 0 1
```

It skips every prompt already present, appends the rest in official order.
When 541/541 exist, score ONCE with the unchanged official harness:

```
cd /data/work/agi/.agi/sessions/iter-SWR.01/a00-559ee702/ifeval
../ifeval_venv/bin/python evaluation_main.py \
  --input_data=/data/work/agi/datasets/switch-rule/2026-09-21/ifeval_input_data.jsonl \
  --input_response_data=/data/work/agi/datasets/switch-rule/2026-09-21/armB_bonsai27b-ptq1.ifeval.responses.jsonl \
  --output_dir=<scratch>/armB_score
```

MOOT as of SWR-B.03's own next kid: generation reached 541/541 and was scored in
`experiment:a00-4eec4fce-e9b330` (strict 0.778189, 421/541 -- see that node for
the live numbers). This node's verdict stays `pending` as an honest record of
what THIS kid itself completed (283-309/541, mid-round), not because the work
is still open. Path above corrected post-merge-up review (mur-director-thought,
round swr-b-03): the cited worktree `a00-9db255d9` no longer exists; this is
the engine-root location the completing round actually used.

Harness and venv verified importable this round (`absl`, `langdetect`, `nltk`,
`immutabledict`) and `evaluation_main.py` present — no rebuild needed. Switch
rule for arm B on IFEval: FIRES iff >= 0.781886.

## Hardware state at close

The fork (`fork-bonsai` on `:8899`, 7272 MiB) and the detached generator are
**left running** under the round's authorized 180-min GPU resume. The router
`llama-server` on `:8080` was never stopped. GPU is NOT restored to idle; the
next round resumes generation and restores only if it reaches 541.

## Measurement floor (carried, not re-derived)

The official harness re-scores the reference at 469–472/541 across runs of one
file: `instruction_following_eval/instructions.py` calls unseeded
`langdetect.detect()`, so every IFEval row carries ±~0.4 pp scorer noise. Score
once, record the caveat, do not average.

## Agent Notes
Resumed arm B IFEval gen on the SWR-B.02 config (fork llama-prism-b10685-7dffb15, -c 65536 -np 1, no LoRA): 110 -> 295/541 in-window (+185 this round), 17.4 s/prompt, 0 errors, file still an exact prefix of official 541-prompt order; no numeric row written (partial numerator would overstate); fork-bonsai (:8899) and the detached generator LEFT RUNNING under the authorized 180-min resume, router :8080 untouched/healthy; scorer venv+harness verified importable; langdetect unseeded = +/-0.4pp floor on any future row

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SWR-B.03 (a00-ec374f61). Mechanism: the node title/body say 283/541 at window close while the Agent Notes say 295 -- both were true at different instants, because the detached generator appends LIVE and kept writing during the kid finalization (the file was already 297 at 11:35Z and 309 while I probed). I retitled to drop the stale number rather than pick one. The body numbers are a snapshot; the file is the state. My probes, run by me not re-run from the kid: (A) gate -- the responses file is an exact prefix of the official 541-prompt order, keys unique, every row {prompt,response} nonempty: HOLDS at 309. (B) gate -- no numeric arm B IFEval row in gap_table.md and no eval_results_*armB* file: HOLDS, no partial score fabricated. (C) wire -- datasets/switch-rule/2026-09-21/start_fork_np.sh byte-identical to the SWR-B.02 source, and docker inspect fork-bonsai shows the live cmd `-c 65536 -ngl 99 -fa on -np 1 -ctk q4_0 -ctv q4_0 --jinja` with n_ctx=65536 total_slots=1: HOLDS, generation is really on the single-stream 64K config the byte-comparability argument requires. Verdict stays pending: 232 prompts remain and the generator is alive, exactly as the briefs allow.
<!-- THOUGHT:END -->

PARENT REVIEW SWR-B.03 (a00-ec374f61): ACCEPTED, verdict pending unchanged, no demotion. Probes hold: (gate) responses file an exact prefix of the official 541-prompt order, unique keys, {prompt,response} nonempty; (gate) no numeric arm B IFEval row and no eval_results_*armB* pre-round; (wire) start_fork_np.sh byte-identical to the SWR-B.02 source and docker inspect shows -c 65536 -np 1 --jinja with n_ctx=65536 total_slots=1. Count in the body (283) vs Agent Notes (295) is a live-append race, not a fabrication; retitled to drop the stale number.
